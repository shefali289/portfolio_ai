"""Shared fixtures.

Tests run against a *fixture* content directory, never the real `content/`.
That is the whole reason `CONTENT_DIR` is a setting rather than a hardcoded
relative path: editing the real portfolio content must never be able to break
a backend test, and a test must be able to construct malformed content on
purpose.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
REAL_CONTENT_DIR = REPO_ROOT / "content"


def _valid_content() -> dict[str, dict]:
    """A minimal but schema-valid set of all five content files."""
    return {
        "profile": {
            "name": "Test Person",
            "title": "Test Engineer",
            "location": "Auckland, New Zealand",
            "summary": "A test summary.",
            "links": {
                "email": "test@example.com",
                "linkedin": "https://linkedin.com/in/test",
                "github": "https://github.com/test",
            },
            "education": [
                {
                    "id": "edu-1",
                    "qualification": "Master of Information Technology",
                    "institution": "Test University",
                    "location": "New Zealand",
                    "start": "2022",
                    "end": "2023",
                    "grade": "GPA 7.25/9",
                }
            ],
            "certifications": [
                {"id": "cert-1", "name": "Test Certification", "issuer": "Test Issuer"}
            ],
            "languages": [{"name": "English", "proficiency": "Full professional proficiency"}],
        },
        "experience": {
            "roles": [
                {
                    "id": "role-1",
                    "title": "Test Engineer",
                    "company": "Test Company",
                    "location": "Auckland, New Zealand",
                    "start": "2025-06",
                    "end": None,
                    "current": True,
                    "highlights": ["Did a testable thing."],
                    "technologies": ["Python"],
                }
            ]
        },
        "skills": {
            "groups": [
                {
                    "id": "group-1",
                    "name": "Test Group",
                    "skills": [
                        {"name": "Python", "evidence": [{"type": "role", "ref": "role-1"}]},
                        {"name": "Unproven", "evidence": [], "todo": "TODO: link evidence"},
                    ],
                }
            ]
        },
        "projects": {
            "projects": [
                {
                    "id": "project-1",
                    "name": "Test Project",
                    "date": "2022-05",
                    "context": "Test context",
                    "description": "A test project.",
                    "technologies": ["Python"],
                    "links": {"demo": None, "repo": "https://github.com/test/project"},
                }
            ]
        },
        "engineering-notes": {
            "achievements": [
                {"id": "ach-1", "name": "Test Achievement", "issuer": "Test Issuer"}
            ],
            "building": [],
            "learning": [],
            "beyond": [],
            "todo": [],
        },
    }


def _write_content(directory: Path, files: dict[str, dict]) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    for stem, payload in files.items():
        (directory / f"{stem}.json").write_text(json.dumps(payload), encoding="utf-8")
    return directory


@pytest.fixture
def content_dir(tmp_path: Path) -> Path:
    """A complete, valid content directory in a temp location."""
    return _write_content(tmp_path / "content", _valid_content())


@pytest.fixture
def make_content_dir(tmp_path: Path):
    """Build a content directory with targeted mutations, for failure cases."""

    def _make(*, drop: str | None = None, malformed: str | None = None,
              invalid: str | None = None) -> Path:
        files = _valid_content()
        if drop:
            files.pop(drop)
        if invalid:
            files[invalid] = {"unexpected": "shape"}
        directory = _write_content(tmp_path / "mutated", files)
        if malformed:
            (directory / f"{malformed}.json").write_text("{ not json", encoding="utf-8")
        return directory

    return _make


@pytest.fixture
def real_content_dir() -> Path:
    """The actual `content/` directory — used only to prove it validates."""
    return REAL_CONTENT_DIR
