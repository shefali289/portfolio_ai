"""Generation providers.

Selected by env var and resolved through `resolve_provider`, so adding one never
touches a call site. Every provider falls back to `TemplateProvider` when
unreachable — a live demo must never show a broken AI feature.
"""

from __future__ import annotations

import logging
from typing import Protocol

import httpx

from app.ai.prompts import build_prompt
from app.config import Settings, get_settings

logger = logging.getLogger(__name__)


class AIProvider(Protocol):
    name: str

    def generate(self, question: str, context: list[str]) -> str: ...


class TemplateProvider:
    """No LLM at all. Retrieval still ran, so the answer is real content.

    This is the always-works fallback: it needs no key, no network and no model,
    which is what lets the feature be demonstrated anywhere.
    """

    name = "template"

    def generate(self, question: str, context: list[str]) -> str:
        if not context:
            from app.ai.prompts import REFUSAL  # noqa: PLC0415

            return REFUSAL
        lead = "Here is what the portfolio says:"
        body = "\n\n".join(f"• {c}" for c in context)
        return f"{lead}\n\n{body}"


class GeminiProvider:
    name = "gemini"

    def __init__(self, api_key: str, model: str) -> None:
        self._api_key = api_key
        self._model = model

    def generate(self, question: str, context: list[str]) -> str:
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self._model}:generateContent"
        )
        payload = {"contents": [{"parts": [{"text": build_prompt(question, context)}]}]}
        response = httpx.post(url, params={"key": self._api_key}, json=payload, timeout=30.0)
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()


class OllamaProvider:
    """Local and offline. Cannot be deployed — development only."""

    name = "ollama"

    def __init__(self, base_url: str, model: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model

    def generate(self, question: str, context: list[str]) -> str:
        response = httpx.post(
            f"{self._base_url}/api/generate",
            json={"model": self._model, "prompt": build_prompt(question, context),
                  "stream": False},
            timeout=60.0,
        )
        response.raise_for_status()
        return response.json()["response"].strip()


def resolve_provider(choice: str | None = None, settings: Settings | None = None) -> AIProvider:
    """Never raises: an unknown or unconfigured provider degrades to template."""
    settings = settings or get_settings()
    choice = (choice or settings.ai_provider).lower()

    if choice == "gemini" and settings.gemini_api_key:
        return GeminiProvider(settings.gemini_api_key, settings.gemini_model)
    if choice == "ollama":
        return OllamaProvider(settings.ollama_base_url, settings.ollama_model)
    if choice not in {"template", "gemini", "ollama"}:
        logger.warning("Unknown AI_PROVIDER %r - falling back to template", choice)
    elif choice == "gemini":
        logger.warning("AI_PROVIDER=gemini but no GEMINI_API_KEY - falling back to template")
    return TemplateProvider()


def generate_with_fallback(
    provider: AIProvider, question: str, context: list[str]
) -> tuple[str, str]:
    """Returns (answer, provider_name_actually_used)."""
    try:
        return provider.generate(question, context), provider.name
    except Exception as exc:  # noqa: BLE001 - any provider failure must degrade, not 500
        logger.warning("Provider %s failed (%s) - falling back to template", provider.name, exc)
        fallback = TemplateProvider()
        return fallback.generate(question, context), fallback.name
