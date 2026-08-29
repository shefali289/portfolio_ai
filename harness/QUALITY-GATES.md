# Quality Gates

Six gates. A stage may not start until the one before it passes, so failure is
caught where it was caused rather than three stages later.

This file is the **index**. Policy detail lives in `instructions/`; enforcement
lives in `scripts/` and CI.

| Gate | When | Blocks on | Policy | Enforced by |
|---|---|---|---|---|
| **G0** branch | before `/build` writes | on `main`; branch ≠ task slug; behind `origin/main` | [`instructions/branch-gate.md`](instructions/branch-gate.md) | `scripts/branch_gate.py` |
| **G1** design | Design → Plan | unanswered questions; untestable criteria; unjustified dependency | [`instructions/design-gate.md`](instructions/design-gate.md) | checklist |
| **G2** test | Test → Develop | tests that did not fail for the right reason | [`skills/tdd-cycle.md`](skills/tdd-cycle.md) | RED output in `3-test.md` |
| **G3** build | Develop → Review | unplanned file changes; unapproved dependency; hardcoded content | [`skills/tdd-cycle.md`](skills/tdd-cycle.md) | tests green |
| **G4** review | Review → Complete | failing tests, lint, typecheck, a11y, secrets | [`agents/review-agent.md`](agents/review-agent.md) | `.github/workflows/pr-checklist.yml` |
| **G5** completion | before archive + PR | unmet criteria; unpruned learning; missing PR body | this file | `scripts/final_checklist.py` |

Plus the **approval gate**, which is not a stage but a standing rule:
[`instructions/approval-gate.md`](instructions/approval-gate.md) — when to stop
and ask rather than decide.

## Run them

```bash
python harness/scripts/branch_gate.py --slug <slug> --rebase   # G0
python harness/scripts/health_check.py                          # structural
python harness/scripts/final_checklist.py --slug <slug>         # G5
```

`final_checklist.py` decides whether a task is complete. It re-runs both suites
rather than trusting an earlier run, and requires **real RED evidence** — so
tests written after the code fail the gate. **A task is not done until it exits
0.** See [`scripts/README.md`](scripts/README.md).

## G2 and G3 in detail

The two gates with no policy file of their own, because the skill covers them.

**G2 — RED.** Tests exist for every behaviour in `## Tests First`; they were
**run**; they failed **for the expected reason**; the failure output is pasted
into `3-test.md` as evidence. A test that passes before the feature exists
blocks this gate. AI features must additionally have the grounding test — an
out-of-scope question is refused, not answered.

**G3 — GREEN.** All G2 tests now pass with output recorded. No files changed
outside the plan's list, or the deviation is recorded in `4-develop.md`. No new
dependency beyond the approved design. No hardcoded portfolio content; unknowns
are explicit `TODO`s.

## G5 — completion

- Every acceptance criterion in `task.md` ticked
- No unresolved blocking findings in `5-review.md`
- `completion.md` written with **real** validation results
- Learnings distilled into `learning/`, and `learning/` pruned to cap
- `AGENT-MANIFEST.md` and `.agent-manifest.json` task status updated
- `pull-request.md` written from `templates/pull-request.md`

## Recording

Every result goes in the task's gate table:

```markdown
| **G0** branch | before build | PASS | 2026-08-29 | |
| **G4** review | review | PARTIAL | 2026-08-29 | frontend lint not configured |
```

`PARTIAL` and `SKIPPED` are honest and allowed. A gate reported `PASS` without
running is the one unrecoverable failure — it makes every later gate
meaningless.

## In CI

`.github/workflows/pr-checklist.yml` runs the mechanical half on every PR:
branch gate, harness health, gate log, secret scan, backend (`ruff`, `pytest`,
content JSON) and frontend (`tsc`, lint, `vitest`, build), then renders the
final checklist. Application jobs **skip cleanly** until that side is built and
report `SKIPPED` — never as passed.
