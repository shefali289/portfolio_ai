# User Overrides

Where Shefali corrected the harness. **The highest-value learning signal here** -
an override means an agent's default was wrong for this project, and left
unrecorded it will be repeated on the next feature.

Record an override whenever the user rejects, reverses or materially changes an
agent's decision, choice of approach, or output.

## Format

`### <date> - <feature>`, then **Agent proposed** / **User chose** / **Why** /
**Rule now**. Every entry must end in a rule promoted somewhere durable
(`conventions.md`, `decisions.md`, a skill, `HARNESS-RULES.md`) — an override
recorded but not promoted will be made again. **Cap: 80 lines.**

---

### 2026-08-29 - Harness setup

- **Agent proposed:** a five-agent lifecycle where each agent inspects the
  repository for the context it needs.
- **User chose:** `/plan` as a single entry point, explicit handoffs between
  agents, and a learning store so context is not re-sent per task.
- **Why:** re-deriving context every stage burns tokens and scales badly - cost
  would grow with repo size, agent count and feature count together.
- **Rule now:** read budgets per agent (`HANDOFF-PROTOCOL.md`), handoffs capped
  at 60 lines, `learning/` read before exploring. Promoted to
  `HARNESS-RULES.md` rules 5-9.

### 2026-08-29 - Harness structure

- **Agent proposed:** terse file names (`manifest.md`, `rules.md`, `memory/`).
- **User chose:** self-describing names - `AGENT-MANIFEST.md`,
  `HARNESS-RULES.md`, `learning/` - plus quality gates, branch gate, PR on
  completion, and a harness health check.
- **Why:** the repo is an interview artefact. A stranger should understand the
  structure from the file names alone, and process discipline should be visible
  rather than implied.
- **Rule now:** top-level harness docs use uppercase self-describing names; every
  feature passes G0-G5 and ends in a PR. See `QUALITY-GATES.md`.

### 2026-08-29 - Commit and push approval

- **Agent proposed:** treating local commits on a feature branch as safe to make
  without asking, and pushing once the user had approved a push earlier.
- **User chose:** ask every time, before every commit and every push.
- **Why:** approval for one push is not approval for the next. History is shared
  and hard to undo once pulled; a file edit is not.
- **Rule now:** `HARNESS-RULES.md` rule 10, `instructions/approval-gate.md`
  (moved from "decide without asking" to "always ask"), and the commit steps in
  `/build` and `/complete` now stage and propose rather than execute.

### 2026-08-29 - Foundation privacy boundary

- **Agent proposed:** keep the resume phone number in `docs/resume.md` while
  excluding it only from publicly served `content/`.
- **User chose:** redact it and rewrite local history before any push.
- **Why:** a public repository exposes documentation as effectively as an API;
  excluding data from one surface does not make it private.
- **Rule now:** personal data intentionally excluded from public content must
  also be excluded from docs and reachable git history. Promoted to
  `harness/learning/conventions.md`.

### 2026-08-30 - Design quality is a deliverable

- **Agent proposed:** four options, including leaving the plain Phase 2 layout
  as-is, and treating visual design as optional polish.
- **User chose:** redesign now, before the AI phases, and make the UI/UX
  genuinely distinctive.
- **Why:** a default-looking portfolio undercuts the work it presents, and
  Phases 3-5 build UI on top of whatever exists.
- **Rule now:** a phase that ships UI must state its **art direction**, not only
  its structure. "Renders correctly" is not "designed", and no phase plan should
  leave visual design unowned.
