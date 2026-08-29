# Quality Gates

Six gates. A stage may not start until the gate before it passes. Each gate is
cheap and mechanical - the point is that failure is caught at the stage that
caused it, not three stages later.

Every gate result is recorded in the task's `## Gate Log`.

---

## G0 - Branch Gate  (before `/build` writes anything)

| Check | Fail action |
|---|---|
| Not on `main` | create `feature/<slug>` and switch |
| Branch name matches the task slug exactly | rename, or stop and ask |
| Working tree clean, or changes belong to this task | stop, report |
| Exactly one task in `tasks/active/` | stop, ask which to continue |

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

- Every requirement in `task.md` met
- No unresolved blocking findings in `5-review.md`
- `completion.md` written with **real** validation results
- Learnings distilled into `learning/`, and `learning/` pruned
- `AGENT-MANIFEST.md` task status updated
- PR description written from `templates/pull-request.md`

---

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
