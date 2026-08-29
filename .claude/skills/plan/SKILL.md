---
name: plan
description: Start a feature or phase - runs Design then Planning agents, writes task.md
when_to_use: Use when starting a phase or feature: 'start phase 1', '/plan foundation', 'add feature: X'.
argument-hint: <phase number | feature description>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
disable-model-invocation: true
---

# /plan — Design + Planning

Target: **$1**

Entry point for every feature and every phase. Nothing is implemented here.

## Step 0 — Load the manifest, then memory

Read, in this order, before touching anything else:

1. `harness/AGENT-MANIFEST.md` — resolves **$1** to a task slug, branch and
   description, and lists the skills available
2. `harness/learning/architecture-map.md`
3. `harness/learning/conventions.md`
4. `harness/learning/decisions.md`
5. `harness/learning/gotchas.md`
6. `harness/HARNESS-RULES.md`

If **$1** matches a manifest slug (`foundation`, `rag-assistant`, …) or a phase
number, use that row's slug, branch and description. If it matches nothing, treat
it as a new feature: slugify it and **add a row to the manifest** so the name
resolves next time.

These replace exploring the repository. **Do not scan the codebase to work out
what exists** — memory tells you. Read source files only to verify a specific
fact memory left open, and only the files memory points you at.

If the target is a numbered phase, also read that phase's section in
`docs/plan.md`.

## Step 1 — Resolve the task directory

Look in this order:

1. `harness/tasks/active/<slug>/` — already in flight. Report progress and
   **stop**; do not regenerate the plan. Suggest `/build`.
2. `harness/tasks/completed/<slug>/` — already done. Report and stop.
3. `harness/tasks/planned/<slug>/` — **the normal case.** A brief already
   exists. `git mv` it to `active/`, create `handoffs/`, and fill it in.
4. Nothing — a new feature. Create `active/<slug>/` from
   `harness/templates/task.md`, plus `handoffs/`, and add a manifest row.

Stop and ask if another feature is already in `active/` — there is normally
exactly one.

## Step 2 — Design Agent

Follow `harness/agents/design-agent.md`. Answer its seven questions concisely.

Write `handoffs/1-design.md` using the format in `harness/HANDOFF-PROTOCOL.md`
(**under 60 lines**). Fill the `## Design` and `## Existing Components Reused`
sections of `task.md`.

If the feature adds little value or is designed wrong, say so and stop. That is
a valid outcome.

## Step 3 — Planning Agent

Follow `harness/agents/planning-agent.md`. Work from `1-design.md` — you have
already paid for that context; do not re-read source files it resolved.

Produce 4–10 verifiable steps. Name the skill each step uses
(`harness/skills/`, indexed in the manifest) rather than restating its procedure
— that is what keeps the plan short and the steps consistent.

Write `handoffs/2-plan.md` and fill the `## Implementation Steps`,
`## Files Likely To Change`, `## Tests First` and `## Out of Scope` sections of
`task.md`.

## Step 4 — Gate G1

Check `harness/QUALITY-GATES.md` G1: seven questions answered, no unjustified
new system or dependency, `1-design.md` under 60 lines. Record the result in the
task's `## Gate Log`. Append anything consequential to `## Decisions Taken`.

## Step 4b — Report

Print concisely:

- branch to create: `feature/<slug>`
- the numbered steps, each naming the skill it will use
- files that will change
- anything needing a decision from the user

Then stop. Wait for `/build`.

## Rules

- No implementation files are created or edited by this command.
- Prefer extending existing architecture over new systems.
- Never invent portfolio content — unknowns become explicit `TODO` placeholders.
