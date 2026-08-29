# AGENTS.md

Entry point for any coding agent working in this repository, in the
[agents.md](https://agents.md) convention. Claude Code reads `CLAUDE.md`;
GitHub Copilot reads `.github/copilot-instructions.md`; both defer here.

## The one rule

**No implementation without an active task.** All work goes through the harness
in [`harness/`](harness/):

```
Design -> Plan -> Test -> Develop -> Review -> Complete
  G1      G1     G0,G2      G3        G4        G5
```

| Command | Does |
|---|---|
| `/plan <slug>` | Design + Planning -> `task.md`, handoffs 1-2 |
| `/build` | Test RED + Develop GREEN -> handoffs 3-4 |
| `/review` | Verifies only, never extends -> handoff 5 |
| `/complete` | Report, learn, PR, archive |
| `/status` · `/health` | Where things stand · whether the harness has rotted |

Task slugs: `foundation`, `portfolio-ui`, `rag-assistant`, `agentic-job-match`,
`mcp-integration`, `final-polish`. Each has a brief in `harness/tasks/planned/`.

## Before you explore

Read [`harness/learning/`](harness/learning/) — a maintained digest of how this
codebase works — **instead of scanning the repo**. Explore only what it does not
cover. It is written at `/complete` and read at `/plan`, which is what keeps
each feature cheaper than the last.

Then read only your stage's handoff and the files it names. Read budgets:
[`harness/HANDOFF-PROTOCOL.md`](harness/HANDOFF-PROTOCOL.md).

## Machine-readable index

[`.agent-manifest.json`](.agent-manifest.json) — agents, skills, gates, scripts,
paths, limits and tasks. CI validates every path in it against the filesystem.

## Gates

| Gate | Blocks on | Enforced by |
|---|---|---|
| G0 branch | on `main`, or branch != task slug | `harness/scripts/branch_gate.py` |
| G1 design | unanswered questions, unjustified dependency | `harness/instructions/design-gate.md` |
| G2 test | tests that did not fail for the right reason | `harness/skills/tdd-cycle.md` |
| G3 build | unplanned file changes, hardcoded content | `harness/skills/tdd-cycle.md` |
| G4 review | failing tests, lint, typecheck, a11y | `.github/workflows/pr-checklist.yml` |
| G5 done | unmet criteria, unpruned learning, missing PR | `harness/scripts/final_checklist.py` |

## Non-negotiables

- **Never write to `main`.** Branch `feature/<slug>` matching the task.
- **The resume is the source of truth.** Never invent experience, employers,
  dates, metrics or skills. Unknowns are explicit `TODO` placeholders.
- **The AI must never claim experience absent from `content/`.**
- **RED first** — write the test, run it, confirm it fails for the right reason.
- **Never report a check as passing without running it.** Not run = `SKIPPED`.
- **Never claim a PR was created when it was not.**
- **Stop and ask** when `harness/instructions/approval-gate.md` says to.

## Commands

```bash
python harness/scripts/branch_gate.py --slug <slug> --rebase   # G0
python harness/scripts/health_check.py                          # harness health
python harness/scripts/final_checklist.py --slug <slug>         # G5
```

Full list: [`harness/context/execution-commands.md`](harness/context/execution-commands.md).
