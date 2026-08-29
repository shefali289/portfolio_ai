# Handoff Protocol

## The problem this solves

Naively, each agent in the lifecycle re-reads the repository to work out what
exists. Five agents × a growing codebase means the same context is paid for five
times per feature, and again for every future feature. Cost grows with
repo size × number of agents × number of features.

The fix: **agents pass forward a distilled handoff, not the repository.** Each
agent reads a small handoff from the one before it, plus only the files that
handoff explicitly names.

```
Design ──1-design.md──> Plan ──2-plan.md──> Test ──3-test.md──> Develop
                                                                   │
                                                            4-develop.md
                                                                   │
                                                                   ▼
                            memory/ <──5-review.md── Review
```

Only the **Design Agent** is allowed to explore broadly - and even it starts from
`harness/learning/`, not from a blind scan. Every later agent is on a read budget.

## Read budgets

| Agent | May read | Must NOT read |
|---|---|---|
| **Design** | `harness/learning/*`, `task.md`, files memory points it at | the whole repo - memory first, targeted reads only |
| **Planning** | `1-design.md`, `harness/learning/architecture-map.md` | source files - the design already resolved them |
| **Test** | `2-plan.md`, `harness/learning/conventions.md`, existing test files it extends | implementation source - it is writing tests first |
| **Developer** | `2-plan.md`, `3-test.md`, `learning/conventions.md`, the exact files the plan names | anything outside the plan's file list |
| **Review** | `4-develop.md`, `task.md`, the diff | files unchanged by this feature |

If an agent believes it needs something outside its budget, it says so in its
handoff rather than reading silently. That surfaces a bad plan instead of hiding
it behind extra tokens.

## Handoff format

Every handoff is **under 60 lines**. It is a briefing, not a transcript. If it
grows past that, the feature is too big - split it.

```markdown
# Handoff: <stage> -> <next stage>

## Done
Two or three lines. What this stage actually produced.

## You need to know
The 3-6 facts the next agent cannot proceed without. Decisions, constraints,
signatures, names. No narrative.

## Files
- path/to/file.py - what it now contains / what to do with it

## Do NOT re-read
What the next agent can safely skip because it is captured above.

## Open questions
Anything unresolved. Empty is a valid and good answer.

## New learnings
Anything worth promoting to harness/learning/ at completion. Empty is fine.
```

## Why `Do NOT re-read` matters

It is the instruction that makes the saving real. Without it an agent will
re-open files "to be safe" and the budget is silently spent. Naming what is
already settled gives the next agent explicit permission to skip it.

## Where handoffs live

```
harness/tasks/active/<feature>/handoffs/
    1-design.md
    2-plan.md
    3-test.md
    4-develop.md
    5-review.md
```

They move to `completed/` with the task. They are the record of *how* a feature
was reasoned about, which is far more useful in an interview than the diff.

## Lifecycle to command mapping

| Command | Stages | Handoffs written |
|---|---|---|
| `/plan` | Design -> Planning | `1-design.md`, `2-plan.md` |
| `/build` | Test -> Developer | `3-test.md`, `4-develop.md` |
| `/review` | Review | `5-review.md` |
| `/complete` | Completion | `completion.md` + memory update |
