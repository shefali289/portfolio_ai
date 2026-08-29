# Handoff: Design -> Planning

## Done
Verified the repo is genuinely greenfield: `content/` holds only `.gitkeep`,
`backend/app/{api,services,rag,ai,agents,integrations}` are empty dirs,
`frontend/` is empty, and `backend/requirements.txt` is already pinned for
everything Phase 1 needs. Design is three thin slices — content schema, backend
read path, frontend render path — and nothing else.

## You need to know

1. **No new backend dependency.** `requirements.txt` already pins fastapi,
   uvicorn, pydantic, pydantic-settings, pytest, ruff. Do not add to it.
2. **Frontend deps are pre-approved by `docs/plan.md`**: Vite, React, TS,
   Tailwind, Vitest, RTL, ESLint. Resolve exact versions at install time —
   `decisions.md` records that a recalled pin turned out not to exist.
3. **Two model locations, no duplication.** The five content models live in
   `services/content_models.py` (domain); `api/schemas.py` holds only
   `HealthResponse` and `ErrorResponse`. `/api/profile` returns the domain
   `Profile` directly — never restate it as a second schema.
4. **`ContentService` loads all five files eagerly at startup**, validates via
   Pydantic, caches in memory. A malformed file fails loudly on boot, not on
   the first request.
5. **The content directory is a setting, not a relative path.** `CONTENT_DIR`
   in `config.py` defaults to repo-root `content/`. Hardcoding `../content`
   breaks depending on uvicorn's cwd, and tests need a fixture directory.
6. **THE RESUME IS NOT IN THE REPO.** Rules 16/17 forbid inventing content, so
   unless the user supplies it, all five files ship schema-correct with explicit
   `"TODO: <what is needed>"` values. See Open questions.

## Files
- `content/{profile,experience,skills,projects,engineering-notes}.json` — schema real, values TODO
- `backend/app/config.py` — pydantic-settings: `CONTENT_DIR`, `CORS_ORIGINS`
- `backend/app/services/content_models.py` — the five Pydantic content models
- `backend/app/services/content.py` — `ContentService`: eager load, validate, cache
- `backend/app/api/schemas.py` — `HealthResponse`, `ErrorResponse` only
- `backend/app/api/routes.py` — `/api/health`, `/api/profile`, both thin
- `backend/app/main.py` — app, CORS from settings, router, startup content load
- `frontend/src/lib/api.ts` — the only `fetch` in the codebase
- `frontend/src/types/content.ts` — hand-written TS mirrors of the Pydantic models
- `frontend/src/components/Profile.tsx` — name + title; loading/error/empty
- `frontend/src/App.tsx` — layout shell (header / main / footer)

## Do NOT re-read
`docs/architecture.md`, `docs/setup.md`, `docs/plan.md`, `requirements.txt`,
`.env.example`, `harness/skills/{content-extraction,api-endpoint}.md` — every
constraint they impose is captured above. Repo state is settled: greenfield.

## Open questions
**Where is the resume?** It is the declared source of truth and it is not in the
repo. Options: (a) user supplies it now → real content this phase; (b) ship
schema-correct TODO placeholders, fill later. Everything else is unblocked
either way. Recommend (a) if the file exists — Phase 2 renders these fields and
Phase 3 embeds them.

## New learnings
- `branch_gate.py`'s `BRANCH_RE` accepts a leading digit, so `feature/01-foundation` passes G0.
- Phase slugs are numbered `01-`…`06-`; the number is the run order.
