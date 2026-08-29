"""FastAPI application.

`create_app` is a factory so tests can wire the app to a fixture content
directory. `app` at module level is what `uvicorn app.main:app` serves, built
from settings.

Content is loaded during app construction, not on first request: if a content
file is malformed the process fails immediately and visibly.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import get_settings
from app.services.content import ContentService


def create_app(content_dir: Path | None = None) -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="AI-Powered Engineer Portfolio API",
        description="Serves portfolio content from content/*.json.",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Eager load — a bad content file must fail the boot, not a live request.
    app.state.content = ContentService(content_dir or settings.content_dir)
    app.include_router(router)

    return app


app = create_app()
