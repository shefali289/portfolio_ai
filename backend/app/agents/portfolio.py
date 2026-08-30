"""Agent 2 — find portfolio evidence for each requirement.

One responsibility: retrieve. It does not judge sufficiency — that is agent 3.

The retriever is **injected**, never constructed here. That keeps one search
path shared with Ask My Portfolio: two retrieval implementations would drift
apart and start answering the same question differently.
"""

from __future__ import annotations

import re

from app.agents.base import Requirement, RequirementEvidence, RequirementMatch, Verdict
from app.rag.retriever import Retriever

# An exact term hit is unambiguous evidence, so it scores above any threshold.
EXACT_TERM_SCORE = 1.0


def _exact_hits(term: str, retriever: Retriever) -> list[RequirementEvidence]:
    """Chunks that name the requirement verbatim.

    Vector search alone under-serves single-word requirements: a one-token query
    against a long chunk scores low on cosine, so "FastAPI" looked like a gap
    even though a role explicitly lists it. A term that literally appears in the
    portfolio is evidence, and reporting it as a gap would understate real
    experience - the opposite of the honesty this feature is for.
    """
    pattern = re.compile(rf"(?<!\w){re.escape(term)}(?!\w)", re.IGNORECASE)
    return [
        RequirementEvidence(text=chunk.text, source=chunk.source, score=EXACT_TERM_SCORE)
        for chunk in retriever.chunks
        if pattern.search(chunk.text)
    ]


def gather_evidence(
    requirements: list[Requirement], retriever: Retriever, k: int = 3
) -> list[RequirementMatch]:
    gathered: list[RequirementMatch] = []

    for requirement in requirements:
        exact = _exact_hits(requirement.text, retriever)
        seen = {e.source for e in exact}

        semantic = [
            RequirementEvidence(text=hit.chunk.text, source=hit.chunk.source, score=hit.score)
            for hit in retriever.retrieve(requirement.text, k=k)
            if hit.chunk.source not in seen
        ]

        gathered.append(
            RequirementMatch(
                requirement=requirement,
                # Verdict is deliberately provisional here; agent 3 decides.
                verdict=Verdict.GAP,
                evidence=(exact + semantic)[:k],
            )
        )

    return gathered
