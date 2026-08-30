# Handoff: Developer -> Review

## Done
All 8 steps. Backend 42/42, frontend 30/30, ruff + eslint + tsc clean. Verified
live against the real resume: FastAPI and PostgreSQL attributed to the Spark
role; **Kubernetes and Terraform reported as gaps**, which is correct — neither
appears anywhere in the portfolio.

## You need to know

1. **Two real defects were found by running it, not by the tests.** Both are
   fixed and now have regression tests:
   - **False gap.** "FastAPI" was reported as a gap although a role lists it —
     a one-token query against a long chunk scores low on lexical cosine. A
     false gap *understates* real experience, and is invisible unless you know
     the resume. Fix: `_exact_hits` in `portfolio.py` — a term named verbatim
     is evidence, scored 1.0, merged ahead of vector hits.
   - **Junk requirement.** "Engineer" was extracted from "AI Engineer" and
     reported as a gap. Fix: generic job-ad nouns added to `_COMMON`.
2. **The verdict is never asked of a model.** `assess_evidence` computes it from
   retrieval scores against `GROUNDING_THRESHOLD`, with `STRONG_MATCH = 0.45`
   separating match from partial. A gap carries no evidence at all.
3. **One search path.** `JobMatchService` is constructed with `ai.retriever` —
   the same instance Ask My Portfolio uses. `AiService` gained a `retriever`
   property purely to make that sharing explicit.
4. **Steps are returned, not streamed.** `run_chain` times each agent and
   returns `steps[]`; the UI renders them after the fact. No new transport.
5. **`ChainError` aborts the run.** Any raising agent yields an error, never a
   partial report.

## Files
- `backend/app/agents/{base,requirement,portfolio,evidence,response,chain}.py` — new
- `backend/app/services/job_match.py` — new; `services/ai.py` gained `retriever`
- `backend/app/api/{routes,schemas}.py`, `app/main.py` — endpoint + app state
- `backend/app/rag/retriever.py` — exposes `chunks` for exact-term lookup
- `frontend/src/components/JobMatch{,.test}.tsx`, `lib/api.ts`,
  `types/content.ts`, `App.tsx`

## Look at closely
- **`_exact_hits` scans every chunk per requirement** — O(chunks x requirements).
  Fine at ~19 chunks; would need an index if the corpus grew a lot.
- **Extraction is heuristic.** Capitalisation plus a stopword list will both
  over- and under-fire on unusual JDs; the `_COMMON` list is empirical, not
  principled.
- **`STRONG_MATCH = 0.45` is tuned against lexical vectors**, same caveat as
  `GROUNDING_THRESHOLD` — unvalidated against Gemini embeddings.

## Do NOT re-read
`1-design.md`, `2-plan.md`, `3-test.md`. `index.css` is untouched — the UI reuses
existing classes.

## Open questions
None.

## New learnings
- **Run the feature against real data before trusting the suite.** Both defects
  passed every test written from the plan; only the live run against the actual
  resume exposed them.
- Vector search alone under-serves single-token queries. Pair it with an exact
  term check when the query is a name rather than a sentence.
