## feat: github integration and a portfolio MCP server

Closes: harness task `05-mcp-integration` (Phase 5)

> **Base this on `feature/04-agentic-job-match`, not `main`.** This is the fifth
> branch in an unmerged stack; targeting `main` will show four phases of
> ancestors as if they were this PR.

### What this adds

A public GitHub REST client, six portfolio tools exposed over **both** MCP and
HTTP, a From My GitHub section, and live repository data attached to grounded
answers as separately-attributed evidence. Asking "Python projects" now returns
portfolio evidence and live repositories side by side, each labelled with where
it came from.

### Why

The portfolio should demonstrate the difference between RAG and tools — stored
knowledge versus live external capability — and that one question can draw on
both without either being mistaken for the other. Collapsing them into one list
would hide exactly the distinction worth showing.

### How

- **One tool layer, two adapters.** Six plain callables in `integrations/tools.py`
  are the capability; `mcp_server.py` registers them and the HTTP router calls
  the same objects. Written and tested once, translated twice.
- **Live data supplements a grounded answer; it never rescues an ungrounded
  one.** This is rule 15 applied to refusal — a tool must not widen what the
  assistant is willing to answer. `git diff -- backend/app/rag/` is **empty**,
  and the Phase 3 refusal test passes unchanged.
- **Tool selection is deterministic, not model-decided** — a question matches on
  a repository's language, topics or name parts, word-bounded. The feature works
  with the `template` provider and no API key, exactly like refusal-by-threshold
  and gap-by-score before it.
- **Failure returns a reason, never an exception**, and only successes are
  cached: caching a blip would turn it into a 15-minute outage.
- **Repos ranked by recency, never curated.** A hand-picked list would be
  portfolio content the resume does not support. Forks are excluded.
- **No new dependency.** `mcp` and `httpx` were already pinned; verified
  installed on Python 3.14.7 before designing around them.

### Changed

| Area | Files |
|---|---|
| Backend | `integrations/{github,tools,mcp_server}.py`, `services/ai.py`, `api/{routes,schemas}.py`, `config.py`, `main.py` |
| Frontend | `components/GitHubProjects.tsx`, `components/AskPortfolio.tsx`, `App.tsx`, `lib/api.ts`, `types/content.ts` |
| Content | none — the GitHub username is read from `content/profile.json` |
| Harness | task, handoffs 1–5, completion report; `.env.example` corrected |

### Tests

| Suite | Result |
|---|---|
| `pytest` | 79 passed |
| `npm test` | 39 passed (10 files) |
| `ruff` / `eslint` / `tsc` | clean |

New tests lock in: fork exclusion and recency ranking; four GitHub failure modes;
cache hit, expiry, and that a failure is never cached as a success; exactly six
MCP tools whose payloads match the underlying functions; combined attribution on
a grounded answer; and that an ungrounded question still refuses with
`live_sources: []`. RED evidence in `handoffs/3-test.md`.

### Quality gates

| Gate | Result |
|---|---|
| G0 branch | PASS |
| G1 design | PASS |
| G2 test (RED) | PASS |
| G3 build (GREEN) | PASS |
| G4 review | PASS — 3 findings, none blocking |
| G5 completion | PASS |

### Lessons learned

- One tool layer with two thin adapters: the MCP surface needed four tests
  rather than a subprocess, and the HTTP route was three lines.
- Two defects survived a green suite and were caught only by running against the
  real account — hyphenated repo names never matched a question, and
  `.env.example` documented two settings that did not exist.
- Check every mock of a module before growing its exports.

### User overrides

None. Tool reach and tool selection were put to the user at `/plan` and accepted
as designed.

### Known limitations

- **The MCP `search_resume` tool does not apply the grounding threshold.** Chat
  refuses "What is the capital of France?"; the tool returns four sub-threshold
  passages for it. Scores are returned so a client *can* filter, but nothing
  marks them as below the bar. Reviewer input welcome — this is a decision, not
  an oversight.
- A hanging GitHub adds up to 5s to a grounded answer, once per cache window.
- `From GitHub (live)` is a styled paragraph, not a heading, so heading
  navigation skips it; it is announced via `aria-live`.
- Conversational phrasings are refused under the lexical embedding fallback
  ("What Python projects has she built?" scores 0.228 against 0.25). Pre-existing
  Phase 3 behaviour, resolved once `GEMINI_API_KEY` is set.

### Harness

Task, handoffs 1–5 and completion report:
`harness/tasks/completed/05-mcp-integration/`
