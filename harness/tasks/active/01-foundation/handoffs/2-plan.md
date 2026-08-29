# Handoff: Planning -> Test

## Done
Eight ordered steps, back-to-front: content schema → backend RED → backend
GREEN → frontend scaffold → frontend RED → frontend GREEN → end-to-end check.
Every step is verifiable by a command. Skills are named, not restated.

## You need to know

1. **Step order is not negotiable.** Steps 2 and 6 write failing tests and must
   be run and seen RED before steps 3 and 7 implement against them. G2 requires
   the failure output pasted into `3-test.md`.
2. **Tests point at a fixture content dir**, never at real `content/`, so a
   later content edit cannot break a backend test. `CONTENT_DIR` is overridden
   in a pytest fixture — this is why it is a setting.
3. **`frontend/` is empty**, so step 4 is `npm create vite@latest` scaffolding,
   not editing. Everything before step 4 is backend-only and can be verified
   without Node running.
4. **The end-to-end proof (step 8) is the acceptance criterion**: both servers
   up, browser shows the real name and title from the API, no CORS error. That
   single check is what "Phase 1 done" means.
5. **Content values may be `TODO:` strings** pending the resume decision. The
   schema, the service, the endpoint and the render path are all testable
   against TODO values — no step is blocked by it.

## Steps
1. `content/*.json` + `services/content_models.py` — schema first (`content-extraction`)
2. RED: `backend/tests/test_content_service.py`, `test_api.py` (`tdd-cycle`)
3. `config.py`, `services/content.py` — make step 2 GREEN
4. `api/schemas.py`, `api/routes.py`, `main.py` — endpoints (`api-endpoint`)
5. Scaffold `frontend/` — Vite+React+TS+Tailwind, Vitest+RTL, ESLint
6. RED: `Profile.test.tsx` — loading, error, and rendered-name cases (`tdd-cycle`)
7. `types/content.ts`, `lib/api.ts`, `Profile.tsx`, `App.tsx` — GREEN (`react-component`)
8. Full validation: pytest, npm test, ruff, lint, tsc, both servers, browser

## Files
See `## Files Likely To Change` in `task.md` — same list, with the frontend
config files (`vite.config.ts`, `tsconfig.json`, `package.json`, `vitest.setup.ts`)
that step 5 generates.

## Do NOT re-read
`1-design.md` decisions are settled — model placement, eager loading,
`CONTENT_DIR` as a setting, no new backend deps. Do not re-derive them, and do
not re-inspect the empty `backend/app/` or `frontend/` trees.

## Open questions
Resolved. The resume was supplied and transcribed to `docs/resume.md` — that is
the source of truth for step 1, and every content value must trace to a line in
it. Two calls step 1 makes, neither of which justifies a sixth content file:
education + certifications become fields on `profile.json`; the phone number
stays in `docs/resume.md` and never enters `content/`, which is publicly served
and embedded into the RAG index.

## New learnings
None yet — Phase 1 establishes the patterns the rest of the project copies, so
`architecture-map.md` and `conventions.md` get their real entries at `/complete`.
