# Decisions

One line each: the choice, and the reason. Rejected options included.

> Seeded from scaffolding. Append at `/complete`; never rewrite history here.

## 2026-08-29 - Scaffolding

- **Vite + React over Next.js** - no SSR or routing needs for a single-page
  portfolio; faster dev loop.
- **JSON files over a database** - five small files that belong in git and feed
  both the UI and the RAG index.
- **`content/` at repo root, not inside backend** - consumed by both the API and
  the ingestion script; it is the source of truth, not a backend detail.
- **Generation and embedding abstracted separately** - they have different
  deployment constraints. Ollama cannot deploy at all; local MiniLM needs torch
  (~1 GB) and busts the Vercel 500 MB Python bundle. Gemini serves both in prod.
- **`template` provider as automatic fallback** - retrieval is real even with no
  LLM, so a live demo never shows a broken AI feature.
- **FAISS kept despite a tiny corpus** - numpy dot-product would do for ~60
  chunks; kept because it is specified and is a recognisable talking point.
  Swappable behind the retriever if it ever becomes friction.
- **Dependency versions resolved, not recalled** - pins come from
  `uv pip compile` against Python 3.14, after a guessed version proved not to
  exist.

## 2026-08-29 - Harness

- **Handoff files over shared context** - each agent reads a <60-line briefing
  plus named files, not the repository. Cost stops scaling with repo size.
- **`harness/learning/` over re-exploration** - the Design Agent reads a
  maintained digest. Feature N+1 is cheaper than feature N, not more expensive.
- **Slash commands as the entry points** - `/plan`, `/build`, `/review`,
  `/complete` map to lifecycle stages so a phase always starts the same way.

## 2026-08-29 - Foundation

- **Eager validated content loading** - malformed JSON fails application startup
  instead of surfacing during a live request.
- **One typed frontend API client** - components never call `fetch`, keeping the
  backend seam reusable and mockable.
- **Strict content models (`extra="forbid"`)** - typoed keys fail validation
  rather than silently rendering incomplete portfolio sections.

## 2026-08-29 - Portfolio UI

- **One aggregate content endpoint** - five cached models share one page-level
  loading/error/retry lifecycle instead of repeating routes and request state.
- **Evidence integrity before rendering** - validate every skill evidence ref at
  content load, then resolve human-readable labels in the frontend.
- **Content-derived filters and omitted empty narratives** - the resume does not
  support a fixed taxonomy or Building/Learning/Beyond copy, so the UI invents neither.
- **Semantic HTML and Tailwind over a UI/motion dependency** - native controls,
  visible focus, and `motion-safe` CSS satisfy the interaction and a11y needs.
