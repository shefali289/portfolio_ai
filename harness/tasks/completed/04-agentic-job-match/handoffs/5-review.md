# Handoff: Review -> Completion

## Check results
| Check | Result |
|---|---|
| `pytest` | **PASS** — 42 passed |
| `ruff check .` | **PASS** — All checks passed |
| `npm test` | **PASS** — 9 files, 30 tests |
| `npm run lint` · `tsc --noEmit` | **PASS** — clean |
| gaps reported honestly | **PASS** — live: Kubernetes and Terraform are gaps; FastAPI and PostgreSQL correctly attributed to the Spark role |
| chain order + failure | **PASS** — four steps in order; a raising agent yields `ChainError`, no partial report |
| one search path | **PASS** — `JobMatchService` receives `ai.retriever`; no second retriever exists |
| works with no API key | **PASS** — extraction and verdicts are lexical; no key needed |
| 375px | **PASS** — measured in-browser with the new sections: `scrollWidth=375`, **0 overflowing elements** |
| keyboard / labels | **PASS** — textarea has a label, native controls, headings nested correctly |
| content unchanged | **PASS** — no `content/` file touched this phase |

## Findings

**1 · LOW — a bare skills-list mention is presented as a *strong* match.**
`EXACT_TERM_SCORE = 1.0` puts any verbatim term above `STRONG_MATCH`, so a
requirement satisfied only by an entry in `content/skills.json` reads the same as
one demonstrated in a role. The evidence text is shown, so the reader can see
which it is — but "strong" arguably overstates a bare listing. Given this
portfolio's "assume nothing" stance it is worth deciding deliberately.
*Fix:* score skills-group chunks below role/project chunks, so a listing lands
as `partial`.

**2 · LOW — `app/rag/retriever.py` was modified, which the plan excluded.**
`2-plan.md` said `app/rag/*` was not to be touched; a `chunks` property was added
so `_exact_hits` could scan the corpus. Small and additive, but a real scope
deviation the plan did not anticipate — recorded rather than glossed.

**3 · LOW — requirement extraction is heuristic.**
Capitalisation plus an empirical stopword list will over- and under-fire on
unusual job ads. Acceptable for a portfolio feature, and an LLM path can layer
on top when a key exists, but it is not principled.

Nothing blocks completion. All three are judgement calls, not defects.

## New learnings
- **Run a feature against real data before trusting its suite.** Both Phase 4
  defects — a false gap on FastAPI and "Engineer" extracted as a requirement —
  passed every test written from the plan. Only the live run exposed them.
- **A false negative can be worse than the failure mode you designed against.**
  This feature was built to stop gaps being softened; the bug that mattered was
  the opposite, inventing a gap that understated real experience.
- Vector search under-serves single-token queries: pair it with an exact-term
  check when the query is a name rather than a sentence.
- A gap-reporting feature needs a test proving a gap is *reachable*, or an
  over-narrow extractor makes the honest answer impossible by construction.

## User overrides
None this phase. The standing rule from Phase 3 — the UI renders resume content
only, inferred data is deleted — held: no content file was touched.

## Open questions
None. Finding 1 is worth a decision before the portfolio is shown to recruiters.
