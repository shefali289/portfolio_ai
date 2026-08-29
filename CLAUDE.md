# AI-Powered Engineer Portfolio

React + TypeScript + Vite frontend, FastAPI backend, RAG/agents/MCP AI features.
`content/*.json` grounds both the UI and the AI.

## Read AGENTS.md first

**[`AGENTS.md`](AGENTS.md) is the entry point** — lifecycle, commands, gates and
the non-negotiable rules. It applies to every agent working here, Claude
included. This file adds only what is specific to Claude Code.

## Commands

Slash commands live in `.claude/skills/`, each `disable-model-invocation` — they
run only when you type them:

```
/plan <slug>   /build   /review   /complete   /status   /health
```

Task slugs and their briefs: `harness/AGENT-MANIFEST.md`.

## Reading order — stop when answered

1. `harness/context/current-task.md` — what is in flight, one small file
2. `harness/AGENT-MANIFEST.md` — **your row only**, not the whole file
3. `harness/learning/` — how this codebase works; **read this instead of
   exploring the repo**
4. Your stage's handoff, plus only the files and skills it names

Honour each handoff's `Do NOT re-read`. Budgets: `harness/HANDOFF-PROTOCOL.md`.

## Environment

Windows + Git Bash. Python 3.14.7 (CI uses 3.12 — verify wheels resolve before
pinning), Node 24, `uv` for Python envs. `gh` is installed but needs a one-off
`gh auth login`. No Ollama, no Docker.

**Long chained heredocs fail in this shell** — one mismatched terminator
swallows the rest and the whole command dies. Write files one at a time, or
generate them from a script file.

Full gotchas: `harness/learning/gotchas.md`.
