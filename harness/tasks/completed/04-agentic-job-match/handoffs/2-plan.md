# Handoff: Planning -> Test

## Done
Eight steps: agents bottom-up, then the chain, then the endpoint, then the UI.
Step 2 is the RED gate. No new dependency, no new top-level system.

## You need to know

1. **Write the agents in dependency order** — `base` types first, then each
   agent against those types. Every agent is a function `(input) -> output`
   with Pydantic models on both sides; the chain just composes them.
2. **`portfolio_agent` takes the retriever as an argument.** Do not let it
   construct one, or tests reach the network and the second-search-path rule is
   broken by accident.
3. **`evidence_agent` decides gap vs match on the retrieval score**, reusing
   `GROUNDING_THRESHOLD`. It never asks a model whether the evidence is good
   enough — that is how gaps get softened.
4. **`requirement_agent` needs the no-LLM path first.** Build the lexical
   extraction (match the JD against the skill vocabulary from `ContentService`)
   and test it; the LLM path is an enhancement layered on top, not the baseline.
5. **The chain records steps as it goes** — name, status, ms — and returns them.
   The failure test asserts a raising agent propagates and no partial report is
   returned.
6. **Existing tests must stay green.** 27 backend, 24 frontend. Nothing in this
   phase changes Phase 3's behaviour.

## Steps
1. `app/agents/base.py` — `Requirement`, `RequirementMatch`, `JobMatchReport`, `AgentStep` (`agent-workflow`)
2. **RED** — `tests/test_agents.py` + `tests/test_job_match_api.py` (`tdd-cycle`)
3. `agents/requirement.py` — lexical extraction from the skill vocabulary, LLM path optional (`agent-workflow`)
4. `agents/portfolio.py` — retrieve per requirement via the injected `Retriever` (`agent-workflow`)
5. `agents/evidence.py` — match / partial / **gap** by score; never soften (`agent-workflow`)
6. `agents/response.py` + `agents/chain.py` — compose, record steps, propagate failure (`agent-workflow`)
7. `services/job_match.py` + `POST /api/ai/job-match` in `routes.py`/`schemas.py` (`api-endpoint`)
8. `JobMatch.tsx` + `lib/api.ts` + one `App.tsx` section; full validation incl. 375px (`react-component`, `a11y-responsive`)

## Files
See `## Files Likely To Change` in `task.md`. `index.css` is not touched — the
UI reuses the existing component classes.

## Do NOT re-read
`1-design.md`; `app/rag/*`; `app/ai/*`. Phase 3's retrieval and providers are
settled — call them.

## Open questions
None.

## New learnings
Pending. The interesting one will be whether the lexical requirement extraction
is good enough to make the feature demonstrable with no API key.
