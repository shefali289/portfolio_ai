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
