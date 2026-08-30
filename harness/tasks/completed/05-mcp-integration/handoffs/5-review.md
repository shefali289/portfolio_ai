# Handoff: Review -> Complete

## Check results

| Check | Result |
|---|---|
| backend | **PASS** — `79 passed in 4.16s`, ruff `All checks passed!` |
| frontend | **PASS** — `Tests 39 passed (39)`; eslint + `tsc --noEmit` clean |
| secrets · rule 15 | **PASS** — diff hits are comments explaining a token's *absence*; `git diff -- backend/app/rag/` empty |
| 375px | **PASS** — `scrollWidth == clientWidth`, 0 overflowing elements |
| states · keyboard | **PASS** — loading, unavailable, loaded reached live (empty unit-tested only); 6 real `<a>`, no `tabindex`, one `<h1>` |
| refusal · no provider | **PASS** — out-of-scope `grounded=false`, `live_sources: []`; `template` + lexical throughout |

## Findings

**1 · MEDIUM — the MCP `search_resume` tool bypasses the grounding guarantee**
(`integrations/tools.py`). Chat refuses an out-of-scope question; the tool
returns four sub-threshold passages for the same one:

```
"What is the capital of France?"    threshold 0.25
  search_resume -> 0.140 / 0.091 / 0.076 / 0.000   (4 returned)
  chat          -> grounded: False                  (refused)
```

Scores are returned, so a careful client *can* filter — but nothing marks them
as below the bar, and rule 18 is a project guarantee, not a per-endpoint one.
**Not blocking**: the criteria never asked the tool to enforce grounding, and a
search tool returning scored hits is defensible. Decide deliberately.

**2 · MEDIUM — a hanging GitHub adds up to 5s to a grounded answer**
(`services/ai.py::_live_sources`, inline on the answer path):
`cold 537.3 ms · warm 0.5 ms · github blackholed 5026.4 ms`. The answer stays
correct and degrades to no live sources, and the 15-minute cache confines this
to one question per window; a refused connection is instant, only a hanging
host costs the full `github_timeout_s`. **Not blocking.**

**3 · LOW — `From GitHub (live)` is a `<p class="eyebrow">`, not a heading**
(`AskPortfolio.tsx`). Heading navigation skips it; it is inside the
`aria-live` region, so the gap is navigation, not announcement.

**Carried forward, not new:** `"What Python projects has she built?"` scores
0.228 against a 0.25 threshold — pre-existing Phase 3 lexical-embedding
behaviour. The user chose to leave the threshold alone until Gemini is wired up.

## New learnings

- **Two adapters over one tool layer** — plain callables in `integrations/`,
  MCP and HTTP thin over them; a capability is written once. → architecture-map
- **A second consumer of retrieval does not inherit the first's guarantees.**
  Refusal lives in `AiService`, not `Retriever`. → gotchas
- **A tool on the answer path spends its timeout on every cache miss.** → gotchas
- **Verify a degraded path by degrading it**: pointing `GITHUB_API_BASE` at a
  dead port proved the real UI copy, which its unit test could not.

## User overrides

None. Tool reach and tool selection were put to the user at `/plan` and
accepted as designed.
