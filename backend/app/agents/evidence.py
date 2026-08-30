"""Agent 3 — decide whether the evidence actually supports each requirement.

One responsibility, and the one that carries the feature's integrity: a
requirement with nothing above the retrieval threshold is a **gap**.

The verdict is computed from retrieval scores, never asked of a model. Asking an
LLM "is this good enough evidence?" is how a gap quietly becomes a partial
match, which would make the whole report untrustworthy.
"""

from __future__ import annotations

from app.agents.base import RequirementMatch, Verdict
from app.rag.retriever import GROUNDING_THRESHOLD

# Comfortably above the grounding floor: enough to call it a real match rather
# than a weak lexical coincidence.
STRONG_MATCH = 0.45


def assess_evidence(gathered: list[RequirementMatch]) -> list[RequirementMatch]:
    assessed: list[RequirementMatch] = []

    for item in gathered:
        supporting = [e for e in item.evidence if e.score >= GROUNDING_THRESHOLD]

        if not supporting:
            # No evidence. Report it as a gap and carry nothing forward - a gap
            # with attached "evidence" reads as a soft match.
            assessed.append(
                RequirementMatch(requirement=item.requirement, verdict=Verdict.GAP, evidence=[])
            )
            continue

        best = max(e.score for e in supporting)
        verdict = Verdict.MATCH if best >= STRONG_MATCH else Verdict.PARTIAL
        assessed.append(
            RequirementMatch(
                requirement=item.requirement, verdict=verdict, evidence=supporting
            )
        )

    return assessed
