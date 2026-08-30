# Handoff: Test -> Developer

## Done
15 new tests: 10 in `test_agents.py` (extraction, retrieval injection, gap vs
match, chain order, gap reporting, failure propagation, and two regressions),
5 in `test_job_match_api.py`, 6 in `JobMatch.test.tsx`. All confirmed RED.

## You need to know

1. **`extract_requirements(jd, content)` must work with no LLM.** `template` is
   the default provider, so extraction is lexical. The test asserts "Python"
   comes out of a plain JD with no key configured.
2. **Extraction must also catch terms the portfolio has never heard of.** If
   requirements could only be known skills, a gap would be impossible by
   construction. The Kubernetes test pins this.
3. **`gather_evidence(requirements, retriever)` takes the retriever as an
   argument.** Never construct one inside — that is how a second search path
   appears and starts disagreeing with Ask My Portfolio.
4. **`assess_evidence` decides the verdict from scores**, reusing
   `GROUNDING_THRESHOLD`. A gap carries **no evidence at all** — a gap with
   attached chunks reads as a soft match.
5. **`run_chain` records steps and propagates failure.** The test monkeypatches
   `app.agents.chain.assess_evidence` to raise and asserts `ChainError` — no
   half-filled report.
6. **Two regression tests came from running it for real**, not from the plan:
   a verbatim term must never be a gap, and generic job-ad nouns must not be
   extracted. Both were live defects — see `4-develop.md`.

## Commands
`cd backend && .venv/Scripts/python.exe -m pytest` · `cd frontend && npm test`

## RED evidence
```
tests/test_agents.py:10: from app.agents.chain import ChainError, run_chain
E   ModuleNotFoundError: No module named 'app.agents.chain'

tests/test_job_match_api.py — 5 failed (404 vs 200/422, KeyError: 'steps',
  KeyError: 'summary', gap assertions)

Error: Failed to resolve import "./JobMatch" from JobMatch.test.tsx
 Test Files  1 failed | 8 passed (9)
```

## Files
`backend/tests/{test_agents,test_job_match_api}.py` (new) ·
`frontend/src/components/JobMatch.test.tsx` (new)

## Do NOT re-read
`2-plan.md`; `app/rag/*`; `app/ai/*`. Phase 3's retrieval and providers are
settled — call them as they are.

## Open questions
None.

## New learnings
- A gap-reporting feature needs a test proving a gap is *possible*, or an
  over-narrow extractor will quietly make the honest answer unreachable.
