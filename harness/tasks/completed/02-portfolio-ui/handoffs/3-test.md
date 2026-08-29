# Handoff: Test -> Developer

## Done
Added backend aggregate-endpoint and cross-file evidence integrity tests, plus
frontend aggregate page, Profile prop contract, experience disclosure, project
filter, skill evidence, empty/omitted state, and evidence-index tests. G2 passes.

## You need to know
1. Backend RED command targeted two tests. Results: `2 failed`; `/api/content`
   returned 404 and invalid `role:missing-role` evidence did not raise.
2. Frontend RED ran six Phase 2 files. Results: `6 failed` suites;
   `6 failed | 1 passed` tests. Missing ExperienceTimeline/ProjectGallery/
   SkillsExplorer/evidence modules and absent aggregate App/Profile behaviour
   are the expected failures.
3. The one passing frontend assertion is the existing “no phone number” privacy
   invariant, not new Phase 2 behaviour; keep it green through the refactor.
4. `App` calls `getContent()` once, owns loading/error/retry, and passes content
   to pure sections. Collection components own honest empty states.
5. Public contracts fixed by tests: `Profile({profile})`,
   `ExperienceTimeline({roles})`, `ProjectGallery({projects})`, and
   `SkillsExplorer({content})`; `buildEvidenceIndex(content)` returns keyed labels.
6. The invalid evidence error must name both `skills.json` and the missing ref.

## Commands
- Backend: `.venv/Scripts/python.exe -m pytest -q tests/test_api.py::test_content_returns_all_five_validated_content_areas tests/test_content_service.py::test_invalid_skill_evidence_reference_raises_a_clear_error`
- Frontend: `npm.cmd test -- src/App.test.tsx src/components/Profile.test.tsx src/components/ExperienceTimeline.test.tsx src/components/ProjectGallery.test.tsx src/components/SkillsExplorer.test.tsx src/lib/evidence.test.ts`

## Files
- `backend/tests/{test_api,test_content_service}.py`
- `frontend/src/App.test.tsx`, `frontend/src/components/{Profile,ExperienceTimeline,ProjectGallery,SkillsExplorer}.test.tsx`
- `frontend/src/lib/evidence.test.ts`

## Do NOT re-read
Implementation source beyond files named in `2-plan.md`; test contracts and RED
reasons are fully captured above.

## Open questions
None.

## New learnings
- On Windows PowerShell, use `npm.cmd`; the `npm.ps1`/`npx.ps1` shims are blocked
  by execution policy before the test runner starts.
