## feat: build resume-backed portfolio UI

Closes: harness task `02-portfolio-ui` (Phase 2)

### What this adds

The portfolio now renders every supported resume-backed section from one typed,
validated API response. It includes expandable experience, content-derived project
filters, skill evidence, credentials and achievements, optional engineering notes,
contact links, and honest loading/error/empty states.

### Why

This makes the portfolio presentable before any AI feature lands, while keeping
every experience claim grounded in the existing content source of truth.

### How

- one `/api/content` response avoids repeated routes and request state
- eager cross-content validation prevents dead skill-evidence references
- filters derive from project technologies; empty narrative arrays stay omitted
- native semantic controls and Tailwind provide responsive/a11y behavior without a dependency

### Changed

| Area | Files |
|---|---|
| Backend | aggregate schema/route, content evidence validation, tests |
| Frontend | page composition, typed client/models, evidence index, seven sections, tests/styles |
| Content | unchanged — all displayed claims use existing validated JSON |
| Harness | task, handoffs 1–5, completion, learning, manifests |

### Tests

| Suite | Result |
|---|---|
| `pytest` | 16 passed |
| `npm test` | 6 files, 16 passed |
| `ruff` / `lint` / `tsc` | clean |

New tests lock the aggregate API, invalid evidence refs, page states/retry,
experience disclosure, project filtering, skill evidence, and honest empty states.
RED evidence is preserved in `handoffs/3-test.md`.

### Quality gates

| Gate | Result |
|---|---|
| G0 branch | PASS |
| G1 design | PASS |
| G2 test (RED) | PASS |
| G3 build (GREEN) | PASS |
| G4 review | PASS |
| G5 completion | PASS |

### Lessons learned

- Verify actual browser viewport metrics before diagnosing a Windows Edge screenshot.
- Keep responsive checks manual and behavior tests independent of styling classes.
- Seed aggregate fixtures with non-empty data from every simple section.

### User overrides

None during Phase 2.

### Known limitations

- Dedicated non-empty tests for Credentials, Contact, and Engineering Notes remain LOW follow-up work.
- AI, live GitHub data, resume download, analytics, and contact submission are deliberately out of scope.
- `gh auth status` reports an invalid token; the PR body is ready but creation is pending authentication.

### Harness

Task, handoffs 1–5 and completion report: `harness/tasks/completed/02-portfolio-ui/`
