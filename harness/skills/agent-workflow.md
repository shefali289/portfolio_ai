# Skill: Add an Agent to a Workflow

**Used by:** Developer Agent
**When:** extending the job-match chain in `app/agents/`

## Steps

1. **One responsibility.** If it needs "and" to describe, it is two agents.
2. **Typed in, typed out** - Pydantic models. The chain is composed of
   functions, not a framework.
3. **Place it** in the sequence: requirement -> portfolio -> evidence -> response.
4. **Reuse retrieval** - the portfolio agent calls the existing RAG service.
   Never build a second search path.
5. **Evidence rule** - no evidence means the agent reports a gap. It must never
   soften a gap into a partial match. Honest gaps are the feature.
6. **Emit progress** so the UI can show the step ticking over.
7. **Test** the agent alone, then the chain: order preserved, failure propagates
   rather than silently returning a partial result.

## Done when

Each step is independently testable, the UI shows real progress, and a genuine
gap is reported as a gap.
