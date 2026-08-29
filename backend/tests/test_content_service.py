"""ContentService — loads, validates and caches `content/*.json`."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.services.content import ContentError, ContentService


def test_loads_all_five_content_files(content_dir: Path) -> None:
    service = ContentService(content_dir)

    assert service.profile.name == "Test Person"
    assert len(service.experience.roles) == 1
    assert len(service.skills.groups) == 1
    assert len(service.projects.projects) == 1
    assert len(service.engineering_notes.achievements) == 1


def test_missing_file_raises_a_clear_error(make_content_dir) -> None:
    directory = make_content_dir(drop="profile")

    with pytest.raises(ContentError) as excinfo:
        ContentService(directory)

    message = str(excinfo.value)
    assert "profile.json" in message
    assert "not found" in message.lower()


def test_malformed_json_raises_a_clear_error(make_content_dir) -> None:
    directory = make_content_dir(malformed="projects")

    with pytest.raises(ContentError) as excinfo:
        ContentService(directory)

    assert "projects.json" in str(excinfo.value)


def test_schema_violation_raises_a_clear_error(make_content_dir) -> None:
    """A file that is valid JSON but the wrong shape must fail loudly."""
    directory = make_content_dir(invalid="skills")

    with pytest.raises(ContentError) as excinfo:
        ContentService(directory)

    assert "skills.json" in str(excinfo.value)


def test_missing_directory_raises_a_clear_error(tmp_path: Path) -> None:
    with pytest.raises(ContentError):
        ContentService(tmp_path / "does-not-exist")


def test_content_is_loaded_once_and_cached(content_dir: Path) -> None:
    """Eager load at construction: deleting the files afterwards changes nothing."""
    service = ContentService(content_dir)
    for json_file in content_dir.glob("*.json"):
        json_file.unlink()

    assert service.profile.name == "Test Person"


def test_skills_carry_evidence_or_an_explicit_todo(content_dir: Path) -> None:
    """The grounding rule: an unproven skill must say so, not claim experience."""
    service = ContentService(content_dir)

    for group in service.skills.groups:
        for skill in group.skills:
            assert skill.evidence or skill.todo, f"{skill.name} has neither evidence nor a TODO"


def test_invalid_skill_evidence_reference_raises_a_clear_error(make_content_dir) -> None:
    directory = make_content_dir()
    skills_path = directory / "skills.json"
    skills = json.loads(skills_path.read_text(encoding="utf-8"))
    skills["groups"][0]["skills"][0]["evidence"] = [
        {"type": "role", "ref": "missing-role"}
    ]
    skills_path.write_text(json.dumps(skills), encoding="utf-8")

    with pytest.raises(ContentError) as excinfo:
        ContentService(directory)

    message = str(excinfo.value)
    assert "missing-role" in message
    assert "skills.json" in message


def test_the_real_content_directory_validates(real_content_dir: Path) -> None:
    """The actual portfolio content must parse — this is what ships."""
    service = ContentService(real_content_dir)

    assert service.profile.name
    assert service.experience.roles
    assert service.skills.groups
