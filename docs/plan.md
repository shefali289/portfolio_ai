# Six-Phase Implementation Plan

One focused day. Each phase is one branch, several small commits, and one task
directory that moves from `harness/tasks/active/` to `completed/` when done.

Every phase runs the same lifecycle:
**Design -> Plan -> Test -> Develop -> Review -> Complete.**

---

## Phase 1 - Foundation · `feature/01-foundation` · ~1.5h

Frontend and backend both running, content extracted, tests wired.

- extract resume into `content/*.json` (5 files)
- FastAPI app, settings, CORS, `ContentService`, `/api/health`, `/api/profile`
- Vite + React + TS + Tailwind, layout shell, typed API client
- pytest + Vitest/RTL configured and green

**Done when:** the browser renders the real name/title fetched from the API.

---

## Phase 2 - Portfolio UI · `feature/02-portfolio-ui` · ~2.5h

The whole site, looking excellent, with no AI in it yet.

- Hero, Experience timeline (expandable), Projects (case-study cards + filters)
- Skills (grouped, click-to-see-evidence - no percentage bars)
- What I'm Building & Learning, Beyond Engineering, Contact
- Motion animations, responsive down to 375px, accessibility pass

**Done when:** a polished, complete portfolio stands on its own without AI.

---

## Phase 3 - RAG + GenAI · `feature/03-rag-assistant` · ~2h

- chunk `content/*.json` into `{text, source, type}` records
- `EmbeddingProvider` abstraction: Gemini (deployable) / local MiniLM (offline)
- index with FAISS, persist locally, record provider + dim in index metadata
- `AIProvider` abstraction: Gemini / Ollama / template fallback
- `POST /api/ai/chat` - retrieve, ground, generate, cite
- Ask My Portfolio UI with source chips
- **grounding test**: an out-of-scope question is refused, not answered

**Done when:** "What AI experience does she have?" returns a grounded, cited answer.

---

## Phase 4 - Agentic Job Match · `feature/04-agentic-job-match` · ~1.5h

- `requirement_agent` -> `portfolio_agent` -> `evidence_agent` -> `response_agent`
- `POST /api/ai/job-match` running the workflow in sequence
- Why Me? UI: paste a JD, watch the four steps tick over
- output shows strong matches with evidence, and honest gaps

**Done when:** a pasted job description yields matches, evidence and gaps.

---

## Phase 5 - MCP / External Context · `feature/05-mcp-integration` · ~1.5h

Both halves of the MCP story, kept small:

- `integrations/github.py` - public GitHub API, no token required
- a tiny MCP server exposing `get_profile`, `get_projects`, `search_projects`,
  `search_resume`, `get_skills`, `get_github_projects`
- "From My GitHub" section + the assistant using GitHub as a tool source
- answers attribute stored knowledge and live tool data separately

**Done when:** a question returns both portfolio evidence and live repo data.

---

## Phase 6 - Final Polish · `feature/06-final-polish` · ~1.5h

- Engineer Mode toggle: endpoint, chunks retrieved, retrieval ms, generation ms,
  sources, tool used
- loading / error / empty states everywhere
- mobile + accessibility final pass, README, architecture diagram, screenshots
- deploy to Vercel (frontend + Python functions), prebuilt index committed
- full test suite, lint, typecheck

**Done when:** the Definition of Done checklist is fully satisfied.

---

## Sequencing notes

- Phase 2 delivers a portfolio that is already presentable. If the day runs
  short, everything after it is additive rather than load-bearing.
- The `template` provider means Phases 3-6 are demonstrable even with no key -
  providers swap by env var, never by code change.
- Core dependencies stay ML-free so the backend deploys serverless. Install
  `requirements-local.txt` only if you want offline embeddings.

## Branch and commit approach

One branch per phase, off `main`, several small conventional commits inside it.

```
feature/01-foundation
feature/02-portfolio-ui
feature/03-rag-assistant
feature/04-agentic-job-match
feature/05-mcp-integration
feature/06-final-polish
```

```
feat: initialise React and FastAPI applications
feat: extract resume content into structured JSON
test: add content service and health endpoint tests
feat: add portfolio experience section
feat: add project case studies with filtering
test: add RAG retrieval and grounding tests
feat: implement portfolio RAG assistant
feat: add agentic job matching workflow
feat: integrate GitHub context tools
feat: add engineer mode
chore: deploy frontend and API to vercel
docs: document AI portfolio architecture
```

Future features use the same lifecycle on `feature/<name>`, `fix/<name>` or
`improvement/<name>` - the harness does not change.
