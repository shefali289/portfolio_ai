"""Agent 4 — compose the report a reader actually sees.

One responsibility: turn verdicts into prose. It states gaps plainly rather than
burying them, because a match report that hides its gaps is worth nothing to the
person reading it.

Composition is deterministic by default so the feature works with no API key.
"""

from __future__ import annotations

from app.agents.base import RequirementMatch, Verdict


def _plural(n: int, word: str) -> str:
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def compose_response(assessed: list[RequirementMatch]) -> str:
    matched = [m for m in assessed if m.verdict is not Verdict.GAP]
    gaps = [m for m in assessed if m.verdict is Verdict.GAP]

    if not assessed:
        return "No requirements could be read from that job description."

    lines = [
        f"Found evidence for {_plural(len(matched), 'requirement')} "
        f"of {len(assessed)}."
    ]

    if matched:
        strong = [m for m in matched if m.verdict is Verdict.MATCH]
        partial = [m for m in matched if m.verdict is Verdict.PARTIAL]
        if strong:
            lines.append("Strong: " + ", ".join(m.requirement.text for m in strong) + ".")
        if partial:
            lines.append(
                "Partial: " + ", ".join(m.requirement.text for m in partial) + "."
            )

    if gaps:
        # Stated plainly. No hedging, no "could quickly learn".
        lines.append(
            "Not evidenced in this portfolio: "
            + ", ".join(m.requirement.text for m in gaps)
            + "."
        )

    return " ".join(lines)
