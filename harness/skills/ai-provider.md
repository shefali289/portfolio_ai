# Skill: Add a Provider Implementation

**Used by:** Developer Agent
**When:** adding a generation or embedding backend

## Steps

1. **Pick the interface** - `AIProvider` (generation, in `app/ai/`) or
   `EmbeddingProvider` (vectors, in `app/rag/`). They are separate on purpose:
   different deployment constraints. Do not merge them.
2. **Implement it.** Nothing else changes - no call site is touched.
3. **Register** in the factory, keyed by its env-var value.
4. **Document** the env vars in `.env.example`.
5. **Fail soft** - on unavailability, fall back to `TemplateProvider` rather than
   erroring. A live demo must never show a broken AI feature.
6. **Test** with a stub: the interface contract, and the fallback path.
7. **Check deployability** - anything pulling torch is local-only and must stay
   out of `requirements.txt`. See `learning/gotchas.md`.

## Done when

Provider swaps by env var alone, fallback works, and `requirements.txt` is
still free of ML dependencies.
