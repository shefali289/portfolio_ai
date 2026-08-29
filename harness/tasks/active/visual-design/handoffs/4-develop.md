# Handoff: Developer -> Review

## Done
All 8 steps. 23/23 frontend tests green, lint + `tsc` clean, build 22.19 kB CSS.
Live at `localhost:5173` against the API: 5 roles, 2 projects, **18 of 34 skills
evidenced**. The token-first bet held — restyling the shared component layer
moved all seven components and **not one existing test needed editing**.

## You need to know

1. **The identity lives in `index.css`.** `@theme` holds the palette/type/radii;
   semantic vars (`--surface-*`, `--text-*`, `--accent*`) are redefined once
   under `prefers-color-scheme: dark`. Components reference the semantic vars,
   never raw palette values, so a third scheme would be cheap.
2. **Dark is the designed default**, light is a real alternate. No toggle —
   Phase 6 owns Engineer Mode and should own that control.
3. **One RED test was not actually RED.** "selecting a second skill closes the
   first" passed immediately, because the existing implementation already did
   single-selection. It is a regression guard, not TDD evidence — the other
   four new assertions were genuinely RED. Called out rather than dressed up.
4. **Reveal degrades open.** `useReveal` computes its initial state lazily; with
   no `IntersectionObserver` or under reduced motion it reports visible on the
   first render and never observes. `reveal-armed` (the hiding class) only
   exists inside `@media (prefers-reduced-motion: no-preference)`.
5. **New provenance motif.** `.provenance` / `.meta` in mono name the source
   file under each section ("content/experience.json"). This is also the natural
   hook for Phase 6's Engineer Mode.
6. **`Profile` gained an optional `evidence` prop** (counts derived in `App`).
   Optional on purpose, so the existing `Profile.test.tsx` passes untouched.

## Files
- `frontend/src/index.css` — tokens + restyled component layer (the main lever)
- `frontend/index.html` — Google Fonts link, `color-scheme` + `theme-color` meta
- `frontend/src/App.tsx` — section rail with active tracking, reveal, provenance footer
- `frontend/src/hooks/useReveal.ts` + `.test.ts` — new
- `frontend/src/components/Reveal.tsx` — new wrapper
- `frontend/src/components/{Profile,ExperienceTimeline,ProjectGallery,SkillsExplorer,Credentials,EngineeringNotes,Contact}.tsx`

## Look at closely
- **Contrast in both schemes.** Values were chosen to clear 4.5:1 but were not
  instrument-measured — no browser here. Worth a real check.
- **`useActiveSection` observes by `document.getElementById`** after render.
  Fine today; if sections ever mount lazily it will silently track nothing.
- **375px was reasoned, not seen.** The grid is single-column below `md` and the
  numerals are `aria-hidden`, but a real device check is still owed.

## Do NOT re-read
`1-design.md`, `2-plan.md` — concept, token rationale and constraints are here.
Nothing under `backend/` or `content/` changed; do not diff them.

## Open questions
None blocking.

## New learnings
- A shared `@layer components` seam makes a full re-skin a one-file change and
  leaves behaviour tests untouched — worth keeping as a rule for UI phases.
- `react-hooks/set-state-in-effect` fires again on lazy-init patterns; the fix
  is to trust the lazy initial state rather than re-assert it in the effect.
- Killing stale dev servers matters: three orphaned Vite instances held 5173-5175
  and a stale uvicorn served old code, producing confusing 200-but-HTML replies.
