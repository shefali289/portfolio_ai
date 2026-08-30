# Deployment

## Target

| Piece | Host | Why |
|---|---|---|
| Frontend | **Vercel** | Static Vite build; free, instant, custom domain |
| Backend | **Vercel Python Functions** | Same project, one deploy, no second dashboard |
| LLM | **Gemini free tier** | The only provider that works from a serverless host |
| Embeddings | **Gemini `gemini-embedding-001`** | Keeps the bundle free of torch |
| Vector index | **committed file** | Built at ingest time, read at runtime |

## The constraint that drives this design

Vercel's Python bundle limit is **500 MB** (raised from 250 MB). A CPU-only
`torch` + `sentence-transformers` install is roughly **1 GB** on Linux, and
loading torch on a cold start is slow even when it fits.

So *neither* the LLM *nor* the local embedding model can be deployed:

| Approach | Local dev | Deployed |
|---|---|---|
| Ollama generation | works | **impossible** - needs a resident model |
| MiniLM embeddings | works | **too large** - torch busts the bundle |
| Gemini generation | works | works |
| Gemini embeddings | works | works |

This is why the project abstracts **both** generation and embedding behind
interfaces rather than only the LLM:

```
AIProvider          -> GeminiProvider | OllamaProvider | TemplateProvider
EmbeddingProvider   -> GeminiEmbedder | LocalEmbedder (MiniLM)
```

Same codebase, two configurations, selected by env var:

```
Local dev  : AI_PROVIDER=ollama  EMBEDDING_PROVIDER=local   -> fully offline, no key
Production : AI_PROVIDER=gemini  EMBEDDING_PROVIDER=gemini  -> serverless, no ML deps
```

Both must produce the same index shape, so the index is **rebuilt** when the
embedding provider changes - the two models have different dimensions and their
vectors are not interchangeable. `ingest.py` writes the provider name and
dimension into the index metadata and refuses to load a mismatched index.

## Steps

1. Push to GitHub.
2. Import the repo on Vercel. Root `frontend/`, framework Vite.
3. Add `api/index.py` exposing the FastAPI app, and a `vercel.json` routing
   `/api/*` to it.
4. Set env vars in Vercel: `GEMINI_API_KEY`, `AI_PROVIDER=gemini`,
   `EMBEDDING_PROVIDER=gemini`, `CORS_ORIGINS=<deployed origin>`.
5. Nothing to commit for the index. The corpus is ~60 chunks and the app
   builds the vector index **in memory at startup** (`AiService.build`), so
   there is no persisted index and `backend/.index/` stays gitignored. The
   cost is one embedding batch per cold start; with the `hashing` fallback it
   is free.

## What is verified, and what is not

Deployment cannot be executed from this repository, so be precise about which
parts are actually checked.

**Verified** (`backend/tests/test_deploy_config.py`):

- `api/index.py` imports the same FastAPI app `uvicorn` serves, and answers
  `/api/health` and `/api/content` through it
- `vercel.json` parses, pins no Python runtime, and does not stub out install

**Not verified — confirm on the first deploy:**

- **That the `/api/(.*)` rewrite preserves the original path.** If Vercel hands
  the function `/api/index` instead of `/api/health`, every route 404s. Check
  `/api/health` first; if it fails, the rewrite is the reason.
- Cold-start time with `EMBEDDING_PROVIDER=gemini`, which embeds the corpus on
  each cold start.
- That the bundle stays under 500 MB. `requirements.txt` includes the backend's
  pins, so `pytest` and `ruff` ship with the function.

No pinned runtime is deliberate: `@vercel/python@4.3.0` was pinned once and
shipped a Python older than 3.11, which cannot import `StrEnum`. An unverifiable
pin is worse than none, because it looks deliberate.

## If the bundle ever needs torch

Move the backend to **Hugging Face Spaces** (free, 16 GB RAM, Docker, built for
ML) or **Render**, and point the Vercel frontend at it via `VITE_API_URL`. The
provider abstraction means no application code changes - only env vars.

## Demo safety

`TemplateProvider` composes an answer from retrieved chunks with no LLM call. If
the Gemini key is missing, rate-limited or offline mid-interview, the AI features
still return grounded, cited answers instead of an error. Retrieval is real in
every configuration.
