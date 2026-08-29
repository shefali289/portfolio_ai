---
name: review
description: Review the active feature - checklist, tests, lint, typecheck. Verifies only.
when_to_use: Use when verifying the active harness task before completing it.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
disable-model-invocation: true
---

# /review — Review Agent

Verifies the active feature. **Does not extend it.**

## Step 0 — Load only what you need

Read exactly:

1. `harness/tasks/active/*/handoffs/4-develop.md` — what was built and deviated
2. `harness/tasks/active/*/task.md` — the requirements to check against
3. `git diff main...HEAD` — the actual change

**Do not read files this feature did not touch.** The diff is the scope.

## Step 1 — Run the checks

Run them for real and record actual output:

```bash
cd backend  && pytest -q && ruff check .
cd frontend && npm test -- --run && npm run lint && npx tsc --noEmit
```

Skip with a note anything not yet configured — never report a check as passing
when it did not run.

## Step 2 — Work the checklist

Use `harness/agents/review-agent.md`, plus `harness/skills/a11y-responsive.md`
for the UI pass. Every requirement in `task.md`; tests, lint, typecheck; secrets;
input validation; 375px and desktop; loading/error/empty states reachable;
keyboard and alt text; unnecessary complexity; content consistent with the
resume; docs updated.

For AI features also: answers cite sources, out-of-scope questions are refused,
the app still works with the LLM provider unavailable.

## Step 2b — Gate G4

Record each check in the task's `## Gate Log` as `PASS`, `FAIL` or `SKIPPED`
with the reason. A check that did not run is **never** `PASS`. `PARTIAL` is
honest and allowed — see `harness/QUALITY-GATES.md`.

## Step 3 — Write the handoff

`handoffs/5-review.md`:

- **Findings** — severity, file, what is wrong, evidence. Only real problems.
- **Check results** — actual pass/fail per command.
- **New learnings** — candidates for `harness/learning/` at `/complete`.
- **User overrides** — anything the user reversed or redirected during this
  feature, for `learning/user-overrides.md`.

"No findings" is a legitimate result. Do not pad the list.

## Step 4 — Report

Findings ranked most severe first, plus check results.

## Step 5 — Hand off

Do not dead-stop. End by **asking whether to continue**, and continue in the
same turn if the answer is yes:

> No blocking findings, G4 passed. Continue to `/complete` now, or stop here?

If findings are blocking, the handoff is back to `/build` to fix them, not
forward to `/complete` — say so and ask. Continue automatically **without
asking** only when the user has already said to run the phase, or the whole
lifecycle, end to end.

See `harness/instructions/stage-handoff.md`.

## Rules

- Report only what is actually broken, with evidence.
- Do not fix things here and do not add enhancements — findings become work,
  either now via `/build` or as the next feature's task.
