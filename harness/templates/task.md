# Task: <Name>

| | |
|---|---|
| **Slug** | `<slug>` |
| **Branch** | `feature/<slug>` |
| **Phase** | <phase or "feature"> |
| **Status** | brief · planned · building · in review · complete |
| **Started / Completed** | — |

> **One task, one record.** Every stage writes back into this file, so it ends up
> holding the whole story: what was asked, what was decided, what was tested,
> what gates passed, what was learned, and what the PR said. Handoffs stay small
> and disposable; **this is the durable artefact.**

---

# 1 · Intent  *(written at `/plan`)*

## Feature

What are we adding?

## Goal

What problem does this solve?

## Acceptance Criteria

Testable, checked off at `/review`. If a line cannot be verified, rewrite it.

- [ ] ...
- [ ] ...
- [ ] ...

## User Experience

What should the user be able to do? Include the empty, loading and error states.

## Out of Scope

Deliberately excluded, and why.

---

# 2 · Design  *(Design Agent, `/plan`)*

Answer each in one or two sentences.

1. **Where does this live?**
2. **What can be reused?**
3. **Frontend changes?**
4. **Backend changes?**
5. **AI / RAG / MCP?**
6. **New dependency?** (Default: no.)
7. **Simplest implementation?**

## Existing Components Reused

## Rejected Alternatives

One line each, with the reason.

---

# 3 · Plan  *(Planning Agent, `/plan`)*

## Implementation Steps

4–10 ordered steps, each naming the skill it uses and the files it touches.

1. ...

## Files Likely To Change

## Skills Used

`harness/skills/...`

---

# 4 · Tests  *(Test Agent, `/build`)*

## Tests First

What must fail before implementation exists.

- ...

## TDD Evidence

RED then GREEN. Tests written after the code fail G2 — the failure output is the
proof, and `final_checklist.py` checks for it.

| | |
|---|---|
| **RED - command** | `pytest -q tests/test_x.py` |
| **RED - failed for the right reason** | paste the failure, or point at `handoffs/3-test.md` |
| **GREEN - result** | `N passed` |

---

# 5 · Gates  *(each stage records its own)*

See `harness/QUALITY-GATES.md`. `PARTIAL`/`SKIPPED` are honest and allowed;
a check reported `PASS` without running is not.

| Gate | When | Result | Date | Note |
|---|---|---|---|---|
| **G0** branch | before `/build` writes | — | | `branch_gate.py` |
| **G1** design | Design → Plan | — | | |
| **G2** test (RED) | Test → Develop | — | | failure output recorded |
| **G3** build (GREEN) | Develop → Review | — | | |
| **G4** review | Review → Complete | — | | tests · lint · typecheck · a11y |
| **G5** completion | before archive + PR | — | | `final_checklist.py` |

## Final Checklist  *(`/complete`)*

`python harness/scripts/final_checklist.py --slug <slug>` — must exit 0.
Paste the result table, then confirm the manual items by hand:

- [ ] content traces to the resume; no invented experience
- [ ] AI answers cite sources; out-of-scope questions refused
- [ ] works at 375px and desktop
- [ ] loading, error and empty states reachable
- [ ] keyboard navigable; images have alt text

---

# 6 · Record  *(appended as the work happens)*

## Decisions Taken

What was decided mid-flight, and why. Not a diary — consequential choices only.

| Date | Decision | Reason |
|---|---|---|

## User Overrides

Where the user reversed or redirected an agent. **Highest-value learning signal
here** — unrecorded, it gets repeated. Every entry must end in a promoted rule.
Promote to `harness/learning/user-overrides.md` at `/complete`.

| Date | Agent proposed | User chose | Why | Rule now |
|---|---|---|---|---|

## Lessons Learned

- **Worked:**
- **Cost time:**
- **Do differently:**

Promoted to `harness/learning/` at `/complete`.

## Known Limitations

Intentionally not implemented.

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

Body written to `pull-request.md` from `harness/templates/pull-request.md`.

| | |
|---|---|
| **Title** | `<type>: <description>` |
| **URL** | — (or the compare URL if `gh` could not open it) |
| **Merged** | — |

**What it adds:** two or three sentences.

**Why:** the problem it solves.

## Suggested Commit Message

```
<type>: <description>
```
