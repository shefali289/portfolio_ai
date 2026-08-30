"""HTTP interface. Thin by design: parse, call a service, return.

Any branching here that is not error mapping belongs in a service.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.agents.base import JobMatchReport
from app.api.schemas import (
    ChatRequest,
    ChatResponse,
    ContentResponse,
    HealthResponse,
    JobMatchRequest,
)
from app.services.ai import AiService
from app.services.content import ContentService
from app.services.content_models import Profile
from app.services.job_match import JobMatchService

router = APIRouter(prefix="/api")


def get_content(request: Request) -> ContentService:
    """The service is built once at startup and held on app state."""
    return request.app.state.content


def get_ai(request: Request) -> AiService:
    return request.app.state.ai


def get_job_match(request: Request) -> JobMatchService:
    return request.app.state.job_match


# Annotated form rather than a `Depends()` default: ruff flags the default-arg
# form as B008, and this is FastAPI's current idiom regardless.
ContentDep = Annotated[ContentService, Depends(get_content)]
AiDep = Annotated[AiService, Depends(get_ai)]
JobMatchDep = Annotated[JobMatchService, Depends(get_job_match)]


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/profile", response_model=Profile)
def profile(content: ContentDep) -> Profile:
    return content.profile


@router.get("/content", response_model=ContentResponse)
def portfolio_content(content: ContentDep) -> ContentResponse:
    return ContentResponse(
        profile=content.profile,
        experience=content.experience,
        skills=content.skills,
        projects=content.projects,
        engineering_notes=content.engineering_notes,
    )


@router.post("/ai/chat", response_model=ChatResponse)
def chat(request: ChatRequest, ai: AiDep) -> ChatResponse:
    """Retrieve, ground, generate.

    An ungrounded question is refused inside the service, before any model is
    called - refusal is a property of retrieval, not a request to the LLM.
    """
    return ai.answer(request.question)


@router.post("/ai/job-match", response_model=JobMatchReport)
def job_match(request: JobMatchRequest, service: JobMatchDep) -> JobMatchReport:
    """Run the four-agent chain over a job description.

    Returns the report plus the steps it took, so the UI can show each agent
    ticking over. A requirement with no evidence comes back as a gap.
    """
    return service.match(request.job_description)
