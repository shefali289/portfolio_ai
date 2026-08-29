# Handoff: Design -> Planning

## Done
Phase 2 shipped a correct, accessible, content-driven UI with no visual identity:
default slate/cyan Tailwind, centred `max-w-6xl` stack, one weight of idea per
section. Everything below is a *re-skin plus one signature interaction* — no data
model, endpoint or content file changes.

## The concept: **Evidence**
This portfolio's actual thesis is that every claim traces to a source, and the AI
may only say what `content/*.json` supports. The design should *state* that
rather than hide it. So: a provenance aesthetic — monospace metadata, visible
connections between a skill and the roles that prove it, and skills with no
evidence rendered honestly as unproven instead of quietly dropped.

## You need to know

1. **Dark-first, system-preference driven.** Deep ink ground, warm off-white
   text, one restrained accent. No toggle — the Engineer Mode toggle is Phase 6
   and should own that surface. Both schemes must meet 4.5:1.
2. **Design tokens go in `index.css` via Tailwind v4 `@theme`**, not scattered
   utilities. Colour, type scale, radii, shadow, spacing rhythm defined once. The
   existing `@layer components` classes (`.section-card`, `.eyebrow`,
   `.button-primary`…) are the seam — restyle them and every component inherits.
3. **Type pairing: a display grotesk + a mono for metadata.** Loaded via a
   Google Fonts `<link>` in `index.html` — **not** an npm package, so no new
   dependency. Must degrade to a system stack if the font fails.
4. **The signature interaction is the Skills Evidence Explorer.** Selecting a
   skill highlights the roles/projects that prove it and shows the proof. The
   data already exists — `ContentService` validates evidence refs and
   `SkillsExplorer` already resolves labels. This is presentation, not new logic.
5. **Motion is CSS + IntersectionObserver only.** Phase 2 rejected an animation
   library and rule 21 still applies. Staggered scroll reveal, all of it behind
   `motion-safe:` / `prefers-reduced-motion`.
6. **Branch is level with `origin/main`.** Phase 2 merged as PR #2 while this
   was being planned, so `improvement/visual-design` sits on plain `main` — no
   stacking, no merge-order constraint.
7. **Tests assert behaviour, never styling.** Existing component tests must keep
   passing untouched; conventions forbid asserting class names or timing. New
   tests cover the evidence-explorer *interaction*, not its appearance.

## Files
- `frontend/src/index.css` — tokens + restyled component layer (the main lever)
- `frontend/index.html` — font `<link>`, theme-color meta
- `frontend/src/App.tsx` — editorial grid, section rail, scroll-reveal hook
- `frontend/src/components/*.tsx` — 7 components, presentation only
- `frontend/src/hooks/useReveal.ts` — new, IntersectionObserver + reduced motion

## Do NOT re-read
`backend/`, `content/`, `docs/plan.md`. No backend or content change is in scope.
`architecture-map.md` and `conventions.md` are captured above.

## Open questions
None blocking. Dark-first is a judgement call the user can reverse cheaply —
it is one token block, not a rewrite.

## New learnings
- Re-check remote state at G0, not from a handoff written minutes earlier:
  Phase 2 merged mid-plan, which dissolved a stacking constraint the design had
  reasoned around.
