# Approval Gate

When the harness **stops and asks** instead of deciding.

An agent that asks about everything is useless; one that never asks is
dangerous. This is the line.

## Always stop and ask

- **Destructive or irreversible git**: force-push, history rewrite, `reset
  --hard` on shared work, deleting a branch with unmerged commits, `git clean`.
- **Anything outward-facing**: opening or merging a PR, pushing to `main`,
  deploying, publishing, or sending data to an external service.
- **A new dependency, framework, database or AI library** not approved in the
  design. Default answer is no — see `HARNESS-RULES.md` rule 19.
- **A new top-level directory or parallel system.** Almost always a design
  error; re-examine before proposing.
- **Content not backed by the resume.** Never invent to fill a gap — mark
  `TODO` and ask.
- **Anything costing money**, or committing to a paid tier.
- **Deleting or overwriting** a file the agent did not create in this task.
- **A gate that cannot pass** for a reason the task did not anticipate. Report
  it; do not relax the gate to go green.

## Decide without asking

- Anything the approved `task.md` already describes.
- Ordinary edits inside the plan's file list.
- Running tests, lint, typecheck, the gate scripts.
- Local commits on the feature branch.
- Naming, structure and style choices inside an approved step.

## How to ask

State the decision, the options, and a recommendation — then stop. Do not
proceed on a "probably fine". One clear question beats three rounds of
clarification.

## After an override

If the user chooses differently, that is an **override**: record it in the
task's `## User Overrides` table and promote it to
`harness/learning/user-overrides.md` at `/complete`. An override that is not
promoted will be made again.
