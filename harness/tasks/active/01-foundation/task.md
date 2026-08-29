# Task: Foundation

| | |
|---|---|
| **Slug** | `01-foundation` |
| **Branch** | `feature/01-foundation` |
| **Phase** | Phase 1 |
| **Status** | built — G0–G3 passed, awaiting `/review` |
| **Started / Completed** | 2026-08-29 / — |

> **Brief only.** `/plan 01-foundation` fills in Design, Plan and the rest. Every stage
> writes back here, so this file ends up holding the whole story. Do not
> implement from this file alone.

---

# 1 · Intent

## Feature

A running React + TypeScript frontend, a running FastAPI backend, the shared
`content/` data extracted from the resume, and the test tooling both sides use
for the rest of the project.

## Goal

Establish the skeleton every later phase plugs into, so Phases 2-6 only ever
add features - never restructure. Nothing here is thrown away.

## Acceptance Criteria

Refined at `/plan`, checked off at `/review`.

- [ ] `npm run dev` serves the site at `localhost:5173`
- [ ] `uvicorn app.main:app --reload` serves the API at `localhost:8000`
- [ ] the page fetches `/api/profile` and renders the real name and title from
      `content/profile.json` - proving the stack is wired end to end
- [ ] all five `content/*.json` files exist, parse, and contain only resume-backed
      content (unknowns as explicit `TODO`)
- [ ] `pytest` and `npm test` both run and pass
- [ ] `ruff check`, `npm run lint` and `tsc --noEmit` are clean

## User Experience

Not user-facing yet. The developer-facing outcome is both servers running and
the browser rendering live API data with no CORS errors.

## Out of Scope

Full portfolio sections (Phase 2). RAG, embeddings, any LLM call (Phase 3).
Agents (Phase 4). MCP/GitHub (Phase 5). Engineer Mode, animations, deployment
(Phase 6). No styling beyond the layout shell.

---

# 2 · Design  *(Design Agent, `/plan`)*

**1 · Where should this feature live?**
Across the three areas that already exist: `content/*.json` for data,
`backend/app/{config,services,api}` for the read path, `frontend/src` for the
render path. No new top-level directory.

**2 · Which existing components can be reused?**
None — greenfield. This phase *creates* the seams everything later reuses:
`ContentService`, `lib/api.ts`, the layout shell and both test setups.

**3 · Frontend changes?**
Yes, all of it: Vite + React + TS + Tailwind scaffold, typed API client, layout
shell, one `Profile` component, Vitest + RTL wired.

**4 · Backend changes?**
Yes: `config.py` (pydantic-settings), `services/content_models.py`,
`services/content.py`, `api/schemas.py`, `api/routes.py`, `main.py`, pytest.

**5 · AI / RAG / MCP?**
No — deliberately. `rag/`, `ai/`, `agents/`, `integrations/` stay empty until
Phase 3+. Phase 1 only guarantees the content they will later consume is loaded
and validated through one service.

**6 · New dependency?**
Backend: **none** — `requirements.txt` is already pinned and sufficient.
Frontend: the stack named in `docs/plan.md` (Vite, React, TS, Tailwind, Vitest,
RTL, ESLint), pre-approved by the phase plan. Versions get resolved at install,
never recalled.

**7 · Simplest implementation that fully satisfies the request?**
Five JSON files with real schema; one `ContentService` that eagerly loads,
validates and caches them; two thin endpoints (`/api/health`, `/api/profile`);
one React page whose `Profile` component renders name and title through the one
API client. Nothing else.

### Key technical decisions

- **Eager load at startup, not per request.** Malformed content fails the boot,
  so a broken file can never be served as a 500 halfway through a demo.
- **`CONTENT_DIR` is a setting, not a relative path.** Resolving `../content`
  from module code depends on uvicorn's cwd; a setting also lets tests point at
  a fixture directory.
- **Domain models and HTTP schemas are separate files but not duplicated.**
  `/api/profile` returns the domain `Profile`; `schemas.py` carries only
  `HealthResponse` and `ErrorResponse`.
