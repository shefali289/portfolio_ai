# Handoff: Test -> Developer

## Done
14 backend tests across `test_content_service.py` (8) and `test_api.py` (6), plus
`conftest.py` fixture builders. Run and confirmed RED. Frontend tests come at
plan step 6, after the scaffold.

## You need to know

1. **`ContentService(content_dir)` takes the directory as a constructor arg**
   and exposes `.profile`, `.experience`, `.skills`, `.projects`,
   `.engineering_notes` as validated models. Raises `ContentError`.
2. **`ContentError` messages must name the offending file** — tests assert the
   filename appears in the string, and the missing-file case also asserts
   `"not found"`.
3. **`create_app(content_dir=...)` is the factory `main.py` must expose**, so a
   test can wire an app to fixture content. `uvicorn app.main:app` still needs a
   module-level `app` built from settings.
4. **Load is eager and cached.** `test_content_is_loaded_once_and_cached` deletes
   every JSON file after construction and still reads `.profile`.
5. **Two grounding tests are non-negotiable:**
   `test_skills_carry_evidence_or_an_explicit_todo` and
   `test_profile_does_not_expose_a_phone_number`. Never weaken either to go green.
6. **`test_the_real_content_directory_validates`** runs against the real
   `content/` — models must match the five files as written.

## Commands
```bash
cd backend && .venv/Scripts/python.exe -m pytest
```
The venv is Python **3.14.7**, created with `uv venv --python 3.14`. Plain
`uv venv` picks a 3.11 off PATH and `numpy==2.5.2` then refuses to resolve.

## RED evidence
```
tests/test_api.py:10: from app.main import create_app
E   ModuleNotFoundError: No module named 'app.main'

tests/test_content_service.py:9: from app.services.content import ContentError, ContentService
E   ModuleNotFoundError: No module named 'app.services.content'

2 errors in 2.67s
```
Failing on the absent module is the correct RED here: the feature is greenfield,
so there is nothing yet to fail *inside*. No test passed before its code existed.

## Files
- `backend/tests/{conftest,test_content_service,test_api}.py`
- `backend/pyproject.toml` — pytest `pythonpath=["."]`, ruff config

## Do NOT re-read
`2-plan.md` steps 1-2 are done. Do not rewrite the models to suit the
implementation — the tests and the real content pin their shape.

## Open questions
None.

## New learnings
- `uv venv` needs `--python 3.14` here; the bare command silently selects a
  uv-managed 3.11 and dependency resolution then fails.
