# Task: Final Polish + Deploy

| | |
|---|---|
| **Slug** | `06-final-polish` |
| **Branch** | `feature/06-final-polish` |
| **Phase** | Phase 6 |
| **Status** | brief — not started |
| **Started / Completed** | — |

> **Brief only.** `/plan 06-final-polish` fills in Design, Plan and the rest. Every stage
> writes back here, so this file ends up holding the whole story. Do not
> implement from this file alone.

---

# 1 · Intent

## Feature

Engineer Mode, state coverage, mobile and accessibility passes, README,
architecture diagram, screenshots, and deployment to Vercel.

## Goal

Reach the Definition of Done: a portfolio ready to publish and demonstrate.

## Acceptance Criteria

Refined at `/plan`, checked off at `/review`.

- [ ] Engineer Mode toggles and shows endpoint, chunks, retrieval ms,
      generation ms, sources and tool used
- [ ] a response missing metrics degrades gracefully
- [ ] every AI surface has loading, error and empty states
- [ ] the deployed site is reachable and AI features work against Gemini
- [ ] every Definition of Done item in the master plan is satisfied
- [ ] full test suite, lint and typecheck green across both sides

## User Experience

An Engineer Mode toggle reveals, per AI response: endpoint, chunks retrieved,
vector search ms, generation ms, sources used, and tool used where applicable.

## Out of Scope

New AI capabilities. Custom domain, analytics.

---

# 2 · Design  *(Design Agent, `/plan`)*

_(seven questions — unanswered until `/plan`)_

## Existing Components Reused

Metrics already returned by the Phase 3 and 4 endpoints - this phase displays
them, it does not add new measurement.

## Rejected Alternatives

_(filled at `/plan`)_

---

# 3 · Plan  *(Planning Agent, `/plan`)*

## Implementation Steps

_(4–10 steps — filled at `/plan`)_

## Files Likely To Change

_(filled at `/plan`)_

## Skills Used

`react-component`, `a11y-responsive`, `tdd-cycle`

---

# 4 · Tests  *(Test Agent, `/build`)*

## Tests First

- Engineer Mode toggles and renders real metrics from the response
- metrics absent from a response degrade gracefully
- every AI surface has loading, error and empty states
- full suite green across backend and frontend

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

`python harness/scripts/final_checklist.py --slug 06-final-polish` — must exit 0.
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

Deployed site reachable; production AI features working.

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
