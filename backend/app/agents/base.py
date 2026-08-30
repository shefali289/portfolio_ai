"""Types shared by the job-match chain.

The chain is four plain functions composed in sequence — deliberately not a
framework. Each agent is typed in and typed out, which is what makes each one
independently testable and the sequence legible.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class Verdict(StrEnum):
    """How well the portfolio supports one requirement.

    `GAP` is a first-class outcome, not a failure. A requirement with no
    supporting evidence is reported as a gap and never softened into a partial
    match — honest gaps are the point of the feature.
    """

    MATCH = "match"
    PARTIAL = "partial"
    GAP = "gap"


class Requirement(BaseModel):
    """One thing the job description asks for."""

    text: str
    source_line: str = ""


class RequirementEvidence(BaseModel):
    """A retrieved chunk offered as support for a requirement."""

    text: str
    source: str
    score: float


class RequirementMatch(BaseModel):
    requirement: Requirement
    verdict: Verdict
    evidence: list[RequirementEvidence] = Field(default_factory=list)


class AgentStep(BaseModel):
    """One step of the chain, for the UI to show as it ran."""

    name: str
    label: str
    status: str = "done"
    ms: float = 0.0


class JobMatchReport(BaseModel):
    matches: list[RequirementMatch]
    gaps: list[RequirementMatch]
    summary: str
    steps: list[AgentStep] = Field(default_factory=list)
    provider: str = "none"
