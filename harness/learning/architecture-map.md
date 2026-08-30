# Architecture Map

Where things live, and where to extend. Updated when a new area appears.

> All six phases are built. Deployment config exists and is tested; the deploy
> itself has not been run - it needs credentials the harness does not hold.

## Areas

| Path | Responsibility | Extend by |
|---|---|---|
| `content/*.json` | portfolio data, source of truth for UI **and** AI | adding a field + its Pydantic model + its TS type |
| `backend/app/api/` | HTTP only - thin routers, no logic | adding a route that calls a service |
| `backend/app/services/` | application behaviour | adding a service module |
| `backend/app/rag/` | retrieval + embedding providers | adding an `EmbeddingProvider` impl |
| `backend/app/ai/` | generation providers, prompts | adding an `AIProvider` impl |
| `backend/app/agents/` | sequential agent workflows | adding an agent module to a chain |
| `backend/app/integrations/` | external systems - GitHub, MCP | adding a callable to `tools.py` |
| `frontend/src/components/` | UI components | new component + its test |
| `frontend/src/lib/api.ts` | the single typed API client | adding a method |

## Key seams

- `ContentService` is the **only** reader of `content/`. RAG ingestion,
  API routes and MCP tools all go through it. Never open the JSON directly.
- `/api/content` is the portfolio UI boundary: one response exposes all five
  eagerly validated content models and one page owner handles request state.
- Skill evidence refs are validated by `ContentService` before the frontend
  resolves them into role/project/credential labels.
- `AIProvider` (`app/ai/provider.py`) and `EmbeddingProvider`
  (`app/rag/embeddings.py`) are **separate on purpose** — different deployment
  constraints. Each has a factory keyed by env var, and each degrades to a
  zero-config fallback (`template`, `hashing`) rather than failing.
- `AiService` (`app/services/ai.py`) owns retrieve -> ground -> generate. The
  router only parses and returns.
- **Refusal is a retrieval property**: `Retriever.is_grounded` compares the top
  score with `GROUNDING_THRESHOLD` *before* any model is called.
- The FAISS index stamps provider + dimension and refuses a mismatch; re-run
  `python -m app.rag.ingest` after any content or provider change.
- `app/agents/` is the job-match chain: `requirement -> portfolio -> evidence ->
  response`, four composed functions with `chain.py` timing each and raising
  `ChainError` on any failure. Extend by adding a function, not a framework.
- **One retriever instance** is shared: `JobMatchService` is constructed with
  `AiService.retriever`, so job match and Ask My Portfolio cannot drift apart.
- **One tool layer, two adapters.** `integrations/tools.py` holds six plain
  callables (`PortfolioTools`); `mcp_server.py` registers them and the HTTP
  router calls the same objects. A capability is written and tested once, and
  neither adapter may transform what a tool returns.
- **Refusal lives in `AiService`, not in `Retriever`.** Anything else that reads
  the retriever - the MCP `search_resume` tool included - starts ungrounded and
  must apply the threshold itself if it needs the guarantee.
- `GitHubClient` returns `RepoFetchResult(repos, reason)` and never raises: a
  supplementary section must not be able to break a page. Only successes are
  cached; the username is parsed from `content/profile.json`.
- `frontend/src/lib/api.ts` is the only place `fetch` is called.
- **Engineer Mode is a display layer, not instrumentation.** `lib/engineerMode`
  holds the toggle, `lib/engineerModeContext` the hook (split so neither file
  exports both a component and a hook), and `components/Metrics` renders only
  fields the AI responses already carry - a metric it lacks is omitted, never
  zeroed.
- `api/index.py` + `vercel.json` are the deploy surface, covered by
  `tests/test_deploy_config.py`: it fails if a Python runtime is pinned again.

## Test layout

- Backend behaviour lives in `backend/tests/`, with fixture content isolated
  from the real portfolio except for one validation test.
- Frontend component behaviour is colocated as `*.test.tsx` under `frontend/src/`.
