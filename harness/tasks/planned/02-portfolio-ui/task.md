# Task: Portfolio UI

| | |
|---|---|
| **Slug** | `02-portfolio-ui` |
| **Branch** | `feature/02-portfolio-ui` |
| **Phase** | Phase 2 |
| **Status** | brief — not started |
| **Started / Completed** | — |

> **Brief only.** `/plan 02-portfolio-ui` fills in Design, Plan and the rest. Every stage
> writes back here, so this file ends up holding the whole story. Do not
> implement from this file alone.

---

# 1 · Intent

## Feature

Every portfolio section, rendered from `content/*.json`, with no AI yet: Hero,
Experience timeline, Projects, Skills, What I'm Building & Learning, Beyond
Engineering, Contact.

## Goal

A portfolio that stands on its own and is presentable as-is. If the day runs
short, everything after this phase is additive rather than load-bearing.

## Acceptance Criteria

Refined at `/plan`, checked off at `/review`.

- [ ] every section renders from `content/*.json` - no hardcoded copy anywhere
- [ ] experience items expand and collapse
- [ ] project filters (AI / Automation / Backend / Cloud / Frontend) narrow and reset
- [ ] clicking a skill shows where it was used; **no percentage bars**
- [ ] loading, error and empty states exist for every data-driven section
- [ ] no horizontal scroll at 375px; keyboard navigable throughout

## User Experience

Hero states the positioning with Explore Work / Ask My AI / Resume / GitHub /
Contact. Experience is a timeline that expands rather than a wall of text.
Projects are case-study cards - problem, solution, approach, tech, impact.

## Out of Scope

Any AI feature: Ask My Portfolio, Why Me?, GitHub, Engineer Mode.

---

# 2 · Design  *(Design Agent, `/plan`)*

_(seven questions — unanswered until `/plan`)_

## Existing Components Reused

`ContentService` and the API client from `01-foundation`. New endpoints only if a
section needs data not already served.

## Rejected Alternatives

_(filled at `/plan`)_

---

# 3 · Plan  *(Planning Agent, `/plan`)*

## Implementation Steps

_(4–10 steps — filled at `/plan`)_

## Files Likely To Change

_(filled at `/plan`)_

## Skills Used

`react-component`, `tdd-cycle`, `a11y-responsive`

---

# 4 · Tests  *(Test Agent, `/build`)*

## Tests First

- each section renders content from mocked API data, not hardcoded copy
- an experience item expands and collapses
- a project filter narrows the visible set; clearing restores it
- a skill click reveals its evidence list
- loading, error and empty states for every data-driven section

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

`python harness/scripts/final_checklist.py --slug 02-portfolio-ui` — must exit 0.
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

All sections render real resume content; filters and expanders work; 375px and
desktop clean.

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
