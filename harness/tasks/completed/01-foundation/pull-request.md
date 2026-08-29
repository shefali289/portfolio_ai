## feat: establish portfolio foundation

Closes: harness task `01-foundation` (Phase 1)

### What this adds

Adds five resume-backed content files, a validated FastAPI read path, and a
React/Vite shell that renders the live profile through one typed API client.
It also establishes backend and frontend test, lint, and typecheck tooling.

### Why

Every later portfolio and AI phase needs stable content, API, UI, and testing
seams without hardcoded copy or claims absent from the resume.

### How

- eagerly load and validate all content at application startup
- keep `ContentService` as the only filesystem reader
- isolate HTTP schemas from domain content models
- keep component network access behind `frontend/src/lib/api.ts`

### Changed

| Area | Files |
|---|---|
| Backend | `backend/app/`, `backend/tests/`, `backend/pyproject.toml` |
| Frontend | `frontend/src/` and Vite/Vitest/ESLint/TypeScript config |
| Content | `content/*.json`, `docs/resume.md` |
| Harness | task record, five handoffs, completion report, learning store |

### Tests

| Suite | Result |
|---|---|
| `pytest` | 14 passed |
| `npm test` | 5 passed |
| `ruff` / `lint` / `tsc` | clean |

New tests cover content parsing and caching, missing/malformed files, API health
and profile responses, privacy grounding, and profile UI states. RED evidence
is preserved in `handoffs/3-test.md`.

### Quality gates

| Gate | Result |
|---|---|
| G0 branch | PASS |
| G1 design | PASS |
| G2 test (RED) | PASS |
| G3 build (GREEN) | PASS |
| G4 review | PARTIAL — live visual/keyboard review unavailable |
| G5 completion | PASS |

### Lessons learned

- Resolve interpreter and package peer constraints before scaffolding.
- Non-interactive Vite scaffolding needs a deterministic fallback.
- Privacy boundaries apply to docs and git history as well as served content.

### User overrides

- Redact private contact data from documentation and reachable history before push.

### Known limitations

- Visual checks at 375px and desktop were skipped because no browser was available.
- Reduced-motion handling for the loading pulse was deferred by user.
- Evidence references need cross-file validation in Phase 2.

### Harness

Task, handoffs 1-5 and completion report: `harness/tasks/completed/01-foundation/`
