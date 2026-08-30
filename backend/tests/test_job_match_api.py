"""POST /api/ai/job-match."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app

JD = """We are hiring a Python engineer.
You will build FastAPI services and deploy them on Kubernetes."""


@pytest.fixture
def client(content_dir: Path) -> TestClient:
    return TestClient(create_app(content_dir=content_dir))


def test_job_match_returns_a_report(client: TestClient) -> None:
    response = client.post("/api/ai/job-match", json={"job_description": JD})

    assert response.status_code == 200
    body = response.json()
    assert set(body) >= {"matches", "gaps", "summary", "steps", "provider"}


def test_the_four_steps_are_returned_in_order(client: TestClient) -> None:
    body = client.post("/api/ai/job-match", json={"job_description": JD}).json()

    assert [s["name"] for s in body["steps"]] == [
        "requirement",
        "portfolio",
        "evidence",
        "response",
    ]
    assert all(s["label"] for s in body["steps"])


def test_an_unsupported_requirement_is_reported_as_a_gap(client: TestClient) -> None:
    """Honest gaps are the feature. Never softened, never omitted."""
    body = client.post("/api/ai/job-match", json={"job_description": JD}).json()

    gap_texts = [g["requirement"]["text"].lower() for g in body["gaps"]]
    assert any("kubernetes" in t for t in gap_texts)
    assert all(g["evidence"] == [] for g in body["gaps"])


def test_the_summary_names_the_gaps(client: TestClient) -> None:
    body = client.post("/api/ai/job-match", json={"job_description": JD}).json()

    assert "not evidenced" in body["summary"].lower()


def test_a_blank_job_description_is_rejected(client: TestClient) -> None:
    assert client.post("/api/ai/job-match", json={"job_description": "  "}).status_code == 422
