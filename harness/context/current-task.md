# Current Task

Pointer to what is in flight. Maintained by `/plan` and `/complete`.

---

No task is in flight. `05-mcp-integration` completed 2026-08-30 and is archived
in `harness/tasks/completed/05-mcp-integration/`.

## Next lifecycle command

```
/plan 06-final-polish
```

**The last phase.** Engineer Mode, accessibility, mobile, README, and deploy to
Vercel. Deployment constraints already known: the Vercel Python bundle limit is
500 MB, so `requirements.txt` must stay free of ML dependencies and production
must use Gemini embeddings.

## Branches — all merged

All six PRs are merged. `main` carries every phase.

| PR | Branch | Merged into |
|---|---|---|
| #1 | `feature/01-foundation` | `main` |
| #2 | `feature/02-portfolio-ui` | `main` |
| #3 | `improvement/visual-design` | `main` |
| #4 | `feature/03-rag-assistant` | `improvement/visual-design` |
| #5 | `feature/04-agentic-job-match` | `feature/03-rag-assistant` |
| #6 | `feature/05-mcp-integration` | `feature/04-agentic-job-match` |

**#4-#6 targeted their parent branch, not `main`**, which is how a stack works
and why merging them did not advance `main` on its own. `chore/sync-task-records`
carried the collapsed stack into `main` in one integration merge.

**Branch Phase 6 off `main`.** The stack is finished; there is nothing to stack on.

## Owed — decisions the user still holds

- **The MCP `search_resume` tool does not apply the grounding threshold**
  (Phase 5, review finding 1). Chat refuses a question the tool answers with
  four sub-threshold passages. Decide whether the tool should enforce the
  threshold, return a `grounded` flag, or stay as-is.
- **A bare skills-list mention counts as a strong job match** (Phase 4 finding).
  Decide whether a listing should rank below a demonstrated role.
- **`GROUNDING_THRESHOLD` and `STRONG_MATCH` are tuned against lexical
  vectors** and unvalidated against semantic ones. The user chose to leave them
  until `GEMINI_API_KEY` is set — a genuine Phase 6 task, since moving either
  number changes behaviour for every question.
