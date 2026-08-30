# Handoff: Review -> Build (one blocking finding)

## Check results

| Check | Result |
|---|---|
| backend | **PASS** — `79 passed`, ruff clean; no secrets in the diff |
| frontend | **PASS** — `53 passed` (12 files); eslint + `tsc` clean; build succeeds |
| Engineer Mode, live | **PASS** — off by default; real metrics on; **no `0.00 ms`** |
| 375px · headings · keyboard | **PASS** — no overflow, one `<h1>`, real controls |

## Findings

**1 · HIGH, BLOCKING — `vercel.json` pins a runtime that cannot run this code.**

```
vercel.json        "runtime": "@vercel/python@4.3.0"
npm registry       latest is 11.0.0; 4.3.0 predates Python 3.11
agents/base.py:10  from enum import StrEnum      <- Python 3.11+
```

The deploy would fail at import with `ImportError: cannot import name
'StrEnum'` — a defect introduced by this phase, in the artifact the phase
exists to produce, and the project's own recorded gotcha in a new costume: a
version pin written from memory rather than verified. Fix: drop the `runtime`
pin or pin one verified to ship 3.11+. One line, but it belongs in `/build`.

**2 · MEDIUM — the `/api/(.*)` -> `/api/index` rewrite is unverified.** If
Vercel does not preserve the original path, FastAPI receives `/api/index` and
every route 404s. Unconfirmable without deploying, so it must not be recorded
as working.

**3 · MEDIUM — `installCommand` is overridden to `echo`.** Its interaction with
the Python function's dependency install is unverified; it may leave the
function without its packages.

**4 · LOW — root `requirements.txt` ships `pytest` and `ruff` to production.**
A deliberate trade for a single source of truth, but worth seeing.

**5 · LOW — ten sub-44px tap targets at 375px**, all pre-existing. WCAG 2.2 SC
2.5.8 asks 24x24 with an inline-link exception, so this is the harness's
stricter bar, not an AA failure.

**Outstanding:** screenshots (step 7) and the MCP grounding flag (step 8, unapproved) are recorded as owed, not dropped.

## New learnings

- **Verify a version pin against the registry, not memory** — the second time
  this project has been bitten. `gotchas.md` says it for Python packages; it
  needs to say it for platform runtimes too.
- **Config you cannot execute is not verified config.** `api/index.py` was
  provable by importing it; `vercel.json` was not, and the difference should be
  stated rather than blurred into "deploy config written".
- **A display-only feature still needs a falsifiable rule** — "a missing metric
  omits its row" gave this phase a test worth writing; "show metrics" would not.

## User overrides

None. The theme toggle was declined by the agent at `/plan` with reasons, and
the user did not reverse it.
