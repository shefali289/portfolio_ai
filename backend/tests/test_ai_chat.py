"""POST /api/ai/chat — grounded answers, and refusal when ungrounded."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.ai.provider import TemplateProvider, resolve_provider
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
