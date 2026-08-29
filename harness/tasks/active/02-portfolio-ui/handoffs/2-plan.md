# Handoff: Planning -> Test

## Done
Eight verifiable steps order backend RED/GREEN, frontend RED/GREEN, semantic
sections/interactions, responsive/a11y polish, then full validation. G1 passes.

## You need to know
1. Start with failing backend tests for one `/api/content` response and real
   skill-evidence cross-references; preserve the failure output in `3-test.md`.
2. `ContentResponse` belongs in `api/schemas.py`; `routes.py` only composes the
   five already-cached `ContentService` models. No service or content changes.
3. Frontend gets one aggregate `getContent()` call in `api.ts`; `App.tsx` owns
   loading/error/retry and passes data to pure semantic components.
4. Write interaction tests before components: experience disclosure, technology
   filter/reset, skill evidence, empty collections, and omitted empty narratives.
5. Evidence resolution spans role, project, certification, education, and
   achievement ids. Unknown refs fail integrity tests; TODO-only skills render
   honestly without invented evidence.
6. User approved omitting empty Building/Learning/Beyond sections and deriving
   filters from project technologies. No fixed taxonomy or TODO copy in the UI.

## Steps
1. Backend RED: endpoint + cross-reference tests (`tdd-cycle`)
2. Backend GREEN: schema + thin route (`api-endpoint`, `tdd-cycle`)
3. Frontend RED: page, evidence, disclosure and filter tests (`tdd-cycle`)
4. Aggregate types/client/page state + evidence resolver (`react-component`)
5. Experience, credentials, notes and contact (`react-component`, `a11y-responsive`)
6. Projects and skills interactions (`react-component`, `a11y-responsive`)
7. Navigation, focus, responsive and reduced-motion polish (`a11y-responsive`)
8. Full mechanical + browser validation (`tdd-cycle`, `a11y-responsive`)

## Files
Exact paths are in `task.md` → `## Files Likely To Change`; do not add content,
dependencies, routing, AI, or a resume asset.

## Do NOT re-read
Source files or `1-design.md`; all current seams, content decisions, component
boundaries and paths needed for Test/Developer are captured above and in task.md.

## Open questions
None.

## New learnings
- Treat content integrity as UI behaviour when the UI exposes cross-file refs;
  validate refs before building evidence navigation on them.
