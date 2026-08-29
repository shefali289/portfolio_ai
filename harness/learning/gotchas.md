# Gotchas

Things that cost time. Symptom -> cause -> fix.

> Append whenever something surprising happens. Empty sections are fine.

## Environment

- **Python here is 3.14.7** - newer than most wheels target. Verify a package
  resolves (`uv pip compile --python-version 3.14`) before pinning it. A pin
  recalled from memory produced a version that does not exist.
- **No Ollama, no Docker, no `gh` CLI installed.** The GitHub integration must
  use the public REST API, which needs no auth for public repos.
- **Windows + Git Bash.** venv activation is `.venv/Scripts/activate`, not
  `bin/activate`. Avoid `-o /dev/null` with `uv` - it fails to persist on Windows.
- **Long chained heredocs in one Bash call are fragile here.** A single
  mismatched terminator silently swallows the rest and the whole command fails.
  Write files one at a time.

## Deployment

- **Vercel Python bundle limit is 500 MB.** `torch` + `sentence-transformers` is
  ~1 GB installed. Local embeddings cannot be deployed - use Gemini embeddings in
  production and keep `requirements.txt` free of ML dependencies.
- **Index vectors are provider-specific.** Gemini and MiniLM have different
  dimensions. Switching `EMBEDDING_PROVIDER` requires a re-ingest; the index
  stores its provider + dim and must refuse to load a mismatch.

## AI behaviour

_(none yet - expect entries once RAG is running)_
