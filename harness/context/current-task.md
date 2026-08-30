# Current Task

Pointer to what is in flight. Maintained by `/plan` and `/complete`.

---

| | |
|---|---|
| **Active task** | Final Polish + Deploy |
| **Slug** | `06-final-polish` |
| **Phase** | 6 of 6 — the last |
| **Branch** | `feature/06-final-polish`, off `main` |
| **Stage** | rebuilt after review — G0-G3 passed, awaiting re-`/review` |
| **Task file** | `harness/tasks/active/06-final-polish/task.md` |
| **Started** | 2026-08-30 |

## Next command

```
/review
```

Rebuilt for review findings 1-3. The blocking one — `vercel.json` pinning
`@vercel/python@4.3.0`, a runtime too old to import `StrEnum` — is fixed and
now guarded by `backend/tests/test_deploy_config.py`. Backend 85/85, frontend
53/53, ruff + eslint + tsc clean, build succeeds. Commits staged, unapproved.

## Handoffs written

- `handoffs/1-design.md` — Design → Planning
- `handoffs/2-plan.md` — Planning → Test
- `handoffs/3-test.md` — Test → Developer (RED evidence)
- `handoffs/4-develop.md` — Developer → Review (rebuilt)
- `handoffs/5-review.md` — Review → Build (findings 1-3, now addressed)

## The rule this phase is built around

**Engineer Mode displays; it does not measure.** Every metric it shows is
already returned by `/api/ai/chat` and `/api/ai/job-match`. If a step seems to
need new backend instrumentation, the design is wrong — stop and report it.

And: **a missing metric omits its row.** Rendering `0.0 ms` would present a
fabricated measurement as real, which is inventing content in a different
costume.

## Gates passed

- **G0** branch — PASS, 2026-08-30
- **G1** design — PASS, 2026-08-30
- **G2** test RED — PASS, 2026-08-30
- **G3** build GREEN — PASS, 2026-08-30

## Branches

`main` is fully in sync — PRs #1–#7 all merged, all five previous phases
included. Phase 6 branches off `main`; there is no stack any more.

## Blocking — the user owns these

- **Deployment cannot be run from here.** Vercel needs their account and
  `GEMINI_API_KEY`. Config gets written and verified; the deploy criterion is
  `SKIPPED` with a reason until they run it, and is never marked `PASS`.
- **Step 8 (MCP `search_resume` grounding flag) is unapproved.** If it is still
  unanswered when `/build` reaches it, skip it and record it as owed — do not
  decide it inside `/build`.

## Owed

- **A bare skills-list mention counts as a strong job match** (Phase 4). Decide
  whether a listing should rank below a demonstrated role.
- **`GROUNDING_THRESHOLD` and `STRONG_MATCH` are tuned against lexical
  vectors.** Out of scope here; revisit once `GEMINI_API_KEY` makes retrieval
  semantic.
