# Conventions

Patterns to copy. Written as "do X", not as prose.

## Content

- Portfolio data lives in `content/*.json` and is rendered from there. Never
  hardcode copy into a component.
- Every content field has a Pydantic model (backend) and a TS type (frontend),
  hand-written to match. No codegen.
- Missing information is an explicit `TODO` placeholder, never an invented value.
- Personal data intentionally excluded from public content is also excluded
  from documentation and reachable git history before any push.
- Omit source-empty narrative sections and derive filter labels from existing
  content; never turn TODO authoring notes into public portfolio copy.

## Backend

- Routers are thin: parse, call a service, return. No logic in `api/`.
- Validate cross-content references during eager content loading so the API
  never serves evidence links that the UI cannot resolve.
- Settings come from `pydantic-settings` in `config.py`. Never read `os.environ`
  directly in a module.
- Providers are selected by env var and resolved through a factory, so adding an
  implementation never touches a call site.

## Frontend

- One API client (`lib/api.ts`). Components never call `fetch`.
- Style through a shared `@layer components` seam, not per-component utilities:
  a whole re-skin then becomes a one-file change and no behaviour test moves.
- Define colour as semantic vars (`--surface-*`, `--text-*`, `--accent`) over
  `@theme` palette tokens; redefine only the semantic layer per colour scheme.
- Progressive enhancement degrades **open**: put the class that hides content
  inside `@media (prefers-reduced-motion: no-preference)` so content is never
  stranded behind an observer that cannot run.
- Announce state with `aria-describedby`, not `aria-label`, when the element
  already has a good accessible name — renaming it breaks behaviour tests and
  makes the control harder to refer to.
- For an aggregate page request, the page owner handles loading/error/retry once;
  pure collection components handle their own honest empty state.

## Tests

- RED first: write it, run it, confirm it fails for the right reason.
- Test behaviour, never styling, class names or animation timing.
- Aggregate page fixtures include a non-empty item for every simple section;
  focused interaction tests supplement rather than replace render coverage.
- One grounding test is mandatory for every AI feature: an out-of-scope question
  must be refused, not answered.

## Naming

- Branches: `feature/<name>`, `fix/<name>`, `improvement/<name>`.
- Commits: conventional (`feat:`, `test:`, `docs:`, `chore:`).
