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

### 02-portfolio-ui - 2026-08-29
- **Worked:** One validated aggregate payload kept page state simple while pure
  semantic components made disclosures, filters, and evidence easy to verify.
- **Cost time:** Edge's minimum headless window masqueraded as mobile overflow,
  and the first regression response coupled tests to Tailwind classes.
- **Do differently:** Verify browser viewport metrics first, keep responsive
  checks manual, and seed aggregate fixtures with every simple section.

## visual-design (2026-08-30)

- **Worked:** a shared `@layer components` seam made a full re-skin a one-file
  change; 16 existing behaviour tests passed untouched, which is the proof it
  stayed presentation-only.
- **Cost time:** orphaned dev servers on 5173-5175 and port 8000 served stale
  code during verification and produced misleading responses.
- **Do differently:** compute contrast rather than trusting the eye. Eleven
  token pairs looked fine and were; the twelfth looked fine and was a real
  WCAG AA failure on the primary button.
- **Do differently:** state honestly when a test was not RED. One new test
  passed on write because the behaviour already existed; it is a regression
  guard and the gate says PARTIAL rather than implying evidence it lacks.

## 03-rag-assistant (2026-08-30)

- **Worked:** deleting inferred data rather than hiding it. Removing `evidence`
  from `skills.json` simplified the schema, the service and the tests together.
- **Cost time:** orphaned dev servers. A uvicorn child outlived its killed
  parent and held port 8000, serving code without the new route; it read as a
  routing bug for several rounds.
- **Do differently:** verify the tool before believing its output. A "375px
  overflow" that stood for three tasks was Chrome headless clamping to a 500px
  minimum window and cropping the screenshot - not a layout bug at all.
- **Do differently:** when adding a provider, document it in the same change.
  The review caught `hashing` being the silent default with nothing describing it.
