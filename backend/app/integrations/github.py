"""Public GitHub API.

No token, no write operations: public repository metadata is all this needs, and
avoiding auth means there is no secret to store or rotate for the demo.

Two rules shape everything here:

- **A failure returns a reason, never an exception.** The section this feeds is
  supplementary — GitHub being slow, rate-limited or down must degrade one
  section, never break a page or an answer.
- **Nothing is invented.** Repositories are reported as the API returns them,
  ranked by recency. A hand-curated list would be portfolio content that the
  resume does not support.
"""

from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass, field
from urllib.parse import urlparse

import httpx

from app.config import Settings
from app.services.content import ContentService

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GithubRepo:
    name: str
    description: str | None
    url: str
    language: str | None
    topics: list[str] = field(default_factory=list)
    pushed_at: str = ""


@dataclass(frozen=True)
class RepoFetchResult:
    """`reason` is None on success, and a human-readable sentence otherwise.

    Callers branch on `reason`, never on an exception: this is what lets the UI
    say *why* the section is empty instead of showing a broken state.
    """

    repos: list[GithubRepo]
    reason: str | None = None


def username_from_url(url: str) -> str:
    """`https://github.com/someone/` -> `someone`."""
    path = urlparse(url).path.strip("/")
    return path.split("/")[0] if path else ""


class GitHubClient:
    """Lists a user's public repositories, cached in process.

    `transport` is injectable so tests never touch the network, never consume
    the shared rate-limit budget, and never depend on what the real account
    happens to contain today.
    """

    def __init__(
        self,
        username: str,
        *,
        settings: Settings,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.username = username
        self._settings = settings
        self._transport = transport
        self._cached: RepoFetchResult | None = None
        self._cached_at = 0.0

    @classmethod
    def from_content(cls, content: ContentService, settings: Settings) -> GitHubClient:
        """The username comes from the portfolio, never a literal in the code."""
        return cls(
            username=username_from_url(content.profile.links.github or ""),
            settings=settings,
        )

    def list_repos(self) -> RepoFetchResult:
        if self._fresh():
            return self._cached  # type: ignore[return-value]

        result = self._fetch()
        # Only a success is cached. Caching a blip would turn a momentary
        # failure into a 15-minute outage of the section.
        if result.reason is None:
            self._cached = result
            self._cached_at = time.monotonic()
        return result

    def _fresh(self) -> bool:
        if self._cached is None:
            return False
        return (time.monotonic() - self._cached_at) < self._settings.github_cache_ttl_s

    def _fetch(self) -> RepoFetchResult:
        if not self.username:
            return RepoFetchResult([], "No GitHub account is listed in the portfolio.")

        url = f"{self._settings.github_api_base}/users/{self.username}/repos"
        try:
            with httpx.Client(
                transport=self._transport, timeout=self._settings.github_timeout_s
            ) as client:
                response = client.get(
                    url,
                    params={"sort": "pushed", "per_page": 100, "type": "owner"},
                    headers={"Accept": "application/vnd.github+json"},
                )
        except httpx.TimeoutException:
            logger.warning("GitHub request timed out")
            return RepoFetchResult([], "GitHub did not respond in time.")
        except httpx.HTTPError as exc:
            logger.warning("GitHub request failed: %s", exc)
            return RepoFetchResult([], "GitHub could not be reached right now.")

        if response.status_code == 403 and response.headers.get("X-RateLimit-Remaining") == "0":
            return RepoFetchResult([], "GitHub rate limit reached — try again shortly.")
        if response.status_code == 404:
            return RepoFetchResult([], f"No public GitHub account found for {self.username}.")
        if response.status_code != 200:
            logger.warning("GitHub returned %s", response.status_code)
            return RepoFetchResult([], "GitHub returned an unexpected response.")

        try:
            payload = response.json()
        except ValueError:
            return RepoFetchResult([], "GitHub returned an unreadable response.")
        if not isinstance(payload, list):
            return RepoFetchResult([], "GitHub returned an unexpected response.")

        return RepoFetchResult(self._select(payload))

    def _select(self, payload: list[dict]) -> list[GithubRepo]:
        """Own work, most recently pushed first, capped.

        Forks are excluded: they are someone else's repository, and listing them
        as portfolio work would overstate it.
        """
        owned = [item for item in payload if isinstance(item, dict) and not item.get("fork")]
        owned.sort(key=lambda item: item.get("pushed_at") or "", reverse=True)
        return [
            GithubRepo(
                name=item.get("name", ""),
                description=item.get("description"),
                url=item.get("html_url", ""),
                language=item.get("language"),
                topics=list(item.get("topics") or []),
                pushed_at=item.get("pushed_at") or "",
            )
            for item in owned[: self._settings.github_repo_limit]
        ]


def repos_matching(question: str, repos: list[GithubRepo]) -> list[GithubRepo]:
    """Which repositories a question actually names.

    Tool selection is **deterministic**, never model-decided. This is the same
    guarantee as refusal-by-threshold (Phase 3) and gap-by-score (Phase 4): the
    behaviour holds with the `template` provider and no API key, and it cannot
    drift because a prompt changed.

    Matching is on repository *identity* — name, language, topics — not on the
    description, which is prose and would match almost anything.

    Names are matched whole *and* by their parts: `agentic-ai` is the most
    direct evidence for a question about AI, but the full string almost never
    appears in a sentence someone would actually type.

    Every comparison is word-bounded. Without that, the topic `ai` matches
    inside "available" and the tool fires on nearly every question — noise
    attributed as evidence is worse than no attribution at all.
    """
    asked = question.lower()

    def named(term: str | None) -> bool:
        if not term or len(term) < 2:
            return False
        return re.search(rf"(?<!\w){re.escape(term.lower())}(?!\w)", asked) is not None

    def identifies(repo: GithubRepo) -> bool:
        parts = re.split(r"[-_.]+", repo.name)
        return (
            named(repo.language)
            or named(repo.name)
            or any(named(part) for part in parts)
            or any(named(topic) for topic in repo.topics)
        )

    return [repo for repo in repos if identifies(repo)]
