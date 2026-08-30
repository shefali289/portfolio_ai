# Task: Final Polish + Deploy

| | |
|---|---|
| **Slug** | `06-final-polish` |
| **Branch** | `feature/06-final-polish` |
| **Phase** | Phase 6 |
| **Status** | built — G0-G3 passed, awaiting `/review` |
| **Started / Completed** | 2026-08-30 / — |

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
- [ ] it is **off by default** and the choice survives a reload
- [ ] **a missing metric omits its row entirely** — never a fabricated `0.0 ms`
- [ ] `localStorage` being unavailable means "off", never a crash
- [ ] every AI surface has loading, error and empty states
- [ ] `vercel.json` parses and `api/index.py` imports the FastAPI app
- [ ] **the deployed site is reachable and AI features work against Gemini** —
      blocked on the user's Vercel account and `GEMINI_API_KEY`; `SKIPPED` with
      a reason until then, never `PASS`
- [ ] the Definition of Done is **written into `docs/plan.md`** as the union of
      the six per-phase "Done when" lines plus the harness final checklist
- [ ] full test suite, lint and typecheck green across both sides

## User Experience

An Engineer Mode toggle reveals, per AI response: endpoint, chunks retrieved,
vector search ms, generation ms, sources used, and tool used where applicable.

## Out of Scope

New AI capabilities. Custom domain, analytics.

Also excluded, deliberately:

- **A light/dark theme toggle** — declined, see Rejected Alternatives.
- **New backend instrumentation** — every metric already exists.
- **Retuning `GROUNDING_THRESHOLD`** — it is tuned against a lexical fallback;
  revisit only once `GEMINI_API_KEY` is set and retrieval is semantic.
- **Running the deploy** — needs the user's Vercel account and API key.

---

# 2 · Design  *(Design Agent, `/plan`)*

**1 · Where does it live?** Almost entirely `frontend/src/` — a context, a panel
component, and two surfaces that render it. Plus `api/index.py` and
`vercel.json` at the repo root, which Vercel requires.

**2 · What is reused?** Every metric Engineer Mode displays is already returned
by `/api/ai/chat` and `/api/ai/job-match`. The existing `@layer components`
style seam, skeleton, error and empty patterns are reused unchanged.

**3 · Frontend changes?** Yes — the toggle, the context, the panel, and its
placement in the two AI surfaces.

**4 · Backend changes?** Only the MCP `search_resume` grounding flag, and only
if the user approves it. This phase displays; it does not measure.

**5 · AI / RAG / MCP?** No new capability. The one MCP change is a correctness
fix carried over from the Phase 5 review, not new behaviour.

**6 · New dependency?** **No.** The diagram is Mermaid in Markdown, which
GitHub renders natively.

**7 · Simplest sufficient implementation?** A React context holding one boolean
persisted to `localStorage`, and a `<Metrics>` component driven entirely by
fields already present in the responses.

## Key technical decisions

- **A missing metric omits its row.** Rendering `0.0 ms` would present a
  fabricated measurement as real — the same failure mode as inventing portfolio
  content, in a different costume.
- **Off by default.** A recruiter should meet the portfolio, not the
  instrumentation; an engineer can switch it on in one click.
- **One toggle, not two.** `decisions.md` deferred the theme toggle to this
  phase; it is **declined**. `prefers-color-scheme` already honours the OS
  setting, and two similar header controls is clutter. Decision closed.
- **The Definition of Done is transcribed, not invented.** `docs/plan.md`
  promises a checklist that does not exist; it is the six per-phase "Done when"
  lines plus the harness final checklist, and nothing new.

## Existing Components Reused

Metrics already returned by the Phase 3 and 4 endpoints - this phase displays
them, it does not add new measurement.

## Rejected Alternatives

