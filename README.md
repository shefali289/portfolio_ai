# AI-Powered Engineer Portfolio

A personal portfolio where AI features are part of the product, not demos bolted
onto the side — built with an AI development harness that is itself part of the
portfolio.

**Status:** all six phases built. Portfolio UI, grounded RAG assistant, agentic
job match, live GitHub + MCP tools and Engineer Mode are implemented and tested
(backend 79, frontend 53). Deployment config is written; the deploy itself has
not been run — see [`docs/deployment.md`](docs/deployment.md).

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

Full detail: [docs/setup.md](docs/setup.md) · canonical commands:
[harness/context/execution-commands.md](harness/context/execution-commands.md)

---

## Part 2 — The Harness

Every line of this project is built through a lightweight AI development harness
in [`harness/`](harness/): five specialised roles over one repository, six
quality gates, and the files that let agents hand work to each other without
re-reading the codebase.

```
Design ──> Plan ──> Test ──> Develop ──> Review ──> Complete
  G1        G1     G0,G2      G3          G4         G5
```

### Commands

| Command | Does | Writes |
|---|---|---|
| `/plan <slug>` | Design + Planning | `task.md`, handoffs 1–2 |
| `/build` | Test (RED) → Develop (GREEN) | handoffs 3–4 |
| `/review` | Verifies — never extends | handoff 5 |
| `/complete` | Report, learn, PR, archive | `completion.md`, `pull-request.md` |
| `/status` | Where the active feature stands | — |
| `/health` | Whether the harness itself has rotted | — |

`/plan 01-foundation`, `/plan 03-rag-assistant` — every task name has a brief already
waiting in `harness/tasks/planned/`.

### Entry points

| File | For |
|---|---|
| [`AGENTS.md`](AGENTS.md) | **any coding agent** — lifecycle, commands, gates, rules |
| [`.agent-manifest.json`](.agent-manifest.json) | machine-readable index; CI validates every path in it |
| [`CLAUDE.md`](CLAUDE.md) | Claude Code specifics |
| [`.github/copilot-instructions.md`](.github/copilot-instructions.md) | GitHub Copilot specifics |
| [`harness/AGENT-MANIFEST.md`](harness/AGENT-MANIFEST.md) | the human index — agent × skill × handoff × task |

`AGENTS.md` states the rules once; the others point at it rather than restating
them.

### How it ties together

```
              AGENTS.md  +  .agent-manifest.json
              rules & entry      machine index
                          │
   ┌──────────────┬───────┴───────┬──────────────┐
   ▼              ▼               ▼              ▼
agents/       skills/       instructions/     tasks/
five roles   how-to packs   gate policy    planned→active→completed
   │              │               │              │
   └────── handoffs 1..5 between stages ─────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
          learning/               scripts/
   read at /plan, written      executable gates,
      at /complete             same locally and in CI
```

### How learning works

The mechanism that matters most.

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
not read. `/health` fails any file over cap.

**Why `user-overrides.md` matters most:** an override means an agent's default
was wrong for this project. Unrecorded, it gets repeated. Every entry must end
in a promoted rule.

### How context stays small

| Agent | Reads | Never reads |
|---|---|---|
| Design | `learning/*`, the task, files learning points at | the repo blindly |
| Planning | handoff 1 | source files |
| Test | handoff 2, conventions | implementation |
| Developer | handoffs 2–3, only files the plan names | anything unplanned |
| Review | handoff 4, the diff | untouched files |

Handoffs are capped at **60 lines** and carry a `Do NOT re-read` section —
explicit permission to skip settled ground. `harness/context/current-task.md` is
a one-file pointer to what is in flight, so no agent walks the task tree.

### How quality is enforced

| Gate | Blocks on | Enforced by |
|---|---|---|
| **G0** branch | on `main`, or branch ≠ task slug | `scripts/branch_gate.py` |
| **G1** design | unanswered questions, untestable criteria | `instructions/design-gate.md` |
| **G2** test | tests that did not fail for the right reason | RED output in `3-test.md` |
| **G3** build | unplanned changes, hardcoded content | tests green |
| **G4** review | failing tests, lint, typecheck, a11y, secrets | `pr-checklist.yml` |
| **G5** done | unmet criteria, unpruned learning, missing PR | `scripts/final_checklist.py` |

Plus a standing **approval gate** ([`instructions/approval-gate.md`](harness/instructions/approval-gate.md)):
destructive git, anything outward-facing, new dependencies, or content not
backed by the resume — stop and ask.

A check that did not run is recorded `SKIPPED`, never `PASS`.

```bash
python harness/scripts/branch_gate.py --slug <slug> --rebase   # G0
python harness/scripts/health_check.py                          # 14 structural checks
python harness/scripts/final_checklist.py --slug <slug>         # G5, must exit 0
```

`final_checklist.py` decides whether a task is complete. It re-runs both suites
rather than trusting an earlier claim, and demands **real RED evidence** — tests
written after the code fail the gate.

### One task, one record

`harness/tasks/<slug>/task.md` accumulates the whole story in seven sections:
intent with testable acceptance criteria · design · plan · tests with RED/GREEN
evidence · gates G0–G5 · decisions, user overrides and lessons learned ·
validation and PR summary.

Handoffs are small and disposable. The task doc is the durable artefact, and it
archives to `harness/tasks/completed/` as the development history.

### Continuous integration

| Workflow | Runs on | Does |
|---|---|---|
| `harness-health.yml` | push to `main`, docs PRs | 14 structural checks |
| `pr-checklist.yml` | every PR into `main` | branch gate, harness health, gate log, secret scan, backend, frontend, rendered checklist |

Application jobs skip cleanly until that side exists and report `SKIPPED` rather
than passing.

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
| [Harness](harness/README.md) | how the development workflow is built |

## Contact

Shefali Sharma · [LinkedIn](https://www.linkedin.com/in/shefali--sharma/) · [GitHub](https://github.com/shefali289)
