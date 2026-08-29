---
description: Where the active feature stands - completed steps, remaining steps, test state
allowed-tools: Read, Glob, Grep, Bash
---

# /status — Feature State

Cheap orientation. Reads state, changes nothing.

## Read

1. `harness/tasks/active/*/task.md` — the plan
2. `harness/tasks/active/*/handoffs/` — which exist tells you the stage
3. `git status --short` and `git branch --show-current`

Nothing else. Do not explore the repo or read source files.

## Infer the stage from the handoffs present

| Present | Stage | Next |
|---|---|---|
| none | not started | `/plan` |
| `1-design.md` | design done | `/plan` finishes planning |
| `2-plan.md` | planned | `/build` |
| `3-test.md` | tests RED | `/build` continues |
| `4-develop.md` | implemented | `/review` |
| `5-review.md` | reviewed | `/complete` |

## Report

- active feature and branch
- current stage
- completed steps and remaining steps from `2-plan.md`
- uncommitted changes
- the single command to run next

Keep it under 15 lines. If nothing is active, say so and list the next phase
from `docs/plan.md`.
