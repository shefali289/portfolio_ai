"""HTTP surface: /api/health and /api/profile."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

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


def test_unknown_route_returns_404(client: TestClient) -> None:
    assert client.get("/api/nope").status_code == 404


def test_cors_headers_allow_the_configured_origin(client: TestClient) -> None:
    response = client.get("/api/health", headers={"Origin": "http://localhost:5173"})

    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
