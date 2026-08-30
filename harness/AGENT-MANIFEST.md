# Agent Manifest

The index. Which agent does what, with which skills, reading what, passing what
on — and every task name usable as `/plan <name>`.

**Agents read only their own row.** Read this file whole only when orienting.

---

## Commands

| Command | Stages | Gate | Writes |
|---|---|---|---|
| `/plan <task>` | Design → Planning | G1 | `task.md`, `1-design.md`, `2-plan.md` |
| `/build [step]` | Test → Developer | G0, G2, G3 | `3-test.md`, `4-develop.md` |
| `/review` | Review | G4 | `5-review.md` |
| `/complete` | Completion | G5 | `completion.md`, `pull-request.md`, `learning/` |
| `/status` | — | — | nothing |
| `/health` | — | — | nothing |

Gates: [`QUALITY-GATES.md`](QUALITY-GATES.md).
Scripts: `harness/scripts/` — `branch_gate.py` (G0), `health_check.py`,
`final_checklist.py` (G5, decides completion). Same scripts run in CI.

---

## Agents

| Agent | Reads | Skills | Writes |
|---|---|---|---|
| **Design** | `learning/*`, `task.md`, files learning points at | — (judgement, not procedure) | `1-design.md` |
| **Planning** | `1-design.md`, `learning/architecture-map.md` | — | `2-plan.md` |
| **Test** | `2-plan.md`, `learning/conventions.md`, existing tests | `tdd-cycle` | `3-test.md` |
| **Developer** | `2-plan.md`, `3-test.md`, `learning/conventions.md`, files the plan names, skills the plan names | `tdd-cycle`, `api-endpoint`, `react-component`, `content-extraction`, `rag-ingestion`, `ai-provider`, `agent-workflow`, `a11y-responsive` | `4-develop.md` |
| **Review** | `4-develop.md`, `task.md`, the diff | `a11y-responsive` | `5-review.md` |

Only **Design** may explore, and it starts from `learning/`, never a blind scan.
Read budgets: [`HANDOFF-PROTOCOL.md`](HANDOFF-PROTOCOL.md).

---

## Skills

| Skill | Used by | When |
|---|---|---|
| [`tdd-cycle`](skills/tdd-cycle.md) | Test, Developer | every behavioural change |
| [`api-endpoint`](skills/api-endpoint.md) | Developer | new backend HTTP surface |
| [`react-component`](skills/react-component.md) | Developer | new UI surface |
| [`content-extraction`](skills/content-extraction.md) | Developer | populating `content/*.json` |
| [`rag-ingestion`](skills/rag-ingestion.md) | Developer | content or embedding provider changes |
| [`ai-provider`](skills/ai-provider.md) | Developer | adding a generation/embedding backend |
| [`agent-workflow`](skills/agent-workflow.md) | Developer | extending the job-match chain |
| [`a11y-responsive`](skills/a11y-responsive.md) | Developer, Review | any UI change, before review |

---

## Handoffs

Each stage writes a **<60-line** briefing. The next agent reads that briefing
plus only the files it names — never the repository.

```
Design ─1─> Plan ─2─> Test ─3─> Develop ─4─> Review ─5─> learning/
```

Sections: `Done` · `You need to know` · `Files` · `Do NOT re-read` ·
`Open questions` · `New learnings`.

`Do NOT re-read` is what makes the saving real. `New learnings` is harvested at
`/complete`.

---

## Learning

| File | Holds | Cap |
|---|---|---|
| [`architecture-map`](learning/architecture-map.md) | where things live, seams to extend | 150 |
| [`conventions`](learning/conventions.md) | patterns to copy | 150 |
| [`decisions`](learning/decisions.md) | choices made and rejected | 150 |
| [`gotchas`](learning/gotchas.md) | what broke and why | 150 |
| [`lessons-learned`](learning/lessons-learned.md) | what to do differently | 100 |
| [`user-overrides`](learning/user-overrides.md) | where the user corrected the harness | 80 |

Written at `/complete`, read at `/plan`. This is why feature N+1 costs less than
feature N. Over cap means unpruned, which means unread — `/health` checks it.

---

## Tasks

Every task below has a brief in `tasks/planned/<slug>/task.md`, so
**`/plan <slug>` always has somewhere to start.**

`/plan` moves it `planned/` → `active/`; `/complete` moves it → `completed/`.

### Phases — v1.0

| Slug | Phase | Description | Status |
|---|---|---|---|
| `01-foundation` | 1 | React + FastAPI running, resume extracted to `content/*.json`, tests wired | **done** — 2026-08-29 |
| `02-portfolio-ui` | 2 | All portfolio sections rendered from content — no AI yet | **done** — 2026-08-29 |
| `03-rag-assistant` | 3 | Resume-as-is cleanup, then chunking, embeddings, FAISS, providers, `/api/ai/chat` | done 2026-08-30 |
| `04-agentic-job-match` | 4 | Four-agent chain, `/api/ai/job-match`, Why Me? with honest gaps | done 2026-08-30 |
| `05-mcp-integration` | 5 | GitHub API + MCP server, From My GitHub, tool-sourced answers | done 2026-08-30 |
| `06-final-polish` | 6 | Engineer Mode, a11y, mobile, README, deploy to Vercel | brief ready |

Detail: [`docs/plan.md`](../docs/plan.md).

### Improvements

Non-phase work. Unnumbered, on `improvement/` or `fix/` branches.

| Slug | Description | Status |
|---|---|---|
| `visual-design` | Art direction + Evidence Explorer; re-skins Phase 2 before the AI phases build on it | done 2026-08-30 |

### Future candidates

Named so `/plan <slug>` resolves. No brief yet — `/plan` writes one.

`rag-visualizer` · `voice-assistant` · `semantic-project-search` ·
`github-ai-search` · `ai-project-recommender` · `contact-form` ·
`resume-versioning`

### Naming

`feature/<slug>` · `fix/<slug>` · `improvement/<slug>`. Task slug and branch
suffix are always identical, so task, branch and PR are traceable to each other.

**Phase tasks carry their phase number:** `01-foundation` … `06-final-polish`.
The number *is* the run order — the next phase to run is the lowest-numbered slug
not yet in `tasks/completed/`, and `ls harness/tasks/planned/` shows it sorted.
Non-phase work (the future candidates above, fixes, improvements) stays
unnumbered, so a leading number always means "this is a v1.0 phase".

---

## Maintaining this file

- **New skill** → add the file, add a row, name it in the agent's row.
- **New task** → add a row and a brief in `tasks/planned/` before `/plan`.
- **Task completes** → status `done` + date (`/complete` does this).

Keep it an index. Detail lives in the file being indexed.
