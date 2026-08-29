"""Embedding providers.

Separate from `AIProvider` on purpose: generation and embedding have different
deployment constraints. Gemini embeds over HTTP and deploys anywhere; local
MiniLM needs torch (~1 GB), which busts the Vercel bundle — so it lives in
`requirements-local.txt` and is imported lazily, never at module load.
"""

from __future__ import annotations

import logging
from typing import Protocol

import httpx

from app.config import Settings, get_settings

logger = logging.getLogger(__name__)


class EmbeddingProvider(Protocol):
    """Adding an implementation must never touch a call site."""

    name: str
    dim: int

    def embed(self, texts: list[str]) -> list[list[float]]: ...


class GeminiEmbeddingProvider:
    """Production default: an API call, no ML dependency."""

    def __init__(self, api_key: str, model: str, dim: int) -> None:
        self.name = f"gemini:{model}"
        self.dim = dim
        self._api_key = api_key
        self._model = model

    def embed(self, texts: list[str]) -> list[list[float]]:
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self._model}:batchEmbedContents"
        )
        payload = {
            "requests": [
                {
                    "model": f"models/{self._model}",
                    "content": {"parts": [{"text": text}]},
                    "outputDimensionality": self.dim,
                }
                for text in texts
            ]
        }
        response = httpx.post(
            url, params={"key": self._api_key}, json=payload, timeout=30.0
        )
        response.raise_for_status()
        return [item["values"] for item in response.json()["embeddings"]]


class LocalEmbeddingProvider:
    """Offline development only. Imports sentence-transformers lazily."""

    def __init__(self, model_name: str) -> None:
        from sentence_transformers import SentenceTransformer  # noqa: PLC0415

        self._model = SentenceTransformer(model_name)
        self.name = f"local:{model_name}"
        self.dim = int(self._model.get_sentence_embedding_dimension())

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [vector.tolist() for vector in self._model.encode(texts, normalize_embeddings=True)]


class HashingEmbeddingProvider:
    """Zero-dependency lexical fallback. No key, no network, no model.

    Deliberately not semantic: it matches on shared terms, so it will miss a
    paraphrase a real embedding model would catch. It exists so the assistant
    still *works* with no configuration at all, mirroring the `template`
    generation provider. Prefer gemini or local whenever one is available.
    """

    def __init__(self, dim: int = 512) -> None:
        self.name = "hashing"
        self.dim = dim

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._one(text) for text in texts]

    def _one(self, text: str) -> list[float]:
        import math  # noqa: PLC0415
        import re  # noqa: PLC0415
        import zlib  # noqa: PLC0415

        vector = [0.0] * self.dim
        for token in re.findall(r"[a-z0-9]+", text.lower()):
            # Keep two-letter tokens: "AI" is the most load-bearing term in
            # this corpus and a length-3 floor silently discarded it.
            if len(token) < 2 or token in _STOPWORDS:
                continue
            # crc32, not hash(): Python randomises string hashing per process,
            # which would make a persisted index unreadable by the next run.
            vector[zlib.crc32(token.encode()) % self.dim] += 1.0
        norm = math.sqrt(sum(v * v for v in vector)) or 1.0
        return [v / norm for v in vector]


_STOPWORDS = frozenset(
    "a an the is are was were do does did what which who whom whose when where "
    "why how of in on at to for with and or but from by as it its this that "
    "these those have has had can could will would should".split()
)


def get_embedding_provider(settings: Settings | None = None) -> EmbeddingProvider:
    """Selected by env var, resolved through this factory."""
    settings = settings or get_settings()
    choice = settings.embedding_provider.lower()

    if choice == "local":
        return LocalEmbeddingProvider(settings.embedding_model)

    if choice == "hashing":
        return HashingEmbeddingProvider()

    if not settings.gemini_api_key:
        # Never fail to boot over a missing key: degrade to lexical retrieval,
        # exactly as generation degrades to the template provider.
        logger.warning(
            "EMBEDDING_PROVIDER=gemini but no GEMINI_API_KEY - falling back to "
            "lexical hashing embeddings. Retrieval works but is not semantic."
        )
        return HashingEmbeddingProvider()

    return GeminiEmbeddingProvider(
        settings.gemini_api_key, settings.gemini_embedding_model, settings.gemini_embedding_dim
    )