- **Content is written schema-first.** The five files are created with the real
  field structure even where values are `TODO:` placeholders, so Phase 2 and
  Phase 3 have a stable shape to build against.

### UI / UX approach

A single page: header, main, footer. One `Profile` block showing the real name
and title fetched from `/api/profile`. Three states are mandatory and tested —
**loading** (skeleton text), **error** (a plain message plus a retry control),
**empty** (content present but fields blank/`TODO`). No styling beyond the
layout shell; visual design is Phase 2.

## Existing Components Reused

Nothing — greenfield. This phase establishes what later phases reuse:

| Seam | Reused by |
|---|---|
| `ContentService` | Phase 2 sections, Phase 3 RAG ingestion, Phase 5 MCP tools |
| `frontend/src/lib/api.ts` | every later frontend feature — the only `fetch` |
| `config.py` settings | AI/embedding provider selection from Phase 3 |
| layout shell in `App.tsx` | all Phase 2 sections |
| pytest + Vitest setup | every later test |

## Rejected Alternatives

| Alternative | Why rejected |
|---|---|
| Next.js instead of Vite | No SSR or routing need; already settled in `decisions.md` |
| Hardcode name/title in the component to "prove the stack" | Violates rule 22, and proves nothing about the API wiring |
| Serve `content/` as Vite static files | The API must be the seam — RAG and MCP read through `ContentService`, not the filesystem |
| Codegen TS types from Pydantic | Five small files; `conventions.md` calls for hand-written types |
| Lazy-load content per request | Hides a malformed file until the worst moment |
| Defer content to Phase 2 | Phase 2 renders these fields; the schema has to exist first |

---

# 3 · Plan  *(Planning Agent, `/plan`)*

## Implementation Steps

Each step is independently verifiable. Steps 2 and 6 must be seen RED before
the step that follows them.

| # | Step | Skill | Verified by |
|---|---|---|---|
| 1 | Write `content/*.json` (5 files) + `services/content_models.py` — schema first, `TODO:` for anything the resume does not supply | `content-extraction` | every file parses as JSON and validates against its model |
| 2 | **RED** — `backend/tests/test_content_service.py` and `backend/tests/test_api.py`, against a fixture content dir | `tdd-cycle` | `pytest -q` fails for the right reason; output pasted into `3-test.md` |
| 3 | `config.py` (`CONTENT_DIR`, `CORS_ORIGINS`) + `services/content.py` — eager load, validate, cache | — | `pytest -q backend/tests/test_content_service.py` GREEN |
| 4 | `api/schemas.py`, `api/routes.py`, `main.py` — `/api/health`, `/api/profile`, CORS, startup load | `api-endpoint` | `pytest -q` GREEN; `/docs` lists both endpoints |
| 5 | Scaffold `frontend/` — Vite + React + TS + Tailwind, Vitest + RTL, ESLint | — | `npm run dev` serves 5173; `npm test` runs |
| 6 | **RED** — `Profile.test.tsx`: renders name from mocked API, loading state, error state | `tdd-cycle` | `npm test` fails for the right reason |
| 7 | `types/content.ts`, `lib/api.ts`, `Profile.tsx`, `App.tsx` — layout shell + three states | `react-component` | `npm test` GREEN |
| 8 | Full validation: `pytest`, `npm test`, `ruff check`, `npm run lint`, `tsc --noEmit`, both servers, browser check | — | All green; browser shows the real name/title, no CORS error |

## Files Likely To Change

**Content**
`content/profile.json` · `experience.json` · `skills.json` · `projects.json` ·
`engineering-notes.json`

**Backend**
`backend/app/config.py` · `app/services/content_models.py` ·
`app/services/content.py` · `app/api/schemas.py` · `app/api/routes.py` ·
`app/main.py` · package `__init__.py` files ·
`backend/tests/conftest.py` · `tests/test_content_service.py` ·
`tests/test_api.py` · `backend/pyproject.toml` (pytest + ruff config)

