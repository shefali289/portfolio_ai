# Quality Gates

Six gates. A stage may not start until the gate before it passes. Each gate is
cheap and mechanical - the point is that failure is caught at the stage that
caused it, not three stages later.

Every gate result is recorded in the task's `## Gate Log`.

---

## Scripts

Three gates are executable. Run them; do not eyeball them.

```bash
python harness/scripts/branch_gate.py --slug <slug> --rebase   # G0
python harness/scripts/health_check.py                          # structural
python harness/scripts/final_checklist.py --slug <slug>         # G5
```

`final_checklist.py` is the one that decides whether a task is complete — it
re-runs the tests, checks TDD evidence (real RED output), lint, typecheck, the
gate log, learning updates and the completion docs. **A task is not done until
it exits 0.** See [`scripts/README.md`](scripts/README.md).

## G0 - Branch Gate  (before `/build` writes anything)

`python harness/scripts/branch_gate.py --slug <slug> --rebase`

| Check | Fail action |
|---|---|
| Not on `main` | create `feature/<slug>` and switch |
| Branch name matches the task slug exactly | rename, or stop and ask |
| A task directory exists for the slug | run `/plan <slug>` first |
| Working tree clean | commit or stash before rebasing |
| Not behind `origin/main` | `--rebase` brings it current |

The rebase refuses on a dirty tree, aborts cleanly on conflict, and never
force-pushes — after rewriting an already-pushed branch, push with
`--force-with-lease`.

**Never commit to `main`.** Slug and branch suffix are always identical, so the
task, the branch and the PR are trivially traceable to each other.

---

## G1 - Design Gate  (Design -> Planning)

- The seven design questions are answered
- No new top-level system without a stated reason
- Any new dependency is justified, or the answer is "none"
- `1-design.md` is under 60 lines

---

## G2 - Test Gate  (Test -> Developer)  **RED**

- Tests exist for every behaviour in `## Tests First`
- They were **run**, and failed **for the expected reason**
- Failure output is pasted in `3-test.md` as evidence
- AI features: the grounding test (out-of-scope question refused) exists

A test that passes before the feature exists blocks this gate.

---

## G3 - Build Gate  (Developer -> Review)  **GREEN**

- All tests from G2 now pass, run and output recorded
- No files changed outside the plan's list, or the deviation is recorded
- No new dependency beyond the approved design
- No hardcoded portfolio content; unknowns are explicit `TODO`s

---

## G4 - Review Gate  (Review -> Complete)

| Check | Command |
|---|---|
| Backend tests | `cd backend && pytest -q` |
| Backend lint | `cd backend && ruff check .` |
| Frontend tests | `cd frontend && npm test -- --run` |
| Frontend lint | `cd frontend && npm run lint` |
| Typecheck | `cd frontend && npx tsc --noEmit` |

Plus: no secrets committed, 375px and desktop both clean, loading/error/empty
states reachable, content consistent with the resume.

Not-yet-configured checks are recorded as `SKIPPED`, never as `PASS`.

---

## G5 - Completion Gate  (before archiving + PR)

`python harness/scripts/final_checklist.py --slug <slug>` — **must exit 0.**
It re-runs the tests rather than trusting an earlier run, and verifies TDD
evidence: `3-test.md` must contain real failure output, or the tests were
written after the code.

- Every requirement in `task.md` met
- No unresolved blocking findings in `5-review.md`
- `completion.md` written with **real** validation results
- Learnings distilled into `learning/`, and `learning/` pruned
- `AGENT-MANIFEST.md` task status updated
- PR description written from `templates/pull-request.md`

---

## Enforced in CI

`.github/workflows/pr-checklist.yml` runs the mechanical half of these gates on
every PR into `main`:

| Job | Gate | Enforces |
|---|---|---|
| `branch-gate` | G0 | not `main`; branch matches `feature\|fix\|improvement/<slug>`; a task directory exists for the slug |
| `harness` | — | `harness/scripts/health_check.py` |
| `gate-log` | G1–G5 | task records a Gate Log and Decisions Taken; no gate left `FAIL` |
| `secrets` | G4 | no committed credential files; no API keys or hardcoded secrets in the diff |
| `backend` | G4 | `ruff`, `pytest`, `content/*.json` parses |
| `frontend` | G4 | `tsc --noEmit`, lint, `vitest`, `build` |
| `checklist` | — | renders the full checklist and fails if any required job failed |

Application jobs **skip cleanly** until that side is built, and a skipped job is
reported `SKIPPED` — never as passed. The remaining checks (content traces to
the resume, 375px, keyboard, states reachable) are not automatable and are
confirmed in the PR body.

`harness-health.yml` runs the same health check on pushes to `main`.

## Recording

```markdown
## Gate Log
- G0 branch  PASS  2026-08-29  feature/foundation
- G1 design  PASS
- G2 test    PASS  12 failing as expected
- G3 build   PASS  12/12 green
- G4 review  PARTIAL  frontend lint SKIPPED (not configured until Phase 2)
- G5 done    PASS
```

`PARTIAL` is honest and allowed. A gate reported `PASS` without running is the
one unrecoverable failure - it makes every later gate meaningless.
