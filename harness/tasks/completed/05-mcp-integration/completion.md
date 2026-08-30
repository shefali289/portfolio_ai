# Feature Completion

## Feature

MCP + GitHub Context — `05-mcp-integration`

## What Was Added

A public GitHub REST client, six portfolio tools exposed over **both** MCP and
HTTP, a From My GitHub section, and live repository data attached to grounded
answers as separately-attributed evidence.

The phase exists to show the difference between RAG and tools — stored knowledge
versus live external capability — and that one question can draw on both without
either being mistaken for the other.

## Main Files Changed

- `backend/app/integrations/github.py` — client, TTL cache, `repos_matching`
- `backend/app/integrations/tools.py` — `PortfolioTools`, the six callables
- `backend/app/integrations/mcp_server.py` — MCP registration, stdio entry point
- `backend/app/services/ai.py` — live sources on the grounded answer path only
- `backend/app/api/{routes,schemas}.py` — `GET /api/github/repos`, `LiveSource`
- `frontend/src/components/GitHubProjects.tsx` — the new section
- `frontend/src/components/AskPortfolio.tsx` — the separated live block
- `.env.example` — replaced two settings that never existed with the four real ones

## Tests

- `test_github.py` (17) — parsing, fork exclusion, recency, cap, four failure
  modes, cache hit/expiry/failure-not-cached, and five matcher cases
- `test_tools.py` (10) — six tools resolve and return content, not invention
- `test_mcp_server.py` (4) — exactly six tools, all described, payloads match
  the underlying functions
- `test_ai_chat.py` (+4) — combined attribution, refusal keeps `live_sources: []`,
  unrelated question attaches nothing, chat survives GitHub being down
- `test_api.py` (+2) — the route returns 200 with a reason when unavailable
- `GitHubProjects.test.tsx` (7) — loaded, loading, unavailable, empty
- `AskPortfolio.test.tsx` (+2) — live block present when attached, absent when not

## Validation

| Check | Result |
|---|---|
| backend tests | **PASS** — `79 passed` |
| frontend tests | **PASS** — `Test Files 10 passed (10)`, `Tests 39 passed (39)` |
| lint | **PASS** — ruff and eslint clean |
| typecheck | **PASS** — `tsc --noEmit` clean |
| manual check | **PASS** — see below |

Manual, against the real account and in a real browser: 6 repos render;
`Python projects` returns portfolio evidence **and** `portfolio_ai` +
`agentic-ai` under a separate heading; `What is the capital of France?` still
refuses with `live_sources: []`. Degradation was proved by pointing
`GITHUB_API_BASE` at a dead port — honest message, fallback link from content,
no `role="alert"`, zero invented cards. 375px measured in a same-origin iframe:
`scrollWidth == clientWidth`, 0 overflowing elements.

## Gates

| Gate | Result |
|---|---|
| G0 branch | PASS — 3 passed, 1 warn (plan artefacts uncommitted at the time) |
| G1 design | PASS — 7 questions answered, no new dependency |
| G2 test (RED) | PASS — `ModuleNotFoundError: app.integrations.github`; two absence-guard tests declared as unable to be RED |
| G3 build (GREEN) | PASS — 79 / 39, `git diff -- backend/app/rag/` empty |
| G4 review | PASS — 3 findings, none blocking |
| G5 completion | PASS — `final_checklist.py` exits 0 |

## Design Decisions

- **One tool layer, two adapters.** Six plain callables; MCP and HTTP both thin
  over them. The capability is written and tested once.
- **Live data supplements a grounded answer, never rescues an ungrounded one.**
  Rule 15 applied to refusal: a tool must not widen what the assistant answers.
- **Deterministic tool selection, not LLM tool-calling.** Matching on a repo's
  language, topics and name parts keeps the feature working with `template` and
  no API key, and keeps the RAG-vs-tool distinction visible.
- **Repos ranked by recency, never curated.** A hand-picked list would be
  portfolio content the resume does not support. Forks excluded as others' work.
- **No new dependency** — `mcp` and `httpx` were already pinned, and verified
  installed on Python 3.14.7 before the design relied on them.

## Lessons Learned

- **Worked:** one tool layer with two thin adapters — the MCP surface needed
  four tests rather than a subprocess, and the HTTP route was three lines.
- **Cost time:** nothing structural. Handoffs breached the 60-line cap three
  times; rephrasing does not shorten a file, only cutting content does.
- **Do differently:** check every mock of a module before growing its exports.
  `App.test.tsx` mocked `lib/api` and broke the moment a component imported a
  new function from it.

## User Overrides

None. Tool reach and tool selection were both put to the user at `/plan` and
accepted as designed. The user separately chose to leave `GROUNDING_THRESHOLD`
alone until Gemini embeddings are wired up, rather than retune it against
lexical vectors that are a fallback — recorded as a Phase 6 candidate, not an
override of an agent decision.

## Learning Updated

- `architecture-map.md` — header now says Phases 1–5 are built; `integrations/`
  extended by adding a callable; three new seams (one tool layer / two adapters,
  refusal lives in `AiService`, `GitHubClient` never raises)
- `conventions.md` — tools as plain callables, deterministic selection,
  reason-not-exception with successes-only caching
- `decisions.md` — new `2026-08-30 - MCP + GitHub` section, five decisions
- `gotchas.md` — `## AI behaviour` filled for the first time: four entries
- `lessons-learned.md` — `## 05-mcp-integration`

## Known Limitations

- **The MCP `search_resume` tool does not apply the grounding threshold** —
  chat refuses a question the tool answers with four sub-threshold passages.
  Scores are returned, but nothing marks them as below the bar. Review finding 1.
- **A hanging GitHub adds up to 5s to a grounded answer**, once per 15-minute
  cache window. Review finding 2.
- **`From GitHub (live)` is not a heading**, so heading navigation skips it.
  It is announced via `aria-live`. Review finding 3.
- **Conversational phrasings are refused under lexical embeddings** — a
  pre-existing Phase 3 limitation, resolved once `GEMINI_API_KEY` is set.
- Authenticated GitHub, write operations, README ingestion and streaming are
  out of scope by design.

## PR

**Not created** — `gh` is unauthenticated. Branch is pushed. To open it:

```bash
gh auth login -h github.com
gh pr create --base feature/04-agentic-job-match \
  --title "feat: github integration and a portfolio MCP server" \
  --body-file harness/tasks/completed/05-mcp-integration/pull-request.md
```

Compare URL:
https://github.com/shefali289/portfolio_ai/compare/feature/04-agentic-job-match...feature/05-mcp-integration

## Suggested Commit Message

```
docs(harness): complete and archive 05-mcp-integration
```
