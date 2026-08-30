# Handoff: Planning -> Test

## Done

Ten steps: Engineer Mode first (context, panel, both surfaces), then the audits
(states, a11y), then docs and the Definition of Done, then deploy config, then
final validation. Detail in `task.md` `## Implementation Steps`.

## You need to know

1. **No backend metric may be added.** Everything Engineer Mode shows is already
   in the two AI responses. A step that seems to need new instrumentation means
   the design is wrong — stop and report it.
2. **Test the omission, not just the display.** The load-bearing case is a
   response with a metric missing: the row must not render at all. A `0.0 ms`
   row would be a fabricated measurement. Write that test before the panel.
3. **Engineer Mode defaults to OFF and persists.** Three tests: off by default,
   toggling reveals the panel, and the choice survives a remount. `localStorage`
   is unavailable in some browsers — reading it must be wrapped, and a failure
   means "off", never a crash.
4. **`vercel.json` and `api/index.py` cannot be verified by deploying.** Verify
   what is verifiable: the file parses, `api/index.py` imports the FastAPI app,
   and the committed index loads. Do **not** mark the deploy criterion PASS —
   it is `SKIPPED` with the reason until the user runs it.
5. **The MCP `search_resume` grounding fix is step 8 and is not yet approved.**
   If the user has not confirmed by then, skip it and record it as still owed —
   do not decide it inside `/build`.
6. **The Definition of Done is transcribed, not invented** — the six per-phase
   "Done when" lines from `docs/plan.md` plus the harness final checklist.

## Files

- `frontend/src/lib/engineerMode.tsx` + `.test.tsx` - new
- `frontend/src/components/Metrics.tsx` + `.test.tsx` - new
- `frontend/src/components/{AskPortfolio,JobMatch}.tsx` + their tests - modified
- `frontend/src/App.tsx` - provider + header switch
- `backend/app/integrations/tools.py` + `tests/test_tools.py` - step 8 only
- `api/index.py`, `vercel.json` - new, repo root
- `README.md`, `docs/architecture.md`, `docs/plan.md` - docs, diagram, DoD
- `.env.example` - deployed-origin CORS note

## Do NOT re-read

`1-design.md` — its conclusions are in `task.md` `## Design`. The response
shapes you need are in point 1 above.
