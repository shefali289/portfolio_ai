# Task: RAG Assistant — Ask My Portfolio

| | |
|---|---|
| **Slug** | `03-rag-assistant` |
| **Branch** | `feature/03-rag-assistant` |
| **Phase** | Phase 3 |
| **Status** | brief — not started |
| **Started / Completed** | — |

> **Brief only.** `/plan 03-rag-assistant` fills in Design, Plan and the rest. Every stage
> writes back here, so this file ends up holding the whole story. Do not
> implement from this file alone.

---

# 1 · Intent

## Feature

Grounded Q&A over portfolio content: chunking, embeddings, FAISS retrieval, the
generation and embedding provider abstractions, `POST /api/ai/chat`, and the Ask
My Portfolio UI with source citations.

## Goal

Answer real questions about Shefali's experience using only portfolio content,
with visible sources - so the AI is part of the product, not a demo.

## Acceptance Criteria

Refined at `/plan`, checked off at `/review`.

- [ ] "What AI experience does she have?" returns a grounded answer citing the
      AI Engineer role
- [ ] every answer renders source chips naming the projects or roles used
- [ ] **an out-of-scope question is refused, not answered** (grounding test)
- [ ] the index refuses to load when provider or dimension mismatches
- [ ] works end to end with `AI_PROVIDER=template` and no API key
- [ ] the endpoint returns retrieval and generation timings for Engineer Mode

## User Experience

Ask a question, see the answer arrive with source chips beneath. An unsupported
question is answered honestly: "I don't have evidence of that in the portfolio."

## Out of Scope

Job matching (Phase 4). GitHub or MCP (Phase 5). The Engineer Mode UI (Phase 6),
though the endpoint returns the metrics it will display.

---

# 2 · Design  *(Design Agent, `/plan`)*

_(seven questions — unanswered until `/plan`)_

## Existing Components Reused

`ContentService` for content. This phase creates the RAG service and both
provider abstractions that Phases 4-6 reuse.

## Rejected Alternatives

_(filled at `/plan`)_

---

# 3 · Plan  *(Planning Agent, `/plan`)*

## Implementation Steps

_(4–10 steps — filled at `/plan`)_

## Files Likely To Change

_(filled at `/plan`)_

## Skills Used

`rag-ingestion`, `ai-provider`, `api-endpoint`, `react-component`, `tdd-cycle`

---

# 4 · Tests  *(Test Agent, `/build`)*

## Tests First

- chunking produces `{text, source, type}` records covering every content file
- a known query retrieves the expected source
- **grounding: an out-of-scope question is refused** (mandatory)
- index refuses to load on provider/dimension mismatch
- endpoint returns answer + sources + timings
- provider falls back to `template` when the LLM is unavailable
- UI renders loading, error and empty states, and shows citations

## TDD Evidence

RED then GREEN. Tests written after the code fail G2 — the failure output is the
proof, and `final_checklist.py` checks for it.

| | |
|---|---|
| **RED - command** | — |
| **RED - failed for the right reason** | — |
| **GREEN - result** | — |

---

# 5 · Gates

See `harness/QUALITY-GATES.md`. `PARTIAL`/`SKIPPED` are honest; a check reported
`PASS` without running is not.

| Gate | When | Result | Date | Note |
|---|---|---|---|---|
| **G0** branch | before `/build` writes | — | | `branch_gate.py` |
| **G1** design | Design → Plan | — | | |
| **G2** test (RED) | Test → Develop | — | | failure output recorded |
| **G3** build (GREEN) | Develop → Review | — | | |
| **G4** review | Review → Complete | — | | tests · lint · typecheck · a11y |
| **G5** completion | before archive + PR | — | | `final_checklist.py` |

## Final Checklist  *(`/complete`)*

`python harness/scripts/final_checklist.py --slug 03-rag-assistant` — must exit 0.
Paste the result table, then confirm by hand:

- [ ] content traces to the resume; no invented experience
- [ ] AI answers cite sources; out-of-scope questions refused
- [ ] works at 375px and desktop
- [ ] loading, error and empty states reachable
- [ ] keyboard navigable; images have alt text

---

# 6 · Record

## Decisions Taken

| Date | Decision | Reason |
|---|---|---|

## User Overrides

Every entry must end in a promoted rule. Promoted to
`harness/learning/user-overrides.md` at `/complete`.

| Date | Agent proposed | User chose | Why | Rule now |
|---|---|---|---|---|

## Lessons Learned

- **Worked:**
- **Cost time:**
- **Do differently:**

## Known Limitations

_(filled at `/complete`)_

---

# 7 · Validation & PR  *(`/complete`)*

## Validation

Real results only. Not run = `SKIPPED`, never `PASS`.

| Check | Result |
|---|---|
| backend tests | — |
| frontend tests | — |
| lint | — |
| typecheck | — |
| manual check | — |

Re-ingest succeeds after a content change; answers cite real sources.

## PR Summary

| | |
|---|---|
| **Title** | — |
| **URL** | — |
| **Merged** | — |

**What it adds:** —

**Why:** —

## Suggested Commit Message

```
<type>: <description>
```
