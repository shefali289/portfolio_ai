"""The Vercel deployment surface.

Deployment cannot be executed from here, so these tests cover the part that
*is* checkable: the entry point really imports the application, and the config
does not quietly decide something it has no business deciding.

The runtime test exists because a pinned `@vercel/python@4.3.0` shipped a
Python older than 3.11, which cannot import `StrEnum` — the deploy would have
failed at import, and nothing in the suite would have noticed.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[2]
VERCEL_JSON = REPO_ROOT / "vercel.json"
ENTRY = REPO_ROOT / "api" / "index.py"


def _config() -> dict:
    return json.loads(VERCEL_JSON.read_text(encoding="utf-8"))


def _entry_module():
    spec = importlib.util.spec_from_file_location("vercel_entry", ENTRY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- the config ------------------------------------------------------------
def test_vercel_config_parses() -> None:
    assert isinstance(_config(), dict)


def test_no_pinned_python_runtime() -> None:
    """A pinned runtime silently chooses the Python version.

    This codebase needs 3.11+ (`StrEnum`). Rather than pin a version and hope,
    let Vercel resolve its current Python runtime: an unverifiable pin is worse
    than no pin, because it looks deliberate.
    """
    for name, settings in _config().get("functions", {}).items():
        assert "runtime" not in settings, (
            f"{name} pins a runtime. Remove it and let Vercel resolve the "
            f"current Python, or the deploy silently gets an old interpreter."
        )


def test_api_requests_are_routed_to_the_function() -> None:
    rewrites = _config().get("rewrites", [])
    assert any(r["source"].startswith("/api/") for r in rewrites)


def test_install_is_not_stubbed_out() -> None:
    """Overriding installCommand to a no-op can leave the function unbuilt."""
    install = _config().get("installCommand", "")
    assert "echo" not in install.lower()


# --- the entry point -------------------------------------------------------
def test_entry_point_exposes_the_real_application() -> None:
    """One app, not a deployment-only copy: a bug here would be a bug anywhere."""
    module = _entry_module()

    assert module.app.title == "AI-Powered Engineer Portfolio API"


def test_entry_point_serves_the_api() -> None:
    client = TestClient(_entry_module().app)

    assert client.get("/api/health").status_code == 200
    assert client.get("/api/content").status_code == 200
