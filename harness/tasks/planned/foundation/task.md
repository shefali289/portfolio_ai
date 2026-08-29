# Task: Foundation

`/plan foundation`  ·  branch `feature/foundation`  ·  Phase 1

## Feature

Phase 1 - Foundation. A running React + TypeScript frontend, a running FastAPI
backend, the shared `content/` data extracted from the resume, and the test
tooling both sides will use for the rest of the project.

## Goal

Establish the skeleton every later phase plugs into, so that Phases 2-6 only
ever add features - never restructure. Nothing in this phase is thrown away.

## User Experience

Not user-facing yet. The developer-facing outcome:

- `npm run dev` serves the site at `localhost:5173`
- `uvicorn app.main:app --reload` serves the API at `localhost:8000`
- the page fetches `/api/profile` and renders the real name and title from
  `content/profile.json` - proving the whole stack is wired end to end
- `pytest` and `npm test` both run and pass

## Design

**1. Where does this live?** Everywhere - it creates the structure. No feature
logic beyond one profile endpoint used to prove the wiring.

**2. Reuse?** Nothing exists yet. This phase is what later phases reuse.

**3. Frontend changes?** Yes - Vite + React + TS + Tailwind + Vitest, a layout
shell (header/nav/footer), and a typed API client.

**4. Backend changes?** Yes - FastAPI app, settings via pydantic-settings, CORS,
a content-loading service, `/api/health` and `/api/profile`.

**5. AI / RAG / MCP?** No. Deliberately deferred to Phases 3-5. `config.py` does
define the `AI_PROVIDER` / `EMBEDDING_PROVIDER` settings now, so later phases add
implementations rather than rework configuration.

**6. New dependency?** Only the Phase 1 block of `backend/requirements.txt`
(FastAPI, uvicorn, pydantic, pydantic-settings, dotenv, httpx, pytest, ruff) plus
the frontend toolchain. Core requirements stay ML-free so the backend can deploy
serverless; `requirements-local.txt` is optional and local-only.

**7. Simplest implementation?** One `ContentService` that loads and caches the
JSON files from `content/`, and one router that returns them. Every later phase -
UI, RAG ingestion, agents, MCP tools - reads portfolio data through that single
service rather than opening files itself.

**Key decisions**

- `content/` sits at the repository root, not inside the backend, because both
  the API and the RAG ingestion consume it and it is the project's source of
  truth.
- Pydantic models mirror the JSON, so bad content fails loudly at startup rather
  than silently rendering blank sections.
- TypeScript types for content are written by hand to match - a codegen step is
  not worth it at this size.

**Rejected alternatives**

- Next.js - SSR/routing not needed for a single-page portfolio; Vite is faster.
- A database - the content is five small JSON files that belong in git.
- Hardcoding content in components - breaks the rule that content feeds both
  the UI and the AI.

## Existing Components Reused

None - greenfield. Establishes: `ContentService`, the API client, the layout
shell, and the test setup that all later phases build on.

## Files Likely To Change

```
content/profile.json | experience.json | skills.json | projects.json
        engineering-notes.json
backend/app/main.py, config.py
backend/app/api/routes.py, schemas.py
backend/app/services/content_service.py
backend/tests/test_health.py, test_content.py, conftest.py
backend/pyproject.toml            (ruff + pytest config)
frontend/  package.json, vite.config.ts, tsconfig.json, tailwind.config.js,
           index.html, src/main.tsx, src/App.tsx, src/index.css,
           src/lib/api.ts, src/types/content.ts,
           src/components/Layout.tsx, src/test/setup.ts
docs/setup.md
```

## Tests First

Backend (`pytest`)
- `GET /api/health` returns `200 {"status": "ok"}`
- `GET /api/profile` returns the name from `content/profile.json`
- `ContentService` loads all five files and validates them against the schemas
- `ContentService` raises a clear error on malformed/missing JSON

Frontend (`Vitest` + RTL)
- `App` renders the layout shell
- the profile section renders the name returned by a mocked API
- the loading state renders while the request is pending
- the error state renders when the API rejects

All must fail before implementation - RED first.

## Implementation Steps

1. Extract the resume into `content/*.json` (five files, real data only,
   `TODO` placeholders for anything absent from the resume).
2. Scaffold the backend: `main.py`, `config.py`, Pydantic schemas, pytest +
   ruff config. Write the failing backend tests.
3. Implement `ContentService` and the `/api/health` + `/api/profile` routes
   until backend tests pass.
4. Scaffold the frontend with Vite (react-ts), add Tailwind, Vitest and RTL.
5. Write the failing frontend tests (render, loading, error).
6. Implement the layout shell, typed API client and content types until they
   pass.
7. Run both servers together; confirm the browser renders live data from the
   API with no CORS errors.
8. Write `docs/setup.md`; run `ruff check`, `npm run lint`, `tsc --noEmit`.

## Validation

- both dev servers start clean
- browser shows the real name/title fetched from the API
- `pytest` green, `npm test` green
- lint and typecheck clean
- no secrets committed; `.env` is gitignored and `.env.example` is current

## Harness

Slug `foundation` · branch `feature/foundation` · manifest row: Phase 1.
Handoffs land in `handoffs/1-design.md` … `5-review.md`.
Skills used: `content-extraction`, `api-endpoint`, `react-component`,
`tdd-cycle`.

At `/complete`, `learning/architecture-map.md` must be updated with the real
module names — it is currently seeded with `(planned)` entries.

## Out of Scope

Full portfolio sections (Phase 2). RAG, embeddings, any LLM call (Phase 3).
Agents (Phase 4). MCP/GitHub (Phase 5). Engineer Mode, animations, deployment
(Phase 6). No styling beyond the layout shell.

## Gate Log

_(filled during the lifecycle - see `harness/QUALITY-GATES.md`)_

- G0 branch  ·  G1 design  ·  G2 test  ·  G3 build  ·  G4 review  ·  G5 done

## Decisions Taken

_(appended as the lifecycle runs: what was decided and why)_

## PR

_(written at `/complete` from `harness/templates/pull-request.md`)_
