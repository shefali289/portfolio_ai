"""The MCP adapter.

The server is a thin registration layer over `PortfolioTools`. What matters is
that it exposes exactly those tools and that calling one through MCP returns the
same data as calling the function — an adapter that transforms is a bug.

`asyncio.run` rather than pytest-asyncio: the MCP API is async, but nothing else
in this suite is, and one wrapper is cheaper than a plugin-wide mode change.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import httpx
import pytest

from app.config import Settings
from app.integrations.github import GitHubClient
from app.integrations.mcp_server import build_server
from app.integrations.tools import TOOL_NAMES, PortfolioTools
from app.rag.retriever import Retriever
from app.services.content import ContentService


@pytest.fixture
def tools(content_dir: Path, stub_embeddings) -> PortfolioTools:
    content = ContentService(content_dir)

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[])

    return PortfolioTools(
        content=content,
        retriever=Retriever.from_content(content, stub_embeddings),
        github=GitHubClient(
            username="test",
            settings=Settings(),
            transport=httpx.MockTransport(handler),
        ),
    )


def _text(result) -> str:
    return "".join(block.text for block in result.content)


def test_the_server_exposes_exactly_the_six_tools(tools: PortfolioTools) -> None:
    server = build_server(tools)

    listed = asyncio.run(server.list_tools())

    assert sorted(t.name for t in listed) == sorted(TOOL_NAMES)


def test_every_tool_has_a_description(tools: PortfolioTools) -> None:
    """An MCP client picks a tool by its description; a blank one is unusable."""
    listed = asyncio.run(build_server(tools).list_tools())

    assert all(t.description for t in listed)


def test_calling_a_tool_returns_the_same_payload_as_the_function(
    tools: PortfolioTools,
) -> None:
    server = build_server(tools)

    result = asyncio.run(server.call_tool("get_profile", {}))

    assert json.loads(_text(result))["name"] == tools.get_profile()["name"]


def test_a_tool_with_an_argument_is_callable_through_mcp(tools: PortfolioTools) -> None:
    server = build_server(tools)

    result = asyncio.run(server.call_tool("search_projects", {"query": "Python"}))

    assert "Test Project" in _text(result)
