# Handoff: Planning -> Test

## Done
Ten steps. Part A (resume-as-is) runs first and standalone — after step 3 the app
is shippable with no AI at all. Part B then builds RAG on the simplified content.
Steps 4 and 8 are RED gates.

## You need to know

1. **Do Part A first and do not mix it into the RAG commits.** It is a removal;
   keeping it separate means it can ship or be reverted on its own.
2. **Deleting a feature deletes its tests.** The evidence-explorer and
   `_validate_evidence_refs` tests go with the code they cover — that is correct,
   not a weakened suite. Say so in the handoff so it is not read as a regression.
3. **Re-ingest after content changes.** Removing `evidence` from `skills.json`
   changes the chunk text, so ingestion must run after step 2, not before.
4. **Stamp provider + dim in the index and refuse a mismatch** — Gemini and
   MiniLM dimensions differ and a silent mismatch returns plausible nonsense.
5. **`template` must work with no API key.** Every step below has to pass with
   `AI_PROVIDER=template`; a missing key is never a failing test.
6. **The grounding test is the one that matters** — an out-of-scope question is
   refused. Write it in step 8 and never relax it to make a provider pass.

## Steps
1. Strip the provenance layer from the 5 components + `App.tsx` (`react-component`)
2. Remove `evidence`/`todo` from `skills.json`, its models and
   `_validate_evidence_refs`; delete the tests that covered them
3. Validate Part A: `npm test`, `pytest`, lint, `tsc`, and view the app
4. **RED** — chunking, index mismatch, retrieval, and the grounding test (`tdd-cycle`)
5. `app/rag/chunk.py` — `{text, source, type}` records via `ContentService` (`rag-ingestion`)
6. `app/rag/embeddings.py` — `EmbeddingProvider`: Gemini + local, factory (`ai-provider`)
7. `app/rag/index.py` + `ingest.py` — FAISS, persist to `backend/.index/`, stamp + refuse mismatch (`rag-ingestion`)
8. `app/ai/provider.py` + `prompts.py` — `AIProvider`: Gemini, Ollama, template fallback (`ai-provider`)
9. `POST /api/ai/chat` in `routes.py`/`schemas.py` — retrieve, ground, generate, return timings (`api-endpoint`)
10. `AskPortfolio.tsx` + `lib/api.ts`; full validation incl. 375px (`react-component`, `a11y-responsive`)

## Files
See `## Files Likely To Change` in `task.md`. Nothing under `frontend/src/index.css`
changes — the token system stays exactly as it is.

## Do NOT re-read
`1-design.md`; `docs/plan.md`; the RAG skills. Do not re-inspect `index.css` or
the components' styling — Part A removes elements, it does not restyle.

## Open questions
Only the source-chip question from `1-design.md`. It affects **step 10 only**;
steps 1-9 are unaffected either way, so it does not block starting.

## New learnings
Pending.
