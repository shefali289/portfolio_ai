# Task: MCP + GitHub Context

| | |
|---|---|
| **Slug** | `05-mcp-integration` |
| **Branch** | `feature/05-mcp-integration` |
| **Phase** | Phase 5 |
| **Status** | built — G0-G3 passed, awaiting `/review` |
| **Started / Completed** | 2026-08-30 / — |

> **Brief only.** `/plan 05-mcp-integration` fills in Design, Plan and the rest. Every stage
> writes back here, so this file ends up holding the whole story. Do not
> implement from this file alone.

---

# 1 · Intent

## Feature

GitHub public API integration, a small portfolio MCP server, a From My GitHub
section, and answers combining stored knowledge with live tool data.

## Goal

Show the distinction between RAG (stored knowledge) and MCP/tools (external,
live capability) - and that they can answer one question together.

## Acceptance Criteria

Refined at `/plan`, checked off at `/review`.

- [ ] the From My GitHub section renders live public repositories, non-fork,
      most recently pushed first, capped at 6
- [ ] rate-limit, timeout and network failure each yield an honest empty state
      with a reason — never an error dialog, never a fabricated repo
- [ ] the MCP server lists exactly its six tools, and a tool call returns the
      same payload as calling the underlying function
- [ ] one question returns both portfolio and GitHub evidence, **attributed
      separately** in the response and visibly separated in the UI
- [ ] **the RAG implementation is unchanged** — no repo text enters the index,
      `Retriever` and `GROUNDING_THRESHOLD` are untouched
- [ ] an ungrounded question is still refused, with `live_sources == []`
- [ ] the GitHub username is read from `content/profile.json`, never hardcoded

## User Experience

A From My GitHub section shows selected repositories. Asking "What Python
projects has she built?" returns portfolio evidence and live repositories,
attributed separately.

## Out of Scope

Authenticated GitHub features, write operations, other MCP servers.

Also excluded, deliberately:

- **Repo README ingestion** — that would put live text into the RAG corpus.
- **Streaming or background refresh** — the TTL cache is refreshed on request.
- **Commit history, stars, traffic, contribution graphs** — all need auth, and
  none is portfolio evidence the resume supports.
- **An MCP client in the backend** — the server is the deliverable.

---

# 2 · Design  *(Design Agent, `/plan`)*

**1 · Where does it live?** `backend/app/integrations/` — the area the
architecture map already reserves for GitHub and MCP. No new top-level system.

**2 · What is reused?** `ContentService` backs four of the six tools;
`AiService` gains an attachment step but its retrieve → ground → generate path
is untouched. `httpx` is already a dependency. The frontend reuses the existing
card, skeleton and empty-state patterns.

**3 · Frontend changes?** Yes — a `From My GitHub` section, one `api.ts` method,
and a separately-attributed live block inside `AskPortfolio`.

**4 · Backend changes?** Yes — `integrations/github.py`, `integrations/tools.py`,
`integrations/mcp_server.py`, one route, and `live_sources` on `ChatResponse`.

**5 · AI / RAG / MCP?** MCP yes; RAG **deliberately untouched**. Repo text never
enters the index — that is the whole point of rule 15.

**6 · New dependency?** **No.** `mcp==2.1.1` and `httpx==0.28.1` are already
pinned in `requirements.txt` and installed in `backend/.venv` (verified, Python
3.14.7). Phase 1 pre-pinned MCP for exactly this phase.

**7 · Simplest sufficient implementation?** Six plain functions in `tools.py`,
backed by `ContentService` and a small cached `GitHubClient`. MCP and HTTP are
both thin adapters over those functions, so the capability is written once.

## Key technical decisions

- **Tool selection is deterministic, not model-decided** — the GitHub tool fires
  when a question names a term present in repo metadata. This continues the
  house pattern (refusal by threshold, gap by score) and keeps the feature
  working with the default `template` provider and no API key.
- **Grounding stays a RAG property** — live repos supplement a grounded answer
  and never rescue an ungrounded one. A tool must not widen what the assistant
  will answer.
- **Repos ranked by recency, never curated** — a hand-picked list would be
  invented content. Non-fork, sorted by `pushed_at`, capped at 6.
- **Failure returns a reason, not an exception** — `RepoFetchResult(repos=[],
  reason=...)`, so a supplementary section can never break the page.

## Existing Components Reused

RAG service unchanged - adding a tool must not reshape retrieval.
`ContentService` backs the MCP tools.

## Rejected Alternatives

