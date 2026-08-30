"""FAISS vector index with provider metadata.

The index records which provider and dimension produced its vectors, and
**refuses to load against a different one**. Gemini and MiniLM vectors are not
interchangeable: loading one against the other returns confident nonsense, which
is far worse than an error.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import faiss
import numpy as np


class IndexMismatchError(RuntimeError):
    """The stored vectors were not produced by the provider now in use."""


class VectorIndex:
    def __init__(self, index: faiss.Index, metadata: list[dict[str, Any]],
                 provider_name: str, dim: int) -> None:
        self._index = index
        self.metadata = metadata
        self.provider_name = provider_name
        self.dim = dim

    @property
    def size(self) -> int:
        return int(self._index.ntotal)

    # -- build / persist ---------------------------------------------------
    @classmethod
    def build(cls, texts: list[str], metadata: list[dict[str, Any]],
              provider: Any) -> VectorIndex:
        vectors = np.asarray(provider.embed(texts), dtype="float32")
        faiss.normalize_L2(vectors)
        # Inner product on normalised vectors == cosine similarity.
        index = faiss.IndexFlatIP(vectors.shape[1])
        index.add(vectors)
        return cls(index, metadata, provider.name, int(vectors.shape[1]))

    def save(self, directory: Path) -> None:
        directory.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self._index, str(directory / "vectors.faiss"))
        (directory / "meta.json").write_text(
            json.dumps(
                {"provider": self.provider_name, "dim": self.dim, "metadata": self.metadata},
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, directory: Path, provider: Any) -> VectorIndex:
        meta_path = directory / "meta.json"
        if not meta_path.exists():
            raise IndexMismatchError(
                f"No index at {directory}. Build it with `python -m app.rag.ingest`."
            )

        meta = json.loads(meta_path.read_text(encoding="utf-8"))

        if meta["provider"] != provider.name:
            raise IndexMismatchError(
                f"Index was built with '{meta['provider']}' but the current provider is "
                f"'{provider.name}'. Re-run `python -m app.rag.ingest`."
            )
        if meta["dim"] != provider.dim:
            raise IndexMismatchError(
                f"Index dimension {meta['dim']} != provider dimension {provider.dim}. "
                "Re-run `python -m app.rag.ingest`."
            )

        index = faiss.read_index(str(directory / "vectors.faiss"))
        return cls(index, meta["metadata"], meta["provider"], meta["dim"])

    # -- query -------------------------------------------------------------
    def search(self, vector: list[float], k: int) -> list[tuple[int, float]]:
        query = np.asarray([vector], dtype="float32")
        faiss.normalize_L2(query)
        scores, ids = self._index.search(query, min(k, max(self.size, 1)))
        return [(int(i), float(s)) for i, s in zip(ids[0], scores[0], strict=True) if i != -1]
