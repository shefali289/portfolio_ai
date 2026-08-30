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

## Blocking everything downstream

**Five branches are pushed but unmerged**, each stacked on the last:

```
main ── improvement/visual-design ── feature/03-rag-assistant
     ── feature/04-agentic-job-match ── feature/05-mcp-integration
```

No PR has opened since Phase 2 because GitHub CLI is unauthenticated:

```text
gh auth login -h github.com
```

PR bodies are ready in each task's `pull-request.md`. **Each PR must target its
parent branch, not `main`** — otherwise every PR shows its ancestors' commits.
Merge bottom-up. Phase 6 ends in a deploy, so this stack has to clear first.

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
