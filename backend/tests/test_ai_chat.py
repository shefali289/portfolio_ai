"""POST /api/ai/chat — grounded answers, and refusal when ungrounded."""

from __future__ import annotations

from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient

from app.ai.provider import TemplateProvider, resolve_provider
from app.config import Settings
from app.integrations.github import GitHubClient
from app.main import create_app


@pytest.fixture
def client(content_dir: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    # template + stub embeddings: no network, no API key, deterministic.
    monkeypatch.setenv("AI_PROVIDER", "template")
    return TestClient(create_app(content_dir=content_dir))


def test_chat_answers_from_portfolio_content(client: TestClient) -> None:
    response = client.post("/api/ai/chat", json={"question": "What does the Test Engineer do?"})

    assert response.status_code == 200
    body = response.json()
    assert body["answer"]
    assert body["grounded"] is True


def test_chat_refuses_an_out_of_scope_question(client: TestClient) -> None:
    """The grounding test. Never relax this to make a provider pass."""
    response = client.post("/api/ai/chat", json={"question": "What is the capital of France?"})

    assert response.status_code == 200
    body = response.json()
    assert body["grounded"] is False
    assert "don't have evidence" in body["answer"].lower()


def test_chat_returns_timings_for_engineer_mode(client: TestClient) -> None:
    body = client.post("/api/ai/chat", json={"question": "What does the Test Engineer do?"}).json()

    assert set(body) >= {
        "answer", "grounded", "sources", "retrieval_ms", "generation_ms", "provider",
    }
    assert isinstance(body["retrieval_ms"], (int, float))
    assert isinstance(body["generation_ms"], (int, float))


def test_chat_rejects_an_empty_question(client: TestClient) -> None:
    assert client.post("/api/ai/chat", json={"question": "   "}).status_code == 422


def test_template_provider_needs_no_api_key() -> None:
    """The always-works fallback: a live demo never shows a broken AI feature."""
    provider = TemplateProvider()

    answer = provider.generate("question", ["Test Engineer did a testable thing."])

    assert "testable thing" in answer.lower()


def test_unknown_provider_falls_back_to_template(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_PROVIDER", "does-not-exist")

    assert isinstance(resolve_provider("does-not-exist"), TemplateProvider)


# ---------------------------------------------------------------------------
# Phase 5 — live GitHub sources attached to a grounded answer.
#
# The rule under test is rule 15: a tool never reshapes RAG. Live repos may
# *supplement* an answer retrieval already grounded; they may never rescue one
# it refused. The refusal test above must keep passing untouched — that is the
# evidence the guarantee survived this phase.
# ---------------------------------------------------------------------------
REPOS = [
    {
        "name": "friday",
        "description": "A Python assistant.",
        "html_url": "https://github.com/test/friday",
        "language": "Python",
        "topics": ["ai"],
        "pushed_at": "2026-08-01T00:00:00Z",
        "fork": False,
    }
]


def _github_client(payload: list[dict] | None = None) -> GitHubClient:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload if payload is not None else REPOS)

    return GitHubClient(
        username="test", settings=Settings(), transport=httpx.MockTransport(handler)
    )


@pytest.fixture
def live_client(content_dir: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("AI_PROVIDER", "template")
    return TestClient(create_app(content_dir=content_dir, github_client=_github_client()))


def test_a_grounded_answer_attaches_live_sources_separately(live_client: TestClient) -> None:
    """Portfolio evidence and live repo data, attributed to their own origins."""
    body = live_client.post(
        "/api/ai/chat", json={"question": "What Python work has the Test Engineer done?"}
    ).json()

    assert body["grounded"] is True
    assert body["sources"], "portfolio evidence should still be present"
    assert body["live_sources"], "the Python repo should have been attached"
    assert body["live_sources"][0]["type"] == "github-repo"
    assert body["live_sources"][0]["url"] == "https://github.com/test/friday"
    # Separately attributed: a live repo must never appear as portfolio evidence.
    assert all(s["type"] != "github-repo" for s in body["sources"])


def test_an_ungrounded_question_is_still_refused_with_no_live_sources(
    live_client: TestClient,
) -> None:
    """A tool must not widen what the assistant is willing to answer."""
    body = live_client.post(
        "/api/ai/chat", json={"question": "What is the capital of France?"}
    ).json()

    assert body["grounded"] is False
    assert body["live_sources"] == []


def test_an_unrelated_grounded_question_attaches_nothing(live_client: TestClient) -> None:
    """The tool fires on a metadata match, not on every grounded question."""
    body = live_client.post(
        "/api/ai/chat", json={"question": "Where did the Test Person study?"}
    ).json()

    assert body["grounded"] is True
    assert body["live_sources"] == []


def test_chat_works_when_github_is_unavailable(
    content_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A dead tool degrades the answer, never the endpoint."""
    monkeypatch.setenv("AI_PROVIDER", "template")

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("no route to host")

    broken = GitHubClient(
        username="test", settings=Settings(), transport=httpx.MockTransport(handler)
    )
    client = TestClient(create_app(content_dir=content_dir, github_client=broken))

    body = client.post(
        "/api/ai/chat", json={"question": "What Python work has the Test Engineer done?"}
    ).json()

    assert body["grounded"] is True
    assert body["live_sources"] == []
