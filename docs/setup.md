# Setup Guide

## Already installed on this machine

Verified before scaffolding:

| Tool | Version | Status |
|---|---|---|
| Git | 2.53.0 | OK |
| Node.js | 24.14.1 | OK (current LTS line) |
| npm | 11.11.0 | OK |
| Python | 3.14.7 | OK |
| uv | 0.12.4 | OK - used instead of pip/venv |

## Installed since

- **GitHub CLI 2.98.0** — needed by `/complete` to open PRs. Requires a one-off
  `gh auth login`. Without auth the harness writes the PR body and gives you the
  compare URL instead.

## Not installed

| Tool | Needed for | Decision |
|---|---|---|
| **Ollama** | local LLM (Phase 3+) | Optional - see AI provider below |
| Docker | nothing | Not required by this project |
| gh CLI | opening PRs at `/complete` | **Installed** (2.98.0) — run `gh auth login` once |
| pnpm | nothing | npm is fine |

## AI provider - chosen by env var, no lock-in

Two things are abstracted, not one: **generation** and **embedding**. That is
what lets the same codebase run fully offline locally and fully serverless in
production. See [deployment.md](deployment.md) for why.

| Config | `AI_PROVIDER` | `EMBEDDING_PROVIDER` | Key? | Deployable? |
|---|---|---|---|---|
| Production (default) | `gemini` | `gemini` | yes, free | yes |
| Fully offline dev | `ollama` | `local` | no | no |
| Zero setup / fallback | `template` | either | no | yes |

- **Gemini** - free tier key from https://aistudio.google.com/apikey. Works
  locally and deployed. `gemini-embedding-001` covers embeddings on the same key.
- **Ollama** - install from https://ollama.com, then `ollama pull llama3.2`
  (~2 GB). Free, offline, private - but local only.
- **`template`** - no LLM at all. Retrieval still runs for real and the answer is
  composed from the retrieved chunks. This is the automatic fallback whenever a
  provider is unreachable, so a live demo never shows a broken AI feature.

Switching providers is an env var change. No code changes, but **rebuild the
index** when `EMBEDDING_PROVIDER` changes - the models have different dimensions:

```bash
python -m app.rag.ingest
```

## Backend

```bash
cd backend
uv venv                       # creates .venv
source .venv/Scripts/activate # Git Bash on Windows
# PowerShell:  .venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
uvicorn app.main:app --reload
```

`requirements.txt` is deployment-safe and has no ML dependencies. Only install
`requirements-local.txt` if you want offline embeddings - it adds torch (~2.5 GB
on Windows) and cannot be deployed.

API: http://localhost:8000 - docs at http://localhost:8000/docs

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Site: http://localhost:5173

## Environment

```bash
cp .env.example .env
```

Add your Gemini key. With no key set, the app falls back to `template` and still
runs - retrieval works, answers are composed from retrieved chunks.

## Commands

| Command | Where | Purpose |
|---|---|---|
| `pytest` | `backend/` | backend tests |
| `ruff check .` | `backend/` | backend lint |
| `npm test` | `frontend/` | component tests |
| `npm run lint` | `frontend/` | frontend lint |
| `npx tsc --noEmit` | `frontend/` | typecheck |
| `python -m app.rag.ingest` | `backend/` | rebuild the vector index (Phase 3+) |
