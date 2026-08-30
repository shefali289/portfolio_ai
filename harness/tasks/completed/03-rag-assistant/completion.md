# Feature Completion

## Feature

RAG Assistant — Ask My Portfolio — `03-rag-assistant`

## What Was Added

**Part A — the resume as it is.** The provenance layer added by `visual-design`
is gone: derived counts, the skills coverage ratio, per-skill evidence expansion
and the `content/*.json` source footers. Skills render as plain grouped lists,
exactly as the resume categorises them. The inferred `evidence` links were
**deleted from `skills.json`**, not merely hidden — they were the agent's
inference, and "assume nothing" means the assumption leaves the content.

**Part B — a grounded assistant.** Chunking through `ContentService`, an
`EmbeddingProvider` abstraction (Gemini, local MiniLM, and a zero-dependency
lexical fallback), a FAISS index stamped with provider and dimension that
refuses to load against a mismatch, an `AIProvider` abstraction (Gemini, Ollama,
template) and `POST /api/ai/chat` returning answer, sources and timings.

## Main Files Changed

- `content/skills.json` + `content_models.py`, `content.py` — evidence removed
- 5 frontend components + `App.tsx` — provenance layer removed
- `backend/app/rag/{chunk,embeddings,index,retriever,ingest}.py` — new
- `backend/app/ai/{provider,prompts}.py`, `app/services/ai.py` — new
- `backend/app/api/{routes,schemas}.py`, `app/config.py`, `app/main.py`
- `frontend/src/components/AskPortfolio.tsx`, `lib/api.ts`, `types/content.ts`
- `.env.example`, `docs/setup.md` — the `hashing` provider documented

## Tests

- backend 27 (13 new: chunking, index round-trip, provider and dimension
  mismatch, retrieval, grounding, endpoint, refusal, timings, validation,
  fallback); frontend 24 (5 new for `AskPortfolio`)
- **The grounding test is the one that matters**: an out-of-scope question is
  refused, verified live as well as in the suite
- Tests removed with the feature they covered: evidence explorer,
  `_validate_evidence_refs`

## Validation

| Check | Result |
|---|---|
| backend tests | PASS — `27 passed` |
| frontend tests | PASS — `Test Files 8 passed (8)`, `Tests 24 passed (24)` |
| lint | PASS — ruff and eslint clean |
| typecheck | PASS — `tsc --noEmit` clean |
| manual check | PASS — grounded question answers with timings; "What is the capital of France?" returns `grounded=false` and the refusal; blank question 422. **375px measured in-browser**: `scrollWidth=375`, 0 overflowing elements |

## Gates

| Gate | Result | Note |
|---|---|---|
| G0 branch | PASS | stacked on the unmerged `improvement/visual-design` |
| G1 design | PASS | 7 questions, no new dependency, one open question recorded |
| G2 test | PASS | 13 tests RED for the right reason before implementation |
| G3 build | PASS | 4 deviations recorded |
| G4 review | PASS | all checks; 1 MEDIUM finding fixed in cycle, 2 LOW recorded |
| G5 completion | PASS | `final_checklist.py --slug 03-rag-assistant` exits 0 |

## Design Decisions

- **Refusal is decided by retrieval, before any model runs.** Asking an LLM to
  police its own scope is a request; a similarity threshold is a guarantee.
- **A lexical embedding fallback was added** (not in the plan). Without it the
  app cannot boot with no `GEMINI_API_KEY`, contradicting an acceptance
  criterion. It is a third implementation behind the existing abstraction — no
  new system, no new dependency — and it costs quality, never availability.
- **Inferred data deleted, not hidden.** Removing `evidence` from the content
  removed the assumption; the schema, service and tests all got simpler.
- **Two-letter tokens kept when embedding** — a `len < 3` floor silently dropped
  "AI", the most load-bearing term in this corpus.

## Lessons Learned

- **Worked:** deleting inferred data rather than hiding it — everything
  downstream simplified with it.
- **Cost time:** orphaned dev servers. A uvicorn child outlived its killed
  parent and held port 8000, serving code without the new route.
- **Do differently:** verify the tool before believing its output. A "375px
  overflow" that stood for three tasks was Chrome headless clamping to a 500px
  minimum window and cropping the screenshot.

## Known Limitations

- Retrieval is lexical without a `GEMINI_API_KEY`; it misses paraphrases.
- `GROUNDING_THRESHOLD = 0.25` is unvalidated against semantic embeddings.
- Answers do not display sources — deferred to Phase 6.
- No prebuilt index is committed; deployment will need one.
