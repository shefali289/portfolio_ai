# AI-Powered Engineer Portfolio

A personal portfolio where AI features are part of the product, not demos bolted
onto the side — built with an AI development harness that is itself part of the
portfolio.

**Status:** scaffolded. Phase 1 not started. Run `/plan foundation` to begin.

---

## Part 1 — The Product

The same structured content that renders the site also grounds every AI answer.

| Feature | What it does | Demonstrates |
|---|---|---|
| **Ask My Portfolio** | Grounded Q&A over resume and projects, with citations | RAG, GenAI |
| **Why Me?** | Paste a job description → matches, evidence, honest gaps | Agentic AI |
| **From My GitHub** | Live repositories as an external context source | MCP / tool calling |
| **Engineer Mode** | Endpoint, chunks retrieved, retrieval and generation timings | Transparency |
| **Built With AI Engineering** | The harness that built this repo | Agentic SDLC |

### Why the AI is not a demo

```
content/*.json  ──┬──> ContentService ──> REST ──> Portfolio UI
                  │
                  └──> chunk + embed ──> FAISS ──> Ask My Portfolio
                                                   Why Me?
                                                   agent workflow
```

One source of truth feeds both. That is what makes the assistant *unable* to
claim experience the resume does not contain — and a grounding test enforces it.

### Stack

**Frontend** React · TypeScript · Vite · Tailwind · Motion
**Backend** Python 3.14 · FastAPI · Pydantic
**AI** Gemini (free tier) · FAISS · pluggable generation + embedding providers
**Tests** pytest · Vitest · React Testing Library
**Tooling** MCP Python SDK · GitHub public API

Free and open-source throughout. Runs with no API key and no LLM installed.

### Quick start

```bash
cd backend  && uv venv && uv pip install -r requirements.txt && uvicorn app.main:app --reload
cd frontend && npm install && npm run dev
```

Full detail: [docs/setup.md](docs/setup.md).

---

## Part 2 — The Harness

Every line of this project was built through a lightweight AI development
harness in [`harness/`](harness/). It is deliberately small: six roles operating
over one repository, plus the files that let them hand work to each other
without re-reading it.

```
Design ──> Plan ──> Test ──> Develop ──> Review ──> Complete
  G1        G1      G0,G2      G3          G4         G5
```

### Commands

| Command | Does | Writes |
|---|---|---|
| `/plan <task>` | Design + Planning | `task.md`, handoffs 1–2 |
| `/build` | Test (RED) → Develop (GREEN) | handoffs 3–4 |
| `/review` | Verifies — never extends | handoff 5 |
| `/complete` | Report, learn, PR, archive | `completion.md`, `pull-request.md` |
| `/status` | Where the active feature stands | — |
| `/health` | Whether the harness itself has rotted | — |

`/plan foundation`, `/plan rag-assistant` — every task name has a brief already
waiting in `harness/tasks/planned/`.

### How it ties together

```
              AGENT-MANIFEST.md
         the index: agents · skills · tasks
                      │
   ┌──────────────────┼──────────────────┐
   ▼                  ▼                  ▼
agents/            skills/           tasks/
five roles      reusable how-to    planned → active → completed
   │                  │                  │
   └────── handoffs 1..5 between ────────┘
                      │
                      ▼
                 learning/
        read at /plan · written at /complete
```

- **[`AGENT-MANIFEST.md`](harness/AGENT-MANIFEST.md)** — the index. Which agent
  reads what, uses which skills, writes which handoff; every task name.
- **[`agents/`](harness/agents/)** — five roles. Design decides, Planning
  sequences, Test writes failing tests, Developer makes them pass, Review
  verifies.
- **[`skills/`](harness/skills/)** — reusable procedures (add an endpoint, add a
  component, ingest content). Agents follow them instead of improvising.
- **[`HANDOFF-PROTOCOL.md`](harness/HANDOFF-PROTOCOL.md)** — how work passes
  between agents, and each agent's read budget.
- **[`learning/`](harness/learning/)** — what the harness knows.
- **[`QUALITY-GATES.md`](harness/QUALITY-GATES.md)** — G0–G5.

### How learning works

This is the mechanism that matters most.

