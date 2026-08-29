# Handoff: Developer -> Review

## Done
All 8 plan steps. Backend 14/14, frontend 5/5, ruff + eslint + tsc clean. Both
servers run and the browser path is proven: `content/profile.json` ->
`ContentService` -> FastAPI -> Vite proxy -> `api.ts` -> `Profile`. Live
`/api/profile` returns "Shefali Sharma" / "AI Engineer".

## You need to know

1. **Three deviations from the plan**, all recorded in `## Decisions Taken`:
   `npm create vite` cancelled under a non-interactive shell, so the scaffold was
   hand-written; **TypeScript is 5.9.3, not the latest 7.0.2**, because
   `typescript-eslint@8` requires `<6.1.0` and TS 7 would break the lint gate;
   `pyproject.toml` replaced the planned `pytest.ini` and carries ruff config too.
2. **`vite.config.ts` proxies `/api` to `localhost:8000`.** Not in the plan.
   It means the browser talks to one origin in dev; CORS is still configured
   server-side and still tested.
3. **Two grounding tests exist and must not be weakened.**
   `test_skills_carry_evidence_or_an_explicit_todo` (every skill has evidence or
   a TODO) and `test_profile_does_not_expose_a_phone_number`, mirrored on the
   frontend by a regex assertion that no phone-shaped string renders.
4. **Content carries 21 explicit TODOs** — 19 skills the resume lists without
   ever showing them in use, 1 Heroku demo link to re-verify, and 3 empty
   narrative sections in `engineering-notes.json`. All deliberate; none invented.
5. **`extra="forbid"` on every content model.** A typo'd key in a content file
   fails validation at startup instead of silently rendering an empty section.

## Files
- `content/*.json` — five files, all resume-traceable
- `backend/app/{config,main}.py`, `app/api/{routes,schemas}.py`, `app/services/{content,content_models}.py`
- `backend/tests/{conftest,test_content_service,test_api}.py`, `backend/pyproject.toml`
- `frontend/src/{App,main}.tsx`, `src/components/Profile{,.test}.tsx`, `src/lib/api.ts`, `src/types/content.ts`
- `frontend/{package.json,vite.config.ts,tsconfig.json,eslint.config.js,vitest.setup.ts,index.html}`

## Look at closely
- **`Profile.tsx` retry path.** `load()` deliberately does *not* setState
  synchronously (react-hooks/set-state-in-effect); `retry()` sets loading from
  the click handler instead. Verify the retry actually re-renders loading.
- **`skills.json` evidence refs are unvalidated strings** — `ref: "role-1"` is
  not checked against `experience.json` ids. Phase 2 will need that check.

## Do NOT re-read
`1-design.md`, `2-plan.md`, `3-test.md` — conclusions are captured here.
`backend/requirements.txt` is untouched and no backend dependency was added.

## Open questions
None blocking. The 21 TODOs are content gaps for a later pass, not defects.

## New learnings
- `uv venv` needs `--python 3.14` here; bare `uv venv` picks a uv-managed 3.11
  and `numpy==2.5.2` then fails to resolve.
- `npm create vite` cancels under a non-interactive shell — hand-write the
  scaffold instead of expecting the wizard.
- Latest is not always installable: `typescript-eslint@8` caps TypeScript below
  6.1.0, so TS 7.0.2 was rejected. Check peer ranges before pinning a major.
- `ruff` B008 flags FastAPI's `Depends()` default-arg form; the `Annotated`
  alias is the clean fix, not a per-line ignore.
- `health_check.py` walked into `backend/.venv` and failed on vendored
  Markdown; it now skips dependency and cache directories.
