"""HTTP-facing shapes only.

Domain content models live in `app/services/content_models.py`. Endpoints that
return portfolio content return those models directly, so there is no second
copy of `Profile` here to drift out of step with the content files.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from app.agents.base import JobMatchReport
from app.services.content_models import (
    EngineeringNotes,
    Experience,
    Profile,
    Projects,
    Skills,
)


class HealthResponse(BaseModel):
    status: str


class ErrorResponse(BaseModel):
    """Errors return a typed shape, never a bare 500 with a stack trace."""

    detail: str


class ContentResponse(BaseModel):
    """The five cached content areas consumed by the portfolio page."""

    profile: Profile
    experience: Experience
    skills: Skills
    projects: Projects
    engineering_notes: EngineeringNotes


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)

    @field_validator("question")
    @classmethod
    def _not_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("question must not be blank")
        return cleaned


class ChatSource(BaseModel):
    source: str
    type: str


class LiveSource(BaseModel):
    """Evidence fetched from an external tool, not retrieved from the portfolio.

    Kept in its own field rather than mixed into `sources` so a reader can
    always tell stored knowledge from live data — the distinction Phase 5
    exists to demonstrate.
    """

    source: str
    type: str
    url: str


class ChatResponse(BaseModel):
    """`grounded=False` means the question was refused, not answered."""

    answer: str
    grounded: bool
    sources: list[ChatSource]
    retrieval_ms: float
    generation_ms: float
    provider: str
    live_sources: list[LiveSource] = []


class GithubRepoResponse(BaseModel):
    name: str
    description: str | None
    url: str
    language: str | None
    topics: list[str]
    pushed_at: str


class GithubReposResponse(BaseModel):
    """`reason` says why the list is empty, so the UI degrades honestly."""

    repos: list[GithubRepoResponse]
    reason: str | None = None


class JobMatchRequest(BaseModel):
    job_description: str = Field(min_length=1, max_length=20000)

    @field_validator("job_description")
    @classmethod
    def _not_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("job_description must not be blank")
        return cleaned


JobMatchResponse = JobMatchReport
