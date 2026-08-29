# Current Task

Pointer to what is in flight. Agents read **this** instead of scanning
`harness/tasks/` — one small file rather than a directory walk.

Maintained by `/plan` (on start) and `/complete` (on finish). If it disagrees
with `harness/tasks/active/`, the directory wins and this file is stale — fix it.

---

| | |
|---|---|
| **Active task** | Foundation |
| **Slug** | `01-foundation` |
| **Branch** | `feature/01-foundation` (created) |
| **Phase** | 1 of 6 |
| **Stage** | built — G0-G3 passed, awaiting `/review` |
| **Task file** | `harness/tasks/active/01-foundation/task.md` |
| **Started** | 2026-08-29 |

## Next command

```
/review
```

All 8 plan steps are done. Backend 14/14, frontend 5/5, ruff + eslint + tsc
clean. Commits are staged and awaiting approval — nothing is committed yet.

## Handoffs written

- `handoffs/1-design.md` — Design → Planning (58 lines)
- `handoffs/2-plan.md` — Planning → Test (52 lines)
- `handoffs/3-test.md` — Test → Developer (RED evidence)
- `handoffs/4-develop.md` — Developer → Review

## Gates passed

- **G0** branch — PASS, 2026-08-29 (tree dirty: WARN)
- **G1** design — PASS, 2026-08-29
- **G2** test RED — PASS, 2026-08-29
- **G3** build GREEN — PASS, 2026-08-29

## Open questions blocking progress

**None blocking.** The resume question is resolved — it was supplied 2026-08-29
and transcribed verbatim to [`docs/resume.md`](../../docs/resume.md). That file
is the source of truth for step 1; every value in `content/*.json` must trace to
a line in it.

Two schema calls step 1 must make (do not invent a sixth content file):

- **Education and certifications** have no obvious home in the five files.
  Fold them into `profile.json` as fields — that is where a reader and the RAG
  index will both look for them.
- **Phone number stays out of `content/`.** `profile.json` is served by the
  public API and embedded into the RAG index. Email and LinkedIn are already
  public; the phone number should not be. Keep it in `docs/resume.md` only.
