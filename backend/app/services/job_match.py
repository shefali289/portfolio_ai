"""Job-match orchestration.

Thin by design: it holds the content and retriever the chain needs and runs it.
The reasoning lives in `app/agents/`, one responsibility per module.
"""

from __future__ import annotations

from app.agents.base import JobMatchReport
from app.agents.chain import run_chain
from app.rag.retriever import Retriever
from app.services.content import ContentService


class JobMatchService:
    def __init__(self, content: ContentService, retriever: Retriever) -> None:
        self._content = content
        self._retriever = retriever

    def match(self, job_description: str) -> JobMatchReport:
        # Reuses the same retriever as Ask My Portfolio - one search path.
        return run_chain(job_description, self._content, self._retriever)
