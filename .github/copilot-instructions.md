# Copilot Instructions

This repository is developed through an AI harness. The rules are the same
whichever assistant is driving.

**Read [`AGENTS.md`](../AGENTS.md) first** — lifecycle, commands, gates and the
non-negotiable rules. This file adds only what is specific to Copilot.

## Before writing any code

1. There must be an active task in `harness/tasks/active/`. Check
   `harness/context/current-task.md`. If nothing is active, the work has not
   been planned — stop and say so.
2. Read `harness/learning/` instead of exploring the repository.
3. Read only your stage's handoff in the task's `handoffs/`, plus the files it
   names.

## Gates you must run

```bash
python harness/scripts/branch_gate.py --slug <slug> --rebase   # G0, before writing
python harness/scripts/final_checklist.py --slug <slug>         # G5, must exit 0
```

Full command list: [`harness/context/execution-commands.md`](../harness/context/execution-commands.md).

## Never commit or push without asking

Every `git commit` and every `git push`, on every branch — the feature branch
included. Stage the work, propose the message, and wait.

## Stop and ask

[`harness/instructions/approval-gate.md`](../harness/instructions/approval-gate.md)
— destructive git, anything outward-facing, a new dependency, or content not
backed by the resume.
