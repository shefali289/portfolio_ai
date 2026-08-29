# Task: Foundation

| | |
|---|---|
| **Slug** | `foundation` |
| **Branch** | `feature/foundation` |
| **Phase** | Phase 1 |
| **Status** | brief — not started |
| **Started / Completed** | — |

> **Brief only.** `/plan foundation` fills in Design, Plan and the rest. Every stage
> writes back here, so this file ends up holding the whole story. Do not
> implement from this file alone.

---

# 1 · Intent

## Feature

A running React + TypeScript frontend, a running FastAPI backend, the shared
`content/` data extracted from the resume, and the test tooling both sides use
for the rest of the project.

## Goal

Establish the skeleton every later phase plugs into, so Phases 2-6 only ever
add features - never restructure. Nothing here is thrown away.

## Acceptance Criteria

Refined at `/plan`, checked off at `/review`.

- [ ] `npm run dev` serves the site at `localhost:5173`
- [ ] `uvicorn app.main:app --reload` serves the API at `localhost:8000`
- [ ] the page fetches `/api/profile` and renders the real name and title from
      `content/profile.json` - proving the stack is wired end to end
- [ ] all five `content/*.json` files exist, parse, and contain only resume-backed
      content (unknowns as explicit `TODO`)
- [ ] `pytest` and `npm test` both run and pass
- [ ] `ruff check`, `npm run lint` and `tsc --noEmit` are clean

## User Experience

Not user-facing yet. The developer-facing outcome is both servers running and
the browser rendering live API data with no CORS errors.

## Out of Scope

Full portfolio sections (Phase 2). RAG, embeddings, any LLM call (Phase 3).
Agents (Phase 4). MCP/GitHub (Phase 5). Engineer Mode, animations, deployment
(Phase 6). No styling beyond the layout shell.

---

# 2 · Design  *(Design Agent, `/plan`)*

_(seven questions — unanswered until `/plan`)_

## Existing Components Reused

Nothing - greenfield. Establishes `ContentService`, the API client, the layout
shell and the test setup that all later phases build on.

## Rejected Alternatives

_(filled at `/plan`)_

---

# 3 · Plan  *(Planning Agent, `/plan`)*

## Implementation Steps

_(4–10 steps — filled at `/plan`)_

## Files Likely To Change

_(filled at `/plan`)_

## Skills Used

`content-extraction`, `api-endpoint`, `react-component`, `tdd-cycle`

---

# 4 · Tests  *(Test Agent, `/build`)*

## Tests First

Backend
- `GET /api/health` returns `200 {"status": "ok"}`
- `GET /api/profile` returns the name from `content/profile.json`
- `ContentService` loads all five files and validates them
- `ContentService` raises a clear error on malformed/missing JSON

Frontend
- `App` renders the layout shell
- the profile section renders the name from a mocked API
- loading state renders while the request is pending
- error state renders when the API rejects

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

`python harness/scripts/final_checklist.py --slug foundation` — must exit 0.
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

Both dev servers start clean; the browser shows the real name/title fetched from
the API; no secrets committed and `.env` is gitignored.

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
