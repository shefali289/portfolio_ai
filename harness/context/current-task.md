# Current Task

Pointer to what is in flight. Maintained by `/plan` and `/complete`.

---

No task is in flight. `04-agentic-job-match` completed 2026-08-30 and is
archived in `harness/tasks/completed/04-agentic-job-match/`.

## Next lifecycle command

```
/plan 05-mcp-integration
```

Phase 5: GitHub REST integration and an MCP server, so the assistant can reach
live repository data. **Keep RAG and tools distinct** (rule 15) — RAG retrieves
stored portfolio knowledge, MCP reaches external capability. Adding a tool must
never reshape retrieval, and the two sources stay separately attributed.

## Blocking everything downstream

**Four branches are committed but unmerged**, each stacked on the last:

```
main ── improvement/visual-design ── feature/03-rag-assistant ── feature/04-agentic-job-match
```

No PR has opened since Phase 2 because GitHub CLI is unauthenticated:

```text
gh auth login -h github.com
```

PR bodies are ready in each task's `pull-request.md`. The longer this stack
grows, the harder the eventual merge; worth clearing before Phase 5.

## Owed

- **A bare skills-list mention counts as a strong job match** (Phase 4 finding).
  Decide whether a listing should rank below a demonstrated role.
- Retrieval is lexical until `GEMINI_API_KEY` is set; both `GROUNDING_THRESHOLD`
  and `STRONG_MATCH` are tuned against lexical vectors and unvalidated against
  semantic ones.