| Option | Why not |
|---|---|
| New instrumentation for Engineer Mode | Every metric is already measured and returned; adding more would duplicate it. |
| A light/dark theme toggle | `prefers-color-scheme` already decides from the OS. Two header toggles is clutter, and neither would be discoverable. |
| Streaming metrics or a `/debug` endpoint | A second transport for one panel. |
| An exported PNG architecture diagram | Mermaid renders on GitHub, diffs in git, and needs no tool. |
| Many large committed screenshots | They are the first thing to go stale, and they bloat the clone. |
| Deploying from here | Needs the user's Vercel account and API key. Claiming a deploy that did not happen would be worse than leaving it open. |

---

# 3 · Plan  *(Planning Agent, `/plan`)*

## Implementation Steps

| # | Step | Skill | Verified by |
|---|---|---|---|
| 1 | **RED→GREEN** `lib/engineerMode.tsx` + test — context, `localStorage` persistence wrapped in try/catch, default OFF | `tdd-cycle` | off by default; survives remount; unavailable storage means off, not a crash |
| 2 | **RED→GREEN** `components/Metrics.tsx` + test — renders endpoint, chunks, both timings, provider, tool used; **omits any row whose metric is absent** | `react-component` | a fixture with `generation_ms` missing renders no such row, and no `0.0` |
| 3 | **RED→GREEN** render `<Metrics>` in `AskPortfolio` and `JobMatch`; Job Match adds its four chain steps with per-step ms | `react-component` | panel hidden when off, present when on, in both surfaces |
| 4 | Header switch + provider in `App.tsx`, labelled and keyboard operable | `a11y-responsive` | reachable by tab, `aria-pressed` reflects state |
| 5 | Audit loading / error / empty on every AI surface; fill any gap found | `a11y-responsive` | each state reached in a real browser, not only in tests |
| 6 | Full a11y + 375px pass across all sections including GitHub and Why Me | `a11y-responsive` | `scrollWidth == clientWidth`, headings unskipped, focus visible |
| 7 | `README.md` rewrite + Mermaid architecture diagram in `docs/architecture.md` + a small number of screenshots | — | diagram renders on GitHub; README matches actual behaviour |
| 8 | **Only if approved** — MCP `search_resume` returns a `grounded` flag (Phase 5 review finding 1) | `tdd-cycle` | out-of-scope query marked ungrounded; if unapproved, record as still owed |
| 9 | `api/index.py` + `vercel.json` + committed index; `.env.example` gains the deployed-origin CORS note | `api-endpoint` | `vercel.json` parses, `api/index.py` imports the app, index loads |
| 10 | Write the Definition of Done into `docs/plan.md`; run the full suite, lint, typecheck | — | real output recorded in `## Validation` |

## Files Likely To Change

**New:** `frontend/src/lib/engineerMode.tsx` + test,
`frontend/src/components/Metrics.tsx` + test, `api/index.py`, `vercel.json`

**Modified:** `frontend/src/App.tsx`, `components/{AskPortfolio,JobMatch}.tsx`
and their tests, `README.md`, `docs/{architecture,plan}.md`, `.env.example`,
and — step 8 only — `backend/app/integrations/tools.py` + `tests/test_tools.py`

**Must not change:** `backend/app/rag/`, `services/ai.py`, `api/schemas.py`.
Engineer Mode displays what these already return. Needing to touch them means
the design is wrong — stop and report it.

## Skills Used

`react-component`, `a11y-responsive`, `tdd-cycle`

---

# 4 · Tests  *(Test Agent, `/build`)*

## Tests First

- Engineer Mode is **off by default**, toggles on, and the choice survives a
  remount
- `localStorage` throwing (private mode, blocked site data) means **off**, not a
  crash
- the metrics panel renders endpoint, chunks, both timings, provider, tool used
- **a response missing a metric omits that row entirely** — no `0.0 ms` shown
- the panel is absent from both AI surfaces while Engineer Mode is off
- Job Match renders its four chain steps with per-step timings
- every AI surface has loading, error and empty states
- step 8 only: `search_resume` marks an out-of-scope query ungrounded
- full suite green across backend and frontend

## TDD Evidence

RED then GREEN. Tests written after the code fail G2 — the failure output is the
proof, and `final_checklist.py` checks for it.

