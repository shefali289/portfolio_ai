# Handoff: Review -> Complete (re-review; G4 PARTIAL, nothing blocking)

## Check results

| Check | Result |
|---|---|
| backend | **PASS** — `85 passed in 3.98s`, ruff clean; no secrets in the diff |
| frontend | **PASS** — `53 passed` (12 files); eslint + `tsc` clean |
| production build | **PASS** — `npm run build` succeeds |
| deploy config | **PASS** — `test_deploy_config.py` `6 passed` |
| Engineer Mode, live | **PASS** — off by default; real metrics on; **no `0.00 ms`** |
| 375px · headings · keyboard | **PASS** — no overflow, one `<h1>`, real controls |
| **deployed site** | **SKIPPED** — needs the user's Vercel account and key |

Live UI results carry over from the build: `git diff 71a974c..HEAD -- frontend/`
is empty, so nothing rendered changed after that browser run — stated, not
re-claimed.

## Previous findings

- **1 · HIGH, blocking — runtime pin. FIXED.** `vercel.json` pins no runtime,
  and `test_no_pinned_python_runtime` fails if one reappears, so the defect is
  regression-tested rather than merely corrected.
- **3 · MEDIUM — `installCommand` stub. FIXED**, likewise guarded.
- **2 · MEDIUM — the `/api/(.*)` rewrite. OPEN, unfixable here.** Whether Vercel
  preserves the original path cannot be established without deploying.
  `docs/deployment.md` now separates verified from unverified and names
  `/api/health` as the first check. Correctly *not* recorded as working.
- **4 · LOW — `pytest`/`ruff` ship to production.** Unchanged, deliberate.
- **5 · LOW — ten sub-44px tap targets**, all pre-existing. Unchanged.

## New findings

None. The rebuild touched `vercel.json`, `docs/deployment.md` and one new test
file; nothing in it introduced a defect.

## Why G4 is PARTIAL, not PASS

Nothing blocks, but two checks did not pass on their own terms: the deployed
site was never reached, and the rewrite is unverifiable from here. Recording
PASS would claim a deployment nobody performed. PARTIAL with both reasons
stated is honest, and `/complete` can proceed on it.

## New learnings

- **Verify a version pin against its registry, not memory.** Second time here.
  `gotchas.md` says it for Python packages; it must say it for platform
  runtimes too — `@vercel/python@4.3.0` existed, so "does it exist" was the
  wrong question; "does it run this code" was.
- **Config you cannot execute is not verified config.** `api/index.py` was
  provable by importing it; `vercel.json` was not, and the build report blurred
  the two.
- **A defect found in review should leave a test behind, not just a fix.** The
  pin got through because deploy config was invisible to the suite.
- **A display-only feature still needs a falsifiable rule** — "a missing metric
  omits its row" was testable; "show metrics" would not have been.

## User overrides

None. The theme toggle was declined at `/plan` with reasons; not reversed.
