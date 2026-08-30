"""The portfolio tool layer.

These six callables are the capability. MCP and HTTP are both thin adapters
over them, so testing the functions directly tests what both surfaces expose.
"""

from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from app.config import Settings
from app.integrations.github import GitHubClient
from app.integrations.tools import TOOL_NAMES, PortfolioTools
from app.rag.retriever import Retriever
from app.services.content import ContentService


def _github(payload: list[dict] | None = None, *, status: int = 200) -> GitHubClient:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, json=payload if payload is not None else [])

    return GitHubClient(
        username="test", settings=Settings(), transport=httpx.MockTransport(handler)
    )


@pytest.fixture
def tools(content_dir: Path, stub_embeddings) -> PortfolioTools:
    content = ContentService(content_dir)
    return PortfolioTools(
        content=content,
        retriever=Retriever.from_content(content, stub_embeddings),
        github=_github(
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


def test_exactly_six_tools_are_exposed() -> None:
    """The phase specifies six. A seventh is scope creep; a fifth is a gap."""
    assert TOOL_NAMES == (
        "get_profile",
        "get_projects",
        "search_projects",
        "search_resume",
        "get_skills",
        "get_github_projects",
    )


def test_every_tool_name_resolves_to_a_callable(tools: PortfolioTools) -> None:
    for name in TOOL_NAMES:
        assert callable(getattr(tools, name)), name


def test_get_profile_returns_content_not_invention(tools: PortfolioTools) -> None:
    profile = tools.get_profile()

    assert profile["name"] == "Test Person"
    assert profile["title"] == "Test Engineer"


def test_get_projects_returns_the_portfolio_projects(tools: PortfolioTools) -> None:
    projects = tools.get_projects()

    assert [p["name"] for p in projects] == ["Test Project"]


def test_search_projects_matches_on_a_technology(tools: PortfolioTools) -> None:
    assert [p["name"] for p in tools.search_projects("Python")] == ["Test Project"]


def test_search_projects_returns_empty_for_an_absent_term(tools: PortfolioTools) -> None:
    assert tools.search_projects("Kubernetes") == []


def test_search_resume_returns_grounded_chunks(tools: PortfolioTools) -> None:
    hits = tools.search_resume("What does the Test Engineer do?")

    assert hits
    assert all({"text", "source", "type", "score"} <= set(h) for h in hits)


def test_get_skills_returns_the_skill_groups(tools: PortfolioTools) -> None:
    groups = tools.get_skills()

    assert [g["name"] for g in groups] == ["Test Group"]
    assert "Python" in [s["name"] for s in groups[0]["skills"]]


def test_get_github_projects_returns_live_repos(tools: PortfolioTools) -> None:
    result = tools.get_github_projects()

    assert result["reason"] is None
    assert [r["name"] for r in result["repos"]] == ["friday"]


def test_get_github_projects_degrades_with_a_reason(
    content_dir: Path, stub_embeddings
) -> None:
    """A tool failure is reported, never raised into whatever called it."""
    content = ContentService(content_dir)
    tools = PortfolioTools(
        content=content,
        retriever=Retriever.from_content(content, stub_embeddings),
        github=_github(status=500),
    )

    result = tools.get_github_projects()

    assert result["repos"] == []
    assert result["reason"] is not None
