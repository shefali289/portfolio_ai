---
description: Implement the active feature - runs Test agent (RED) then Developer agent (GREEN)
argument-hint: [step number to resume from]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# /build — Test + Develop

Implements the active feature. Requires `/plan` to have run.

## Step 0 — Load only what you need

Read exactly:

1. `harness/tasks/active/*/handoffs/2-plan.md` — the steps and file list
2. `harness/tasks/active/*/handoffs/3-test.md` — if it exists (resuming)
3. `harness/learning/conventions.md` — the patterns to copy
4. **only the `harness/skills/*.md` the plan names** — not the whole folder

**Do not read `1-design.md`** — the plan already carries its conclusions.
**Do not explore the repo.** Open only files the plan names. If you need a file
it does not name, record that in the handoff as a planning gap.

If `$1` is given, resume at that step. Otherwise start at the first unfinished
step in `2-plan.md`.

If no active task exists, stop and say `/plan` must run first.

## Step 1 — Gate G0: Branch Gate  (before writing anything)

```bash
python harness/scripts/branch_gate.py --slug <slug> --rebase
```

Checks: not on `main` · branch matches the task slug · task directory exists ·
tree clean · not behind `origin/main` (rebasing if so).

If it blocks:

- on `main` → `git checkout -b feature/<slug>`, then rerun
- branch name mismatch → stop and ask
- unrelated uncommitted changes → stop and report
- rebase conflict → it aborted cleanly; resolve by hand, do not force anything

**Never write to `main`.** Record the result in the task's `## Gate Log`. If the
rebase rewrote an already-pushed branch, push with `--force-with-lease`.

## Step 2 — Test Agent (RED)

Follow `harness/agents/test-agent.md` and `harness/skills/tdd-cycle.md`.

Write the tests from `task.md`'s `## Tests First`. Then **run them and confirm
they fail for the expected reason.** A test passing before the feature exists is
broken — fix it before continuing.

Write `handoffs/3-test.md`: what was asserted, the exact commands to run them,
and the failure output confirming RED.

**Gate G2** — tests exist for every behaviour in `## Tests First`, they were run,
and they failed for the expected reason with output pasted as evidence. A test
that passes before the feature exists blocks this gate. Record in `## Gate Log`.

## Step 3 — Developer Agent (GREEN)

Follow `harness/agents/developer-agent.md`.

Work the steps in order, following the skill each step names. Run the relevant
tests after each. Implement only what the plan describes.

**Stop and report if** the plan turns out to be wrong, a file outside the plan
needs changing, or a new dependency is required. Do not silently redesign.

Write `handoffs/4-develop.md`: what was built, deviations from the plan, current
test state, and anything the Review Agent should look at closely.

**Gate G3** — all G2 tests now pass with output recorded, no files changed
outside the plan (or the deviation is recorded), no unapproved dependency, no
hardcoded portfolio content. Record in `## Gate Log`.

Append any consequential choice to the task's `## Decisions Taken`.

## Step 4 — Commit

Small conventional commits as you go, not one large commit at the end:

```
feat: <what>
test: <what>
```

## Step 5 — Report

Steps completed, test results (real output, not a claim), deviations, what
remains. Then stop. Suggest `/review`.

## Rules

- Smallest reasonable solution. No unrelated refactoring.
- No new framework, database or AI library unless the design approved it.
- Content is read from `content/*.json`, never hardcoded.
- Never report a test as passing without having run it.
