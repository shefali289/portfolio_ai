"""ContentService — the only reader of `content/`.

RAG ingestion, API routes and (from Phase 5) MCP tools all go through this
service rather than opening the JSON themselves. One reader means one place
where the content contract is enforced.

Loading is **eager**: every file is read and validated when the service is
constructed, so a malformed content file fails at startup rather than midway
through serving a request.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypeVar

from pydantic import ValidationError

from app.services.content_models import (
    ContentModel,
    EngineeringNotes,
    Experience,
    Profile,
    Projects,
    Skills,
)

ModelT = TypeVar("ModelT", bound=ContentModel)


class ContentError(RuntimeError):
    """Content is missing, unreadable, or does not match its model.

    Always names the offending file, because "validation error" without a
    filename is useless when five files are loaded at once.
    """


class ContentService:
    """Loads, validates and caches the five portfolio content files."""

    def __init__(self, content_dir: Path) -> None:
        self._content_dir = Path(content_dir)
        if not self._content_dir.is_dir():
            raise ContentError(f"Content directory not found: {self._content_dir}")

        self.profile: Profile = self._load("profile.json", Profile)
        self.experience: Experience = self._load("experience.json", Experience)
        self.skills: Skills = self._load("skills.json", Skills)
        self.projects: Projects = self._load("projects.json", Projects)
        self.engineering_notes: EngineeringNotes = self._load(
            "engineering-notes.json", EngineeringNotes
        )

    @property
    def content_dir(self) -> Path:
        return self._content_dir

    def _load(self, filename: str, model: type[ModelT]) -> ModelT:
        path = self._content_dir / filename
        try:
            raw = path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise ContentError(f"{filename}: not found in {self._content_dir}") from exc
        except OSError as exc:
            raise ContentError(f"{filename}: could not be read ({exc})") from exc

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ContentError(f"{filename}: is not valid JSON ({exc})") from exc

        try:
            return model.model_validate(payload)
        except ValidationError as exc:
            raise ContentError(f"{filename}: does not match its schema ({exc})") from exc
