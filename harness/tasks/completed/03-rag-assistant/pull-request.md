## feat: resume-as-is portfolio with a grounded assistant

Closes: harness task `03-rag-assistant` (Phase 3)

### What this adds

The portfolio now shows the resume as it is — the provenance layer is gone and
the inferred skill-evidence links are deleted from the content, not merely
hidden. On top of that, a grounded assistant: chunking through `ContentService`,
embedding and generation provider abstractions, a FAISS index that refuses a
provider mismatch, and `POST /api/ai/chat` returning answer, sources and timings.

### Why

The previous design presented information *about* the content beside the content
— derived counts, a skills coverage ratio, source-file labels — which described
the tool to the reader instead of showing them the resume. Several of its
evidence links were inference rather than resume fact. The assistant then
answers questions from that content, and refuses anything it cannot support.

### How

- **Refusal is decided by retrieval, before any model is called.** If nothing
  clears the similarity threshold the question is out of scope. Asking a model
  to police its own scope is a request; a threshold is a guarantee.
- **Inferred data deleted, not hidden.** The resume lists Python and separately
  mentions Python in a Spark bullet; it never says Python was used at Spark.
  Removing `evidence` from `skills.json` also removed
  `ContentService._validate_evidence_refs`.
- **A lexical embedding fallback was added, beyond the plan.** Without it the
  app cannot boot with no `GEMINI_API_KEY`, contradicting the "works with no API
  key" criterion. It is a third implementation behind the existing abstraction —
  no new system, no new dependency — costing quality, never availability.
- **Two-letter tokens are kept when embedding.** A `len < 3` floor silently
  dropped "AI", the most load-bearing term in this corpus.
- Kept simple: no new dependency, and the index builds in memory at startup
  (~19 chunks) with `python -m app.rag.ingest` for the deployment path.

### Changed

| Area | Files |
|---|---|
| Backend | `app/rag/*` and `app/ai/*` (new), `services/ai.py` (new), `api/{routes,schemas}.py`, `config.py`, `main.py`, `services/content{,_models}.py` |
| Frontend | `AskPortfolio.tsx` (new), `App.tsx`, `Profile`, `SkillsExplorer`, `ProjectGallery`, `Contact`, `lib/api.ts`, `types/content.ts` |
| Content | `content/skills.json` — `evidence` and `todo` removed |
| Harness | `tasks/active/03-rag-assistant/*`, `.env.example`, `docs/setup.md` |

### Tests

| Suite | Result |
|---|---|
| `pytest` | 27 passed |
| `npm test` | 24 passed (8 files) |
| `ruff` / `lint` / `tsc` | clean |

New tests lock in: chunking, index round-trip, provider **and** dimension
mismatch refusal, retrieval, the grounding threshold, the endpoint contract,
refusal, timings, blank-question validation, template fallback, and the
`AskPortfolio` states. RED evidence in `handoffs/3-test.md`.

Tests for the removed evidence explorer and `_validate_evidence_refs` were
deleted with the code they covered — not a weakened suite.

### Quality gates

| Gate | Result |
|---|---|
| G0 branch | PASS |
| G1 design | PASS |
| G2 test (RED) | PASS |
| G3 build (GREEN) | PASS |
| G4 review | PASS — 1 MEDIUM finding (undocumented provider) fixed in cycle |
| G5 completion | PASS |

### Lessons learned

- Deleting inferred data beats hiding it — schema, service and tests all
  simplified with it.
- Verify the tool before believing its output: a "375px overflow" that stood for
  three tasks was Chrome headless clamping to a 500px minimum window.
- Adding a provider is not done until `.env.example` describes it.

### User overrides

- **Show the resume, assume nothing.** The evidence/provenance layer was removed
  and inferred links deleted. Promoted rule: the UI renders resume content only;
  inferred data is deleted, not hidden.
- **Source chips deferred to Phase 6** rather than decided here.

### Known limitations

Retrieval is lexical without a `GEMINI_API_KEY` and misses paraphrases.
`GROUNDING_THRESHOLD = 0.25` is unvalidated against semantic embeddings. Answers
do not display sources. No prebuilt index is committed.

### Harness

Task, handoffs 1–5 and completion report: `harness/tasks/completed/03-rag-assistant/`
