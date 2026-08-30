# Handoff: Planning -> Test

## Done
Eight steps, tokens-first so every later step inherits the system rather than
re-deciding it. Steps 2 and 6 are RED gates. No backend, content or API change.

## You need to know

1. **Step 1 is the whole design system.** Tokens + restyled `@layer components`
   in `index.css`. Because Phase 2 routed everything through `.section-card`,
   `.eyebrow`, `.button-primary`, `.tag`, `.filter-button`, `.text-link`,
   `.empty-state`, restyling those classes moves all seven components at once.
   Do this before touching any `.tsx`.
2. **Existing tests must stay green throughout.** They assert behaviour, so a
   pure re-skin cannot break them. If one breaks, the change went too far into
   markup — that is the signal, not an excuse to edit the test.
3. **The one genuinely new behaviour is the evidence explorer** (step 6-7):
   selecting a skill reveals which roles/projects prove it, and unproven skills
   say so. That is the only step needing new RED tests.
4. **`useReveal` must no-op under `prefers-reduced-motion`** and must not hide
   content when IntersectionObserver is unavailable — content visible by
   default, animation added, never the reverse. A test asserts content renders
   without the observer.
5. **375px is a step, not an afterthought.** Step 8 checks it explicitly; the
   editorial grid in step 3 must collapse to a single column.

## Steps
1. Design tokens + restyled component layer — `index.css`, `index.html` (fonts)
2. **RED** — `useReveal.test.ts`, evidence-explorer tests (`tdd-cycle`)
3. Editorial shell: grid, sticky section rail, scroll progress — `App.tsx`
4. Hero: display type, content-derived counts, provenance chip — `Profile.tsx`
5. Timeline spine + expandable role cards — `ExperienceTimeline.tsx`
6. Project case-study cards, index numerals, tech tags — `ProjectGallery.tsx`
7. **Evidence Explorer** — `SkillsExplorer.tsx` + `hooks/useReveal.ts` (`react-component`)
8. Credentials/Notes/Contact polish, then full validation: `npm test`,
   `npm run lint`, `tsc --noEmit`, 375px + desktop, keyboard, reduced motion

## Files
`frontend/src/index.css` · `frontend/index.html` · `src/App.tsx` ·
`src/hooks/useReveal.ts` (new) · `src/hooks/useReveal.test.ts` (new) ·
`src/components/{Profile,ExperienceTimeline,ProjectGallery,SkillsExplorer,Credentials,EngineeringNotes,Contact}.tsx`
· existing `*.test.tsx` (should need no edits)

**Not touched:** everything under `backend/`, `content/`, and `lib/api.ts`.

## Do NOT re-read
`1-design.md` — concept, tokens rationale, dark-first and no-new-dependency are
captured here. Do not re-inspect the backend.

## Open questions
None blocking.

## New learnings
Pending — the useful one will be whether a token-first re-skin really does move
seven components without touching their tests.
