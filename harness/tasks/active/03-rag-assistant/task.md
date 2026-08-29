# Task: RAG Assistant — Ask My Portfolio

| | |
|---|---|
| **Slug** | `03-rag-assistant` |
| **Branch** | `feature/03-rag-assistant` |
| **Phase** | Phase 3 |
| **Status** | built — G0-G3 passed, awaiting `/review` |
| **Started / Completed** | 2026-08-30 / — |

> **Brief only.** `/plan 03-rag-assistant` fills in Design, Plan and the rest. Every stage
> writes back here, so this file ends up holding the whole story. Do not
> implement from this file alone.

---

# 1 · Intent

## Feature

Two parts.

**A · Resume as it is.** Remove the evidence/provenance layer added by
`visual-design` — derived counts, "N of M skills evidenced", per-skill evidence
expansion, and the `content/*.json` source footers. The app shows what the
resume says and assumes nothing beyond it.

**B · RAG assistant.** Grounded Q&A over portfolio content: chunking,
embeddings, FAISS retrieval, the generation and embedding provider
abstractions, `POST /api/ai/chat`, and the Ask My Portfolio UI.

## Goal

**A:** the portfolio should present the resume, not commentary about the
resume. The provenance layer described the tool to the reader instead of showing
them the content, and several of its links were inferred rather than stated.

**B:** answer real questions about Shefali's experience using only portfolio
content — so the AI is part of the product, not a demo, and cannot claim
experience the resume does not contain.

## Acceptance Criteria

Refined at `/plan`, checked off at `/review`.

**Part A**
- [ ] no derived counts, coverage line, evidence expansion or `content/*.json`
      footer appears anywhere in the UI
- [ ] skills render as plain grouped lists, exactly as the resume categorises them
- [ ] `skills.json` carries no inferred `evidence` refs and no `todo` authoring notes
- [ ] the design system, dark scheme, timeline and project cards are unchanged

**Part B**
- [ ] "What AI experience does she have?" returns a grounded answer drawn from
      the AI Engineer role
- [ ] **an out-of-scope question is refused, not answered** (grounding test)
- [ ] the index refuses to load when provider or dimension mismatches
- [ ] works end to end with `AI_PROVIDER=template` and no API key
- [ ] the endpoint returns retrieval and generation timings for Engineer Mode

## User Experience

The portfolio reads as a resume: sections, roles, projects, skills — nothing
about where the data came from.

Below it, ask a question and the answer arrives. An unsupported question is
answered honestly: "I don't have evidence of that in the portfolio." Whether the
answer carries source chips is the one open question — see Design.

## Out of Scope

Job matching (Phase 4). GitHub or MCP (Phase 5). The Engineer Mode UI (Phase 6),
though the endpoint returns the metrics it will display. Restyling anything —
Part A removes elements, it does not redesign; the token system stays as it is.
Re-adding evidence links to `skills.json` in any form.

---

# 2 · Design  *(Design Agent, `/plan`)*

**1 · Where does this live?**
Part A in `frontend/src/components` + `content/skills.json`. Part B in
`backend/app/rag/` (retrieval, embeddings), `app/ai/` (generation), one route in
`app/api/`, one component in `frontend/src/components`.

**2 · What can be reused?**
`ContentService` is the only content reader and stays that way — ingestion goes
through it. The design system, layout shell and API client all stand.

**3 · Frontend changes?**
Yes: removals across five components (Part A), plus one new `AskPortfolio`
component (Part B).

**4 · Backend changes?**
Yes: `_validate_evidence_refs` and the `evidence`/`todo` model fields come out;
`rag/` and `ai/` are created; one route is added.

**5 · AI / RAG / MCP?**
RAG and generation, both behind env-var-selected provider abstractions. No MCP —
that is Phase 5, and adding a tool must never reshape RAG.

