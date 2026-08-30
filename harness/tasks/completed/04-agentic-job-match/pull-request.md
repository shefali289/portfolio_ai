## feat: agentic job match with honest gaps

Closes: harness task `04-agentic-job-match` (Phase 4)

### What this adds

A four-agent chain — requirement, portfolio, evidence, response — behind
`POST /api/ai/job-match`, and a Why Me? section that takes a pasted job
description and reports evidenced requirements alongside honest gaps. The chain
times each step and returns them, so the UI shows the sequence that ran.

### Why

It demonstrates decomposed agent responsibility rather than one large prompt,
and produces a match report a recruiter can actually trust — because a
requirement the portfolio cannot evidence is reported as a gap rather than
softened into a near-match.

### How

- **Four composed functions, not a framework.** The decomposition is the
  demonstration; an agent library would hide exactly the thing worth showing.
- **The verdict is computed, never asked of a model.** `assess_evidence` uses
  retrieval scores against `GROUNDING_THRESHOLD`, with `STRONG_MATCH` separating
  match from partial. Asking an LLM "is this evidence sufficient?" is how a gap
  quietly becomes a partial match.
- **One search path.** `JobMatchService` receives the `AiService` retriever, the
  same instance Ask My Portfolio uses.
- **A failing step aborts the run** with `ChainError` — no partial report that
  looks complete.
- **Exact-term evidence alongside vector search**, because single-token
  requirements were producing false gaps (below).

### Two defects found by running it, not by the tests

Both passed every test written from the plan; only the live run against the real
resume exposed them, and both now have regression coverage.

- **"FastAPI" was reported as a gap** although a role explicitly lists it. A
  one-token query against a long chunk scores low on lexical cosine. A false gap
  *understates* real experience — the mirror of the softening this feature
  exists to prevent, and invisible unless you know the resume.
- **"Engineer" was extracted as a requirement** from "AI Engineer" and reported
  as a gap. Generic job-ad nouns are no longer treated as requirements.

### Changed

| Area | Files |
|---|---|
| Backend | `app/agents/*` (new), `services/job_match.py` (new), `services/ai.py`, `rag/retriever.py`, `api/{routes,schemas}.py`, `main.py` |
| Frontend | `JobMatch{,.test}.tsx` (new), `App.tsx`, `lib/api.ts`, `types/content.ts` |
| Content | none |
| Harness | `tasks/active/04-agentic-job-match/*` |

### Tests

| Suite | Result |
|---|---|
| `pytest` | 42 passed |
| `npm test` | 30 passed (9 files) |
| `ruff` / `lint` / `tsc` | clean |

New tests lock in: lexical extraction with no LLM, a gap being *reachable* at
all, retriever injection, gap vs match by score, chain order, failure
propagation, the endpoint contract, and the six `JobMatch` UI states. RED
evidence in `handoffs/3-test.md`.

### Quality gates

| Gate | Result |
|---|---|
| G0–G3 | PASS |
| G4 review | PASS — 3 LOW findings, none blocking |
| G5 completion | PASS |

### Lessons learned

- Run a feature against real data before trusting a green suite.
- A false negative can be worse than the failure mode you designed against: this
  was built to stop gaps being softened, and the bug that mattered invented a
  gap that understated real experience.
- Vector search under-serves single-token queries; pair it with an exact-term
  check when the query is a name rather than a sentence.

### User overrides

None this phase. Phase 3's standing rule — the UI renders resume content only,
inferred data is deleted — held: no content file was touched.

### Known limitations

A bare skills-list mention counts as a *strong* match, the same as a
demonstrated role (evidence is shown, so a reader can tell). Extraction is
heuristic. `STRONG_MATCH` is unvalidated against semantic embeddings. No LLM
path for extraction or summary yet.

### Harness

Task, handoffs 1–5 and completion report:
`harness/tasks/completed/04-agentic-job-match/`