| Option | Why not |
|---|---|
| Index repos into FAISS | A tool reshaping retrieval. Directly violates rule 15. |
| LLM tool-calling | Needs a real model; breaks the zero-key guarantee and hides the RAG-vs-tool distinction this phase exists to show. |
| Fetch repos on every chat request | A network call on the refusal path, for a result usually unused. |
| A backend MCP client calling its own server | A loopback that adds a process boundary and demonstrates nothing. |
| Authenticated GitHub (stars, traffic) | A token to store and rotate; explicitly out of scope. |
| Persisted cache file | State to invalidate; a dict is enough for one process at 60 req/hr. |

---

# 3 · Plan  *(Planning Agent, `/plan`)*

## Implementation Steps

Each step is independently verifiable. Tests precede the code they cover.

| # | Step | Skill | Verified by |
|---|---|---|---|
| 1 | Settings (`github_api_base`, `github_cache_ttl_s`, `github_repo_limit`) in `config.py`; `LiveSource` + `live_sources: list[LiveSource] = []` on `ChatResponse` in `schemas.py` | `api-endpoint` | existing suite still green — the field is additive |
| 2 | **RED** `tests/test_github.py`: parses repos, excludes forks, orders by `pushed_at`, caps at 6, derives the username from `profile.json`, and returns `repos=[], reason=...` on 403 rate-limit / timeout / network error | `tdd-cycle` | tests fail with `ModuleNotFoundError` |
| 3 | **GREEN** `integrations/github.py` — `GithubRepo`, `RepoFetchResult`, `GitHubClient` with a 15-minute in-process TTL cache | `tdd-cycle` | `test_github.py` passes |
| 4 | **RED→GREEN** `tests/test_tools.py` + `integrations/tools.py` — the six callables (`get_profile`, `get_projects`, `search_projects`, `search_resume`, `get_skills`, `get_github_projects`) over `ContentService` and `GitHubClient` | `tdd-cycle` | `test_tools.py` passes |
| 5 | **RED→GREEN** `tests/test_mcp_server.py` + `integrations/mcp_server.py` — the server lists exactly six tools and a call returns the same payload as the function it wraps | `tdd-cycle` | `test_mcp_server.py` passes |
| 6 | **RED→GREEN** attach live sources in `services/ai.py` (grounded answers only) and add `GET /api/github/repos` to `routes.py` | `api-endpoint` | new tests in `test_ai.py` / `test_api.py`; the existing refusal test still passes unchanged |
| 7 | **RED→GREEN** `types/content.ts`, `lib/api.ts` `getGithubRepos()`, `components/GitHubProjects.test.tsx` then `GitHubProjects.tsx`; register the `github` section in `App.tsx` | `react-component` | component tests cover loaded, loading and unavailable states |
| 8 | **RED→GREEN** `AskPortfolio.test.tsx` — live results render under their own `From GitHub (live)` heading, separate from portfolio sources | `react-component` | test passes; existing AskPortfolio tests untouched |
| 9 | Validate: full backend + frontend suites, ruff, eslint, `tsc --noEmit`, 375px and desktop, a live run against the real account, and `.env.example` documenting the new settings | `a11y-responsive` | real output recorded in `## Validation` |

## Files Likely To Change

**New**

- `backend/app/integrations/__init__.py`
- `backend/app/integrations/github.py`
- `backend/app/integrations/tools.py`
- `backend/app/integrations/mcp_server.py`
- `backend/tests/test_github.py`, `test_tools.py`, `test_mcp_server.py`
- `frontend/src/components/GitHubProjects.tsx` + `.test.tsx`

**Modified**

- `backend/app/config.py` — three settings
- `backend/app/api/schemas.py` — `LiveSource`, `live_sources`, `GithubReposResponse`
- `backend/app/api/routes.py` — `GET /api/github/repos`
- `backend/app/services/ai.py` — attach live sources to grounded answers
- `backend/app/main.py` — build the client, hold it on app state
- `backend/tests/test_ai.py`, `test_api.py` — new cases only
- `frontend/src/types/content.ts`, `frontend/src/lib/api.ts`
- `frontend/src/App.tsx` — register the section
- `frontend/src/components/AskPortfolio.tsx` + `.test.tsx`
- `.env.example`, `docs/setup.md`

**Must not change:** `backend/app/rag/*` — if this phase needs to touch
retrieval, the design is wrong; stop and report it.

## Skills Used

`api-endpoint`, `react-component`, `tdd-cycle`, `a11y-responsive`

---

# 4 · Tests  *(Test Agent, `/build`)*

## Tests First

- GitHub client parses repo data; handles rate limit and network failure
- the section renders repos and degrades when the API is unavailable
- MCP server exposes the tools and returns valid results
- a combined answer attributes stored vs live evidence separately

