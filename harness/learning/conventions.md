# Conventions

Patterns to copy. Written as "do X", not as prose.

> Seeded from the agreed design. Confirm and correct after Phase 1.

## Content

- Portfolio data lives in `content/*.json` and is rendered from there. Never
  hardcode copy into a component.
- Every content field has a Pydantic model (backend) and a TS type (frontend),
  hand-written to match. No codegen.
- Missing information is an explicit `TODO` placeholder, never an invented value.
- Personal data intentionally excluded from public content is also excluded
  from documentation and reachable git history before any push.

## Backend

- Routers are thin: parse, call a service, return. No logic in `api/`.
- Settings come from `pydantic-settings` in `config.py`. Never read `os.environ`
  directly in a module.
- Providers are selected by env var and resolved through a factory, so adding an
  implementation never touches a call site.

## Frontend

- One API client (`lib/api.ts`). Components never call `fetch`.
- Every data-driven component handles three states: loading, error, empty.

## Tests

- RED first: write it, run it, confirm it fails for the right reason.
- Test behaviour, never styling, class names or animation timing.
- One grounding test is mandatory for every AI feature: an out-of-scope question
  must be refused, not answered.

## Naming

- Branches: `feature/<name>`, `fix/<name>`, `improvement/<name>`.
- Commits: conventional (`feat:`, `test:`, `docs:`, `chore:`).
