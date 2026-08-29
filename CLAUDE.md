# AI-Powered Engineer Portfolio

React + TypeScript + Vite frontend, FastAPI backend, RAG/agents/MCP AI features.
`content/*.json` grounds both the UI and the AI.

## Work through the harness

No implementation without an active task.

```
/plan <task>   Design + Planning          G1
/build         Test RED -> Develop GREEN  G0, G2, G3
/review        Verify only, never extend  G4
/complete      Report, learn, PR, archive G5
/status        Where the active feature stands
/health        Whether the harness itself has rotted
```

Task names live in `harness/AGENT-MANIFEST.md`; each has a brief in
`harness/tasks/planned/`. `/plan foundation`, `/plan rag-assistant`.

## Read in this order — stop when answered

1. `harness/AGENT-MANIFEST.md` — **your row only**, not the whole file
2. `harness/learning/` — how this codebase works. **Read this instead of
   exploring the repo.** Explore only what it does not cover.
3. Your stage's handoff in `harness/tasks/active/<slug>/handoffs/`
4. Only the files and skills that handoff names

Honour each handoff's `Do NOT re-read`. Re-opening settled files "to be safe" is
the failure mode the protocol exists to prevent. Read budgets:
`harness/HANDOFF-PROTOCOL.md`.

## Gates

G0 branch · G1 design · G2 test (RED) · G3 build (GREEN) · G4 review · G5 done.
A stage cannot start until the previous gate passes. Record every result in the
task's `## Gate Log`. See `harness/QUALITY-GATES.md`.

## Non-negotiables

- **Never write to `main`.** Branch `feature/<slug>`, slug matching the task.
- **The resume is the source of truth.** Never invent experience, employers,
  dates, metrics or skills. Unknowns are explicit `TODO` placeholders.
- **The AI must never claim experience absent from `content/`.** "No evidence in
  the portfolio" is a correct answer, and a test enforces it.
- **RED first** — write the test, run it, confirm it fails for the right reason.
- **Never report a check as passing without running it.** Not run = `SKIPPED`.
- **Never claim a PR was created when it was not.**
- **Extend, do not duplicate.** One RAG implementation, one generation
  abstraction, one embedding abstraction.
- Content renders from `content/*.json`, never hardcoded into components.

## Learning

At `/complete`, promote each handoff's `New learnings` into `harness/learning/`
and prune. User overrides matter most — an override means a default was wrong
for this project, and unrecorded it gets repeated.

## Environment

Windows + Git Bash. Python 3.14.7 (verify wheels resolve before pinning), Node
24, `uv` for Python envs. No Ollama, Docker or `gh` installed; no git remote yet.
Long chained heredocs fail here — write files one at a time.

Full rules: `harness/HARNESS-RULES.md`.
