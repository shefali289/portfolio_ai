# Handoff: Developer -> Review

## Done
All 10 steps. Backend 27/27, frontend 24/24, ruff + eslint + tsc clean. Verified
live: `/api/ai/chat` answers a grounded question with timings and **refuses an
out-of-scope one**; the portfolio shows the resume with no provenance layer.

## You need to know

1. **Four deviations from the plan** — all in `## Decisions Taken`:
   - **`HashingEmbeddingProvider` added** (not planned). Without it the app
     cannot boot with no `GEMINI_API_KEY`, which contradicts the acceptance
     criterion "works with no API key". It is a third implementation behind the
     existing abstraction — no new system, no new dependency — and it degrades
     lexically, mirroring how generation degrades to `template`.
   - **`app/services/ai.py` added.** Routers stay thin (conventions), so the
     retrieve → ground → generate flow belongs in a service, not the router.
   - **Two-letter tokens are kept** in the hashing provider. A `len < 3` floor
     silently dropped "AI" — the most load-bearing term in this corpus — and the
     known-query check returned "Data & Analytics" instead of an AI role.
   - **Article agreement in `chunk.py`** ("an AI Engineer"). Chunk text reaches
     the reader verbatim through the template provider, so it is user-facing.
2. **Source chips are NOT rendered.** The API returns `sources`, but the UI
   shows only the answer — following "no source of evidence" for the app. The
   data stays in the payload because Phase 6's Engineer Mode needs it. Reverse
   in the component alone if you want them.
3. **Refusal happens before generation.** `AiService.answer` checks
   `Retriever.is_grounded` and returns `REFUSAL` without calling any provider.
   Asking a model to police its own scope is a request; a threshold is a
   guarantee.
4. **The index is built in memory at startup** (~19 chunks). `python -m
   app.rag.ingest` persists one for deployment and stamps provider + dimension.

## Files
- `backend/app/rag/{chunk,embeddings,index,retriever,ingest}.py` — new
- `backend/app/ai/{provider,prompts}.py`, `app/services/ai.py` — new
- `backend/app/{config,main}.py`, `app/api/{routes,schemas}.py` — extended
- `frontend/src/components/AskPortfolio.tsx`, `lib/api.ts`, `types/content.ts`
- Part A: `content/skills.json`, `content_models.py`, `content.py`, 5 components

## Look at closely
- **Retrieval quality is only lexical** without a Gemini key. "What did she do
  at Spark?" ranks "Data & Analytics" top, though both Spark roles are in the
  top 4. Real embeddings fix this; the fallback is honest but weak.
- **`GROUNDING_THRESHOLD = 0.25` is tuned against hashing embeddings.** It will
  need re-checking when a semantic provider is configured.
- **`skills.json` lost `evidence` and `todo`** — content deletion, not just a UI
  change. Confirm that is the intent.

## Do NOT re-read
`1-design.md`, `2-plan.md`, `3-test.md`. `index.css` is untouched.

## Open questions
Source chips — see point 2. Currently omitted.

## New learnings
- Degrade every provider, not just the generator: a missing key should cost
  quality, never the ability to boot.
- Uvicorn's reloader watching `.venv` reloads on dependency noise and can miss
  app edits; an orphaned child can hold port 8000 after its parent is killed.
