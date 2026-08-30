## feat: engineer mode, deploy config, and the definition of done

Closes: harness task `06-final-polish` (Phase 6 — the last)

### What this adds

**Engineer Mode**: a header toggle, off by default and remembered, revealing
what each AI response actually cost and cited — endpoint, chunks retrieved,
retrieval and generation timings, provider, tool used, and the four chain steps
for Why Me?. Alongside it, the Vercel deployment surface with tests that guard
it, a written Definition of Done, a Mermaid architecture diagram, and
corrections to two documents that described things which do not exist.

### Why

The portfolio claims transparency about its AI. Engineer Mode is that claim made
checkable: a visitor can see the retrieval and generation cost of the answer
they just read, and which sources produced it.

### How

- **Display, not instrumentation.** Every metric was already returned by the
  Phase 3-5 endpoints, so no backend behaviour changed. If a step had needed new
  measurement, the design would have been wrong.
- **A missing metric omits its row.** Rendering `0.00 ms` would present a
  fabricated measurement as a real one — inventing content in a different
  costume — so absence is the first test in the suite.
- **`localStorage` is treated as hostile**, not merely absent: private mode and
  blocked site data both make it throw, so a failure means the toggle is off,
  never a blank page.
- **No Python runtime pinned in `vercel.json`.** It briefly pinned
  `@vercel/python@4.3.0`, which ships a Python older than 3.11 and cannot import
  `StrEnum`; the deploy would have failed at import. An unverifiable pin is
  worse than none because it looks deliberate.
- **The Definition of Done was transcribed, not invented** — the six per-phase
  "Done when" lines plus the checks `final_checklist.py` already enforces.

### Changed

| Area | Files |
|---|---|
| Frontend | `lib/engineerMode.tsx`, `lib/engineerModeContext.ts`, `components/Metrics.tsx`, `components/{AskPortfolio,JobMatch}.tsx`, `App.tsx` |
| Deploy | `api/index.py`, `vercel.json`, `requirements.txt` |
| Backend | `tests/test_deploy_config.py` only — no application code |
| Docs | `README.md`, `docs/{plan,architecture,deployment}.md` |

### Tests

| Suite | Result |
|---|---|
| `pytest` | 85 passed |
| `npm test` | 53 passed (12 files) |
| `ruff` / `eslint` / `tsc` / `build` | clean |

New tests lock in: Engineer Mode off by default and surviving a remount;
`localStorage` throwing on read *or* write meaning "off" rather than a crash; a
metric that is absent omitting its row; the panel being absent while the mode is
off; and — after review — that `vercel.json` pins no Python runtime and the
entry point really serves the app. RED evidence for both cycles in
`handoffs/3-test.md`.

### Quality gates

| Gate | Result |
|---|---|
| G0 branch | PASS |
| G1 design | PASS |
| G2 test (RED) | PASS — two cycles |
| G3 build (GREEN) | PASS |
| G4 review | **PARTIAL** — nothing blocking; see below |
| G5 completion | PASS — after descoping the deploy to `07-deploy` |

**G4 is PARTIAL deliberately.** Review found a blocking defect — the runtime pin
— which is fixed and now regression-tested. Two checks still did not pass on
their own terms: the deployed site was never reached, and the `/api/(.*)`
rewrite cannot be verified without deploying. Recording PASS would claim a
deployment nobody performed.

### Lessons learned

- Designing around a falsifiable rule paid for itself: "a missing metric omits
  its row" produced the phase's best test; "show metrics" would have produced none.
- Verify a version pin against its registry, and ask whether it *runs this code*
  — `4.3.0` existed, which is why "does it exist" was the wrong question.
- A defect found in review should leave a test behind, not just a fix. Deploy
  config was invisible to the suite; now it is not.

### User overrides

None. The deferred theme toggle was declined by the agent at `/plan` with stated
reasons and the user did not reverse it.

### Known limitations

- **The deploy has not been run** — split into `07-deploy` rather than ticked
  falsely. Config is written and tested here; running it needs credentials the
  harness does not hold.
- **The `/api/(.*)` rewrite is unverified** — if Vercel does not preserve the
  path, every route 404s. Check `/api/health` first; `docs/deployment.md`
  separates what is verified from what is not.
- Ten sub-44px tap targets, all pre-existing; the fix touches `.text-link`
  sitewide. WCAG 2.2 SC 2.5.8 asks 24×24 with an inline-link exception.
- `pytest` and `ruff` ship with the function — the cost of one dependency source
  of truth.
- No screenshots (they need a deployed URL), and the MCP `search_resume`
  grounding flag remains unapproved since Phase 5.

### Harness

Task, handoffs 1-5 and completion report:
`harness/tasks/completed/06-final-polish/`
