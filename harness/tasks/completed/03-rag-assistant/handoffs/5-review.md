# Handoff: Review -> Completion

## Check results
| Check | Result |
|---|---|
| `pytest` | **PASS** — 27 passed |
| `ruff check .` | **PASS** — All checks passed |
| `npm test` | **PASS** — 8 files, 24 tests |
| `npm run lint` · `tsc --noEmit` | **PASS** — clean |
| secrets / keys | **PASS** — no `.env`, key or index artefact tracked |
| content traces to resume | **PASS** — all 34 skills appear verbatim in `docs/resume.md` |
| grounding (out-of-scope refused) | **PASS** — verified live, `grounded=false` + refusal |
| works with no API key | **PASS** — template + hashing fallback, verified live |
| **375px** | **PASS** — measured in-browser: `clientWidth=375 scrollWidth=375 overflow=false`, **0 elements past the boundary** |
| keyboard / labels | **PASS** — input has a label, controls are native, no images to alt |

The 375px check was outstanding across three tasks and is now closed with real
evidence. See New learnings for why it kept failing to run.

## Findings

**1 · MEDIUM — the new embedding provider was undocumented. FIXED.**
`HashingEmbeddingProvider` runs whenever `GEMINI_API_KEY` is unset — the default
developer experience — but `.env.example` and `docs/setup.md` listed only
`gemini | local`, so a developer with no key silently got lexical retrieval with
nothing explaining it. `ai-provider` step 4 requires documenting env vars; both
now describe `hashing` and what it trades away.

**2 · LOW — `GROUNDING_THRESHOLD = 0.25` is tuned against lexical vectors.**
Cosine distributions differ between hashing and semantic embeddings, and real
embeddings can score negative, so the refusal boundary is unvalidated for the
production path. *Fix:* re-check once a key is configured.

**3 · LOW — lexical retrieval mis-ranks some questions.**
"What did she do at Spark?" puts "Data & Analytics" first, though both Spark
roles are in the top 4 and the answer still draws on them. Inherent to the
fallback.

Nothing blocks completion. Finding 1 was handed back to `/build` and fixed in
this cycle; 2 and 3 are limitations of the lexical fallback, recorded for when a
key is configured.

## New learnings
- **Chrome headless has a ~500px minimum window width.** Test narrow viewports
  in a same-origin iframe and measure `scrollWidth`, or you will read your own
  cropped screenshot as a layout bug.
- Uvicorn's `--reload` watching `.venv` reloads on dependency noise and can miss
  app edits; an orphaned child can hold the port after its parent dies, so
  `Get-NetTCPConnection` reports a PID that no longer exists.
- Adding a provider is not done until `.env.example` describes it.

## User overrides
- **Show the resume, assume nothing.** The evidence/provenance layer was removed
  and the inferred `evidence` links deleted from `skills.json` — not merely
  hidden, because they were the agent's inference rather than resume facts.
  Promoted rule: the UI renders resume content only; inferred data is deleted.
- **Source chips deferred to Phase 6** rather than decided here.

## Open questions
None.
