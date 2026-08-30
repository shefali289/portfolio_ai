# Task: Deploy to Vercel

| | |
|---|---|
| **Slug** | `07-deploy` |
| **Branch** | `feature/07-deploy` |
| **Phase** | Phase 7 |
| **Status** | brief — not started |
| **Started / Completed** | — |

> **Brief only.** `/plan 07-deploy` fills in Design, Plan and the rest.
>
> **Descoped from Phase 6 on 2026-08-30.** The deploy config was written and
> tested there, but running the deploy needs a Vercel account and a
> `GEMINI_API_KEY` the harness does not hold. Holding Phase 6 open for an action
> outside the repository would not make anything truer, so it was split out
> rather than ticked falsely or quietly dropped.

---

# 1 · Intent

## Feature

Run the Vercel deployment, confirm the live site, and close the one Definition
of Done item Phase 6 could not.

## Goal

A reachable public URL where the portfolio renders and the AI features answer
against Gemini rather than the lexical fallback.

## Acceptance Criteria

Refined at `/plan`, checked off at `/review`.

- [ ] the deployed site is reachable and the portfolio renders
- [ ] **`/api/health` returns 200 on the deployed origin** — check this first;
      if it 404s, the `/api/(.*)` rewrite is not preserving the path, which is
      the one thing Phase 6 could not verify
- [ ] AI features answer against Gemini, not the `hashing` fallback
- [ ] an out-of-scope question is still refused in production
- [ ] cold-start time is measured and recorded, not guessed
- [ ] the function bundle is under Vercel's 500 MB limit
- [ ] `CORS_ORIGINS` is set to the deployed origin

## What already exists

Written and tested in Phase 6 — do not rebuild it:

- `api/index.py` — exposes the same FastAPI app, proven to serve `/api/health`
  and `/api/content` through the entry point
- `vercel.json` — pins no Python runtime, deliberately
- `requirements.txt` — includes `backend/requirements.txt`
- `backend/tests/test_deploy_config.py` — fails if a runtime is pinned again
- `docs/deployment.md` — separates what is verified from what is not

## User Experience

A public URL that can be put on a CV.

## Out of Scope

Custom domain, analytics, CI-triggered deploys.

---

# 2 · Design  *(Design Agent, `/plan`)*

_(seven questions — unanswered until `/plan`)_

## Existing Components Reused

Everything. This task runs and verifies the Phase 6 deploy surface; it should
add no application code.

## Rejected Alternatives

_(filled at `/plan`)_

---

# 3 · Plan  *(Planning Agent, `/plan`)*

## Implementation Steps

_(4–10 steps — filled at `/plan`)_

## Files Likely To Change

_(filled at `/plan`)_

## Skills Used

`api-endpoint`, `a11y-responsive`

---

# 4 · Tests  *(Test Agent, `/build`)*

## Tests First

- `/api/health` on the deployed origin returns 200
- a grounded question returns sources with `provider` reporting Gemini
- an out-of-scope question is refused in production

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

`python harness/scripts/final_checklist.py --slug 07-deploy` — must exit 0.
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
