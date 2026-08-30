# Current Task

Pointer to what is in flight. Maintained by `/plan` and `/complete`.

---

| | |
|---|---|
| **Active task** | MCP + GitHub Context |
| **Slug** | `05-mcp-integration` |
| **Phase** | 5 of 6 |
| **Branch** | `feature/05-mcp-integration` (fifth in the stack, off `feature/04-agentic-job-match`) |
| **Stage** | built — G0-G3 passed, awaiting `/review` |
| **Task file** | `harness/tasks/active/05-mcp-integration/task.md` |
| **Started** | 2026-08-30 |

## Next command

```
/review
```

All 9 steps done. Backend 79/79, frontend 39/39, ruff + eslint + tsc clean.
Verified live against the real account: 6 repos render, `Python projects`
returns portfolio evidence *and* two live repos separately attributed, and an
out-of-scope question still refuses. Commits staged and unapproved.

## Handoffs written

- `handoffs/1-design.md` — Design → Planning
- `handoffs/2-plan.md` — Planning → Test
- `handoffs/3-test.md` — Test → Developer (RED evidence)
- `handoffs/4-develop.md` — Developer → Review

## The rule this phase is built around

**Rule 15 — a tool never reshapes RAG.** No repo text enters the index,
`backend/app/rag/` is not touched, and live GitHub results only *supplement* an
already-grounded answer. An ungrounded question is still refused. The existing
refusal test must pass unchanged; that is the evidence.

## Gates passed

- **G0** branch — PASS, 2026-08-30
- **G1** design — PASS, 2026-08-30
- **G2** test RED — PASS, 2026-08-30
- **G3** build GREEN — PASS, 2026-08-30

## Raised for the user

**The brief's own demo question is refused.** `"What Python projects has she
built?"` scores 0.228 against `GROUNDING_THRESHOLD = 0.25`; `"Python projects"`
scores 0.322 and works. A pre-existing Phase 3 lexical-embedding limitation,
not caused by this phase, and unfixable here without touching `rag/`.

## Owed

- **A bare skills-list mention counts as a strong job match** (Phase 4 finding).
  Decide whether a listing should rank below a demonstrated role.
- Retrieval is lexical until `GEMINI_API_KEY` is set; both `GROUNDING_THRESHOLD`
  and `STRONG_MATCH` are tuned against lexical vectors and unvalidated against
  semantic ones.
- **Four branches are pushed but unmerged**, each stacked on the last:
  `main ── improvement/visual-design ── feature/03-rag-assistant ──
  feature/04-agentic-job-match`. PR bodies are ready in each task's
  `pull-request.md`; `gh auth login -h github.com` is still needed to open them.
