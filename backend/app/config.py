"""Application settings.

Every setting is read here and nowhere else — modules take what they need from
`get_settings()` rather than reaching into `os.environ` (conventions.md).

`CONTENT_DIR` is a setting rather than a relative path on purpose: resolving
`../content` from module code depends on the directory uvicorn happened to be
started from, and tests need to point the app at a fixture directory.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=REPO_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    content_dir: Path = Field(default=REPO_ROOT / "content")
    cors_origins: list[str] = Field(default=["http://localhost:5173"])

    # --- AI / RAG (Phase 3) ------------------------------------------------
    # Generation and embedding are selected separately: they have different
    # deployment constraints. See docs/setup.md.
    ai_provider: str = Field(default="template")
    embedding_provider: str = Field(default="gemini")
    index_dir: Path = Field(default=REPO_ROOT / "backend" / ".index")

    gemini_api_key: str = Field(default="")
    gemini_model: str = Field(default="gemini-2.0-flash")
    gemini_embedding_model: str = Field(default="gemini-embedding-001")
    gemini_embedding_dim: int = Field(default=768)

    ollama_base_url: str = Field(default="http://localhost:11434")
    ollama_model: str = Field(default="llama3.2")

    embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_origins(cls, value: object) -> object:
        """`CORS_ORIGINS` is a comma-separated string in .env, a list in code."""
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
