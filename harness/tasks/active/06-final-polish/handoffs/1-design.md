# Handoff: Design -> Planning

## Done

Engineer Mode designed as a **display-only** feature: every metric it shows is
already returned by the Phase 3-5 endpoints. No new measurement, no new
dependency.

## You need to know

1. **Every metric already exists.** `/api/ai/chat` returns `retrieval_ms`,
   `generation_ms`, `provider`, `sources[]`, `live_sources[]`;
   `/api/ai/job-match` returns `steps[].ms`, `steps[].label`, `provider`.
   "Chunks retrieved" is `sources.length`; "tool used" is `live_sources`.
   **If a step seems to need a new backend metric, the design is wrong — stop.**
2. **A missing metric is omitted, never shown as zero.** `0.0 ms` presented as a
   measurement is a lie; the row simply does not render. That is the criterion
   "a response missing metrics degrades gracefully".
3. **One toggle, not two.** `decisions.md` deferred the theme toggle to this
   phase. Recommendation: **do not add one** — `prefers-color-scheme` already
   honours the OS choice and two header controls is clutter. Decision closed.
4. **The Definition of Done does not exist as a checklist.** `docs/plan.md`
   promises one and the brief's criteria depend on it. It is the union of the
   six per-phase "Done when" lines plus the harness final checklist — write
   those into `docs/plan.md`; **do not invent new criteria.**
5. **Deployment execution is blocked on the user** — Vercel needs their account
   and `GEMINI_API_KEY`. Config can be written and verified locally; the deploy
   cannot. That acceptance criterion stays open until they run it.
6. **`GROUNDING_THRESHOLD` is finally touchable here**, but only revisit it if
   `GEMINI_API_KEY` is set — it is tuned against a lexical fallback.

## Design decisions

- **A React context holding one boolean, persisted to `localStorage`** — the
  toggle is global, the panel per-response; rejected prop-drilling.
- **`api/index.py` + `vercel.json` at repo root** — Vercel requires that
  location; the one justified new top-level path.
- **Mermaid in Markdown for the diagram** — renders on GitHub, diffs in git.

## Rejected alternatives

New instrumentation (all already measured); a theme toggle (see 3); streaming
metrics or a debug endpoint (a second transport for one panel); an exported
PNG diagram; large committed screenshots.

## UI/UX

A single `Engineer Mode` switch in the header, off by default and remembered.
When on, each AI response grows a compact metrics panel: endpoint, chunks,
both timings, provider, tool used; Job Match adds its four steps with ms.

## Files

`frontend/src/lib/engineerMode.tsx` (context), `components/Metrics.tsx` (panel),
`components/{AskPortfolio,JobMatch}.tsx` (render it), `api/index.py` and
`vercel.json` (new, root), `README.md`, `docs/{architecture,plan}.md`.

## Do NOT re-read

`api/schemas.py`, `agents/base.py`, `services/ai.py`, `docs/deployment.md` - see points 1 and 5.
