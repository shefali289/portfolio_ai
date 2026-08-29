"""Turn portfolio content into retrievable chunks.

One coherent idea per chunk: a role or a project stays whole rather than being
split mid-thought, so a retrieved chunk is enough to answer from on its own.

Content is read through `ContentService` — never by opening the JSON directly.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.services.content import ContentService


@dataclass(frozen=True)
class Chunk:
    """`text` is what gets embedded; `source` is a human label; `type` groups it."""

    text: str
    source: str
    type: str


def build_chunks(content: ContentService) -> list[Chunk]:
    chunks: list[Chunk] = []
    profile = content.profile

    if profile.summary:
        # "an AI Engineer", not "a AI Engineer" - this text reaches the reader
        # verbatim through the template provider.
        article = "an" if profile.title[:1].upper() in "AEIOU" else "a"
        chunks.append(
            Chunk(
                text=f"{profile.name} is {article} {profile.title} based in "
                f"{profile.location}. {profile.summary}",
                source=f"{profile.name} — profile",
                type="profile",
            )
        )

    for role in content.experience.roles:
        period = f"{role.start} to {'present' if role.current else (role.end or 'unknown')}"
        body = " ".join(role.highlights)
        tech = f" Technologies: {', '.join(role.technologies)}." if role.technologies else ""
        chunks.append(
            Chunk(
                text=f"{role.title} at {role.company}, {role.location} ({period}). {body}{tech}",
                source=f"{role.title} · {role.company}",
                type="role",
            )
        )

    for project in content.projects.projects:
        tech = f" Technologies: {', '.join(project.technologies)}." if project.technologies else ""
        chunks.append(
            Chunk(
                text=f"Project: {project.name} ({project.date}, {project.context}). "
                f"{project.description}{tech}",
                source=f"Project · {project.name}",
                type="project",
            )
        )

    for group in content.skills.groups:
        names = ", ".join(skill.name for skill in group.skills)
        if names:
            chunks.append(
                Chunk(text=f"{group.name} skills: {names}.", source=group.name, type="skills")
            )

    for item in profile.education:
        chunks.append(
            Chunk(
                text=f"{item.qualification} at {item.institution}, {item.location} "
                f"({item.start}-{item.end}). {item.grade}.",
                source=item.institution,
                type="education",
            )
        )

    if profile.certifications:
        names = ", ".join(f"{c.name} ({c.issuer})" for c in profile.certifications)
        chunks.append(Chunk(text=f"Certifications: {names}.", source="Certifications",
                            type="certification"))

    if content.engineering_notes.achievements:
        names = ", ".join(
            f"{a.name} ({a.issuer})" for a in content.engineering_notes.achievements
        )
        chunks.append(Chunk(text=f"Achievements: {names}.", source="Achievements",
                            type="achievement"))

    return chunks