**6 · New dependency?**
**No.** `faiss-cpu`, `numpy` and `httpx` are already pinned;
`sentence-transformers` stays in `requirements-local.txt` only, because torch
(~1 GB) would bust the Vercel 500 MB bundle.

**7 · Simplest implementation?**
Delete the meta-layer rather than restyle it. Then the smallest real RAG: chunk
per role/project, one FAISS index stamped with provider and dimension, two
provider interfaces, one endpoint, one component.

### Key technical decisions

- **Part A ships independently.** After step 3 the portfolio is complete and
  correct with no AI in it, so the removal is not hostage to the RAG work.
- **Inferred data is removed, not just hidden.** The `evidence` refs were the
  agent's inference — the resume never states where a skill was used. "Assume
  nothing" means deleting them, not merely not rendering them.
- **Grounding survives the removal.** Refusing an out-of-scope question is
  anti-hallucination, not provenance decoration, and rule 18 requires it.
- **Index refuses a provider/dimension mismatch** rather than returning
  plausible nonsense from incompatible vectors.

## Existing Components Reused

| Reused | How |
|---|---|
| `ContentService` | the only content reader; ingestion loads through it |
| design tokens + `@layer components` | unchanged — Part A removes elements, never restyles |
| `lib/api.ts` | one added method for the chat endpoint |
| page-level loading/error/retry in `App.tsx` | the pattern `AskPortfolio` copies |

This phase creates the RAG service and both provider abstractions that Phases
4-6 reuse.

## Rejected Alternatives

| Alternative | Why rejected |
|---|---|
| Keep the evidence layer but tone it down | The user asked for the resume as it is; a quieter version of the same idea is still the tool talking about itself |
| Hide `evidence` refs but leave them in `skills.json` | They are inferred, not stated. "Assume nothing" means deleting them |
| Merge `AIProvider` and `EmbeddingProvider` | Different deployment constraints — Ollama cannot deploy, MiniLM needs torch. Settled in `decisions.md` |
| numpy dot-product instead of FAISS | ~60 chunks would not need FAISS, but it is specified and is a recognisable talking point |
| Drop the `template` provider | It is what makes a live demo work with no key |
| Do Part B first | Content shape changes in Part A; ingesting twice wastes the work |

---

# 3 · Plan  *(Planning Agent, `/plan`)*

## Implementation Steps

Part A first — after step 3 the app is shippable with no AI in it. Steps 4 and 8
are RED gates.

| # | Step | Skill | Verified by |
|---|---|---|---|
| 1 | Strip the provenance layer from `Profile`, `SkillsExplorer`, `ProjectGallery`, `Contact`, `App` | `react-component` | no counts/coverage/source footers render |
| 2 | Remove `evidence` + `todo` from `skills.json`, its models, and `_validate_evidence_refs`; delete the tests covering them | — | `pytest` green with the removed tests gone |
| 3 | **Validate Part A** — `npm test`, `pytest`, lint, `tsc`, and view the app | `a11y-responsive` | portfolio reads as a resume, nothing about the data |
| 4 | **RED** — chunking, index mismatch, retrieval, and the grounding test | `tdd-cycle` | fails for the right reason; output in `3-test.md` |
| 5 | `app/rag/chunk.py` — `{text, source, type}` records via `ContentService` | `rag-ingestion` | one coherent chunk per role/project |
| 6 | `app/rag/embeddings.py` — `EmbeddingProvider`, Gemini + local, via factory | `ai-provider` | swaps by env var, no call site changes |
| 7 | `app/rag/index.py` + `ingest.py` — FAISS, persist, stamp provider+dim, refuse mismatch | `rag-ingestion` | known query retrieves the AI Engineer role |
| 8 | `app/ai/provider.py` + `prompts.py` — Gemini, Ollama, `template` fallback | `ai-provider` | works with no API key; grounding test green |
| 9 | `POST /api/ai/chat` — retrieve, ground, generate, return timings | `api-endpoint` | documented shape in `/docs`; timings present |
| 10 | `AskPortfolio.tsx` + `lib/api.ts`; full validation including 375px | `react-component` | answer renders; loading/error/empty reachable |

