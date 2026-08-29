## feat(frontend): evidence-led visual design

Closes: harness task `visual-design` (improvement, between Phase 2 and Phase 3)

### What this adds

A design identity for the portfolio and one signature interaction, replacing
Phase 2's correct-but-default styling. A token system in `index.css` carries the
whole look; the skills section becomes an evidence explorer where selecting a
skill reveals the roles and projects that prove it, and names the content file
the proof came from. Presentation only — no backend, content or API change.

### Why

Phase 2 shipped structure without art direction: default slate/cyan Tailwind, a
centred stack, no identity. Phases 3–5 add AI surfaces *on top* of this UI, so
fixing the design now means those features inherit a finished system instead of
being bolted onto a placeholder and reworked later.

### How

- **The concept is Evidence.** The portfolio's claim is that nothing is asserted
  without a source, so the design says it: the hero reports counts derived from
  content, the skills section leads with "18 of 34 skills evidenced", and skills
  the resume lists but never demonstrates stay visible and say so.
- **Tokens in `@theme`, semantic vars per scheme.** Components reference
  `--surface-*` / `--text-*` / `--accent`, never raw palette values, so a third
  scheme would be one block. Dark is the designed default.
- **No toggle** — Phase 6 owns Engineer Mode and should own that control.
- **No new dependency.** Fonts load via a Google Fonts `<link>` with system
  fallbacks; motion is CSS + `IntersectionObserver`, not an animation library.
- **Reveal degrades open** — the hiding class exists only inside
  `@media (prefers-reduced-motion: no-preference)`, so content is never left
  hidden behind an observer that cannot run.
- **Describe, don't rename** — evidence state is announced via
  `aria-describedby`; `aria-label` would have renamed the button and broken
  existing behaviour tests.

### Changed

| Area | Files |
|---|---|
| Backend | none |
| Frontend | `index.css`, `index.html`, `App.tsx`, all 7 components, new `hooks/useReveal.ts` and `components/Reveal.tsx` |
| Content | none |
| Harness | `tasks/active/visual-design/*`, `AGENT-MANIFEST.md`, `.agent-manifest.json`, `scripts/final_checklist.py` |

### Tests

| Suite | Result |
|---|---|
| `pytest` | 16 passed (untouched by this task) |
| `npm test` | 23 passed (7 files), up from 16 |
| `ruff` / `lint` / `tsc` | clean |

New tests lock in: reveal stays visible with no `IntersectionObserver` and under
reduced motion; proven vs unproven skill state; the evidence coverage summary;
single-selection; source-file provenance. RED evidence in `handoffs/3-test.md`.

**No existing test was edited** — the whole re-skin landed without touching a
behaviour assertion, which is the evidence it stayed a re-skin.

### Quality gates

| Gate | Result |
|---|---|
| G0 branch | PASS |
| G1 design | PASS |
| G2 test (RED) | **PARTIAL** — 4 of 5 new assertions genuinely RED; one passed immediately against existing behaviour and is a regression guard, not TDD evidence |
| G3 build (GREEN) | PASS |
| G4 review | **PARTIAL** — contrast computed across 12 token pairs, 1 AA failure found and fixed (3.56:1 → 5.59:1) plus 2 more a11y fixes; 375px visual check SKIPPED, no browser |
| G5 completion | PASS |

### Lessons learned

- A shared `@layer components` seam turns a full re-skin into a one-file change
  and leaves behaviour tests untouched.
- Compute contrast rather than trusting the eye — eleven token pairs were fine,
  the twelfth was a real AA failure on the primary CTA.
- A `data-*` attribute is a test hook, not an accessibility affordance.

### User overrides

- **Design quality is a deliverable, not a finishing touch.** The plain Phase 2
  layout was rejected in favour of a distinctive UI before the AI phases build
  on it. Promoted rule: a phase that ships UI states its art direction, not only
  its structure.

### Known limitations

No light/dark toggle (Phase 6 owns it). No imagery or logo — nothing in
`content/` supports one. Phase 2's three untested sections were restyled but
still lack render tests. 375px and device contrast unverified in a real browser.

### Harness

Task, handoffs 1–5 and completion report: `harness/tasks/completed/visual-design/`
