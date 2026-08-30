# Handoff: Design -> Planning

## Done
A four-function chain in `app/agents/`, one endpoint, one component. Everything
it needs already exists: Phase 3 built retrieval, both provider abstractions and
the grounded-refusal pattern. This phase adds no new system.

## You need to know

1. **The chain is four plain functions, composed — not a framework.** Rule 21
   and the brief both exclude one. Each agent is typed in, typed out (Pydantic),
   and independently testable:
   `requirement -> portfolio -> evidence -> response`.
2. **Reuse `Retriever`. Never build a second search path.** The portfolio agent
   calls the existing RAG service through `AiService`'s retriever, so job-match
   and Ask My Portfolio always retrieve identically.
3. **Honest gaps are the feature.** A requirement with no retrieved evidence is
   reported as a **gap**, never softened into a partial match. This is the same
   guarantee as Phase 3's refusal, applied per requirement, and it is decided by
   the retrieval score — not by asking the model to be honest.
4. **Requirement extraction must work with no LLM.** `AI_PROVIDER=template` is
   the default, so `requirement_agent` needs a deterministic fallback: match the
   JD against the skill vocabulary already in `content/skills.json` rather than
   depending on generation. With a key, the LLM extracts; without, the lexical
   path still produces a usable list.
5. **Progress is returned, not streamed.** SSE/WebSocket would be a new
   transport for one feature. The response carries a `steps` array with each
   agent's name, status and duration; the UI animates through them. Phase 6 owns
   Engineer Mode if live streaming is ever wanted.
6. **A failing step propagates.** No partial result: if an agent raises, the
   endpoint returns an error rather than a half-filled report. Provider
   *unavailability* still degrades to `template` as before — that is not a step
   failure.

## Files
- `backend/app/agents/{__init__,base,requirement,portfolio,evidence,response,chain}.py`
- `backend/app/services/job_match.py` — orchestration, held on app state
- `backend/app/api/{routes,schemas}.py` — `POST /api/ai/job-match`
- `backend/tests/test_agents.py`, `tests/test_job_match_api.py`
- `frontend/src/components/JobMatch{,.test}.tsx`, `src/lib/api.ts`,
  `src/types/content.ts`, `src/App.tsx` (one new section)

## Do NOT re-read
`app/rag/*` and `app/ai/*` — Phase 3 settled them; call `Retriever.retrieve` and
`resolve_provider` as they are. `index.css` is untouched: the chain UI uses the
existing `.section-card`, `.tag`, `.button-primary` classes.

## Open questions
None. The design follows the brief and the `agent-workflow` skill exactly.

## New learnings
- The grounded-refusal pattern generalises: Phase 3 refuses a whole question,
  Phase 4 refuses a single requirement. Same threshold, same guarantee.