## Files Likely To Change

**Part A — removals**
`frontend/src/components/{Profile,SkillsExplorer,ProjectGallery,Contact}.tsx` ·
`src/App.tsx` · `content/skills.json` ·
`backend/app/services/content_models.py` · `services/content.py` ·
`backend/tests/test_content_service.py` · `src/components/SkillsExplorer.test.tsx`

**Part B — additions**
`backend/app/rag/{__init__,chunk,embeddings,index,retriever,ingest}.py` ·
`app/ai/{__init__,provider,prompts}.py` · `app/api/routes.py` · `app/api/schemas.py` ·
`app/config.py` · `backend/tests/{test_rag,test_ai_chat}.py` ·
`frontend/src/components/AskPortfolio{,.test}.tsx` · `src/lib/api.ts` ·
`src/types/content.ts` · `.env.example` · `.gitignore` (for `backend/.index/`)

**Deliberately not touched:** `frontend/src/index.css` — the token system stays
exactly as it is. `backend/requirements.txt` — no new dependency.

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
| **G0** branch | before `/build` writes | PASS | 2026-08-30 | `feature/03-rag-assistant`, stacked on the unmerged `improvement/visual-design` |
| **G1** design | Design → Plan | PASS | 2026-08-30 | 7 questions answered; no new dependency; `1-design.md` under 60 lines; one open question recorded, non-blocking |
| **G2** test (RED) | Test → Develop | PASS | 2026-08-30 | 13 new tests, all RED for the right reason; output in `3-test.md` |
| **G3** build (GREEN) | Develop → Review | PASS | 2026-08-30 | backend 27/27, frontend 24/24, ruff+eslint+tsc clean, verified live; 4 deviations recorded |
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
| 2026-08-30 | Added `HashingEmbeddingProvider` — not in the plan | Without it the app cannot boot with no `GEMINI_API_KEY`, contradicting the "works with no API key" criterion. A third implementation behind the existing abstraction: no new system, no new dependency, and it mirrors how generation degrades to `template` |
| 2026-08-30 | Added `app/services/ai.py` | Routers stay thin (conventions); retrieve → ground → generate is behaviour, so it belongs in a service |
| 2026-08-30 | Keep two-letter tokens when embedding | A `len < 3` floor silently dropped "AI", the most load-bearing term in this corpus; the known-query check returned "Data & Analytics" instead of an AI role |
| 2026-08-30 | Refuse before generating, on a retrieval threshold | Asking a model to police its own scope is a request; a similarity threshold is a guarantee |
| 2026-08-30 | API returns `sources` but the UI does not render them | Follows "no source of evidence" for the app, while keeping the data Phase 6's Engineer Mode needs |
| 2026-08-30 | Source chips deferred to Phase 6 rather than decided now | Engineer Mode surfaces retrieval internals anyway, so that is the natural place to judge whether a citation helps or clutters |
| 2026-08-30 | Article agreement in chunk text ("an AI Engineer") | Chunk text reaches the reader verbatim through the template provider |

## User Overrides

Every entry must end in a promoted rule. Promoted to
`harness/learning/user-overrides.md` at `/complete`.

| Date | Agent proposed | User chose | Why | Rule now |
|---|---|---|---|---|
| 2026-08-30 | An "Evidence" design: derived counts, a skills coverage ratio, per-skill evidence expansion naming the source file, and `content/*.json` provenance footers | Show the resume as it is; assume nothing beyond it | The layer described the tool to the reader instead of showing the content, and several evidence links were the agent's inference rather than resume facts | The UI renders resume content only. No derived statistic, coverage ratio, source-file label or inferred link is presented as portfolio content. Inferred data is deleted, not merely hidden. |

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
