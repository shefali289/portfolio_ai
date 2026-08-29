# Task: Agentic Job Match — Why Me?

| | |
|---|---|
| **Slug** | `agentic-job-match` |
| **Branch** | `feature/agentic-job-match` |
| **Phase** | Phase 4 |
| **Status** | brief — not started |
| **Started / Completed** | — |

> **Brief only.** `/plan agentic-job-match` fills in Design, Plan and the rest. Every stage
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

- [ ] a pasted job description yields matches, evidence and gaps
- [ ] the four steps appear in the UI as they run
- [ ] **a requirement with no evidence is reported as a gap, never softened**
- [ ] a JD demanding an absent skill (e.g. Kubernetes) reports it as a gap
- [ ] the chain reuses the existing RAG retrieval - no second search path
- [ ] a failing step propagates rather than returning a partial result

## User Experience

Paste a job description. Four steps tick over live: Understanding role,
Searching portfolio, Finding evidence, Preparing response. Output lists strong
matches with evidence, and gaps stated plainly as gaps.

## Out of Scope

Parallel agents, an agent framework, persistence of past matches.

---

# 2 · Design  *(Design Agent, `/plan`)*

_(seven questions — unanswered until `/plan`)_

## Existing Components Reused

The RAG retrieval service from `rag-assistant`. `AIProvider` unchanged.

## Rejected Alternatives

_(filled at `/plan`)_

---

# 3 · Plan  *(Planning Agent, `/plan`)*

## Implementation Steps

_(4–10 steps — filled at `/plan`)_

## Files Likely To Change

_(filled at `/plan`)_

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
| **RED - command** | — |
| **RED - failed for the right reason** | — |
| **GREEN - result** | — |

---

# 5 · Gates

See `harness/QUALITY-GATES.md`. `PARTIAL`/`SKIPPED` are honest; a check reported
`PASS` without running is not.

| Gate | When | Result | Date | Note |
|---|---|---|---|---|
| **G0** branch | before `/build` writes | — | | `branch_gate.py` |
| **G1** design | Design → Plan | — | | |
| **G2** test (RED) | Test → Develop | — | | failure output recorded |
| **G3** build (GREEN) | Develop → Review | — | | |
| **G4** review | Review → Complete | — | | tests · lint · typecheck · a11y |
| **G5** completion | before archive + PR | — | | `final_checklist.py` |

## Final Checklist  *(`/complete`)*

`python harness/scripts/final_checklist.py --slug agentic-job-match` — must exit 0.
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

## User Overrides

Every entry must end in a promoted rule. Promoted to
`harness/learning/user-overrides.md` at `/complete`.

| Date | Agent proposed | User chose | Why | Rule now |
|---|---|---|---|---|

## Lessons Learned

- **Worked:**
- **Cost time:**
- **Do differently:**

## Known Limitations

_(filled at `/complete`)_

---

# 7 · Validation & PR  *(`/complete`)*

## Validation

Real results only. Not run = `SKIPPED`, never `PASS`.

| Check | Result |
|---|---|
| backend tests | — |
| frontend tests | — |
| lint | — |
| typecheck | — |
| manual check | — |

A real job description produces a defensible match report.

## PR Summary

| | |
|---|---|
| **Title** | — |
| **URL** | — |
| **Merged** | — |

**What it adds:** —

**Why:** —

## Suggested Commit Message

```
<type>: <description>
```
