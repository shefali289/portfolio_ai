"""HTTP surface: /api/health and /api/profile."""

from __future__ import annotations

from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.integrations.github import GitHubClient
from app.main import create_app


@pytest.fixture
def client(content_dir: Path) -> TestClient:
    """An app wired to the fixture content directory, not the real one."""
    return TestClient(create_app(content_dir=content_dir))


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_profile_returns_the_name_and_title(client: TestClient) -> None:
    response = client.get("/api/profile")

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Test Person"
    assert body["title"] == "Test Engineer"


def test_profile_returns_the_documented_shape(client: TestClient) -> None:
    body = client.get("/api/profile").json()

    assert set(body) == {
        "name",
        "title",
        "location",
        "summary",
        "links",
        "education",
        "certifications",
        "languages",
    }
    assert body["links"]["email"] == "test@example.com"


def test_profile_does_not_expose_a_phone_number(client: TestClient) -> None:
    """The phone number lives in docs/resume.md and must not reach the API."""
    body = client.get("/api/profile").json()

    assert "phone" not in body
    assert "phone" not in body["links"]


def test_content_returns_all_five_validated_content_areas(client: TestClient) -> None:
    response = client.get("/api/content")

    assert response.status_code == 200
    body = response.json()
    assert set(body) == {
        "profile",
        "experience",
        "skills",
        "projects",
        "engineering_notes",
    }
    assert body["profile"]["name"] == "Test Person"
    assert body["experience"]["roles"][0]["company"] == "Test Company"
    assert body["skills"]["groups"][0]["name"] == "Test Group"
    assert body["projects"]["projects"][0]["name"] == "Test Project"
    assert body["engineering_notes"]["achievements"][0]["name"] == "Test Achievement"


def test_unknown_route_returns_404(client: TestClient) -> None:
    assert client.get("/api/nope").status_code == 404


def test_cors_headers_allow_the_configured_origin(client: TestClient) -> None:
    response = client.get("/api/health", headers={"Origin": "http://localhost:5173"})

    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


# --- Phase 5: GET /api/github/repos ----------------------------------------
def _github(payload: list[dict] | None = None, *, status: int = 200) -> GitHubClient:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, json=payload if payload is not None else [])

    return GitHubClient(
        username="test", settings=Settings(), transport=httpx.MockTransport(handler)
    )


def test_github_repos_returns_live_repositories(content_dir: Path) -> None:
    app = create_app(
        content_dir=content_dir,
        github_client=_github(
            [
                {
                    "name": "friday",
                    "description": "An assistant.",
                    "html_url": "https://github.com/test/friday",
                    "language": "Python",
                    "topics": ["ai"],
                    "pushed_at": "2026-08-01T00:00:00Z",
                    "fork": False,
                }
            ]
        ),
    )

    response = TestClient(app).get("/api/github/repos")

    assert response.status_code == 200
    body = response.json()
    assert [r["name"] for r in body["repos"]] == ["friday"]
    assert body["reason"] is None


def test_github_repos_returns_200_with_a_reason_when_unavailable(content_dir: Path) -> None:
    """A supplementary section must never surface as a failed request."""
    app = create_app(content_dir=content_dir, github_client=_github(status=500))

    response = TestClient(app).get("/api/github/repos")

    assert response.status_code == 200
    body = response.json()
    assert body["repos"] == []
    assert body["reason"]
