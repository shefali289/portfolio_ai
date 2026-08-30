"""Agent 1 — extract what the job description asks for.

One responsibility: turn free text into a list of requirements.

This must work with **no LLM**, because `template` is the default provider. So
extraction is lexical: known skills from `content/*.json`, plus technology-shaped
tokens the JD mentions that the portfolio has never heard of.

That second half matters. If requirements could only ever be skills the
portfolio already knows, a gap would be impossible by construction — the feature
would be incapable of reporting bad news, which is exactly what it exists to do.
"""

from __future__ import annotations

import re

from app.agents.base import Requirement
from app.services.content import ContentService

# Sentence-initial words are capitalised by grammar, not because they are
# technologies. Excluding them stops "We", "You" and "Experience" becoming
# requirements.
_COMMON = frozenset(
    "we you they it this that the a an and or but for with on at to in of is are "
    "will would should must have has had can could you'll experience required "
    "hiring build deploy work working role team strong plus nice "
    # Generic job-ad nouns. Capitalised often enough to look technical, but
    # extracting "Engineer" as a requirement produces a meaningless gap.
    "engineer engineers engineering developer developers development "
    "service services solution solutions platform platforms system systems "
    "candidate candidates applicant company client customer stakeholder "
    "responsibilities requirements qualifications skills knowledge ability "
    "years year senior junior lead principal staff manager".split()
)

_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9+#./-]*")
_HAS_INNER_CAPS_OR_DIGIT = re.compile(r"^[A-Za-z][a-z]*[A-Z0-9]")


def _vocabulary(content: ContentService) -> dict[str, str]:
    """Known skills, lower-cased for matching, mapped to their display name."""
    return {
        skill.name.lower(): skill.name
        for group in content.skills.groups
        for skill in group.skills
    }


def extract_requirements(job_description: str, content: ContentService) -> list[Requirement]:
    text = job_description.strip()
    if not text:
        return []

    vocabulary = _vocabulary(content)
    seen: dict[str, Requirement] = {}

    for line in text.splitlines():
        for sentence in re.split(r"(?<=[.!?])\s+", line):
            for position, match in enumerate(_TOKEN.finditer(sentence)):
                token = match.group(0).strip(".,;:")
                if not token:
                    continue
                lowered = token.lower()

                known = lowered in vocabulary
                # Capitalised but not merely sentence-initial, or shaped like a
                # technology name (FastAPI, PostgreSQL, K8s).
                looks_technical = (
                    bool(_HAS_INNER_CAPS_OR_DIGIT.match(token))
                    or (token[0].isupper() and position > 0 and lowered not in _COMMON)
                )

                if not (known or looks_technical):
                    continue

                display = vocabulary.get(lowered, token)
                seen.setdefault(
                    display.lower(),
                    Requirement(text=display, source_line=sentence.strip()),
                )

    return list(seen.values())
