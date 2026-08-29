# Current Task

Pointer to what is in flight. Maintained by `/plan` and `/complete`.

---

No task is in flight. `visual-design` completed 2026-08-30 and is archived in
`harness/tasks/completed/visual-design/`.

## Next action

The PR for `improvement/visual-design` is **not open** — GitHub CLI is still
unauthenticated:

```text
gh auth login -h github.com
```

Body is ready at `harness/tasks/completed/visual-design/pull-request.md`.
Compare URL:
https://github.com/shefali289/portfolio_ai/compare/main...improvement/visual-design

## Next lifecycle command

```
/plan 03-rag-assistant
```

Phase 3: chunking, embeddings, FAISS, the provider abstractions, `/api/ai/chat`
and Ask My Portfolio. It builds on the design system this task established — the
`@layer components` seam and the `.provenance` motif are the hooks the AI
surfaces should reuse rather than restyle.

## Owed from this task

- A real 375px and device-contrast check in a browser (recorded SKIPPED at G4).
- Render tests for Credentials, Contact and Engineering Notes — carried over
  from Phase 2's LOW finding and still outstanding.
