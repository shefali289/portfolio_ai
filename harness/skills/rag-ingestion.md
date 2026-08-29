# Skill: RAG Ingestion

**Used by:** Developer Agent
**When:** content changes, or the embedding provider changes

## Steps

1. **Load** content through `ContentService` - never open the JSON directly.
2. **Chunk** into `{text, source, type}` records. One coherent idea per chunk;
   keep a project or role together rather than splitting mid-thought.
3. **Embed** through `EmbeddingProvider` - never call a model directly, so the
   provider stays swappable.
4. **Index** with FAISS. Persist to `backend/.index/` (gitignored locally,
   prebuilt and committed for deployment).
5. **Stamp metadata** - provider name and vector dimension. Loading must
   **refuse a mismatch** rather than return silent nonsense: Gemini and MiniLM
   vectors are not interchangeable.
6. **Verify** with a known query - "What AI experience does she have?" must
   retrieve the AI Engineer role.

## Re-ingest whenever

`content/*.json` changes, chunking changes, or `EMBEDDING_PROVIDER` changes.

```bash
python -m app.rag.ingest
```

## Done when

Index builds, a known query retrieves the expected source, and a provider
mismatch is refused loudly.
