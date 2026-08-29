# Skill: Add a FastAPI Endpoint

**Used by:** Developer Agent (with Test Agent for step 2)
**When:** any new backend HTTP surface

## Steps

1. **Schema** - add request/response Pydantic models to `app/api/schemas.py`.
   Response shape is decided here, before anything else.
2. **Failing test** - `backend/tests/test_<area>.py`: status code, response
   shape, and one boundary case. Run it, confirm RED. See `tdd-cycle.md`.
3. **Service** - put the behaviour in `app/services/<area>.py`. Logic never
   lives in the router.
4. **Router** - thin handler in `app/api/routes.py`: parse, call service,
   return. No branching beyond error mapping.
5. **Wire** - include the router in `app/main.py` if new.
6. **Run** - `pytest -q` green, then check `/docs` renders the endpoint.

## Rules

- Router stays thin. If it has an `if` that is not error handling, it belongs in
  the service.
- Settings come from `config.py`, never `os.environ` in a module.
- Errors return a typed shape, never a bare 500 with a stack trace.

## Done when

Test green, endpoint visible and correct in `/docs`, no logic in the router.
