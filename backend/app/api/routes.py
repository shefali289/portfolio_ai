"""HTTP interface. Thin by design: parse, call a service, return.

Any branching here that is not error mapping belongs in a service.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.api.schemas import HealthResponse
from app.services.content import ContentService
from app.services.content_models import Profile

router = APIRouter(prefix="/api")


def get_content(request: Request) -> ContentService:
    """The service is built once at startup and held on app state."""
    return request.app.state.content


# Annotated form rather than a `Depends()` default: ruff flags the default-arg
# form as B008, and this is FastAPI's current idiom regardless.
ContentDep = Annotated[ContentService, Depends(get_content)]


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/profile", response_model=Profile)
def profile(content: ContentDep) -> Profile:
    return content.profile
