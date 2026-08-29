# Architecture Map

Where things live, and where to extend. Updated when a new area appears.

> Seeded before Phase 1. Entries marked `(planned)` are not built yet - the
> Design Agent must verify before relying on them.

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

- `ContentService` (planned) is the **only** reader of `content/`. RAG ingestion,
  API routes and MCP tools all go through it. Never open the JSON directly.
- `AIProvider` and `EmbeddingProvider` (planned) are separate abstractions on
  purpose - they have different deployment constraints. See `decisions.md`.
- `frontend/src/lib/api.ts` (planned) is the only place `fetch` is called.

## Not yet established

Phase 1 has not run. After it completes, this file should name the real modules,
their entry points, and the actual test layout.
