"""MCP adapter.

Registration only. Every tool body lives in `PortfolioTools`, so the MCP surface
and the HTTP surface expose the same behaviour and there is one place to fix.

Run it over stdio:

    cd backend && .venv/Scripts/python.exe -m app.integrations.mcp_server

MCP 2.x renamed `FastMCP` to `MCPServer`; the v1 import path raises a
`ModuleNotFoundError` that says so.
"""

from __future__ import annotations

from typing import Any

from mcp.server.mcpserver import MCPServer

from app.integrations.tools import PortfolioTools

SERVER_NAME = "portfolio"


def build_server(tools: PortfolioTools) -> MCPServer:
    """Register the six portfolio tools on a new server.

    Each wrapper delegates immediately and keeps the underlying docstring: an
    MCP client chooses a tool by its description, so the description is part of
    the interface rather than a comment.
    """
    server = MCPServer(name=SERVER_NAME, version="0.5.0")

    @server.tool(description=tools.get_profile.__doc__)
    def get_profile() -> dict[str, Any]:
        return tools.get_profile()

    @server.tool(description=tools.get_projects.__doc__)
    def get_projects() -> list[dict[str, Any]]:
        return tools.get_projects()

    @server.tool(description=tools.search_projects.__doc__)
    def search_projects(query: str) -> list[dict[str, Any]]:
        return tools.search_projects(query)

    @server.tool(description=tools.search_resume.__doc__)
    def search_resume(query: str, k: int = 4) -> list[dict[str, Any]]:
        return tools.search_resume(query, k=k)

    @server.tool(description=tools.get_skills.__doc__)
    def get_skills() -> list[dict[str, Any]]:
        return tools.get_skills()

    @server.tool(description=tools.get_github_projects.__doc__)
    def get_github_projects() -> dict[str, Any]:
        return tools.get_github_projects()

    return server


def build_default_server() -> MCPServer:
    """Wire the server from settings, for the stdio entry point."""
    from app.config import get_settings  # noqa: PLC0415
    from app.integrations.github import GitHubClient  # noqa: PLC0415
    from app.rag.embeddings import get_embedding_provider  # noqa: PLC0415
    from app.rag.retriever import Retriever  # noqa: PLC0415
    from app.services.content import ContentService  # noqa: PLC0415

    settings = get_settings()
    content = ContentService(settings.content_dir)
    return build_server(
        PortfolioTools(
            content=content,
            retriever=Retriever.from_content(content, get_embedding_provider(settings)),
            github=GitHubClient.from_content(content, settings),
        )
    )


if __name__ == "__main__":  # pragma: no cover - process entry point
    build_default_server().run()
