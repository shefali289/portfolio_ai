"""Grounded question answering.

The behaviour lives here, not in the router: retrieve, decide whether the
question is grounded, and only then generate.

Refusal is decided by **retrieval**, before any model is called. Asking an LLM
to police its own scope is a request, not a guarantee; a similarity threshold is
a guarantee.
"""

from __future__ import annotations

import logging
import time

from app.ai.prompts import REFUSAL
from app.ai.provider import generate_with_fallback, resolve_provider
from app.api.schemas import ChatResponse, ChatSource
from app.config import Settings
from app.rag.retriever import Retriever
from app.services.content import ContentService

logger = logging.getLogger(__name__)


class AiService:
    def __init__(self, retriever: Retriever, settings: Settings) -> None:
        self._retriever = retriever
        self._settings = settings

    @classmethod
    def build(
        cls, content: ContentService, settings: Settings, embedding_provider=None
    ) -> AiService:
        """Build the in-memory index at startup.

        The corpus is ~60 chunks, so indexing on boot costs little and removes a
        whole class of "the index is stale" failure. `embedding_provider` is
        injectable so tests never reach the network.
        """
        if embedding_provider is None:
            from app.rag.embeddings import get_embedding_provider  # noqa: PLC0415

            embedding_provider = get_embedding_provider(settings)
        return cls(Retriever.from_content(content, embedding_provider), settings)

    def answer(self, question: str, k: int = 4) -> ChatResponse:
        started = time.perf_counter()
        hits = self._retriever.retrieve(question, k=k)
        retrieval_ms = (time.perf_counter() - started) * 1000

        if not Retriever.is_grounded(hits):
            # Out of scope. Refuse without generating: no model, no chance to
            # improvise from irrelevant context.
            return ChatResponse(
                answer=REFUSAL,
                grounded=False,
                sources=[],
                retrieval_ms=round(retrieval_ms, 2),
                generation_ms=0.0,
                provider="none",
            )

        provider = resolve_provider(settings=self._settings)
        started = time.perf_counter()
        answer, used = generate_with_fallback(provider, question, [h.chunk.text for h in hits])
        generation_ms = (time.perf_counter() - started) * 1000

        return ChatResponse(
            answer=answer,
            grounded=True,
            sources=[ChatSource(source=h.chunk.source, type=h.chunk.type) for h in hits],
            retrieval_ms=round(retrieval_ms, 2),
            generation_ms=round(generation_ms, 2),
            provider=used,
        )