**Frontend** (all new; step 5 generates the config)
`frontend/package.json` · `vite.config.ts` · `tsconfig.json` ·
`vitest.setup.ts` · `eslint.config.js` · `index.html` · `src/main.tsx` ·
`src/App.tsx` · `src/index.css` · `src/lib/api.ts` · `src/types/content.ts` ·
`src/components/Profile.tsx` · `src/components/Profile.test.tsx`

**Deliberately not touched:** `backend/requirements.txt` (already sufficient),
`app/rag/`, `app/ai/`, `app/agents/`, `app/integrations/` (Phase 3+).

## Skills Used

`content-extraction`, `api-endpoint`, `react-component`, `tdd-cycle`

---

# 4 · Tests  *(Test Agent, `/build`)*

## Tests First

Backend
- `GET /api/health` returns `200 {"status": "ok"}`
- `GET /api/profile` returns the name from `content/profile.json`
- `ContentService` loads all five files and validates them
- `ContentService` raises a clear error on malformed/missing JSON

Frontend
- `App` renders the layout shell
- the profile section renders the name from a mocked API
- loading state renders while the request is pending
- error state renders when the API rejects

## TDD Evidence

RED then GREEN. Tests written after the code fail G2 — the failure output is the
proof, and `final_checklist.py` checks for it.

| | |
|---|---|
| **RED - command** | `backend: .venv/Scripts/python.exe -m pytest` · `frontend: npm test` |
| **RED - failed for the right reason** | Yes. Backend: `ModuleNotFoundError: No module named 'app.main'` / `'app.services.content'`. Frontend: `Failed to resolve import "./Profile"`. Greenfield, so the absent module *is* the correct RED — no test passed before its code existed. Full output in `handoffs/3-test.md`. |
| **GREEN - result** | Backend `14 passed in 0.66s`; frontend `Test Files 1 passed (1) / Tests 5 passed (5)`. |

---

# 5 · Gates

See `harness/QUALITY-GATES.md`. `PARTIAL`/`SKIPPED` are honest; a check reported
`PASS` without running is not.

| Gate | When | Result | Date | Note |
|---|---|---|---|---|
| **G0** branch | before `/build` writes | PASS | 2026-08-29 | `feature/01-foundation`; tree dirty (WARN) — pre-existing harness WIP |
| **G1** design | Design → Plan | PASS | 2026-08-29 | 7 questions answered; no new backend dep; `1-design.md` 58 lines |
| **G2** test (RED) | Test → Develop | PASS | 2026-08-29 | 14 backend + 5 frontend RED; output in `3-test.md` |
| **G3** build (GREEN) | Develop → Review | PASS | 2026-08-29 | 19/19 green; 3 deviations recorded |
| **G4** review | Review → Complete | — | | tests · lint · typecheck · a11y |
| **G5** completion | before archive + PR | — | | `final_checklist.py` |

## Final Checklist  *(`/complete`)*

`python harness/scripts/final_checklist.py --slug 01-foundation` — must exit 0.
Paste the result table, then confirm by hand:

- [ ] content traces to the resume; no invented experience
- [ ] AI answers cite sources; out-of-scope questions refused
- [ ] works at 375px and desktop
- [ ] loading, error and empty states reachable
- [ ] keyboard navigable; images have alt text

---

# 6 · Record

## Decisions Taken

