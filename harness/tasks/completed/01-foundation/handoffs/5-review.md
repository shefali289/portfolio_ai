# Handoff: Review -> Completion

## Check results
| Check | Result |
|---|---|
| `pytest` | **PASS** — `14 passed in 0.55s` |
| `ruff check .` | **PASS** — `All checks passed!` |
| `npm test` | **PASS** — `Test Files 1 passed (1)`, `Tests 5 passed (5)` |
| `npm run lint` | **PASS** — clean |
| `npx tsc --noEmit` | **PASS** — clean |
| secrets / keys | **PASS** — no key, token or `.env` committed; `.gitignore` covers both |
| visual 375px + desktop | **SKIPPED** — no browser available here. Markup reasoned through, not seen. |
| keyboard pass | **PARTIAL** — semantics verified by reading; focus order not exercised live |

Acceptance criteria: all six met; the browser one verified with `curl` through
the Vite proxy rather than visually.

## Findings

**1 · MEDIUM (privacy) — resolved locally, pending history rewrite.**
`docs/resume.md` carried a phone number from commit `5f8380e`, despite keeping
it out of publicly served `content/`. The working tree now replaces it with
`TODO: held offline`; the local commit history must still be rewritten before
anything is pushed. `gh` is unauthenticated, so remote visibility was not
confirmed. **User chose redaction.**

**2 · MEDIUM (a11y) — deferred by user.**
`Profile.tsx` uses `animate-pulse`; Tailwind does not disable animation for
reduced motion on its own. `a11y-responsive.md` step 6 requires it.
*Follow-up:* use `motion-safe:animate-pulse`; user chose not to change it now.

**3 · LOW — `skills.json` evidence refs are unvalidated strings.**
`ref: "role-1"` is never checked against ids in `experience.json`, so a typo
silently produces a dead evidence link. *Fix:* a cross-reference test in Phase 2.

Nothing blocks completion once the approved privacy history rewrite is done.
Findings 2 and 3 remain follow-up work.

## New learnings
- `uv venv` needs `--python 3.14` on this machine; bare `uv venv` selects a
  uv-managed 3.11 and `numpy==2.5.2` then fails to resolve.
- `npm create vite` cancels under a non-interactive shell — hand-write scaffolds.
- **Latest is not always installable.** `typescript-eslint@8` caps TypeScript
  below 6.1.0, so TS 7.0.2 was rejected. Check peer ranges before pinning.
- `ruff` B008 flags FastAPI's `Depends()` default-arg form; an `Annotated` alias
  is the fix, not a per-line ignore.
- Tree-scanning scripts must skip dependency and cache dirs — `health_check.py`
  walked into `backend/.venv` and failed on vendored Markdown.
- Excluding personal data from one surface is not excluding it from the repo —
  see finding 1.

## User overrides
- **Stages must hand off, not dead-stop.** Promoted to rule 4b and
  `harness/instructions/stage-handoff.md`.
- **Phase tasks carry their number** (`01-`…`06-`) so the next one to run is
  obvious from a directory listing.

## Open questions
None. The privacy decision is made; rewriting history still requires the
approval gate before execution.
