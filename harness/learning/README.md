# Harness Learning

What the harness knows. Written at `/complete`, read at `/plan`.

## How learning works

```
   /plan  ──reads──>  learning/  <──writes──  /complete
     │                                             ▲
     ▼                                             │
  Design ─> Plan ─> Test ─> Develop ─> Review ──────┘
                  each handoff carries "New learnings"
```

1. During a feature, each agent notes anything non-obvious in its handoff's
   `## New learnings` — a line or two, not a report.
2. At `/complete`, those lines are **promoted** into the right file below,
   and obsolete entries are **pruned**.
3. At the next `/plan`, the Design Agent reads these files **instead of
   exploring the repository**.

That third step is the point. Exploring costs tokens proportional to repo size,
every feature, forever. Reading a pruned digest is flat — and it improves as the
project grows rather than degrading.

## Files

| File | Holds | Cap |
|---|---|---|
| `architecture-map.md` | where things live, seams to extend | 150 |
| `conventions.md` | patterns to copy | 150 |
| `decisions.md` | choices made and rejected, with reasons | 150 |
| `gotchas.md` | what broke, why, and the fix | 150 |
| `lessons-learned.md` | per feature: what to do differently | 100 |
| `user-overrides.md` | where the user corrected the harness | 80 |

## The rule

**Read learning before exploring. Explore only what it does not cover.**

A Design Agent that opens twelve files to answer a question already in
`architecture-map.md` has failed, even if its design is correct.

## Quality bar

- **Stay under cap.** Over cap means unpruned, which means unread. `/health`
  checks this.
- **One line per entry** wherever possible.
- **Non-obvious only.** If a filename shows it, leave it out.
- **Correct beats complete.** A wrong entry is worse than a missing one — it is
  trusted without checking.
- **Delete, do not annotate.** Superseded entries are removed.
- **Every override ends in a promoted rule.** Otherwise it will be repeated.

## Never put here

File listings, function signatures, dependency versions, or restatements of
`HARNESS-RULES.md`. Learning captures what a competent engineer would only pick
up by *working* in this codebase.
