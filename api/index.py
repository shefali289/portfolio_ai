"""Vercel Python Function entry point.

Vercel looks for a module under `api/` and serves the ASGI app it exports, so
this file exists only to make `backend/app` importable from the repo root and
hand over the same application `uvicorn app.main:app` serves locally. There is
no second app and no deployment-only code path: a bug here would be a bug
everywhere.

Cold starts rebuild the vector index in memory (~60 chunks). With
`EMBEDDING_PROVIDER=gemini` that costs one embedding call per cold start; with
the `hashing` fallback it is free. Nothing is persisted, so there is no
prebuilt index to ship.
"""

from __future__ import annotations

import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.main import app  # noqa: E402  - path must be set before this import

__all__ = ["app"]
