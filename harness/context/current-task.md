# Current Task

Pointer to what is in flight. Maintained by `/plan` and `/complete`.

---

No task is in flight. `06-final-polish` completed 2026-08-30 and is archived in
`harness/tasks/completed/06-final-polish/`.

**All six planned phases are built.** The product is feature-complete and
tested; what remains is running it in public.

## Next lifecycle command

```
/plan 07-deploy
```

Run the Vercel deploy and verify the live site. **Descoped from Phase 6** rather
than dropped: the deploy surface was written and tested there, but running it
needs a Vercel account and `GEMINI_API_KEY` the harness does not hold.

**Check `/api/health` on the deployed origin first.** If it 404s, the
`/api/(.*)` rewrite is not preserving the path — the one thing Phase 6 could not
verify, and the likeliest failure.

## Where the code stands

| | |
|---|---|
| Backend | 85 tests, ruff clean |
| Frontend | 53 tests (12 files), eslint + tsc clean, build succeeds |
| Branches | `main` carries phases 1-5; `feature/06-final-polish` is ahead by 3 commits |

## Owed — decisions the user still holds

- **The MCP `search_resume` tool does not apply the grounding threshold**
  (Phase 5, review finding 1). Chat refuses a question the tool answers with
  four sub-threshold passages. Decide whether the tool should enforce the
  threshold, return a `grounded` flag, or stay as-is.
- **A bare skills-list mention counts as a strong job match** (Phase 4). Decide
  whether a listing should rank below a demonstrated role.
- **Ten tap targets are under 44px at 375px**, all pre-existing. The fix touches
  `.text-link` sitewide; WCAG 2.2 SC 2.5.8 asks 24x24 with an inline-link
  exception, so this is the harness's stricter bar, not an AA failure.
- **`GROUNDING_THRESHOLD` and `STRONG_MATCH` are tuned against lexical vectors.**
  Revisit once `GEMINI_API_KEY` makes retrieval semantic - which `07-deploy`
  will be the first to exercise.
- **No screenshots in the README** - they need the deployed URL, so `07-deploy`
  unblocks them.
