"""The chain: four agents, in sequence.

Composition, not a framework. Each step is timed and recorded so the UI can show
it ticking over, and **any step that raises aborts the run** — a half-filled
report that looks complete is worse than an error.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from app.agents.base import AgentStep, JobMatchReport, Verdict
from app.agents.evidence import assess_evidence
from app.agents.portfolio import gather_evidence
from app.agents.requirement import extract_requirements
from app.agents.response import compose_response
from app.rag.retriever import Retriever
from app.services.content import ContentService

STEP_LABELS = {
    "requirement": "Understanding the role",
    "portfolio": "Searching the portfolio",
    "evidence": "Weighing the evidence",
    "response": "Preparing the response",
}


class ChainError(RuntimeError):
    """A step failed. The run is abandoned rather than partially reported."""


def _run_step(name: str, steps: list[AgentStep], fn: Callable[[], Any]) -> Any:
    started = time.perf_counter()
    try:
        result = fn()
    except Exception as exc:  # noqa: BLE001 - re-raised as ChainError with context
        steps.append(AgentStep(name=name, label=STEP_LABELS[name], status="failed"))
        raise ChainError(f"The '{name}' step failed: {exc}") from exc

    steps.append(
        AgentStep(
            name=name,
            label=STEP_LABELS[name],
            status="done",
            ms=round((time.perf_counter() - started) * 1000, 2),
        )
    )
    return result


def run_chain(
    job_description: str, content: ContentService, retriever: Retriever
) -> JobMatchReport:
    steps: list[AgentStep] = []

    requirements = _run_step(
        "requirement", steps, lambda: extract_requirements(job_description, content)
    )
    gathered = _run_step("portfolio", steps, lambda: gather_evidence(requirements, retriever))
    assessed = _run_step("evidence", steps, lambda: assess_evidence(gathered))
    summary = _run_step("response", steps, lambda: compose_response(assessed))

    return JobMatchReport(
        matches=[m for m in assessed if m.verdict is not Verdict.GAP],
        gaps=[m for m in assessed if m.verdict is Verdict.GAP],
        summary=summary,
        steps=steps,
        provider="template",
    )
