# AI Development Harness

A repeatable AI-assisted development workflow. Six roles over one repository,
plus the files that let them hand work to each other without re-reading it.

Not a framework. Not a platform. If it ever needs its own architecture, it has
failed.

```
Design -> Plan -> Test -> Develop -> Review -> Complete
```

## Commands

| Command | Does | Gates |
|---|---|---|
| `/plan <task>` | Design + Planning | G1 |
| `/build [step]` | Test (RED) + Develop (GREEN) | G0, G2, G3 |
| `/review` | Verifies — never extends | G4 |
| `/complete` | Report, **learn**, PR, archive | G5 |
| `/status` | Where the active feature stands | — |
| `/health` | Is the harness itself still healthy | — |

`<task>` is a slug from [`AGENT-MANIFEST.md`](AGENT-MANIFEST.md) —
`/plan foundation`, `/plan rag-assistant`. Every one has a brief waiting in
`tasks/planned/`.

## What keeps it cheap

Three mechanisms, all pulling the same direction:

**Handoffs** — each stage writes a <60-line briefing. The next agent reads that
plus only the files it names, never the repository.
[`HANDOFF-PROTOCOL.md`](HANDOFF-PROTOCOL.md)

**Learning** — `learning/` is a pruned digest of how this codebase works, written
at `/complete` and read at `/plan`. This is what makes feature N+1 cheaper than
feature N instead of more expensive. [`learning/README.md`](learning/README.md)

**Skills** — `skills/` holds reusable procedures. Agents follow them instead of
re-deriving, which keeps the codebase consistent as well as the token count down.

## What keeps it honest

**Quality gates** G0–G5 — a stage cannot start until the previous gate passes,
so failure is caught where it was caused. A check that did not run is recorded
`SKIPPED`, never `PASS`. [`QUALITY-GATES.md`](QUALITY-GATES.md)

**Branch gate** G0 — never write to `main`; the branch name must match the task
slug, so task, branch and PR are traceable to each other.

**PR on completion** — every feature ends in a PR body carrying the gate table,
lessons learned and user overrides.

## Layout

```
harness/
├── README.md              this file
├── AGENT-MANIFEST.md      THE INDEX - agents, skills, handoffs, task names
├── HARNESS-RULES.md       non-negotiable rules
├── HANDOFF-PROTOCOL.md    how work passes between agents + read budgets
├── QUALITY-GATES.md       G0-G5
├── agents/                the five roles
├── skills/                reusable procedures
├── learning/              what the harness knows - read before exploring
├── templates/             task · completion · pull-request
└── tasks/
    ├── planned/           a brief per known task - /plan starts here
    ├── active/            exactly one, in flight
    └── completed/         task + handoffs + gates + PR = the history
```

## Lifecycle of one feature

```
/plan <slug>     planned/ -> active/, Design + Plan, G1
/build           G0 branch gate, tests RED (G2), implement GREEN (G3)
/review          gates + checklist (G4)
/complete        G5, learn, PR, active/ -> completed/
```

Same lifecycle for the six initial phases and for every feature after them. The
harness does not change; only new task directories are added.
