# Handoff: Test -> Developer

## Done

14 frontend cases across two new files plus two appended to `AskPortfolio`.
All run, all RED for the right reason. No backend tests: this phase adds no
backend behaviour.

## RED evidence

```
cd frontend && npm.cmd test -- --run src/lib/engineerMode.test.tsx \
    src/components/Metrics.test.tsx src/components/AskPortfolio.test.tsx

FAIL src/lib/engineerMode.test.tsx
  Error: Failed to resolve import "./engineerMode" — Does the file exist?
FAIL src/components/Metrics.test.tsx
  Error: Failed to resolve import "./Metrics" — Does the file exist?
FAIL src/components/AskPortfolio.test.tsx
  Error: Failed to resolve import "../lib/engineerMode" — Does the file exist?

Test Files  3 failed (3)      Tests  no tests
```

## Second RED cycle — review finding 1

`tests/test_deploy_config.py` was written to catch the blocking finding:

```
FAILED test_no_pinned_python_runtime   - api/index.py pins a runtime
FAILED test_install_is_not_stubbed_out - assert 'echo' not in 'echo "insta...'
```

GREEN at `6 passed` once the runtime pin and install stub were removed.

## You need to know

1. **The load-bearing test is the omission**, not the display: a response with
   `generationMs` undefined must render **no** generation row and no `0.0`.
2. **`localStorage` is tested as hostile.** Two cases mock `Storage.prototype`
   to throw — `getItem` must yield "off", `setItem` must still toggle for the
   session. Neither may crash.
3. **`Metrics` renders `null` when it has nothing to show** — asserted with
   `toBeEmptyDOMElement`, so an empty panel never appears as a bare border.
4. **The panel must be absent while Engineer Mode is off**, asserted by querying
   the endpoint string, which only the panel renders.
5. Fixtures seed `localStorage` directly rather than clicking the toggle, so the
   surface tests stay about the panel.

## Signatures the tests pin down

`EngineerModeProvider`, `EngineerModeToggle`; `useEngineerMode() -> { enabled,
toggle }`; `Metrics({ endpoint, chunks?, retrievalMs?, generationMs?, provider?,
tools?, steps? })`; the toggle is a `<button>` named "Engineer Mode" carrying
`aria-pressed`.

## Do NOT re-read

`2-plan.md` — the steps are unchanged and these signatures supersede its
sketch. `1-design.md` — not in budget and not needed.
