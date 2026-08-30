# Task: Agentic Job Match — Why Me?

| | |
|---|---|
| **Slug** | `04-agentic-job-match` |
| **Branch** | `feature/04-agentic-job-match` |
| **Phase** | Phase 4 |
| **Status** | complete — 2026-08-30 |
| **Started / Completed** | 2026-08-30 / 2026-08-30 |

> **Brief only.** `/plan 04-agentic-job-match` fills in Design, Plan and the rest. Every stage
> writes back here, so this file ends up holding the whole story. Do not
> implement from this file alone.

---

# 1 · Intent

## Feature

A four-agent sequential workflow - requirement, portfolio, evidence, response -
behind `POST /api/ai/job-match`, with a UI showing each step as it runs.

## Goal

Demonstrate decomposed agent responsibilities rather than one giant prompt, and
produce an honest match report a recruiter would find useful.

## Acceptance Criteria

Refined at `/plan`, checked off at `/review`.

- [x] a pasted job description yields matches, evidence and gaps
- [x] the four steps appear in the UI as they run
- [x] **a requirement with no evidence is reported as a gap, never softened**
- [x] a JD demanding an absent skill (e.g. Kubernetes) reports it as a gap
- [x] the chain reuses the existing RAG retrieval - no second search path
- [x] a failing step propagates rather than returning a partial result

## User Experience

Paste a job description. Four steps tick over live: Understanding role,
Searching portfolio, Finding evidence, Preparing response. Output lists strong
matches with evidence, and gaps stated plainly as gaps.

## Out of Scope

Parallel agents, an agent framework, persistence of past matches.

---

# 2 · Design  *(Design Agent, `/plan`)*

**1 · Where does this live?**
`backend/app/agents/` (the four agents plus the chain),
`app/services/job_match.py` for orchestration, one route in `app/api/`, one
component in `frontend/src/components`.

**2 · What can be reused?**
Almost everything. Phase 3 built `Retriever`, both provider abstractions and the
grounded-refusal pattern. The portfolio agent calls the existing retriever —
there is no second search path — and the UI reuses the existing component
classes.

**3 · Frontend changes?**
One new `JobMatch` component, one API method, one section in `App.tsx`.

**4 · Backend changes?**
Yes: `app/agents/*` (new), `services/job_match.py` (new), one route and its
schemas.

**5 · AI / RAG / MCP?**
AI and RAG, both reused as-is. No MCP — Phase 5 owns that, and adding a tool
must never reshape RAG.

**6 · New dependency?**
**No.** Explicitly no agent framework: the chain is four composed functions,
which is the point of the feature.

**7 · Simplest implementation?**
Four typed functions run in sequence, each independently testable, returning a
report plus the steps it took. One endpoint, one component that animates through
the recorded steps.

### Key technical decisions

- **A gap is decided by retrieval score, not by the model.** A requirement with
  no evidence above `GROUNDING_THRESHOLD` is reported as a gap. This is Phase
  3's refusal guarantee applied per requirement — asking a model to admit a gap
  is a request; a threshold is a guarantee.
- **Requirement extraction has a no-LLM path.** `AI_PROVIDER=template` is the
  default, so requirements are extracted lexically against the skill vocabulary
  in `content/skills.json`; the LLM path is layered on top when a key exists.
- **Progress is returned, not streamed.** The response carries a `steps` array
  (name, status, ms) and the UI animates through it. SSE would be a new
  transport for one feature; Phase 6 owns Engineer Mode if streaming is wanted.
- **A failing step propagates.** No partial report. Provider *unavailability*
  still degrades to `template`, which is not a step failure.

## Existing Components Reused

| Reused | How |
|---|---|
| `Retriever` from Phase 3 | the portfolio agent's only search path |
| `GROUNDING_THRESHOLD` | decides gap vs match, same guarantee as refusal |
| `AIProvider` + `resolve_provider` | unchanged; template fallback still applies |
| `ContentService` | supplies the skill vocabulary for lexical extraction |
| existing component classes | the UI adds no CSS |

## Rejected Alternatives

| Alternative | Why rejected |
|---|---|
| An agent framework (LangChain, CrewAI) | Rule 21 and the brief exclude it; four composed functions *are* the demonstration |
| One large prompt doing all four jobs | The point is decomposed responsibility with independently testable steps |
| A second retrieval path tuned for job matching | `agent-workflow` step 4 forbids it; two search paths drift apart |
| Streaming progress over SSE/WebSocket | A new transport for one feature; a returned `steps` array is enough to animate |
| Letting the model decide whether evidence is sufficient | That is exactly how a gap gets softened into a partial match |
| Parallel agents | Out of scope in the brief; sequence is what makes the chain legible |

