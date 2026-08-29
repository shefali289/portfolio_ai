"""HTTP-facing shapes only.

Domain content models live in `app/services/content_models.py`. Endpoints that
return portfolio content return those models directly, so there is no second
copy of `Profile` here to drift out of step with the content files.
"""

from __future__ import annotations

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class ErrorResponse(BaseModel):
    """Errors return a typed shape, never a bare 500 with a stack trace."""

    detail: str
