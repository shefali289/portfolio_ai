---
description: Close the active feature - gates, learning, PR, archive
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# /complete — Completion, Learning, PR

Closes the active feature. **This is where the harness learns.** Skipping it
makes every later feature more expensive, not just less documented.

## Step 0 — Load only what you need

Read exactly: the active task's `handoffs/*.md` (all five — small by design),
its `task.md`, and `harness/learning/*.md`. Nothing else.

## Step 1 — Gate G5

From `harness/QUALITY-GATES.md`: every requirement in `task.md` met, no
unresolved blocking findings in `5-review.md`. **Re-run both test suites** — do
not trust an earlier run. If anything is outstanding, stop and say what. Never
close a feature to tidy up.

## Step 2 — Completion report

Write `completion.md` from `harness/templates/completion.md`. Validation lines
record **real** results. A skipped check is `SKIPPED`, never `PASS`.

## Step 3 — Learn  ← the step that pays for itself

Walk every handoff's `## New learnings` and promote what is durable:

| Learning | Goes to |
|---|---|
| a new module, area or seam | `learning/architecture-map.md` |
| a pattern to copy | `learning/conventions.md` |
| a consequential or rejected choice | `learning/decisions.md` |
| something surprising that cost time | `learning/gotchas.md` |
| what to do differently next time | `learning/lessons-learned.md` |
| **the user reversed an agent decision** | `learning/user-overrides.md` |

**User overrides matter most** — an override means a default was wrong for this
project, and unrecorded it gets repeated. Every override entry must end in a
promoted rule; an override logged but not promoted will be made again.

Then **prune**: delete entries this feature made obsolete or that are now obvious
from the code. Superseded entries are removed, not annotated. Caps:
`architecture-map` / `conventions` / `decisions` / `gotchas` 150 lines,
`lessons-learned` 100, `user-overrides` 80. Learning that is not pruned is
learning that is not read.

Mark `(planned)` entries in `architecture-map.md` as real now they exist.

## Step 4 — Update the manifest

In `harness/AGENT-MANIFEST.md`: set this task's status to `done` with the date.
Add any new skill and name it in the agent's row. **Correct any skill whose
procedure turned out wrong** — a stale skill is copied blindly next time.

## Step 5 — Pull request

Write `pull-request.md` in the task directory from
`harness/templates/pull-request.md`, including the gate table, lessons learned
and user overrides.

Then create it:

```bash
git push -u origin feature/<slug>
gh pr create --title "<type>: <description>" --body-file <task-dir>/pull-request.md
```

**If `gh` is not installed or there is no git remote** (both currently true —
see `learning/gotchas.md`): write the file, commit it, and report the exact
commands for the user to run. Say plainly that the PR was not created. Never
claim a PR exists when it does not.

## Step 6 — Archive

```bash
git mv harness/tasks/active/<slug> harness/tasks/completed/<slug>
```

Handoffs, gate log and PR body move with it — that is the development history.

## Step 7 — Update docs if behaviour changed

README, `docs/architecture.md`, `docs/setup.md` — only if this feature changed
them.

## Step 8 — Report

- what shipped, and real validation results
- **what the harness learned** — the specific lines added and pruned
- PR status: created, or the commands to create it
- suggested commit message and next task

## Rules

- Never close with unresolved blocking findings.
- Never record a validation result that was not run.
- Never claim a PR was created when it was not.
