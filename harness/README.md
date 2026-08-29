# AI Development Harness

A repeatable AI-assisted development workflow. Five roles over one repository,
plus the files that let them hand work to each other without re-reading it.

Not a framework. Not a platform. If it ever needs its own architecture, it has
failed.

> Working here? Start at [`../AGENTS.md`](../AGENTS.md) — lifecycle, commands,
> gates and rules. This file explains how the harness is put together.

## Layout

```
harness/
├── README.md              this file - how the harness works
├── AGENT-MANIFEST.md      the human index: agents, skills, handoffs, tasks
├── HARNESS-RULES.md       the 23 non-negotiable rules
├── HANDOFF-PROTOCOL.md    how work passes between agents + read budgets
├── QUALITY-GATES.md       G0-G5 index
├── agents/                the five roles
├── skills/                reusable procedures agents follow
├── instructions/          gate policy - approval, branch, design
├── context/               current-task pointer + canonical commands
├── learning/              what the harness knows - read before exploring
├── scripts/               executable gates
├── templates/             task · completion · pull-request
└── tasks/
    ├── planned/           a brief per known task - /plan starts here
    ├── active/            exactly one, in flight
    └── completed/         task + handoffs + gates + PR = the history
```

`../.agent-manifest.json` is the machine-readable mirror. CI validates every
path in it against the filesystem, so a drifting manifest fails the build.

## The three mechanisms that keep it cheap

**Handoffs** — each stage writes a briefing under 60 lines. The next agent reads
that plus only the files it names, never the repository. Each carries a
`Do NOT re-read` section, which is what makes the saving real: without it agents
re-open settled files "to be safe" and the budget leaks silently.
See [`HANDOFF-PROTOCOL.md`](HANDOFF-PROTOCOL.md).

**Learning** — [`learning/`](learning/) is a pruned digest of how this codebase
works, written at `/complete` and read at `/plan`. Exploring a repo costs tokens
proportional to its size, per agent, per feature, forever. Reading a capped
digest is flat, and it *improves* as the project grows. This is why feature N+1
costs less than feature N.

**Skills** — [`skills/`](skills/) holds reusable procedures. Agents follow them
instead of re-deriving, which keeps the codebase consistent as well as the token
count down.

## The three that keep it honest

**Gates G0–G5** — a stage cannot start until the previous gate passes. A check
that did not run is recorded `SKIPPED`, never `PASS`.
See [`QUALITY-GATES.md`](QUALITY-GATES.md).

**Executable enforcement** — `scripts/branch_gate.py`, `scripts/health_check.py`
and `scripts/final_checklist.py` run identically locally and in CI, so green
locally means green in the pipeline. `final_checklist.py` decides whether a task
is complete: it re-runs the tests and demands real RED evidence.

**One durable record** — `tasks/<slug>/task.md` accumulates intent, design,
plan, TDD evidence, gate results, decisions, user overrides, lessons learned and
the PR summary. Handoffs are small and disposable; the task doc is the artefact.

## Lifecycle of one feature

```
/plan <slug>     planned/ -> active/, Design + Plan, G1
/build           G0 branch gate, tests RED (G2), implement GREEN (G3)
/review          gates + checklist (G4)
/complete        G5, learn, PR, active/ -> completed/
```

Same lifecycle for the six initial phases and every feature after them. The
harness does not change; only new task directories are added.
