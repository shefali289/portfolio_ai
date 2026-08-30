# Handoff: Developer -> Review (rebuilt after review findings 1-3)

## Done

Steps 1-7, 9, 10, then a rebuild for review findings 1-3. **Step 8 skipped** —
still unapproved. Backend **85 passed**, frontend **53 passed**, ruff + eslint
+ `tsc` clean, `npm run build` succeeds.

## You need to know

1. **Verified live, not just in tests.** Engineer Mode off by default, panel
   absent; on, it showed `/api/ai/chat`, 4 chunks, 4.95 ms retrieval, 0.03 ms
   generation, `template`, tools `portfolio_ai, agentic-ai`, and survived a
   reload. **No `0.00 ms` row anywhere.** 375px: `scrollWidth == clientWidth`,
   0 overflowing, one `<h1>`, no skipped heading levels.
2. **Two docs described things that are not true** — `deployment.md` said
   "commit the prebuilt index" (there is none; it is built at boot and
   gitignored) and README said "scaffolded, Phase 1 not started". Both fixed.
3. **The Definition of Done was transcribed, not invented** — the six "Done
   when" lines plus the harness checklist, with deployment excluded and why.
4. **`api/index.py` exposes the same app**, now covered by a test rather than
   a one-off manual check.

## Deviations from the plan

- **Split `lib/engineerModeContext.ts` out of `lib/engineerMode.tsx`.** eslint
  warns when one file exports both components and a hook; splitting fixes it
  structurally where a suppression would have hidden it.
- **Step 8 not done** — the MCP grounding flag is still unapproved. Skipped as
  the plan instructed, not decided here. Still owed.

## Fixed after review

**Finding 1 (blocking) fixed and guarded by a test.** `vercel.json` no longer
pins `@vercel/python@4.3.0`, which shipped a Python older than 3.11 and could
not import `StrEnum`. `tests/test_deploy_config.py` fails if a runtime is
pinned again or `installCommand` is stubbed (finding 3, also fixed). The SPA
catch-all rewrite was dropped: no client-side routing, so it could only shadow
static assets.

**Finding 2 documented, not fixed** — whether the `/api/(.*)` rewrite preserves
the path cannot be verified without deploying. `docs/deployment.md` now
separates verified from unverified and names `/api/health` as the check.

**Still open:** ten sub-44px tap targets, all pre-existing (mine is fixed at
44px); the remaining fix touches `.text-link` everywhere, and WCAG 2.2 SC 2.5.8
asks 24x24 with an inline-link exception — a review decision. Screenshots need
a deployed URL; placeholders would be worse than none.

## Files

New: `lib/engineerMode.tsx`, `lib/engineerModeContext.ts`, `components/Metrics.tsx`
(+2 tests), `api/index.py`, `vercel.json`, `requirements.txt`,
`backend/tests/test_deploy_config.py`. Modified: `App.tsx`,
`components/{AskPortfolio,JobMatch}.tsx`, `AskPortfolio.test.tsx`, `README.md`,
`docs/{plan,architecture,deployment}.md`.

## Do NOT re-read

`3-test.md` — both RED cycles are recorded there.
