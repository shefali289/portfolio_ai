# Handoff: Planning -> Test

## Done

Nine steps, back-to-front: settings and schema, then the GitHub client, the tool
layer, the MCP adapter, the AI attachment and route, then the two frontend
surfaces, then validation. Full detail in `task.md` `## Implementation Steps`.

## You need to know

1. **`backend/app/rag/` is off limits this phase.** No repo text enters the
   index; `Retriever` and `GROUNDING_THRESHOLD` are not touched. If a step seems
   to need retrieval changed, the design is wrong — stop and report it.
2. **Write the RED tests in this order:** `test_github.py` (step 2),
   `test_tools.py` (4), `test_mcp_server.py` (5), then the new cases appended to
   `test_ai.py` / `test_api.py` (6). Frontend tests are steps 7 and 8.
3. **Two tests are the point of the phase, not extras:**
   - a grounded question returns portfolio sources *and* `live_sources`, each
     attributed to its own origin;
   - an ungrounded question is **still refused** and returns `live_sources == []`.
     The existing refusal test must pass **unchanged** — that is the proof RAG
     was not reshaped.
4. **Never let a GitHub failure raise into a route.** Three failure tests are
   required: 403 rate-limit, timeout, network error. Each returns
   `RepoFetchResult(repos=[], reason=...)`.
5. **Fixtures must not hit the network.** Inject a fake transport or stub the
   client, as `stub_embeddings` already does for embeddings in `conftest.py`.
6. **The username is parsed from `content/profile.json`** (`links.github`), so a
   fixture profile drives the test, not the real account.

## Files

- `backend/app/integrations/{__init__,github,tools,mcp_server}.py` - new
- `backend/tests/{test_github,test_tools,test_mcp_server}.py` - new
- `backend/app/{config,api/schemas,api/routes,services/ai,main}.py` - modified
- `frontend/src/components/GitHubProjects.{tsx,test.tsx}` - new
- `frontend/src/{types/content.ts,lib/api.ts,App.tsx}` - modified
- `frontend/src/components/AskPortfolio.{tsx,test.tsx}` - modified
- `.env.example`, `docs/setup.md` - document the three new settings

## Do NOT re-read

`1-design.md` — its conclusions are in `task.md` `## Design`. The signatures you
need (`ChatResponse`, `AiService.answer`, `Retriever.is_grounded`,
`ContentService`) are listed above and in the architecture map.
