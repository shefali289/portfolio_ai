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

### 2026-08-29 - Harness setup and structure  *(condensed; rules live elsewhere)*

- **Agent proposed:** agents that inspect the repo per stage; terse file names.
- **User chose:** `/plan` as one entry point with explicit handoffs and a
  learning store; self-describing uppercase names; gates G0-G5 ending in a PR.
- **Why:** re-deriving context every stage scales badly, and the repo is an
  interview artefact where process discipline should be visible.
- **Rule now:** `HARNESS-RULES.md` rules 5-9, `HANDOFF-PROTOCOL.md` budgets,
  60-line handoffs, `QUALITY-GATES.md`.

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

### 2026-08-30 - Show the resume, assume nothing

- **Agent proposed:** an "Evidence" design presenting information about the
  content beside the content - derived counts, a skills coverage ratio,
  per-skill evidence expansion and `content/*.json` source labels.
- **User chose:** show the resume as it is; assume nothing beyond it.
- **Why:** the layer described the tool to the reader instead of showing them
  the resume, and several evidence links were the agent's inference rather than
  resume facts.
- **Rule now:** the UI renders resume content only - no derived statistic,
  coverage ratio, source label or inferred link presented as portfolio content.
  **Inferred data is deleted, not hidden.** Promoted to `conventions.md`.
