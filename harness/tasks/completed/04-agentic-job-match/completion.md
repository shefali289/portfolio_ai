# Feature Completion

## Feature

Agentic Job Match — Why Me? — `04-agentic-job-match`

## What Was Added

A four-agent chain — `requirement -> portfolio -> evidence -> response` — behind
`POST /api/ai/job-match`, and a Why Me? section that takes a pasted job
description and reports evidenced requirements alongside honest gaps.

Four composed functions, deliberately not a framework: the decomposition *is*
the demonstration. Each agent has one responsibility, is typed in and typed out,
and is testable alone.

## Main Files Changed

- `backend/app/agents/{base,requirement,portfolio,evidence,response,chain}.py` — new
- `backend/app/services/job_match.py` — new
- `backend/app/services/ai.py` — exposes `retriever` so there is one search path
- `backend/app/rag/retriever.py` — exposes `chunks` for exact-term lookup
- `backend/app/api/{routes,schemas}.py`, `app/main.py`
- `frontend/src/components/JobMatch{,.test}.tsx`, `lib/api.ts`,
  `types/content.ts`, `App.tsx`

## Tests

- backend 42 (15 new), frontend 30 (6 new)
- The chain tests pin what matters: four steps in order, a raising agent yields
  `ChainError` with no partial report, and **a requirement with no evidence is a
  gap carrying no evidence at all**
- Two regression tests came from live defects, not the plan (see below)

## Validation

| Check | Result |
|---|---|
| backend tests | PASS — `42 passed` |
| frontend tests | PASS — `Test Files 9 passed (9)`, `Tests 30 passed (30)` |
| lint | PASS — ruff and eslint clean |
| typecheck | PASS — `tsc --noEmit` clean |
| manual check | PASS — live against the real resume: FastAPI and PostgreSQL attributed to the Spark role; Kubernetes and Terraform reported as gaps, both genuinely absent. 375px measured in-browser: `scrollWidth=375`, 0 overflowing elements |

## Gates

| Gate | Result | Note |
|---|---|---|
| G0 branch | PASS | third in the unmerged stack |
| G1 design | PASS | no new dependency; explicitly no agent framework |
| G2 test | PASS | 15 tests RED for the right reason |
| G3 build | PASS | 2 live defects found and fixed with regressions |
| G4 review | PASS | all checks; 3 LOW findings, none blocking |
| G5 completion | PASS | `final_checklist.py --slug 04-agentic-job-match` exits 0 |

## Design Decisions

- **The verdict is computed, never asked of a model.** `assess_evidence` uses
  retrieval scores against `GROUNDING_THRESHOLD`. Asking an LLM whether evidence
  is sufficient is exactly how a gap becomes a partial match.
- **One search path.** `JobMatchService` receives `ai.retriever` — the same
  instance Ask My Portfolio uses. Two retrievers would drift apart.
- **Exact-term evidence alongside vector search.** A verbatim term in the corpus
  counts as evidence; without this, single-word requirements produced false gaps.
- **Steps returned, not streamed.** No new transport for one feature.
- **A failing step aborts the run.** `ChainError` rather than a partial report.

## Lessons Learned

- **Worked:** four composed functions. Each defect was traceable to exactly one
  agent, and each agent was testable without the others.
- **Cost time:** nothing structural — the defects surfaced within minutes of
  running the chain against the real resume rather than fixture content.
- **Do differently:** run a feature against real data *before* trusting a green
  suite. Both defects passed every test written from the plan.

## Known Limitations

- A bare skills-list mention counts as a *strong* match, the same as a
  demonstrated role. Evidence is shown, so a reader can tell.
- Requirement extraction is heuristic and will misfire on unusual job ads.
- `STRONG_MATCH = 0.45` is unvalidated against semantic embeddings.
- No LLM path for extraction or summary; both are deterministic.
