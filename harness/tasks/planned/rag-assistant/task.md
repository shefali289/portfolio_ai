# Task: RAG Assistant - Ask My Portfolio

`/plan rag-assistant`  ·  branch `feature/rag-assistant`  ·  Phase 3

> **Brief only.** `/plan` fills in Design, Implementation Steps and Tests First.
> Do not implement from this file alone.

## Feature

Grounded Q&A over portfolio content: chunking, embeddings, FAISS retrieval,
the provider abstractions, `POST /api/ai/chat`, and the Ask My Portfolio UI
with source citations.

## Goal

Answer real questions about Shefali's experience using only portfolio content,
with visible sources - so the AI is part of the product, not a demo.

## User Experience

Ask a question, see the answer stream in with source chips beneath naming the
projects or roles it came from. An unsupported question is answered honestly:
"I don't have evidence of that in the portfolio."

## Reuses

`ContentService` for content. Nothing else exists yet - this phase creates the
RAG service and both provider abstractions that Phases 4-6 reuse.

## Tests First (outline)

- chunking produces `{text, source, type}` records covering every content file
- a known query retrieves the expected source ("AI experience" -> AI Engineer role)
- **grounding test: an out-of-scope question is refused, not answered** (mandatory)
- index refuses to load when provider or dimension does not match
- endpoint returns answer + sources + timing metrics
- provider falls back to `template` when the LLM is unavailable
- UI renders loading, error and empty states, and shows citations

## Skills

`rag-ingestion`, `ai-provider`, `api-endpoint`, `react-component`, `tdd-cycle`

## Validation

"What AI experience does she have?" returns a grounded, cited answer. Works with
`AI_PROVIDER=template` and no API key. Re-ingest succeeds after a content change.

## Out of Scope

Job matching (Phase 4). GitHub or MCP (Phase 5). Engineer Mode UI (Phase 6) -
though the endpoint returns the metrics it will display.

## Gate Log

_(filled during the lifecycle - see `harness/QUALITY-GATES.md`)_

- G0 branch  ·  G1 design  ·  G2 test  ·  G3 build  ·  G4 review  ·  G5 done

## Decisions Taken

_(appended as the lifecycle runs: what was decided and why)_

## PR

_(written at `/complete` from `harness/templates/pull-request.md`)_
