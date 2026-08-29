# Feature Completion

## Feature

Visual Design — `visual-design`

## What Was Added

A design identity for the portfolio, replacing Phase 2's correct-but-default
styling, plus one signature interaction. Presentation only: no backend, content
or API change.

The concept is **Evidence**. This portfolio's claim is that nothing is asserted
without a source, so the design states it rather than burying it: the hero
reports counts derived from content (5 roles, 2 projects, 34 skills), the skills
section leads with how many are actually evidenced (18 of 34), selecting a skill
names the file its proof came from, and skills the resume lists but never
demonstrates stay visible and say so.

Done now rather than in Phase 6 because Phases 3–5 add AI surfaces on top of
this UI — designing after them would mean reworking their surfaces.

## Main Files Changed

- `frontend/src/index.css` — `@theme` tokens plus semantic vars redefined once
  under `prefers-color-scheme: dark`; the restyled `@layer components` seam
- `frontend/index.html` — Google Fonts link, `color-scheme` and `theme-color`
- `frontend/src/App.tsx` — section rail with active tracking, reveal, provenance
- `frontend/src/hooks/useReveal.ts` + `.test.ts` — new
- `frontend/src/components/Reveal.tsx` — new
- All seven existing components — presentation only

## Tests

- 23 frontend tests pass (7 files), up from 16
- 3 new for `useReveal`: visible with no `IntersectionObserver`, visible under
  reduced motion, hidden-then-observed when motion is allowed
- 4 new for the evidence explorer: proven/unproven state, coverage summary,
  single-selection, source-file provenance
- **No existing test was edited** — the whole re-skin landed without touching
  behaviour assertions, which is the evidence it stayed a re-skin

## Validation

| Check | Result |
|---|---|
| backend tests | PASS — `16 passed`, untouched by this task |
| frontend tests | PASS — `Test Files 7 passed (7)`, `Tests 23 passed (23)` |
| lint | PASS — eslint clean, ruff clean |
| typecheck | PASS — `tsc --noEmit` clean |
| manual check | PARTIAL — served live at `localhost:5173` against the API (5 roles, 2 projects, 18/34 evidenced); fonts, dark scheme, reduced-motion and reveal classes all confirmed in served CSS. **Visual check at 375px and on a real device not performed — no browser available.** |

## Gates

| Gate | Result | Note |
|---|---|---|
| G0 branch | PASS | blocked first: branch was behind `origin/main` because Phase 2 merged as PR #2 mid-plan; moved to `origin/main`, identical trees, no commits lost |
| G1 design | PASS | 7 questions answered, no new dependency, handoff under 60 lines |
| G2 test | **PARTIAL** | 4 of 5 new assertions genuinely RED; one passed immediately against existing behaviour and is recorded as a regression guard, not TDD evidence |
| G3 build | PASS | 23/23, lint + tsc clean, verified live |
| G4 review | **PARTIAL** | contrast computed across 12 token pairs — 1 AA failure found and fixed; 2 further a11y findings fixed; 375px visual check SKIPPED |
| G5 done | PASS | `final_checklist.py --slug visual-design` exits 0 |

## Design Decisions

- **Tokens in `@theme`, semantic vars per scheme.** Components never reference
  raw palette values, so a third scheme is one block rather than a sweep.
- **Dark-first, no toggle.** Phase 6 owns Engineer Mode and should own that
  control; two similar toggles is worse than one.
- **No new dependency.** Fonts via a Google Fonts `<link>` with system
  fallbacks; motion is CSS + `IntersectionObserver`, not an animation library.
- **Reveal degrades open.** The hiding class exists only inside
  `@media (prefers-reduced-motion: no-preference)`.
- **Describe, don't rename.** The evidence state is announced via
  `aria-describedby`; `aria-label` was rejected because it would have renamed
  the button and broken existing behaviour tests.

## Lessons Learned

- **Worked:** a shared `@layer components` seam turned a full re-skin into a
  one-file change and left every behaviour test untouched.
- **Cost time:** three orphaned Vite servers and a stale uvicorn held
  5173–5175 and port 8000, serving old code and producing confusing
  200-but-HTML replies during verification.
- **Do differently:** compute contrast instead of trusting the eye — eleven
  pairs were fine, the twelfth was a real AA failure on the primary CTA.

## Known Limitations

- No light/dark toggle; system preference only (Phase 6 owns it).
- No imagery or logo — nothing in `content/` supports one.
- Phase 2's three untested sections (Credentials, Contact, Engineering Notes)
  were restyled but still have no render tests.
- 375px and device contrast unverified in a real browser.