| Date | Decision | Reason |
|---|---|---|
| 2026-08-29 | Phase task slugs numbered `01-`…`06-` | User asked that the phase to run be obvious; the number is the run order, and `branch_gate.py` accepts a leading digit unchanged |
| 2026-08-29 | `ContentService` loads and validates all five files eagerly at startup | A malformed file fails the boot rather than a live request |
| 2026-08-29 | `CONTENT_DIR` is a pydantic setting, not a relative path | Independent of uvicorn's cwd; lets tests point at a fixture directory |
| 2026-08-29 | Domain content models in `services/content_models.py`, HTTP shapes in `api/schemas.py` | `/api/profile` returns the domain model — no second copy of `Profile` to drift |
| 2026-08-29 | Content written schema-first, `TODO:` where the resume is silent | Rules 16/17 — the resume is not in the repo, and nothing may be invented |
| 2026-08-29 | User supplies the resume before `/build` rather than shipping `TODO:` placeholders | Phase 2 renders these fields and Phase 3 embeds them; placeholder content would be redone twice |
| 2026-08-29 | Resume transcribed verbatim to `docs/resume.md`, not a new top-level dir | Rule 13; `docs/` already exists, and a text source is diffable and greppable where a PDF is neither |
| 2026-08-29 | Education + certifications become fields on `profile.json` | They have no home in the other four files, and a sixth content file is not justified |
| 2026-08-29 | Phone number stays in `docs/resume.md`, never in `content/` | `content/` is served by the public API and embedded into the RAG index; email and LinkedIn are already public, the phone need not be |
| 2026-08-29 | Frontend scaffold hand-written instead of `npm create vite` | The wizard cancels under a non-interactive shell; hand-writing also let Tailwind/Vitest/ESLint be wired in one pass |
| 2026-08-29 | **TypeScript pinned to 5.9.3, not the latest 7.0.2** | `typescript-eslint@8.68.0` peer-requires `typescript >=4.8.4 <6.1.0`; TS 7 would break `npm run lint`, which is a G4 gate |
| 2026-08-29 | `backend/pyproject.toml` instead of the planned `pytest.ini` | One file carries both pytest (`pythonpath=["."]`) and ruff config, rather than two |
| 2026-08-29 | Vite dev-server proxies `/api` to `localhost:8000` | Browser talks to one origin in dev; CORS stays configured and tested server-side rather than being worked around |
| 2026-08-29 | `extra="forbid"` on every content model | A typo'd key fails validation at startup instead of silently rendering an empty section |
| 2026-08-29 | `Annotated[…, Depends(…)]` alias rather than a `Depends()` default | ruff B008 flags the default-arg form; the Annotated alias is FastAPI's current idiom, so no per-line ignore is needed |

## User Overrides

Every entry must end in a promoted rule. Promoted to
`harness/learning/user-overrides.md` at `/complete`.

| Date | Agent proposed | User chose | Why | Rule now |
|---|---|---|---|---|
| 2026-08-29 | `/plan` ended with "Then stop. Wait for `/build`." — every stage dead-stopped and told the user which command to type next | Stages must hand off automatically, or at minimum ask; all phases chain | The human was acting as the message bus between stages that already know what follows them, paid on every stage of every phase | New rule 4b + `harness/instructions/stage-handoff.md`; all four lifecycle skills end with a Hand off step that asks and continues on yes |

## Lessons Learned

- **Worked:**
- **Cost time:**
- **Do differently:**

## Known Limitations

_(filled at `/complete`)_

---

# 7 · Validation & PR  *(`/complete`)*

## Validation

Real results only. Not run = `SKIPPED`, never `PASS`.

| Check | Result |
|---|---|
| backend tests | **PASS** — `14 passed in 0.66s` |
| frontend tests | **PASS** — `Test Files 1 passed (1)`, `Tests 5 passed (5)` |
| lint | **PASS** — `ruff: All checks passed!`; `eslint: clean` |
| typecheck | **PASS** — `tsc --noEmit` clean |
| manual check | **PARTIAL** — both servers started; `curl localhost:8000/api/profile` and the Vite proxy at `localhost:5173/api/profile` both return "Shefali Sharma" / "AI Engineer". Visual browser confirmation at 375px and desktop not performed — left for `/review`. |

Both dev servers start clean; the browser shows the real name/title fetched from
the API; no secrets committed and `.env` is gitignored.

## PR Summary

| | |
|---|---|
| **Title** | — |
| **URL** | — |
| **Merged** | — |

**What it adds:** —

**Why:** —

## Suggested Commit Message

```
<type>: <description>
```
