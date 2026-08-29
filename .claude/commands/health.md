---
description: Harness health check - learning size, gate history, drift, unused skills
allowed-tools: Read, Glob, Grep, Bash
---

# /health — Harness Health

Is the harness still working, or has it rotted? Reads state, changes nothing.
Cheap — run it between features.

## Read

`harness/learning/*.md`, `harness/AGENT-MANIFEST.md`, the task directories, and
recent `completion.md` files. **No source files.**

## Measure

```bash
wc -l harness/learning/*.md
ls harness/tasks/planned harness/tasks/active harness/tasks/completed
grep -rc "" harness/tasks/*/*/handoffs/*.md 2>/dev/null
```

### 1. Learning size vs cap

| File | Cap |
|---|---|
| `architecture-map` / `conventions` / `decisions` / `gotchas` | 150 |
| `lessons-learned` | 100 |
| `user-overrides` | 80 |

Over cap = not pruned = **not read**. That is the failure this whole design
exists to prevent.

### 2. Handoff size

Any handoff over 60 lines means a feature was too big, or an agent transcribed
instead of briefing.

### 3. Gate history

Across recent completions: gates recorded, and how many `SKIPPED`/`PARTIAL`.
A pattern of skipping the same gate means it is unenforceable — fix the gate or
drop it honestly.

### 4. Drift

- `(planned)` entries in `architecture-map.md` for things that now exist
- manifest task statuses not matching the task directories
- skills indexed but never used by any completed task
- skills used but not indexed
- tasks in `active/` numbering anything other than 0 or 1

### 5. Learning velocity

Entries added per completed feature. **Zero learnings from a real feature is a
red flag** — either `/complete` was skipped or the handoffs were empty.

### 6. Override follow-through

Every entry in `user-overrides.md` must end in a promoted rule. An override
recorded but not promoted will be repeated.

## Report

Under 25 lines:

```
Harness Health

Learning     4/6 files within cap  (gotchas 158/150 — prune)
Handoffs     avg 41 lines, max 58  OK
Gates        2 features, 12/12 recorded, 1 SKIPPED (frontend lint, Phase 1)
Drift        2 (planned) entries now real; manifest status stale for foundation
Velocity     6 learnings / feature
Overrides    2 recorded, 2 promoted  OK

Fix next: prune gotchas.md, refresh architecture-map.md
```

State what is wrong and the smallest fix. Do not fix it here.
