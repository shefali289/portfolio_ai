# Feature Completion

## Feature

Final Polish + Deploy — `06-final-polish`

## What Was Added

Engineer Mode: a header toggle, off by default and remembered, revealing what
each AI response actually cost and cited — endpoint, chunks retrieved, retrieval
and generation timings, provider, tool used, and the four chain steps for Why
Me?. Every metric was already returned by the Phase 3-5 endpoints, so this phase
**displays rather than measures** and changed no backend behaviour.

Alongside it: the Vercel deployment surface with tests that guard it, a written
Definition of Done, a Mermaid architecture diagram, and corrections to two
documents that described things which do not exist.

## Main Files Changed

- `frontend/src/lib/engineerMode.tsx` — provider and toggle
- `frontend/src/lib/engineerModeContext.ts` — context and hook, split out so
  neither file exports both a component and a hook
- `frontend/src/components/Metrics.tsx` — the panel; omits absent metrics
- `frontend/src/components/{AskPortfolio,JobMatch}.tsx`, `App.tsx` — render it
- `api/index.py`, `vercel.json`, `requirements.txt` — the deploy surface
- `backend/tests/test_deploy_config.py` — guards that surface
- `docs/{plan,architecture,deployment}.md`, `README.md`

## Tests

- `engineerMode.test.tsx` (6) — off by default, toggles, `aria-pressed`,
  survives a remount, and `localStorage` throwing on read *or* write means off
  rather than a crash
- `Metrics.test.tsx` (6) — renders each metric, **omits an absent one**, omits
  the tool row when no tool ran, renders chain steps, renders `null` when empty
- `AskPortfolio.test.tsx` (+2) — panel absent while off, present while on
- `test_deploy_config.py` (6) — no pinned Python runtime, install not stubbed,
  API routed to the function, and the entry point really serves the app

## Validation

| Check | Result |
|---|---|
| backend tests | **PASS** — `85 passed` |
| frontend tests | **PASS** — `Test Files 12 passed (12)`, `Tests 53 passed (53)` |
| lint | **PASS** — ruff and eslint clean |
| typecheck | **PASS** — `tsc --noEmit` clean; `npm run build` succeeds |
| manual check | **PASS** — see below |
| **deployed site** | **descoped to `07-deploy`** — needs a Vercel account and key |

Manual, in a real browser: Engineer Mode off by default with the panel absent;
toggled on it showed `/api/ai/chat`, 4 chunks, 4.95 ms retrieval, 0.03 ms
generation, `template`, tools `portfolio_ai, agentic-ai`, and the choice
survived a reload. **No `0.00 ms` row rendered anywhere.** At 375px:
`scrollWidth == clientWidth`, 0 overflowing elements, one `<h1>`, no skipped
heading levels.

## Gates

| Gate | Result |
|---|---|
| G0 branch | PASS |
| G1 design | PASS — 7 questions, no new dependency |
| G2 test (RED) | PASS — two cycles: the three UI suites, then the deploy-config tests |
| G3 build (GREEN) | PASS — 85 / 53, lint, typecheck, build |
| G4 review | **PARTIAL** — nothing blocking; deploy `SKIPPED` and the `/api/(.*)` rewrite unverifiable from here |
| G5 completion | PASS — after the deployed-site criterion moved to `07-deploy` |

## Design Decisions

- **Engineer Mode displays; it does not measure.** Every metric already existed.
- **A missing metric omits its row.** Rendering `0.00 ms` would present a
  fabricated measurement as real — inventing content in a different costume.
- **The deferred theme toggle was declined.** `prefers-color-scheme` already
  honours the OS setting; two header controls is clutter. Decision closed rather
  than deferred again.
- **The Definition of Done was transcribed, not invented** — the six per-phase
  "Done when" lines plus the harness checklist. Grading the work against a bar
  set by the same agent is worthless.
- **No Python runtime pinned in `vercel.json`.** An unverifiable pin is worse
  than none, because it looks deliberate.

## Lessons Learned

- **Worked:** designing around a falsifiable rule. "A missing metric omits its
  row" produced the phase's best test; "show metrics" would have produced none.
- **Cost time:** handoffs breaching the 60-line cap, repeatedly. Rephrasing does
  not shorten a file — only cutting content does.
- **Do differently:** check a version pin against its registry *before* writing
  it, and never describe config as verified when it cannot be executed.

## User Overrides

None. The theme toggle was declined by the agent at `/plan` with stated reasons
and the user did not reverse it.

## Learning Updated

- `gotchas.md` — the two pin failures merged into one generalised rule (verify
  against the registry, and ask whether it *runs this code*, not merely whether
  it exists); plus "config you cannot execute is not verified config"
- `conventions.md` — a review defect leaves a test behind, not just a fix; a
  display-only feature still needs a falsifiable rule
- `decisions.md` — new `Final polish` section, five decisions
- `architecture-map.md` — header now says all six phases built; Engineer Mode
  and the deploy surface recorded as seams
- `lessons-learned.md` — `## 06-final-polish`

## Known Limitations

- **The deploy has not been run** — moved to `07-deploy`, not dropped. It needs
  a Vercel account and `GEMINI_API_KEY` the harness does not hold.
- **The `/api/(.*)` rewrite is unverified.** If Vercel does not preserve the
  path, every route 404s; check `/api/health` first.
- **Ten sub-44px tap targets**, all pre-existing; the fix touches `.text-link`
  sitewide. WCAG 2.2 SC 2.5.8 asks 24×24 with an inline-link exception.
- **`pytest` and `ruff` ship with the function** — the cost of one dependency
  source of truth.
- **No screenshots** — they need a deployed URL.
- **Step 8 (MCP grounding flag) not implemented** — unapproved since Phase 5.

## PR

**Not created** — awaiting approval. `gh` is authenticated as `shefali289`.

```bash
gh pr create --base main \
  --title "feat: engineer mode, deploy config, and the definition of done" \
  --body-file harness/tasks/completed/06-final-polish/pull-request.md
```

Compare: https://github.com/shefali289/portfolio_ai/compare/main...feature/06-final-polish

## Suggested Commit Message

```
docs(harness): complete and archive 06-final-polish
```
