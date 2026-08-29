# Harness Rules

These apply to every agent, every phase, and every future feature.

## Process

1. **No code before a task exists.** `harness/tasks/active/<feature>/task.md`
   is written and agreed before any implementation file is touched.
2. **One active feature at a time.** Finish or park before starting another.
3. **Design -> Plan -> Test -> Develop -> Review -> Complete.** No skipping
   straight to Develop, even for small changes.
4. **Move the task directory to `completed/` when done.** That is the history.
4b. **Every stage hands off to the next** — it names what follows and asks
   whether to continue, rather than dead-stopping and telling the user which
   command to type. A handoff never approves a commit, never skips a blocking
   question and never relaxes a gate. See
   [`instructions/stage-handoff.md`](instructions/stage-handoff.md).

## Context

5. **Read the manifest, then memory, before exploring.** `AGENT-MANIFEST.md` resolves
   task names and indexes skills; `learning/` says how this codebase works. Only
   the Design Agent explores further, and only for what memory leaves open.
6. **Stay inside your read budget** (`HANDOFF-PROTOCOL.md`). Needing a file outside it is
   a planning gap — record it in the handoff rather than reading silently.
7. **Honour `Do NOT re-read`.** Re-opening settled files "to be safe" is the
   failure mode this whole protocol exists to prevent.
8. **Follow the skill, do not improvise it.** If a skill is wrong, fix the skill
   at `/complete` so the next feature inherits the correction.
9. **Every handoff stays under 60 lines.** Longer means the feature is too big.

## Git

10. **Never commit or push without asking.** Every commit and every push, on
    every branch. Stage the work, show the diff summary and the proposed
    message, then wait. Editing files is reversible; history is not.
11. **Never write to `main`.** Branch `feature/<slug>` matching the task slug.

## Architecture

12. **Extend, do not duplicate.** New capability goes into an existing area:

   | Area | Responsibility |
   |---|---|
   | `frontend/` | UI |
   | `backend/app/api/` | HTTP interface only - thin |
   | `backend/app/services/` | application behaviour |
   | `backend/app/rag/` | retrieval over stored knowledge |
   | `backend/app/ai/` | GenAI + provider abstraction |
   | `backend/app/agents/` | agent workflows |
   | `backend/app/integrations/` | GitHub / MCP / external tools |
   | `content/` | portfolio data (source of truth) |

13. **No new top-level systems** without a strong, stated reason.
14. **One RAG implementation, one generation abstraction, one embedding
    abstraction.** Ever.
15. **Keep RAG and tools distinct.** RAG retrieves stored knowledge; MCP/tools
   reach external or live capabilities. Adding a tool never reshapes RAG.

## Content integrity

16. **The resume is the source of truth.** Never invent experience, employers,
   dates, metrics or skills.
17. **Unknown information becomes an explicit `TODO` placeholder**, never a
    plausible-sounding guess.
18. **The AI must never claim experience absent from `content/`.** Answering
    "I don't have evidence of that in the portfolio" is a correct answer and is
    covered by a test.

## Implementation

19. **Smallest reasonable solution.** Simplicity is a feature.
20. **No unrelated refactoring** inside a feature branch.
21. **No new framework, database or AI library** unless the feature genuinely
    requires it. Adding one is a Design Agent decision, recorded in `task.md`.
22. **Content is rendered from `content/*.json`,** not hardcoded into components.

## Testing

23. **Write the test first** where practical: RED -> GREEN.
24. **Test behaviour, not styling.** Rendering, navigation, API interaction,
    loading / error / empty states, retrieval quality, agent workflow.
25. **Never commit with known-failing tests** without saying so explicitly.

## Explicitly out of scope for this project

Kubernetes, microservices, Kafka, Redis, heavyweight ORMs or databases,
authentication, large LangChain-style abstractions, event-driven architecture,
multiple deployed agents, PBIs, ADR sprawl, mandatory Docker.
