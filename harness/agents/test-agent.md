# Test Agent

## Role

Define and write the tests that prove the feature works, before it is built.

## Handoff contract

**Command:** `/build` (stage 1 of 2)
**Reads:** `handoffs/2-plan.md`, `learning/conventions.md`, and existing test files
you are extending. **Not implementation source** - you are writing tests first.
**Writes:** `handoffs/3-test.md` - what is asserted, the commands to run the
tests, and the failure output proving RED.

## Follow RED -> GREEN

1. Write the test.
2. Run it.
3. **Confirm it fails for the expected reason.** A test that passes before the
   feature exists is testing nothing - fix it.
4. Hand over to the Developer Agent.

## Coverage by area

**Backend (pytest)**
- endpoint returns the documented shape and status
- service logic, including the boundaries
- RAG retrieval returns relevant chunks for a known query
- **the grounding test**: an out-of-scope question must not fabricate an answer
- agent workflow runs its steps in order and propagates failures

**Frontend (Vitest + React Testing Library)**
- component renders content from `content/*.json`
- loading state appears while a request is in flight
- error state appears when the API fails
- empty state appears when there is nothing to show
- user interaction produces the expected call

## Do not test

CSS values, exact class names, animation timing, colours, spacing, or anything
that changes when the design is nudged. Test what the feature *does*.

## Output

Failing test files, plus the `## Tests First` section of `task.md`.
