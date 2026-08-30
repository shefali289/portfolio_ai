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


class ChatResponse(BaseModel):
    """`grounded=False` means the question was refused, not answered."""

    answer: str
    grounded: bool
    sources: list[ChatSource]
    retrieval_ms: float
    generation_ms: float
    provider: str


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