```
during a feature   each handoff carries "New learnings"
                              │
/complete          promote ───┴──> learning/     and prune
                              │
/plan (next)       Design reads learning/ INSTEAD of exploring the repo
```

| File | Holds | Cap |
|---|---|---|
| `architecture-map.md` | where things live, seams to extend | 150 |
| `conventions.md` | patterns to copy | 150 |
| `decisions.md` | choices made **and rejected**, with reasons | 150 |
| `gotchas.md` | what broke, why, the fix | 150 |
| `lessons-learned.md` | per feature: what to do differently | 100 |
| `user-overrides.md` | where the user corrected the harness | 80 |

**Why it exists:** exploring the repository costs tokens proportional to repo
size, per agent, per feature, forever. Reading a pruned digest is flat — and it
*improves* as the project grows.

**Why the caps are enforced:** learning that is not pruned is learning that is
not read. `/health` reports any file over cap.

**Why `user-overrides.md` matters most:** an override means an agent's default
was wrong for this project. Unrecorded, it gets repeated on the next feature.
Every entry must end in a promoted rule.

### How context stays small

| Agent | Reads | Never reads |
|---|---|---|
| Design | `learning/*`, the task, files learning points at | the repo blindly |
| Planning | handoff 1 | source files |
| Test | handoff 2, conventions | implementation |
| Developer | handoffs 2–3, only files the plan names | anything unplanned |
| Review | handoff 4, the diff | untouched files |

Each handoff is capped at **60 lines** and carries a `Do NOT re-read` section —
explicit permission to skip settled ground. Without it, agents re-open files
"to be safe" and the budget leaks silently.

### How quality is enforced

| Gate | When | Blocks on |
|---|---|---|
| **G0 branch** | before any write | on `main`, or branch ≠ task slug |
| **G1 design** | Design → Plan | unanswered questions, unjustified dependency |
| **G2 test** | Test → Develop | tests that did not fail for the right reason |
| **G3 build** | Develop → Review | unplanned file changes, hardcoded content |
| **G4 review** | Review → Complete | failing tests, lint, typecheck, a11y |
| **G5 done** | before archive + PR | unmet requirements, unpruned learning |

A check that did not run is recorded `SKIPPED`, never `PASS`.

Every feature ends in a PR body carrying the gate table, lessons learned and
user overrides — see [`templates/pull-request.md`](harness/templates/pull-request.md).

### Executable gates

```bash
python harness/scripts/branch_gate.py --slug <slug> --rebase   # G0
python harness/scripts/health_check.py                          # structural
python harness/scripts/final_checklist.py --slug <slug>         # G5
```

`final_checklist.py` decides whether a task is complete. It re-runs both test
suites, demands **real RED evidence** in the test handoff (so tests written
after the code fail the gate), and checks lint, typecheck, content parsing, the
gate log, learning updates and the completion docs. A task is not done until it
exits 0 — then it prints the checks that cannot be automated for confirmation by
hand.

### Continuous integration

| Workflow | Runs on | Does |
|---|---|---|
| `harness-health.yml` | push to `main`, PRs touching docs | `harness/scripts/health_check.py` — 13 structural checks |
| `pr-checklist.yml` | every PR into `main` | branch gate, harness health, gate log, secret scan, backend (`ruff`/`pytest`), frontend (`tsc`/lint/`vitest`/build), then the rendered final checklist |

Application jobs skip cleanly until that side exists, and report `SKIPPED`
rather than passing. `python harness/scripts/health_check.py` is the same check CI runs.

### Adding a feature later

The harness does not change; only a new task directory is added.

```
/plan semantic project search    → brief, design, plan
/build                           → RED, then GREEN
/review                          → gates
/complete                        → learn, PR, archive
```

---

## Docs

| Doc | Covers |
|---|---|
| [Setup](docs/setup.md) | installing and running |
| [Architecture](docs/architecture.md) | system design and request flows |
| [Plan](docs/plan.md) | the six phases |
| [Deployment](docs/deployment.md) | hosting, and why it shapes the AI providers |
| [Harness](harness/README.md) | the development workflow |

## Contact

Shefali Sharma · [LinkedIn](https://www.linkedin.com/in/shefali--sharma/) · [GitHub](https://github.com/shefali289)
