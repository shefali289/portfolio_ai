"""Build and persist the vector index.

    python -m app.rag.ingest

Re-run whenever `content/*.json` changes, chunking changes, or
`EMBEDDING_PROVIDER` changes — the index records which provider produced it and
refuses to load against a different one.

The API builds its index in memory at startup, so this script is for the
deployment path: a prebuilt index committed for serverless, where boot time and
outbound API calls both matter.
"""

from __future__ import annotations

import sys

from app.config import get_settings
from app.rag.chunk import build_chunks
from app.rag.embeddings import get_embedding_provider
from app.rag.index import VectorIndex
from app.services.content import ContentService


def main() -> int:
    settings = get_settings()
    content = ContentService(settings.content_dir)
    provider = get_embedding_provider(settings)

    chunks = build_chunks(content)
    if not chunks:
        print("No content to index.", file=sys.stderr)
        return 1

    index = VectorIndex.build(
        texts=[c.text for c in chunks],
        metadata=[{"source": c.source, "type": c.type} for c in chunks],
        provider=provider,
    )
    index.save(settings.index_dir)

    print(f"Indexed {len(chunks)} chunks with '{provider.name}' (dim {provider.dim})")
    print(f"  -> {settings.index_dir}")

    # Verify with a known query, per the rag-ingestion skill.
    from app.rag.retriever import Retriever  # noqa: PLC0415

    hits = Retriever(index, chunks, provider).retrieve("What AI experience does she have?", k=3)
    if hits:
        print(f"  check: top match is {hits[0].chunk.source!r} ({hits[0].score:.2f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
