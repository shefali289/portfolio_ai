# PR Template

Written at `/complete` to `tasks/completed/<slug>/pull-request.md`, then used as
the body of the actual PR.

---

```markdown
## <type>: <short description>

Closes: harness task `<slug>` (<phase or feature>)

### What this adds

2-4 sentences. What a reviewer sees that is new.

### Why

The problem it solves. One short paragraph.

### How

- key decision and its reason
- anything a reviewer would otherwise question
- what was deliberately kept simple

### Changed

| Area | Files |
|---|---|
| Backend | ... |
| Frontend | ... |
| Content | ... |
| Harness | ... |

### Tests

| Suite | Result |
|---|---|
| `pytest` | 24 passed |
| `npm test` | 11 passed |
| `ruff` / `lint` / `tsc` | clean |

New tests: what behaviour they lock in. RED evidence in `handoffs/3-test.md`.

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

- ...

### User overrides

- ... (or "none")

### Known limitations

Deliberately out of scope, and why.

### Harness

Task, handoffs 1-5 and completion report: `harness/tasks/completed/<slug>/`
```
