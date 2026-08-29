# Task: Agentic Job Match - Why Me?

`/plan agentic-job-match`  ·  branch `feature/agentic-job-match`  ·  Phase 4

> **Brief only.** `/plan` fills in Design, Implementation Steps and Tests First.
> Do not implement from this file alone.

## Feature

A four-agent sequential workflow - requirement, portfolio, evidence, response -
behind `POST /api/ai/job-match`, with a UI showing each step as it runs.

## Goal

Demonstrate decomposed agent responsibilities rather than one giant prompt, and
produce an honest match report a recruiter would find useful.

## User Experience

Paste a job description. Four steps tick over live: Understanding role, Searching
portfolio, Finding evidence, Preparing response. Output lists strong matches with
evidence, and gaps stated plainly as gaps.

## Reuses

The RAG retrieval service from `rag-assistant` - the portfolio agent calls it.
No second search path. `AIProvider` unchanged.

## Tests First (outline)

- requirement agent extracts skills from a sample JD
- portfolio agent returns evidence per requirement via existing retrieval
- **evidence agent reports a gap when there is no evidence - never softens it**
- response agent composes from evidence only, inventing nothing
- chain runs in order; a failing step propagates rather than returning partial
- UI shows progress, and the final report with matches and gaps

## Skills

`agent-workflow`, `api-endpoint`, `react-component`, `tdd-cycle`

## Validation

A pasted JD yields matches with evidence and honest gaps. A JD demanding an
absent skill (e.g. Kubernetes) reports it as a gap.

## Out of Scope

Parallel agents, an agent framework, persistence of past matches.

## Gate Log

_(filled during the lifecycle - see `harness/QUALITY-GATES.md`)_

- G0 branch  ·  G1 design  ·  G2 test  ·  G3 build  ·  G4 review  ·  G5 done

## Decisions Taken

_(appended as the lifecycle runs: what was decided and why)_

## PR

_(written at `/complete` from `harness/templates/pull-request.md`)_
