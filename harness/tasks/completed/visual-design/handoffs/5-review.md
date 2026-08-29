# Handoff: Review -> Completion

## Check results
| Check | Result |
|---|---|
| `npm test` | **PASS** — `Test Files 7 passed (7)`, `Tests 23 passed (23)` |
| `npm run lint` | **PASS** — clean |
| `npx tsc --noEmit` | **PASS** — clean |
| `pytest` | **PASS** — `16 passed`, untouched by this task |
| `ruff check .` | **PASS** — clean |
| scope | **PASS** — diff vs `origin/main` touches no `backend/` or `content/` file |
| contrast | **COMPUTED** — 12 token pairs; 11 passed, 1 failed (finding 1) |
| visual 375px | **SKIPPED** — no browser here; markup reasoned, not seen |

## Findings

**1 · MEDIUM (a11y, WCAG AA) — the light-mode primary button fails contrast.**
White on `--accent: #0a9a77` computes to **3.56:1**, under the 4.5:1 needed for
normal text. Dark mode is fine at 11.75:1. Measured, not eyeballed — all twelve
token pairs were computed and this is the only failure.
*Fix:* set light `--accent` to the palette's existing `--color-signal-700`
(`#08765c`) → **5.59:1**. One token, no component change.

**2 · MEDIUM (a11y) — proven vs unproven is conveyed only visually.**
The `2◆` / `—` badge is `aria-hidden` and `data-proven` is not announced, so a
screen-reader user cannot tell an evidenced skill from an unproven one without
expanding every button — undermining the one distinction the design exists to
make. *Fix:* announce the state.

**3 · LOW — `aria-current="true"` on the section rail.** `location` fits better.

**Recorded, not a finding:** G2 was PARTIAL — one of five new tests passed before
implementation because the component already did single-selection.

## Verdict
All three were handed back to `/build` and **fixed in this cycle**:
1. light `--accent` → `signal-700`; re-measured at **5.59:1** (was 3.56:1)
2. evidence state announced via `aria-describedby` on a visually-hidden span —
   `aria-label` was rejected because it would rename the button and break the
   existing behaviour tests; describing keeps the name as the skill itself
3. `aria-current` → `location`

Re-verified after the fixes: 23/23 tests, lint + tsc clean, build 22.16 kB.

## New learnings
- **Compute contrast, do not eyeball it.** Eleven pairs looked fine and were;
  the twelfth looked fine and was not — a real AA failure on the primary CTA.
- A `data-*` attribute is a test hook, not an accessibility affordance — if a
  state is worth asserting in a test, it is worth announcing to a screen reader.
- A shared `@layer components` seam let a whole re-skin land without editing one
  behaviour test — keep as the pattern for UI work.

## User overrides
- **Design quality is a deliverable, not a finishing touch.** The user rejected
  leaving the plain Phase 2 layout and asked for a distinctive UI before the AI
  phases build on it. Promoted rule: a phase that ships UI states its art
  direction, not only its structure.

## Open questions
None. A real 375px/device check is owed and recorded as SKIPPED.
