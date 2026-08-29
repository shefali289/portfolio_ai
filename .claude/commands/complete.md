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

## Step 1 — Gate G5: the final checklist

```bash
python harness/scripts/final_checklist.py --slug <slug>
```

**A task is not complete until this exits 0.** It re-runs the tests itself — do
not trust an earlier run — and checks TDD evidence (real RED output in
`3-test.md`), lint, typecheck, content parsing, the gate log, learning updates
and the completion docs.

Run it, fix what it reports, run it again. If anything is still outstanding,
stop and say what. Never close a feature to tidy up.

Steps 2–5 below fill in the pieces it will demand — so expect to run it once
early to see the gaps, and again at the end to confirm they are closed.

Finally, confirm by hand the checks it prints that cannot be automated: content
traces to the resume, sources cited, 375px, states reachable, keyboard.

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

The remote is `origin` → `github.com/shefali289/portfolio_ai`. `gh` is
installed; if it is not on `PATH`, use `"/c/Program Files/GitHub CLI/gh.exe"`.

**Check `gh auth status` first.** If it reports not logged in, `gh pr create`
will fail — `gh auth login` is interactive and cannot be run from here. In that
case push the branch, write the PR body, and give the user the compare URL plus
the body to paste:

```
https://github.com/shefali289/portfolio_ai/compare/main...feature/<slug>
```

Then say plainly that the PR was **not** created. **Never claim a PR exists when
it does not.**

## Step 5b — Re-run the final checklist

```bash
python harness/scripts/final_checklist.py --slug <slug>
```

It must exit 0 — with `completion.md`, `pull-request.md` and the learning
entries now in place. **Do not archive until it does.**

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
