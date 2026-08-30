"""Prompts for grounded answering.

The refusal string is a constant because it is asserted by the grounding test
and shown verbatim in the UI — it must not drift between provider, route and
test.
"""

from __future__ import annotations

REFUSAL = (
    "I don't have evidence of that in the portfolio. Ask me about the roles, "
    "projects, skills or qualifications it contains."
)

SYSTEM_RULES = """You answer questions about one person's portfolio.

Rules:
- Use ONLY the context below. It is the complete source of truth.
- If the context does not support an answer, say you don't have evidence of it.
- Never invent an employer, date, metric, title or technology.
- Be concise and factual. Do not embellish.
"""


def build_prompt(question: str, context: list[str]) -> str:
    joined = "\n\n".join(f"- {c}" for c in context)
    return f"{SYSTEM_RULES}\nContext:\n{joined}\n\nQuestion: {question}\n\nAnswer:"