_(filled at `/plan`)_

---

# 3 · Plan  *(Planning Agent, `/plan`)*

## Implementation Steps

Agents bottom-up, then the chain, then the endpoint, then the UI. Step 2 is the
RED gate.

| # | Step | Skill | Verified by |
|---|---|---|---|
| 1 | `agents/base.py` — `Requirement`, `RequirementMatch`, `JobMatchReport`, `AgentStep` | `agent-workflow` | types import; models validate |
| 2 | **RED** — `tests/test_agents.py`, `tests/test_job_match_api.py` | `tdd-cycle` | fails for the right reason; output in `3-test.md` |
| 3 | `agents/requirement.py` — lexical extraction from the skill vocabulary | `agent-workflow` | a pasted JD yields requirements with no API key |
| 4 | `agents/portfolio.py` — retrieve per requirement via the injected `Retriever` | `agent-workflow` | no second search path; retriever is a parameter |
| 5 | `agents/evidence.py` — match / partial / **gap** by score | `agent-workflow` | a Kubernetes requirement is reported as a gap |
| 6 | `agents/response.py` + `chain.py` — compose, record steps, propagate failure | `agent-workflow` | order preserved; a raising agent yields no partial report |
| 7 | `services/job_match.py` + `POST /api/ai/job-match` | `api-endpoint` | documented shape in `/docs`; steps and report returned |
| 8 | `JobMatch.tsx` + `lib/api.ts` + `App.tsx` section; full validation | `react-component`, `a11y-responsive` | steps render; gaps shown plainly; 375px clean |

## Files Likely To Change

**Backend (new)**
`app/agents/{__init__,base,requirement,portfolio,evidence,response,chain}.py` ·
`app/services/job_match.py` · `tests/test_agents.py` ·
`tests/test_job_match_api.py`

**Backend (extended)**
`app/api/routes.py` · `app/api/schemas.py` · `app/main.py` (app state)

**Frontend**
`src/components/JobMatch{,.test}.tsx` (new) · `src/lib/api.ts` ·
`src/types/content.ts` · `src/App.tsx`

**Deliberately not touched:** `app/rag/*`, `app/ai/*`, all of `content/`,
`frontend/src/index.css`, and `backend/requirements.txt`.

## Skills Used

`agent-workflow`, `api-endpoint`, `react-component`, `tdd-cycle`

---

# 4 · Tests  *(Test Agent, `/build`)*

## Tests First

- requirement agent extracts skills from a sample JD
- portfolio agent returns evidence per requirement via existing retrieval
- **evidence agent reports a gap when there is no evidence**
- response agent composes from evidence only, inventing nothing
- chain runs in order; a failing step propagates
- UI shows progress and the final report

## TDD Evidence

RED then GREEN. Tests written after the code fail G2 — the failure output is the
proof, and `final_checklist.py` checks for it.

| | |
|---|---|
| **RED - command** | `cd backend && .venv/Scripts/python.exe -m pytest` · `cd frontend && npm test` |
| **RED - failed for the right reason** | Yes. `ModuleNotFoundError: No module named 'app.agents.chain'`; the 5 endpoint tests failed 404-vs-200/422 and `KeyError: 'steps'`; `Failed to resolve import "./JobMatch"`. Output in `handoffs/3-test.md`. |
| **GREEN - result** | backend `42 passed`; frontend `Test Files 9 passed (9)`, `Tests 30 passed (30)` |

---

# 5 · Gates

See `harness/QUALITY-GATES.md`. `PARTIAL`/`SKIPPED` are honest; a check reported
`PASS` without running is not.

| Gate | When | Result | Date | Note |
|---|---|---|---|---|
| **G0** branch | before `/build` writes | PASS | 2026-08-30 | `feature/04-agentic-job-match`, third in the unmerged stack |
| **G1** design | Design → Plan | PASS | 2026-08-30 | 7 questions answered; no new dependency (explicitly no agent framework); `1-design.md` under 60 lines |
| **G2** test (RED) | Test → Develop | PASS | 2026-08-30 | 15 tests RED for the right reason; output in `3-test.md` |
| **G3** build (GREEN) | Develop → Review | PASS | 2026-08-30 | backend 42/42, frontend 30/30, lint+tsc clean; 2 live defects found and fixed with regressions |
| **G4** review | Review → Complete | PASS | 2026-08-30 | all checks PASS incl. 375px measured in-browser (0 overflowing elements) and honest-gap verification against the real resume; 3 LOW findings, none blocking |
| **G5** completion | before archive + PR | PASS | 2026-08-30 | `final_checklist.py --slug 04-agentic-job-match` exits 0 |

