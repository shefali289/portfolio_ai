# Conventions

Patterns to copy. Written as "do X", not as prose.

## Content

- Portfolio data lives in `content/*.json` and is rendered from there. Never
  hardcode copy into a component.
- Every content field has a Pydantic model (backend) and a TS type (frontend),
  hand-written to match. No codegen.
- Missing information is an explicit `TODO` placeholder, never an invented value.
- **The UI renders resume content only.** No derived statistic, coverage ratio,
  source-file label or inferred link is presented as portfolio content.
- **Inferred data is deleted, not hidden.** If a link was the agent's inference
  rather than a resume fact, remove it from the content file — hiding it leaves
  the assumption in the data.
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
- **Every provider degrades, never fails.** A missing key costs quality, not the
  ability to boot: generation falls back to `template`, embedding to `hashing`.
- **A provider is not finished until `.env.example` documents it**, including
  what it trades away.
- Ground refusal in retrieval, not in the prompt. A threshold is a guarantee; an
  instruction to the model is a request. The same applies per-requirement: a
  gap is decided by score, never by asking whether evidence is "good enough".
- Pair vector search with an exact-term check when a query is a name rather than
  a sentence — a one-token query scores low against a long chunk.
- **A tool is a plain callable; MCP and HTTP are thin adapters over it.** Write
  the capability once, test it directly, and let each surface only translate.
- **Tool selection is deterministic, never model-decided** — match on data the
  tool owns (a repo's language, topics, name parts), word-bounded so a short
  term cannot match inside a longer word. Same guarantee as refusal-by-threshold.
- An external call returns a `reason` instead of raising, and only successes are
  cached — caching a blip turns it into an outage for the whole TTL.

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
