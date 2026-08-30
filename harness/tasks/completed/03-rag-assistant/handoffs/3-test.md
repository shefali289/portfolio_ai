# Handoff: Test -> Developer

## Done
13 new backend tests — 7 in `test_rag.py` (chunking, index round-trip, provider
and dimension mismatch, retrieval, grounding) and 6 in `test_ai_chat.py`
(endpoint, refusal, timings, validation, fallback) — plus 5 in
`AskPortfolio.test.tsx`. All confirmed RED.

## You need to know

1. **Tests never touch the network.** `conftest.StubEmbeddingProvider` is a
   hashing vectoriser: similar text shares tokens, so cosine is meaningful with
   no model and no key.
2. **It uses `zlib.crc32`, not `hash()`.** Python randomises string hashing per
   process, so `hash()` made the fixture non-reproducible across runs — and
   would make a persisted index unreadable by the next process.
3. **Stopwords and 256 dims matter.** At 64 dims with stopwords included, an
   unrelated question scored above the grounding threshold and the refusal test
   failed — assertions need enough dimensions to avoid collisions.
4. **`GROUNDING_THRESHOLD = 0.25` is the anti-hallucination gate.** Refusal is
   decided by retrieval score *before* any model is called. Never lower it.
5. **`create_app(content_dir=..., embedding_provider=...)`** — both injectable,
   so the app under test is wired to fixture content and stub embeddings.
6. **Part A's removals delete their tests.** The evidence-explorer and
   `_validate_evidence_refs` tests go with the feature — not a weakened suite.

## Commands
`cd backend && .venv/Scripts/python.exe -m pytest` · `cd frontend && npm test`

## RED evidence
```
tests/test_rag.py:9: from app.rag.chunk import build_chunks
E   ModuleNotFoundError: No module named 'app.rag.chunk'

tests/test_ai_chat.py:10: from app.ai.provider import TemplateProvider, resolve_provider
E   ModuleNotFoundError: No module named 'app.ai.provider'

2 errors in 1.08s
```
```
Error: Failed to resolve import "./AskPortfolio" from
       "src/components/AskPortfolio.test.tsx". Does the file exist?
 Test Files  1 failed | 7 passed (8)
```
Greenfield modules, so the absent module is the correct RED.

## Files
`backend/tests/{test_rag,test_ai_chat}.py` (new) · `tests/conftest.py` (stub) ·
`frontend/src/components/{AskPortfolio,SkillsExplorer}.test.tsx`

## Do NOT re-read
`2-plan.md` steps 1-3 are done — Part A shipped and validated before these were
written. Do not re-inspect `index.css`.

## Open questions
Only the source-chip question; it affects the component, not these tests.

## New learnings
- A hashing stub needs a stable hash and enough dimensions, or the grounding
  threshold it is meant to prove becomes noise.
