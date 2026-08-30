# Task: Visual Design

| | |
|---|---|
| **Slug** | `visual-design` |
| **Branch** | `improvement/visual-design` (from `main`; Phase 2 merged as PR #2) |
| **Phase** | improvement — sits between Phase 2 and Phase 3 |
| **Status** | built — G0–G3 passed, awaiting `/review` |
| **Started / Completed** | 2026-08-30 / — |

> **One task, one record.** Every stage writes back into this file, so it ends up
> holding the whole story: what was asked, what was decided, what was tested,
> what gates passed, what was learned, and what the PR said. Handoffs stay small
> and disposable; **this is the durable artefact.**

---

# 1 · Intent  *(written at `/plan`)*

## Feature

A distinctive visual identity and one signature interaction for the portfolio,
replacing Phase 2's correct-but-default styling. Presentation only — no data
model, endpoint or content change.

## Goal

Phase 2 delivered structure without art direction: default slate/cyan Tailwind,
a centred stack, no identity. Phases 3–5 will add AI surfaces *on top* of this
UI, so fixing the design now means those features inherit a finished system
instead of being bolted onto a placeholder and reworked later.

The design should express what actually makes this portfolio unusual: every
claim traces to a source, and the AI may only say what `content/*.json`
supports. That thesis becomes the aesthetic rather than a footnote.

## Acceptance Criteria

Testable, checked off at `/review`. If a line cannot be verified, rewrite it.

- [x] A token system exists in `index.css` (`@theme`): colour, type scale, radii,
      shadow, spacing — defined once, not scattered across utilities
- [x] Light and dark both render correctly from `prefers-color-scheme`, both
      meeting 4.5:1 on body text — computed across 12 token pairs
- [x] Selecting a skill reveals the roles/projects that prove it; skills with no
      evidence are shown honestly as unproven, never hidden
- [x] Scroll reveal is present, disabled under `prefers-reduced-motion`, and
      content still renders with no IntersectionObserver
- [~] No horizontal scroll at 375px; every interactive target ≥44px —
      **unverified in a browser**; grid collapses below `md` by construction
- [x] Keyboard reaches every control with a visible focus ring
- [x] `npm test`, `npm run lint`, `tsc --noEmit` all clean
- [x] No new npm dependency; existing component tests pass unedited

## User Experience

A dark-first editorial page with a sticky section rail showing reading position.
The hero states name, title and a content-derived count of the evidence behind
it. Experience runs down a timeline spine with expandable roles; projects are
case-study cards with index numerals; skills are the centrepiece — pick one and
the roles and projects proving it light up.

**Loading:** the existing page-level skeleton, restyled to the new tokens.
**Error:** the existing retry card, restyled. **Empty:** unchanged honesty — a
section with no content says so; an unproven skill says it is unproven.

## Out of Scope

Any AI feature (Phases 3–5). A light/dark **toggle** — Phase 6 owns Engineer
Mode and should own that control too; this task honours the system preference
only. Any new npm dependency, animation library, or UI kit. Backend, `content/`
and `lib/api.ts` changes. New copy — the resume is still the only source. A
logo, illustration or photography commission.

---

# 2 · Design  *(Design Agent, `/plan`)*

Answer each in one or two sentences.

**1 · Where does this live?**
Entirely in `frontend/src` — `index.css` for the token system, `App.tsx` for the
shell, the seven existing components for presentation, plus one new hook.

**2 · What can be reused?**
Nearly everything. Phase 2 routed all styling through a `@layer components`
layer (`.section-card`, `.eyebrow`, `.button-primary`, `.tag`, `.filter-button`,
`.text-link`, `.empty-state`), so restyling those classes moves all seven
components at once. The skills evidence data and its label resolution already
exist and are already validated at content load.

**3 · Frontend changes?**
Yes — this is entirely a frontend task.

**4 · Backend changes?**
No. `/api/content` already returns everything needed.

**5 · AI / RAG / MCP?**
No. Phases 3–5 own those, and this task exists so they inherit a finished design.

**6 · New dependency?**
**No.** Fonts load via a Google Fonts `<link>` in `index.html`, which is not an
npm package, and must degrade to a system stack. Motion is CSS plus
`IntersectionObserver` — rule 21 and Phase 2's own decision rule out an
animation library.

**7 · Simplest implementation?**
Tokens first, then one signature interaction. Restyle the shared component layer
so the whole site moves together, then invest the remaining effort in the skills
evidence explorer — the one place where a genuinely new interaction earns its
keep.

### The concept — Evidence

The provenance aesthetic: monospace metadata, visible links between a skill and
what proves it, and unproven skills labelled rather than quietly dropped. The
honesty already enforced in `ContentService` becomes the thing you can see.

### Key technical decisions

- **Dark-first, `prefers-color-scheme` driven, no toggle.** Phase 6 owns
  Engineer Mode and should own the toggle surface; two controls doing similar
  things is worse than one.
- **Tokens in `@theme`, not utilities.** One place to change the identity.
- **Reveal degrades open.** Content is visible by default and animation is
  added — never content hidden awaiting an observer that may not run.

## Existing Components Reused

| Reused | How |
|---|---|
| `@layer components` classes in `index.css` | restyled once; all 7 components inherit |
| `SkillsExplorer` evidence resolution | already resolves refs to labels — becomes the signature interaction |
| `ContentService` evidence validation | guarantees no dead evidence link reaches the UI |
| page-level loading/error/retry in `App.tsx` | restyled, not rebuilt |
| all 7 component tests | assert behaviour, so a re-skin leaves them untouched |

## Rejected Alternatives

| Alternative | Why rejected |
|---|---|
| Add a UI kit (shadcn, MUI, Chakra) | Rule 21 and Phase 2's own decision; the component layer already gives one place to restyle |
| Add Framer Motion / GSAP | Same rule; CSS + IntersectionObserver covers scroll reveal and respects reduced motion for free |
| Light/dark toggle now | Phase 6 owns Engineer Mode and should own the toggle; system preference is enough here |
| Fold this into Phase 6 | Phases 3–5 add UI on top — designing after them means reworking their surfaces |
| Rewrite the components from scratch | The behaviour and its tests are sound; only presentation is weak |
| Commission imagery / a logo | Out of scope, and nothing in `content/` supports it |

---

# 3 · Plan  *(Planning Agent, `/plan`)*

## Implementation Steps

Tokens first, so every later step inherits the system instead of re-deciding it.
Steps 2 and 6 are RED gates.

| # | Step | Skill | Verified by |
|---|---|---|---|
| 1 | Design tokens (`@theme`) + restyled component layer — `index.css`, fonts in `index.html` | — | `npm run build` emits CSS; both colour schemes render |
| 2 | **RED** — `useReveal.test.ts` and evidence-explorer interaction tests | `tdd-cycle` | `npm test` fails for the right reason |
| 3 | Editorial shell: grid, sticky section rail, scroll progress — `App.tsx` | `react-component` | existing tests still green; rail tracks sections |
| 4 | Hero: display type, content-derived evidence counts — `Profile.tsx` | `react-component` | `Profile.test.tsx` passes unedited |
| 5 | Timeline spine + expandable roles — `ExperienceTimeline.tsx` | `react-component` | `ExperienceTimeline.test.tsx` passes unedited |
| 6 | Project case-study cards + index numerals — `ProjectGallery.tsx` | `react-component` | `ProjectGallery.test.tsx` passes unedited |
| 7 | **Evidence Explorer** — `SkillsExplorer.tsx`, `hooks/useReveal.ts` | `react-component` | step 2 tests GREEN |
| 8 | Credentials/Notes/Contact polish + full validation | `a11y-responsive` | `npm test`, lint, `tsc`, 375px, keyboard, reduced motion |

## Files Likely To Change

**Frontend (all of it)**
`frontend/src/index.css` · `frontend/index.html` · `src/App.tsx` ·
`src/hooks/useReveal.ts` *(new)* · `src/hooks/useReveal.test.ts` *(new)* ·
`src/components/{Profile,ExperienceTimeline,ProjectGallery,SkillsExplorer,Credentials,EngineeringNotes,Contact}.tsx`
· `src/components/SkillsExplorer.test.tsx` *(extended)*

**Deliberately not touched:** everything under `backend/`, all of `content/`,
`src/lib/api.ts`, `src/types/content.ts`, and the other six `*.test.tsx` files —
if a re-skin breaks a behaviour test, the change went too far.

## Skills Used

`react-component` · `a11y-responsive` · `tdd-cycle`

---

# 4 · Tests  *(Test Agent, `/build`)*

## Tests First

- `useReveal` returns a visible state when `IntersectionObserver` is undefined
- `useReveal` does not animate under `prefers-reduced-motion`
- selecting a skill exposes the roles/projects that prove it
- a skill with no evidence renders an explicit unproven state
- selecting a second skill clears the first selection
- the skills region is keyboard operable and exposes pressed state

Behaviour only. No test asserts a colour, class name or duration.

## TDD Evidence

RED then GREEN. Tests written after the code fail G2 — the failure output is the
proof, and `final_checklist.py` checks for it.

| | |
|---|---|
| **RED - command** | `npm test` (frontend only — no backend change in this task) |
| **RED - failed for the right reason** | Yes for 4 of 5. `Failed to resolve import "./useReveal"`; `data-proven` attribute absent; `1 of 2 skills evidenced` absent; `content/experience.json` absent. **One did not fail:** "selecting a second skill closes the first" already passed, because the existing component already did single-selection — recorded as a regression guard, not as TDD evidence. |
| **GREEN - result** | `Test Files 7 passed (7)`, `Tests 23 passed (23)` |

---

# 5 · Gates  *(each stage records its own)*

See `harness/QUALITY-GATES.md`. `PARTIAL`/`SKIPPED` are honest and allowed;
a check reported `PASS` without running is not.

| Gate | When | Result | Date | Note |
|---|---|---|---|---|
| **G0** branch | before `/build` writes | PASS | 2026-08-30 | blocked first on `behind origin/main`; Phase 2 had merged as PR #2, so the branch was moved to `origin/main` (identical trees, no commits lost) |
| **G1** design | Design → Plan | PASS | 2026-08-30 | 7 questions answered; no new dependency; `1-design.md` 58 lines |
| **G2** test (RED) | Test → Develop | PARTIAL | 2026-08-30 | 4 of 5 new assertions genuinely RED; the second-skill-closes-first test passed immediately against existing behaviour — a regression guard, not TDD evidence |
| **G3** build (GREEN) | Develop → Review | PASS | 2026-08-30 | 23/23 tests, lint + tsc clean, build 22.19 kB CSS, verified live |
| **G4** review | Review → Complete | PARTIAL | 2026-08-30 | tests/lint/typecheck PASS; contrast computed across 12 token pairs, 1 AA failure found and fixed (3.56:1 → 5.59:1); 2 further a11y findings fixed; visual 375px check SKIPPED — no browser |
| **G5** completion | before archive + PR | PASS | 2026-08-30 | `final_checklist.py --slug visual-design` exits 0 |

## Final Checklist  *(`/complete`)*

`python harness/scripts/final_checklist.py --slug visual-design` — must exit 0.
Paste the result table, then confirm the manual items by hand:

- [ ] content traces to the resume; no invented experience
- [ ] AI answers cite sources; out-of-scope questions refused
- [ ] works at 375px and desktop
- [ ] loading, error and empty states reachable
- [ ] keyboard navigable; images have alt text

---

# 6 · Record  *(appended as the work happens)*

## Decisions Taken

What was decided mid-flight, and why. Not a diary — consequential choices only.

| Date | Decision | Reason |
|---|---|---|
| 2026-08-30 | Redesign now, before Phases 3–5 | Those phases add UI on top; designing after them means reworking their surfaces |
| 2026-08-30 | Unnumbered slug `visual-design` on an `improvement/` branch | Numbered slugs mean v1.0 phases; this is improvement work between phases |
| 2026-08-30 | Branch from `main` after Phase 2 merged as PR #2 | Planning assumed a stack off the unmerged Phase 2 branch; G0 found it merged, so the branch was moved to `origin/main` — identical trees, no commits lost |
| 2026-08-30 | Dark-first via `prefers-color-scheme`, no toggle | Phase 6 owns Engineer Mode and should own the toggle surface |
| 2026-08-30 | Fonts via a Google Fonts `<link>`, not an npm package | Keeps the no-new-dependency rule intact; must degrade to a system stack |

## User Overrides

Where the user reversed or redirected an agent. **Highest-value learning signal
here** — unrecorded, it gets repeated. Every entry must end in a promoted rule.
Promote to `harness/learning/user-overrides.md` at `/complete`.

| Date | Agent proposed | User chose | Why | Rule now |
|---|---|---|---|---|
| 2026-08-30 | Four options including "leave the plain layout as is" | Redesign 02 now, before the AI phases, and make the UI/UX genuinely distinctive | Design quality is a deliverable here, not a finishing touch; a default-looking portfolio undercuts the work it presents | A phase that ships UI must state its art direction, not only its structure — "renders correctly" is not "designed" |

## Lessons Learned

- **Worked:** the shared `@layer components` seam made a full re-skin a
  one-file change; all 16 existing behaviour tests passed untouched.
- **Cost time:** orphaned Vite servers on 5173-5175 and a stale uvicorn on 8000
  served old code during verification, producing misleading 200-with-HTML replies.
- **Do differently:** compute contrast instead of eyeballing it, and say plainly
  when a test was not RED rather than letting the pass count imply evidence.

Promoted to `harness/learning/` at `/complete`.

## Known Limitations

Intentionally not implemented.

- No light/dark toggle — system preference only; Phase 6 owns that control.
- No imagery, logo or illustration; nothing in `content/` supports one.
- Phase 2's three untested sections (Credentials, Contact, Engineering Notes)
  stay untested here — this task restyles them but does not add the render tests
  Phase 2 logged as a LOW finding.

---

# 7 · Validation & PR  *(`/complete`)*

## Validation

Real results only. Not run = `SKIPPED`, never `PASS`.

| Check | Result |
|---|---|
| backend tests | **N/A** — no backend file changed in this task |
| frontend tests | **PASS** — `Test Files 7 passed (7)`, `Tests 23 passed (23)` |
| lint | **PASS** — eslint clean |
| typecheck | **PASS** — `tsc --noEmit` clean |
| manual check | **PARTIAL** — served live at `localhost:5173`: 5 roles, 2 projects, 18/34 skills evidenced; fonts linked; dark scheme, reduced-motion and reveal classes all present in served CSS. **Not done:** visual check at 375px/desktop and instrument-measured contrast — no browser available here. |

## PR Summary

Body written to `pull-request.md` from `harness/templates/pull-request.md`.

| | |
|---|---|
| **Title** | `feat(frontend): evidence-led visual design` |
| **URL** | https://github.com/shefali289/portfolio_ai/pull/3 |
| **Merged** | yes - 2026-08-30 |

**What it adds:** A design identity for the portfolio — a token system carrying
dark-first and light schemes — plus an evidence explorer where selecting a skill
reveals the roles and projects that prove it and names the content file the
proof came from. Presentation only; no backend, content or API change.

**Why:** Phase 2 shipped structure without art direction. Phases 3-5 add AI
surfaces on top of this UI, so fixing the design now means those features
inherit a finished system instead of being reworked around a placeholder.

## Suggested Commit Message

```
feat(frontend): evidence-led visual design
```
