# Handoff: Developer -> Review

## Done

All nine steps. GitHub client with a TTL cache, six tools, an MCP adapter, live
sources attached to grounded answers, `GET /api/github/repos`, and a From My
GitHub section. Backend **79 passed**, frontend **39 passed**, ruff + eslint +
`tsc --noEmit` clean.

## You need to know

1. **`backend/app/rag/` has zero changes** — `git diff HEAD -- backend/app/rag/`
   is empty. Rule 15 held mechanically, not just by intention.
2. **Verified live, not just in tests.** Against the real account: the section
   renders 6 repos; `Python projects` returns portfolio evidence *and*
   `portfolio_ai` + `agentic-ai` as live sources; `What is the capital of
   France?` still refuses with `live_sources == []`. 375px measured in a
   same-origin iframe: `scrollWidth == clientWidth`, 0 overflowing elements.
3. **Two defects were found by running it, both fixed:** `agentic-ai` never
   surfaced for an AI question (only whole repo names were matched — names are
   now matched by their parts, with a regression test and three over-firing
   guards); and `.env.example` documented `GITHUB_USERNAME`/`GITHUB_TOKEN`,
   neither of which exists here, now replaced with the four real settings.

## Deviations from the plan

- `test_ai.py` does not exist; the chat suite is `test_ai_chat.py`. Cases added
  there.
- **`frontend/src/App.test.tsx` was changed although the plan did not name it.**
  Its `vi.mock` of `lib/api` had to gain `getGithubRepos` (via `vi.hoisted`,
  which that file already uses) or every App test failed. Test-only, no
  behaviour change. Planning gap: the plan should list every mock of a module
  whose exports it grows.
- Added `repos_matching` unit tests to `test_github.py`, not in the plan: the
  matcher was reachable only through the chat endpoint, too coarse for guards.

## Look at this closely

**The brief's own demo question is refused.** `"What Python projects has she
built?"` scores **0.228** against `GROUNDING_THRESHOLD = 0.25` — the right chunk
ranks first, but conversational filler dilutes a lexical vector. `"Python
projects"` scores 0.322 and works end to end.

A **pre-existing Phase 3 limitation** exposed by Phase 5, not caused by it.
Fixing it means touching retrieval — forbidden here, and it would weaken the
refusal guarantee for every question. Left unfixed deliberately and raised.

## Files

New: `app/integrations/{__init__,github,tools,mcp_server}.py`,
`tests/{test_github,test_tools,test_mcp_server}.py`,
`components/GitHubProjects.{tsx,test.tsx}`.
Modified: `config.py`, `api/{schemas,routes}.py`, `services/ai.py`, `main.py`,
`tests/{test_ai_chat,test_api}.py`, `types/content.ts`, `lib/api.ts`, `App.tsx`,
`App.test.tsx`, `AskPortfolio.{tsx,test.tsx}`, `.env.example`.

## Do NOT re-read

`3-test.md` — signatures unchanged. `2-plan.md` — deviations are listed above.
