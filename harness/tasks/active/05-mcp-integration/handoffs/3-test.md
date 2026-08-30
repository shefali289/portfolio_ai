# Handoff: Test -> Developer

## Done

40 backend assertions across three new files plus new cases in two existing
ones, and 8 frontend cases across one new file plus two in `AskPortfolio`.
All run, all RED for the right reason.

## RED evidence

```
cd backend && .venv/Scripts/python.exe -m pytest -q
E   ModuleNotFoundError: No module named 'app.integrations.github'
ERROR tests/test_ai_chat.py · test_api.py · test_github.py · test_mcp_server.py · test_tools.py
!!! Interrupted: 5 errors during collection !!!

cd frontend && npm.cmd test -- --run
FAIL src/components/GitHubProjects.test.tsx
  Error: Failed to resolve import "./GitHubProjects" — Does the file exist?
FAIL src/components/AskPortfolio.test.tsx > attributes live GitHub results separately
  TestingLibraryElementError: Unable to find an element with the text: /from github \(live\)/i
Test Files  2 failed | 8 passed (10)   Tests  1 failed | 31 passed (32)
```

## You need to know

1. **Two guard tests assert absence and therefore cannot be RED** — "an
   unrelated grounded question attaches nothing" and "shows no live section when
   nothing was attached". They exist to catch the tool *over*-firing later.
   Recorded here rather than quietly counted as RED evidence.
2. **Signatures the tests pin down:**
   - `username_from_url(url) -> str`; `GitHubClient(username, *, settings, transport=None)`;
     `GitHubClient.from_content(content, settings)`; `.username`; `.list_repos() -> RepoFetchResult`
   - `RepoFetchResult(repos: list[GithubRepo], reason: str | None)` — `reason is None` on success
   - `GithubRepo(name, description, url, language, topics, pushed_at)`
   - `PortfolioTools(content=, retriever=, github=)` with the six methods; `TOOL_NAMES` a tuple in
     the order `get_profile, get_projects, search_projects, search_resume, get_skills, get_github_projects`
   - `build_server(tools) -> MCPServer`; `await server.list_tools()`, `await server.call_tool(name, args)`
   - `create_app(content_dir=..., github_client=...)` — new keyword argument
   - `ChatResponse.live_sources: list[LiveSource]`, `LiveSource(source, type="github-repo", url)`
   - `GET /api/github/repos -> {"repos": [...], "reason": str | None}`
3. **MCP 2.x renamed `FastMCP` to `MCPServer`** (`mcp.server.mcpserver`); the v1
   path raises a `ModuleNotFoundError` saying so. `list_tools`/`call_tool` are
   async, wrapped in `asyncio.run` rather than adding a pytest-asyncio mode.
4. **`live_sources` is optional in TypeScript** (`live_sources?: LiveSource[]`)
   so the existing `ChatAnswer` fixtures keep compiling untouched. The component
   must treat `undefined` as `[]`.
5. **The tool must fire on a metadata match, not on every grounded question.**
   One test asks about education and requires `live_sources == []`.
6. `Settings` needs `github_repo_limit`, `github_cache_ttl_s` (0 disables the
   cache — a test relies on that), `github_api_base`, `github_timeout_s`.

## Planning gap

The plan named `test_ai.py` / `test_api.py`; the real chat suite is
`test_ai_chat.py`. Cases were appended there. No other file outside the plan.

## Do NOT re-read

`2-plan.md` — the steps are unchanged and the signatures above supersede it.
