# Architecture Map

Where things live, and where to extend. Updated when a new area appears.

> Phases 1–2 established the validated content pipeline, aggregate portfolio API,
> typed client, and data-driven UI. AI and integration areas remain planned.

## Areas

| Path | Responsibility | Extend by |
|---|---|---|
| `content/*.json` | portfolio data, source of truth for UI **and** AI | adding a field + its Pydantic model + its TS type |
| `backend/app/api/` | HTTP only - thin routers, no logic | adding a route that calls a service |
| `backend/app/services/` | application behaviour | adding a service module |
| `backend/app/rag/` | retrieval + embedding providers | adding an `EmbeddingProvider` impl |
| `backend/app/ai/` | generation providers, prompts | adding an `AIProvider` impl |
| `backend/app/agents/` | sequential agent workflows | adding an agent module to a chain |
| `backend/app/integrations/` | external systems - GitHub, MCP | adding an integration module |
| `frontend/src/components/` | UI components | new component + its test |
| `frontend/src/lib/api.ts` | the single typed API client | adding a method |

## Key seams

- `ContentService` is the **only** reader of `content/`. RAG ingestion,
  API routes and MCP tools all go through it. Never open the JSON directly.
- `/api/content` is the portfolio UI boundary: one response exposes all five
  eagerly validated content models and one page owner handles request state.
- Skill evidence refs are validated by `ContentService` before the frontend
  resolves them into role/project/credential labels.
- `AIProvider` and `EmbeddingProvider` are not yet built; keep them as separate
  abstractions because they have different deployment constraints. See
  `decisions.md`.
- `frontend/src/lib/api.ts` is the only place `fetch` is called.

## Test layout

- Backend behaviour lives in `backend/tests/`, with fixture content isolated
  from the real portfolio except for one validation test.
- Frontend component behaviour is colocated as `*.test.tsx` under `frontend/src/`.
