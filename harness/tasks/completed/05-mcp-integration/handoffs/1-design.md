# Handoff: Design -> Planning

## Done

Designed GitHub + MCP as **one tool layer with two adapters**. Live repo data is
attached to answers as a separately-attributed block; RAG is untouched (rule 15).
No new dependency: `mcp==2.1.1` and `httpx` are already pinned and installed.

## You need to know

1. **Tool selection is deterministic, never model-decided.** The GitHub tool
   fires when a question names a term present in repo metadata (language or
   topic). House pattern: refusal by threshold (P3), gap by score (P4), tool by
   match (P5). `template` is still the default provider, so nothing may depend
   on an LLM choosing to call a tool.
2. **Grounding stays a RAG property.** Live repos *supplement* a grounded
   answer; they never rescue an ungrounded one, which is still refused. That is
   what "a tool never reshapes RAG" has to mean in practice.
3. **Tools are plain functions; MCP and HTTP are both thin adapters.**
   `integrations/tools.py` holds the six callables backed by `ContentService` +
   `GitHubClient`; `mcp_server.py` registers them, and the router calls the same
   functions. Tests hit the functions directly — no subprocess, no async server.
4. **The username is parsed from `content/profile.json` (`links.github`)**, not
   hardcoded. Content stays the source of truth.
5. **Unauthenticated GitHub allows 60 req/hr.** The client holds a 15-minute TTL
   cache and returns `RepoFetchResult(repos=[], reason=...)` on rate-limit,
   network failure or timeout — never raises into a route, never invents a repo.
6. `ChatResponse` gains `live_sources: list[LiveSource]` defaulting to `[]`.
   Additive, so existing chat tests and the typed client keep working.
7. **Repos by recency, not curation** — non-fork public repos sorted by
   `pushed_at`, capped at 6. A hand-picked list would be invented content.
   Transport is stdio; the cache is an in-process dict.

## Rejected alternatives

- **Indexing repos into FAISS** — a tool reshaping retrieval. Rule 15.
- **LLM tool-calling** — needs a real model, breaks the zero-key guarantee, and
  hides the RAG-vs-tool distinction this phase exists to demonstrate.
- **Fetching repos on every chat request** — a network call on a refusal path.
- **Authenticated GitHub** — a token to store; out of scope.

## UI/UX

New `From My GitHub` section (`id="github"`, nav position after Projects). Cards
show name, description, language, updated date, link. Loading is a skeleton;
unavailable is an honest line plus a link to the profile, not an error dialog,
because the section is supplementary. In `AskPortfolio`, live results sit under a
distinct `From GitHub (live)` heading, separated from portfolio sources.

## Files

- `backend/app/integrations/` — new area, in architecture-map already:
  `github.py`, `tools.py`, `mcp_server.py`
- `backend/app/services/ai.py` — attach live sources to a grounded answer only
- `frontend/src/components/GitHubProjects.tsx` — new section

## Do NOT re-read

`routes.py`, `schemas.py`, `ai.py`, `main.py`, `api.ts`, `App.tsx`,
`requirements.txt`, `config.py` — seams captured above.
