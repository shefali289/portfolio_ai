"""FastAPI application.

`create_app` is a factory so tests can wire the app to a fixture content
directory. `app` at module level is what `uvicorn app.main:app` serves, built
from settings.

Content is loaded during app construction, not on first request: if a content
file is malformed the process fails immediately and visibly. The vector index is
built at the same moment — the corpus is small, and building on boot removes a
whole class of "the index is stale" failure.
"""

from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import get_settings
from app.integrations.github import GitHubClient
from app.integrations.tools import PortfolioTools
from app.services.ai import AiService
from app.services.content import ContentService
from app.services.job_match import JobMatchService

logger = logging.getLogger(__name__)


def create_app(
    content_dir: Path | None = None,
    embedding_provider=None,
    github_client: GitHubClient | None = None,
) -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="AI-Powered Engineer Portfolio API",
        description="Serves portfolio content from content/*.json, and answers "
        "questions grounded in it.",
        version="0.3.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Eager load — a bad content file must fail the boot, not a live request.
    content = ContentService(content_dir or settings.content_dir)
    app.state.content = content
    # One client, so the 15-minute cache is shared by every request rather than
    # each one spending from the 60/hour unauthenticated budget.
    github = github_client or GitHubClient.from_content(content, settings)
    app.state.github = github
    ai = AiService.build(content, settings, embedding_provider, github=github)
    app.state.ai = ai
    # Same retriever instance: job-match and Ask My Portfolio share one search path.
    app.state.job_match = JobMatchService(content, ai.retriever)
    # The same six callables the MCP server exposes back the HTTP surface.
    app.state.tools = PortfolioTools(content=content, retriever=ai.retriever, github=github)

    app.include_router(router)
    return app


app = create_app()