| | |
|---|---|
| **RED - command** | `cd frontend && npm.cmd test -- --run src/lib/engineerMode.test.tsx src/components/Metrics.test.tsx src/components/AskPortfolio.test.tsx` |
| **RED - failed for the right reason** | Yes. `Failed to resolve import "./engineerMode"`, `"./Metrics"`, `"../lib/engineerMode"`; `Test Files 3 failed (3)`, `Tests no tests`. Output in `handoffs/3-test.md`. |
| **GREEN - result** | backend `79 passed`; frontend `Test Files 12 passed (12)`, `Tests 53 passed (53)` |

---

# 5 · Gates

See `harness/QUALITY-GATES.md`. `PARTIAL`/`SKIPPED` are honest; a check reported
`PASS` without running is not.

| Gate | When | Result | Date | Note |
|---|---|---|---|---|
| **G0** branch | before `/build` writes | PASS | 2026-08-30 | 3 passed, 1 warn (plan artefacts uncommitted) |
| **G1** design | Design → Plan | PASS | 2026-08-30 | 7 questions answered; no new dependency; `1-design.md` 60 lines, within cap |
| **G2** test (RED) | Test → Develop | PASS | 2026-08-30 | 3 suites failed to resolve `./engineerMode`, `./Metrics`, `../lib/engineerMode`. Output in `handoffs/3-test.md` |
| **G3** build (GREEN) | Develop → Review | PASS | 2026-08-30 | backend `85 passed`, frontend `53 passed`; ruff + eslint + tsc clean; build succeeds. Rebuilt after review: runtime pin and install stub removed, guarded by `tests/test_deploy_config.py`. Step 8 skipped (unapproved) |
| **G4** review | Review → Complete | **PARTIAL** | 2026-08-30 | Tests, lint, typecheck, a11y and 375px all PASS. **One blocking finding:** `vercel.json` pins `@vercel/python@4.3.0`, which predates Python 3.11 and cannot import `StrEnum` (`agents/base.py:10`). Deploy config FAIL — back to `/build`. See `handoffs/5-review.md` |
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
| 2026-08-30 | Engineer Mode is display-only; no new backend metric | Everything it shows is already returned by the Phase 3-5 endpoints |
| 2026-08-30 | A missing metric omits its row; never `0.0 ms` | Presenting a fabricated measurement as real is the same failure as inventing content |
| 2026-08-30 | The deferred theme toggle is **declined** | `prefers-color-scheme` already honours the OS choice; two header toggles is clutter |
| 2026-08-30 | The Definition of Done is transcribed, not invented | `docs/plan.md` promises a checklist that never existed; it is the six "Done when" lines plus the harness checklist |
| 2026-08-30 | Deployment config is written and verified; the deploy itself is not run | It needs the user's Vercel account and `GEMINI_API_KEY`; claiming an unperformed deploy would be worse than leaving it open |
| 2026-08-30 | `lib/engineerModeContext.ts` split out of `lib/engineerMode.tsx` | eslint warns when one file exports both components and a hook; splitting fixes it structurally where a suppression would hide it |
| 2026-08-30 | Root `requirements.txt` includes `-r backend/requirements.txt` rather than copying pins | Two lists of the same dependencies drift, and a deployed backend differing from the tested one is the failure being avoided |
| 2026-08-30 | Ten pre-existing sub-44px tap targets left unfixed | The fix touches `.text-link` across every section; a sweeping late CSS change is a review decision, not a quiet commit |
| 2026-08-30 | Step 8 (MCP grounding flag) skipped | Unapproved when `/build` reached it; the plan said skip and record rather than decide it here |
| 2026-08-30 | No Python runtime pinned in `vercel.json` | `@vercel/python@4.3.0` shipped a Python older than 3.11 and could not import `StrEnum`; an unverifiable pin is worse than none because it looks deliberate |
| 2026-08-30 | Deploy config guarded by tests rather than prose | `test_deploy_config.py` fails if a runtime is pinned again or install is stubbed — the defect review caught would now be caught by the suite |
| 2026-08-30 | The SPA catch-all rewrite removed | The portfolio has no client-side routing, only hash anchors; the fallback could shadow static assets for no benefit |

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
