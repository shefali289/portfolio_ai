# Current Task

Pointer to what is in flight. Maintained by `/plan` and `/complete`.

---

| | |
|---|---|
| **Active task** | RAG Assistant — Ask My Portfolio |
| **Slug** | `03-rag-assistant` |
| **Branch** | `feature/03-rag-assistant` (stacked on unmerged `improvement/visual-design`) |
| **Phase** | 3 of 6 |
| **Stage** | built — G0-G3 passed, awaiting `/review` |
| **Task file** | `harness/tasks/active/03-rag-assistant/task.md` |
| **Started** | 2026-08-30 |

## Next command

```
/review
```

All 10 steps done. Backend 27/27, frontend 24/24, lint + tsc clean. Verified
live: a grounded question answers with timings, an out-of-scope one is refused.
Commits staged and unapproved.

## Handoffs written

- `handoffs/1-design.md` — Design → Planning
- `handoffs/2-plan.md` — Planning → Test
- `handoffs/3-test.md` — Test → Developer (RED evidence)
- `handoffs/4-develop.md` — Developer → Review

## Gates passed

- **G0** branch — PASS, 2026-08-30
- **G1** design — PASS, 2026-08-30
- **G2** test RED — PASS, 2026-08-30
- **G3** build GREEN — PASS, 2026-08-30

## Open questions

**None.** Source chips are hidden and the decision is **deferred to Phase 6**,
where Engineer Mode surfaces retrieval internals anyway. The API still returns
`sources`; only `AskPortfolio.tsx` omits them, so it is a few lines to reverse.

## Carried over

- `improvement/visual-design` is committed but **its PR is not open** — `gh` is
  unauthenticated. Body ready at `harness/tasks/completed/visual-design/pull-request.md`.
- A real 375px browser check is still owed. Chrome headless clamps its window to
  a 500px minimum on this machine, so `--window-size=375` silently renders at
  500 and crops — do not read that crop as horizontal overflow.