## TDD Evidence

RED then GREEN. Tests written after the code fail G2 — the failure output is the
proof, and `final_checklist.py` checks for it.

| | |
|---|---|
| **RED - command** | `cd backend && .venv/Scripts/python.exe -m pytest -q` · `cd frontend && npm.cmd test -- --run` |
| **RED - failed for the right reason** | Yes. Backend: 5 collection errors, `ModuleNotFoundError: No module named 'app.integrations.github'`. Frontend: `Failed to resolve import "./GitHubProjects"` and `Unable to find an element with the text: /from github \(live\)/i`. Output in `handoffs/3-test.md`. |
| **GREEN - result** | backend `79 passed`; frontend `Test Files 10 passed (10)`, `Tests 39 passed (39)` |

---

# 5 · Gates

See `harness/QUALITY-GATES.md`. `PARTIAL`/`SKIPPED` are honest; a check reported
`PASS` without running is not.

| Gate | When | Result | Date | Note |
|---|---|---|---|---|
| **G0** branch | before `/build` writes | PASS | 2026-08-30 | 3 passed, 1 warn (plan artefacts uncommitted) |
| **G1** design | Design → Plan | PASS | 2026-08-30 | 7 questions answered; no new dependency; `1-design.md` 60 lines, within cap |
| **G2** test (RED) | Test → Develop | PASS | 2026-08-30 | `ModuleNotFoundError: app.integrations.github`; frontend `Failed to resolve import "./GitHubProjects"`. Two absence-guard tests cannot be RED — noted in `3-test.md` |
| **G3** build (GREEN) | Develop → Review | PASS | 2026-08-30 | backend `79 passed`, frontend `39 passed`; ruff + eslint + tsc clean; `git diff -- backend/app/rag/` empty |
| **G4** review | Review → Complete | — | | tests · lint · typecheck · a11y |
| **G5** completion | before archive + PR | — | | `final_checklist.py` |

## Final Checklist  *(`/complete`)*

`python harness/scripts/final_checklist.py --slug 05-mcp-integration` — must exit 0.
Paste the result table, then confirm by hand:

- [ ] content traces to the resume; no invented experience
- [ ] AI answers cite sources; out-of-scope questions refused
- [ ] works at 375px and desktop
- [ ] loading, error and empty states reachable
- [ ] keyboard navigable; images have alt text

---

# 6 · Record

## Decisions Taken

| Date | Decision | Reason |
|---|---|---|
| 2026-08-30 | Tool selection is deterministic, never model-decided | Continues the house pattern and keeps the feature working with `template` and no API key |
| 2026-08-30 | Live repos supplement a grounded answer; they never rescue an ungrounded one | A tool must not widen what the assistant will answer — rule 15 applied to refusal |
| 2026-08-30 | Tools are plain functions; MCP and HTTP are thin adapters | The capability is written once and tested without a subprocess |
| 2026-08-30 | Repos ranked by recency, never curated | A hand-picked list would be invented content |
| 2026-08-30 | No new dependency — `mcp` and `httpx` already pinned | Verified installed on Python 3.14.7 before planning around them |
| 2026-08-30 | Repo names are matched by their parts, not only whole | `agentic-ai` is the most direct evidence for an AI question, but the full string never appears in a typed sentence |
| 2026-08-30 | `.env.example` GitHub block rewritten | It documented `GITHUB_USERNAME`/`GITHUB_TOKEN`, neither of which exists — documenting absent settings is worse than documenting none |
| 2026-08-30 | The lexical-retrieval refusal of conversational phrasings left unfixed | Fixing it means touching `rag/`, forbidden this phase, and would weaken the refusal guarantee for every question |

## User Overrides

Every entry must end in a promoted rule. Promoted to
`harness/learning/user-overrides.md` at `/complete`.

| Date | Agent proposed | User chose | Why | Rule now |
|---|---|---|---|---|

## Lessons Learned

- **Worked:**
- **Cost time:**
- **Do differently:**

## Known Limitations

_(filled at `/complete`)_

---

# 7 · Validation & PR  *(`/complete`)*

## Validation

Real results only. Not run = `SKIPPED`, never `PASS`.

| Check | Result |
|---|---|
| backend tests | — |
| frontend tests | — |
| lint | — |
| typecheck | — |
| manual check | — |

Repos render live; MCP tools callable and listed.

## PR Summary

| | |
|---|---|
| **Title** | — |
| **URL** | — |
| **Merged** | — |

**What it adds:** —

**Why:** —

## Suggested Commit Message

```
<type>: <description>
```