## Final Checklist  *(`/complete`)*

`python harness/scripts/final_checklist.py --slug 04-agentic-job-match` — must exit 0.
Paste the result table, then confirm by hand:

- [ ] content traces to the resume; no invented experience
- [ ] AI answers cite sources; out-of-scope questions refused
- [ ] works at 375px and desktop
- [ ] loading, error and empty states reachable
- [ ] keyboard navigable; images have alt text

---

# 6 · Record

## Decisions Taken

| Date | Decision | Reason |
|---|---|---|
| 2026-08-30 | Exact-term evidence alongside vector search (`_exact_hits`) | "FastAPI" was reported as a gap though a role lists it — a one-token query scores low on lexical cosine. A **false gap understates real experience**, the mirror of the softening this feature prevents |
| 2026-08-30 | Generic job-ad nouns excluded from extraction | "Engineer" was extracted from "AI Engineer" and reported as a gap; junk requirements make the report untrustworthy |
| 2026-08-30 | Verdict computed from retrieval scores, never asked of a model | Asking an LLM whether evidence is sufficient is how a gap becomes a partial match |
| 2026-08-30 | `JobMatchService` receives `ai.retriever` | One search path shared with Ask My Portfolio; two would drift apart |
| 2026-08-30 | Steps returned in the response rather than streamed | SSE would be a new transport for one feature; a `steps[]` array is enough to render the chain |

## User Overrides

Every entry must end in a promoted rule. Promoted to
`harness/learning/user-overrides.md` at `/complete`.

| Date | Agent proposed | User chose | Why | Rule now |
|---|---|---|---|---|

## Lessons Learned

- **Worked:** four composed functions instead of a framework. Each agent was
  testable alone, and the two live defects were each traceable to exactly one
  of them.
- **Cost time:** nothing structural. The defects were found in minutes once
  the chain ran against the real resume rather than fixture content.
- **Do differently:** run a feature against real data *before* trusting a
  green suite. Both defects passed every test written from the plan.

## Known Limitations

Intentionally not implemented.

- **A bare skills-list mention counts as a *strong* match.** `EXACT_TERM_SCORE`
  puts any verbatim term above `STRONG_MATCH`, so a requirement met only by an
  entry in `skills.json` reads like one demonstrated in a role. The evidence is
  shown, so a reader can tell — but it is worth deciding deliberately.
- **Requirement extraction is heuristic** — capitalisation plus an empirical
  stopword list. It will misfire on unusual job ads.
- `STRONG_MATCH = 0.45` is tuned against lexical vectors, unvalidated against
  Gemini embeddings.
- Progress is returned, not streamed; the UI renders the steps after the run.
- No LLM path for extraction or summary yet — both are deterministic.

---

# 7 · Validation & PR  *(`/complete`)*

## Validation

Real results only. Not run = `SKIPPED`, never `PASS`.

| Check | Result |
|---|---|
| backend tests | **PASS** — `42 passed` |
| frontend tests | **PASS** — `Test Files 9 passed (9)`, `Tests 30 passed (30)` |
| lint | **PASS** — ruff and eslint clean |
| typecheck | **PASS** — `tsc --noEmit` clean |
| manual check | **PASS** — live against the real resume: FastAPI and PostgreSQL attributed to the Spark role, Kubernetes and Terraform reported as gaps (both genuinely absent). 375px measured in-browser with the new sections: `scrollWidth=375`, 0 overflowing elements. |

A real job description produces a defensible match report.

## PR Summary

| | |
|---|---|
| **Title** | `feat: agentic job match with honest gaps` |
| **URL** | https://github.com/shefali289/portfolio_ai/pull/5 |
| **Merged** | yes - 2026-08-30 |

**What it adds:** A four-agent chain — requirement, portfolio, evidence,
response — behind `POST /api/ai/job-match`, and a Why Me? section that takes a
pasted job description and reports evidenced requirements alongside honest gaps.

**Why:** it demonstrates decomposed agent responsibility rather than one large
prompt, and produces a match report a recruiter can trust — because a
requirement the portfolio cannot evidence is reported as a gap rather than
softened into a near-match.

## Suggested Commit Message

```
feat: agentic job match with honest gaps
```
