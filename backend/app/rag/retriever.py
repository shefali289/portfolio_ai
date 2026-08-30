"""Retrieval over the portfolio index.

`is_grounded` is the anti-hallucination gate: if nothing clears the similarity
threshold, the question is out of scope and the caller must refuse rather than
let a model improvise from irrelevant context.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.rag.chunk import Chunk, build_chunks
from app.rag.index import VectorIndex
from app.services.content import ContentService

# Cosine similarity below this means nothing relevant was found.
GROUNDING_THRESHOLD = 0.25


@dataclass(frozen=True)
class Hit:
    chunk: Chunk
    score: float


class Retriever:
    def __init__(self, index: VectorIndex, chunks: list[Chunk], provider: Any) -> None:
        self._index = index
        self._chunks = chunks
        self._provider = provider

    @classmethod
    def from_content(cls, content: ContentService, provider: Any) -> Retriever:
        """Build an in-memory index. Used by tests and by first-run startup."""
        chunks = build_chunks(content)
        index = VectorIndex.build(
            texts=[c.text for c in chunks],
            metadata=[{"source": c.source, "type": c.type} for c in chunks],
            provider=provider,
        )
        return cls(index, chunks, provider)

    @property
    def chunks(self) -> list[Chunk]:
        """The indexed corpus, for exact-term lookups alongside vector search."""
        return self._chunks

    def retrieve(self, question: str, k: int = 4) -> list[Hit]:
        vector = self._provider.embed([question])[0]
        return [
            Hit(chunk=self._chunks[i], score=score)
            for i, score in self._index.search(vector, k)
            if i < len(self._chunks)
        ]

    @staticmethod
    def is_grounded(hits: list[Hit]) -> bool:
        return bool(hits) and hits[0].score >= GROUNDING_THRESHOLD
