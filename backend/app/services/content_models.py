"""Pydantic models for `content/*.json` — the portfolio's source of truth.

These are domain models, not HTTP schemas. They describe the shape of the JSON
on disk; `app/api/schemas.py` holds the HTTP-facing shapes. `/api/profile`
returns `Profile` directly, so there is no second copy of this shape to drift.

`extra="forbid"` is deliberate: a typo'd key in a content file should fail
validation loudly at startup rather than being silently dropped and rendering
as an empty section.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ContentModel(BaseModel):
    """Base for every content model: reject unknown keys."""

    model_config = ConfigDict(extra="forbid")


# --------------------------------------------------------------------------
# profile.json
# --------------------------------------------------------------------------
class ProfileLinks(ContentModel):
    email: str
    linkedin: str
    github: str


class Education(ContentModel):
    id: str
    qualification: str
    institution: str
    location: str
    start: str
    end: str
    grade: str


class Certification(ContentModel):
    id: str
    name: str
    issuer: str


class Language(ContentModel):
    name: str
    proficiency: str


class Profile(ContentModel):
    name: str
    title: str
    location: str
    summary: str
    links: ProfileLinks
    education: list[Education]
    certifications: list[Certification]
    languages: list[Language]


# --------------------------------------------------------------------------
# experience.json
# --------------------------------------------------------------------------
class Role(ContentModel):
    id: str
    title: str
    company: str
    location: str
    start: str
    end: str | None = None
    current: bool = False
    highlights: list[str]
    technologies: list[str] = Field(default_factory=list)
    link: str | None = None


class Experience(ContentModel):
    roles: list[Role]


# --------------------------------------------------------------------------
# skills.json
# --------------------------------------------------------------------------
class SkillEvidence(ContentModel):
    """Where a skill was used. `type` names which content file `ref` points into."""

    type: str
    ref: str


class Skill(ContentModel):
    name: str
    evidence: list[SkillEvidence] = Field(default_factory=list)
    todo: str | None = None


class SkillGroup(ContentModel):
    id: str
    name: str
    skills: list[Skill]


class Skills(ContentModel):
    note: str | None = Field(default=None, alias="_note")
    groups: list[SkillGroup]


# --------------------------------------------------------------------------
# projects.json
# --------------------------------------------------------------------------
class ProjectLinks(ContentModel):
    demo: str | None = None
    repo: str | None = None


class Project(ContentModel):
    id: str
    name: str
    date: str
    context: str
    description: str
    technologies: list[str]
    links: ProjectLinks
    todo: str | None = None


class Projects(ContentModel):
    projects: list[Project]


# --------------------------------------------------------------------------
# engineering-notes.json
# --------------------------------------------------------------------------
class Achievement(ContentModel):
    id: str
    name: str
    issuer: str


class EngineeringNotes(ContentModel):
    note: str | None = Field(default=None, alias="_note")
    achievements: list[Achievement]
    building: list[str] = Field(default_factory=list)
    learning: list[str] = Field(default_factory=list)
    beyond: list[str] = Field(default_factory=list)
    todo: list[str] = Field(default_factory=list)
