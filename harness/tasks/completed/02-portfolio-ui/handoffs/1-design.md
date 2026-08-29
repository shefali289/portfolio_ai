# Handoff: Design -> Planning

## Done
Designed Phase 2 as one aggregate content response plus small semantic React
sections. No new dependency, top-level system, AI, RAG, or MCP. User approved
omitting empty narrative sections and using existing technologies as filters.

## You need to know
1. `ContentService` already caches all five models; add one thin `/api/content`
   response rather than per-section endpoints.
2. `api.ts` remains the only `fetch`; `App.tsx` owns one page-level
   loading/error/retry state and passes typed data to pure section components.
3. Reuse layout landmarks, skip link, Vitest/RTL, Pydantic content models, and
   hand-written TS mirrors. No new dependency.
4. Skill evidence must resolve across role/project/certification/education/
   achievement ids. Add the Phase 1 deferred cross-reference test.
5. Use semantic buttons/disclosures, visible focus, 375px layout, and
   `motion-safe` CSS transitions; never test class names or timing.
6. `engineering-notes.json` has achievements but empty building/learning/beyond
   arrays; its TODO text says supply or drop. Projects have technologies but no
   fixed category field.

## Files
- `backend/app/api/{routes,schemas}.py` - aggregate content response
- `backend/tests/test_api.py` - endpoint and cross-reference behaviour
- `frontend/src/{App,index.css}.tsx` - page composition and responsive theme
- `frontend/src/lib/api.ts`, `frontend/src/types/content.ts` - aggregate client/types
- `frontend/src/components/*.tsx` + tests - portfolio sections and interactions

## Do NOT re-read
Phase 1 source beyond the files named above; content shapes, seams, dependencies,
and the full current UI state are captured here and in `task.md`.

## Open questions
None. The content/filter decision is resolved.

## New learnings
- Phase briefs can promise UI taxonomy/content that the source data cannot
  support; verify content shapes before treating acceptance wording as settled.
