# Lessons Learned

One entry per completed feature. What we would do differently.

Written at `/complete` from the handoffs' `## New learnings`. Read by the Design
Agent at `/plan` - so keep it short enough to actually be read.

## Format

```markdown
### <slug> - <date>
- **Worked:** what to repeat
- **Cost time:** what to avoid
- **Do differently:** the concrete change next time
```

Promote anything durable into `conventions.md`, `gotchas.md` or a skill, then
keep only the one-line summary here. This file is a log; the others are the
digest.

**Cap: 100 lines.** Trim oldest entries whose lessons have been promoted.

---

### 01-foundation - 2026-08-29
- **Worked:** Schema-first content and RED tests produced stable seams shared by
  the UI, future RAG ingestion, and MCP without inventing resume claims.
- **Cost time:** Non-interactive scaffolding, interpreter selection, and package
  peer-range mismatches created avoidable setup churn.
- **Do differently:** Resolve tool versions first and apply privacy boundaries
  consistently to content, documentation, and git history.
