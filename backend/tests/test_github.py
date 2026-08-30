"""The GitHub integration: parsing, ranking, caching and honest failure.

Every test here uses a mock transport. A test must never depend on the network,
on a rate-limit budget, or on what the real account happens to contain today.
"""

from __future__ import annotations

from pathlib import Path

import httpx

from app.config import Settings
from app.integrations.github import (
    GitHubClient,
    GithubRepo,
    repos_matching,
    username_from_url,
)
from app.services.content import ContentService


def _repo(
    name: str,
    pushed_at: str,
    *,
    fork: bool = False,
    language: str | None = "Python",
    topics: tuple[str, ...] = (),
) -> dict:
    return {
        "name": name,
        "description": f"The {name} repository.",
        "html_url": f"https://github.com/test/{name}",
        "language": language,
        "topics": list(topics),
        "pushed_at": pushed_at,
        "fork": fork,
    }


def _client(payload: list[dict], *, settings: Settings | None = None) -> GitHubClient:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    return GitHubClient(
        username="test",
        settings=settings or Settings(),
        transport=httpx.MockTransport(handler),
    )


# --- username ---------------------------------------------------------------
def test_username_is_parsed_from_a_profile_url() -> None:
    assert username_from_url("https://github.com/shefali289") == "shefali289"
    assert username_from_url("https://github.com/shefali289/") == "shefali289"


def test_username_is_read_from_content_never_hardcoded(content_dir: Path) -> None:
    """The fixture profile says `test`; the real account must not leak in here."""
    client = GitHubClient.from_content(ContentService(content_dir), Settings())

    assert client.username == "test"


# --- parsing and ranking -----------------------------------------------------
def test_repos_are_parsed_from_the_api() -> None:
    result = _client([_repo("friday", "2026-08-01T00:00:00Z", topics=("ai",))]).list_repos()

    assert result.reason is None
    assert len(result.repos) == 1
    repo = result.repos[0]
    assert repo.name == "friday"
    assert repo.url == "https://github.com/test/friday"
    assert repo.language == "Python"
    assert repo.topics == ["ai"]


def test_forks_are_excluded() -> None:
    """A fork is someone else's work. Showing it would overstate the portfolio."""
    result = _client(
        [
            _repo("mine", "2026-08-01T00:00:00Z"),
            _repo("someone-elses", "2026-08-02T00:00:00Z", fork=True),
        ]
    ).list_repos()

    assert [r.name for r in result.repos] == ["mine"]


def test_repos_are_ordered_by_recency_and_capped() -> None:
    settings = Settings(github_repo_limit=2)
    result = _client(
        [
            _repo("oldest", "2024-01-01T00:00:00Z"),
            _repo("newest", "2026-08-20T00:00:00Z"),
            _repo("middle", "2025-06-01T00:00:00Z"),
        ],
        settings=settings,
    ).list_repos()

    assert [r.name for r in result.repos] == ["newest", "middle"]


# --- failure is a reason, never an exception ---------------------------------
def test_rate_limit_returns_an_empty_result_with_a_reason() -> None:
    """60 requests/hour unauthenticated. Hitting it must not break the page."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, headers={"X-RateLimit-Remaining": "0"}, json={})

    client = GitHubClient(
        username="test", settings=Settings(), transport=httpx.MockTransport(handler)
    )

    result = client.list_repos()

    assert result.repos == []
    assert result.reason is not None
    assert "rate limit" in result.reason.lower()


def test_a_network_error_returns_an_empty_result_with_a_reason() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("no route to host")

    client = GitHubClient(
        username="test", settings=Settings(), transport=httpx.MockTransport(handler)
    )

    result = client.list_repos()

    assert result.repos == []
    assert result.reason is not None


def test_a_timeout_returns_an_empty_result_with_a_reason() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("too slow")

    client = GitHubClient(
        username="test", settings=Settings(), transport=httpx.MockTransport(handler)
    )

    result = client.list_repos()

    assert result.repos == []
    assert result.reason is not None


def test_an_unexpected_status_returns_a_reason_not_an_exception() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={})

    client = GitHubClient(
        username="test", settings=Settings(), transport=httpx.MockTransport(handler)
    )

    assert client.list_repos().repos == []


# --- caching -----------------------------------------------------------------
def test_a_second_call_within_the_ttl_does_not_hit_the_api() -> None:
    """The 60/hr budget is shared by every visitor, so repeat calls must cache."""
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(200, json=[_repo("friday", "2026-08-01T00:00:00Z")])

    client = GitHubClient(
        username="test", settings=Settings(), transport=httpx.MockTransport(handler)
    )

    client.list_repos()
    client.list_repos()

    assert calls == 1


def test_an_expired_cache_entry_is_refetched() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(200, json=[_repo("friday", "2026-08-01T00:00:00Z")])

    client = GitHubClient(
        username="test",
        settings=Settings(github_cache_ttl_s=0),
        transport=httpx.MockTransport(handler),
    )

    client.list_repos()
    client.list_repos()

    assert calls == 2


def test_a_failure_is_not_cached_as_a_success() -> None:
    """Caching a failure for 15 minutes would turn a blip into an outage."""
    responses = [
        httpx.Response(500, json={}),
        httpx.Response(200, json=[_repo("friday", "2026-08-01T00:00:00Z")]),
    ]

    def handler(request: httpx.Request) -> httpx.Response:
        return responses.pop(0)

    client = GitHubClient(
        username="test", settings=Settings(), transport=httpx.MockTransport(handler)
    )

    assert client.list_repos().repos == []
    assert [r.name for r in client.list_repos().repos] == ["friday"]


# --- deterministic tool selection --------------------------------------------
def _repos(*specs: tuple[str, str | None, tuple[str, ...]]) -> list[GithubRepo]:
    return [
        GithubRepo(name=n, description=None, url=f"https://github.com/test/{n}",
                   language=lang, topics=list(topics), pushed_at="2026-08-01T00:00:00Z")
        for n, lang, topics in specs
    ]


def test_a_question_naming_a_language_matches_that_repo() -> None:
    repos = _repos(("friday", "Python", ()), ("site", "JavaScript", ()))

    assert [r.name for r in repos_matching("What Python work is there?", repos)] == ["friday"]


def test_a_question_naming_a_topic_matches() -> None:
    repos = _repos(("friday", None, ("rag",)))

    assert len(repos_matching("Anything using RAG?", repos)) == 1


def test_a_hyphenated_repo_name_matches_on_its_parts() -> None:
    """`agentic-ai` must answer a question about AI.

    Matching the full name only, a repository whose name is the most direct
    evidence for a question never surfaces — the whole string rarely appears in
    a sentence someone would type.
    """
    repos = _repos(("agentic-ai", None, ()), ("resume_analyser_rag", None, ()))

    matched = [r.name for r in repos_matching("What AI work has she done?", repos)]

    assert matched == ["agentic-ai"]


def test_an_unrelated_question_matches_nothing() -> None:
    """The guard against over-firing: a tool that always fires attributes noise."""
    repos = _repos(("friday", "Python", ("ai",)))

    assert repos_matching("Where did she study?", repos) == []


def test_a_substring_is_not_a_match() -> None:
    """`ai` must not match inside `available`, or every question fires the tool."""
    repos = _repos(("thing", None, ("ai",)))

    assert repos_matching("Is she available for work?", repos) == []
