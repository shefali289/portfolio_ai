# Task: Portfolio UI

| | |
|---|---|
| **Slug** | `02-portfolio-ui` |
| **Branch** | `feature/02-portfolio-ui` |
| **Phase** | Phase 2 |
| **Status** | complete — G5 passed; PR body ready, creation blocked by `gh` auth |
| **Started / Completed** | 2026-08-29 / 2026-08-29 |

> **Brief only.** `/plan 02-portfolio-ui` fills in Design, Plan and the rest. Every stage
> writes back here, so this file ends up holding the whole story. Do not
> implement from this file alone.

---

# 1 · Intent

## Feature

Every resume-backed portfolio section, rendered from `content/*.json`, with no
AI yet: Hero, Experience, Projects, Skills, Credentials, Achievements, optional
Engineering Notes, and Contact.

## Goal

A portfolio that stands on its own and is presentable as-is. If the day runs
short, everything after this phase is additive rather than load-bearing.

## Acceptance Criteria

Refined at `/plan`, checked off at `/review`.

- [x] every section renders from `content/*.json` - no hardcoded copy anywhere
- [x] experience items expand and collapse
- [x] project technology filters narrow the visible set and reset cleanly
- [x] clicking a skill shows where it was used; **no percentage bars**
- [x] invalid skill evidence refs fail a cross-content integrity test
- [x] page loading/error/retry and collection empty states are reachable; empty
      Building/Learning/Beyond sections are omitted rather than invented
- [x] no horizontal scroll at 375px; keyboard navigable; reduced motion honoured

## User Experience

Hero states the positioning with Explore Work, GitHub, and Contact actions;
Ask My AI is visibly marked as coming later, and Resume is omitted until a
public asset exists. Experience expands instead of becoming a wall of text.
Projects are concise cards filtered by technologies the content already names.

## Out of Scope

Any AI feature: Ask My Portfolio, Why Me?, live GitHub integration, Engineer
Mode. Also out: new narrative copy, fixed project taxonomy, a public resume
asset, analytics, contact submission, routing, CMS, and animation libraries.

---

# 2 · Design  *(Design Agent, `/plan`)*

**1 · Where should this feature live?**
Primarily in `frontend/src/components/`, composed by `App.tsx`; one aggregate
HTTP response in the existing API exposes all five already-loaded content models.

**2 · Which existing components/services can be reused?**
Reuse `ContentService`, the `request<T>()` API client seam, the `Profile` loading
pattern, content models/types, layout landmarks, skip link, and test setup.

**3 · Frontend changes?**
Yes. Build a portfolio page from focused Hero, Experience, Projects, Skills,
Credentials, Engineering Notes, and Contact components, all fed by API data.

**4 · Backend changes?**
Yes, but only a thin aggregate `/api/content` response composed from the five
cached `ContentService` models; no new application behaviour or storage.

**5 · AI / RAG / MCP?**
No. AI buttons may be visibly disabled/labelled “coming later”; no AI endpoint,
retrieval, agent, or external tool is introduced in Phase 2.

**6 · New dependency?**
No. React, Tailwind, Testing Library, and browser-native disclosure/dialog
semantics cover the UI; motion uses `motion-safe` CSS rather than a library.

**7 · Simplest implementation that fully satisfies the request?**
Fetch one typed content payload, render small semantic components, keep
interaction state local, and use existing technologies as filter/evidence data.

### Key technical decisions

- One aggregate request avoids five endpoint/fetch/loading implementations.
- Empty arrays remain empty UI states or are omitted; no TODO copy becomes a claim.
- Skill evidence refs resolve through an indexed union of roles, projects,
  certifications, education, and achievements, with a cross-reference test.
- Animations are CSS-only and guarded by `motion-safe`.

### UI / UX approach

A compact navigation and strong hero lead into an expandable experience
timeline, filterable project cards, evidence-revealing skill controls,
credentials/achievements, optional narrative sections, and contact links.
The page has one loading/error surface with retry; each collection has an honest
empty state. Semantic buttons/disclosures, visible focus, and 375px layout are
tested and manually reviewed.

## Existing Components Reused

`ContentService`, `api.ts`, content models/types, `Profile` state pattern,
`App.tsx` landmarks and skip link, plus the existing pytest/Vitest setup.

## Rejected Alternatives

| Alternative | Why rejected |
|---|---|
| One endpoint per section | Repeats thin routing, requests, and state for five cached files |
| Framer Motion or a component library | New dependencies add weight without needed behaviour |
| Hardcode narrative copy or project categories | Violates the resume/content source-of-truth rule |
| Render TODO strings publicly | Exposes authoring gaps as portfolio content |

---

# 3 · Plan  *(Planning Agent, `/plan`)*

## Implementation Steps

| # | Step | Skill | Verified by |
|---|---|---|---|
| 1 | **RED:** extend `backend/tests/test_api.py` for `/api/content`; add real-content evidence-ref integrity cases to `test_content_service.py` | `tdd-cycle` | targeted pytest fails because aggregate route/integrity validation is absent |
| 2 | Add `ContentResponse` in `backend/app/api/schemas.py` and thin `/api/content` composition in `routes.py` | `api-endpoint`, `tdd-cycle` | backend targeted tests GREEN; existing 14 remain green |
| 3 | **RED:** add `App.test.tsx`, `ExperienceTimeline.test.tsx`, `ProjectGallery.test.tsx`, `SkillsExplorer.test.tsx`, and `evidence.test.ts` for page states and interactions | `tdd-cycle`, `react-component` | Vitest fails on absent aggregate client/components |
| 4 | Extend `types/content.ts`, `lib/api.ts`, and `lib/evidence.ts`; refactor `App.tsx`/`Profile.tsx` around one aggregate loading/error/retry state | `react-component` | page-state and evidence tests GREEN |
| 5 | Implement semantic `ExperienceTimeline`, `Credentials`, `EngineeringNotes`, and `Contact` sections from passed content only | `react-component`, `a11y-responsive` | render, disclosure, link, and empty/omitted-state tests GREEN |
| 6 | Implement `ProjectGallery` technology filters and `SkillsExplorer` evidence disclosure; no percentage bars or unsupported labels | `react-component`, `a11y-responsive` | filter reset and skill-evidence tests GREEN |
| 7 | Compose navigation/sections and polish `index.css`/Tailwind classes for focus, 375px layout, desktop hierarchy, and `motion-safe` transitions | `a11y-responsive` | keyboard walkthrough; 375px and desktop visual check; no horizontal scroll |
| 8 | Run backend/frontend suites, ruff, ESLint, typecheck, build, both servers, and content/API browser path | `tdd-cycle`, `a11y-responsive` | all mechanical checks GREEN; manual results recorded honestly |

## Files Likely To Change

**Backend**
`backend/app/api/schemas.py` · `backend/app/api/routes.py` ·
`backend/app/services/content.py` ·
`backend/tests/test_api.py` · `backend/tests/test_content_service.py`

**Frontend core**
`frontend/src/App.tsx` · `frontend/src/App.test.tsx` ·
`frontend/src/index.css` · `frontend/src/lib/api.ts` ·
`frontend/src/lib/evidence.ts` · `frontend/src/lib/evidence.test.ts` ·
`frontend/src/types/content.ts`

**Frontend components**
`frontend/src/components/Profile.tsx` + `Profile.test.tsx` · `ExperienceTimeline.tsx` + test ·
`ProjectGallery.tsx` + test · `SkillsExplorer.tsx` + test ·
`Credentials.tsx` · `EngineeringNotes.tsx` · `Contact.tsx`

## Skills Used

`tdd-cycle`, `api-endpoint`, `react-component`, `a11y-responsive`

---

# 4 · Tests  *(Test Agent, `/build`)*

## Tests First

- each section renders content from mocked API data, not hardcoded copy
- an experience item expands and collapses
- a project filter narrows the visible set; clearing restores it
- a skill click reveals its evidence list
- loading, error and empty states for every data-driven section
- empty Building/Learning/Beyond arrays are omitted, not filled with TODO copy
- invalid evidence refs fail against real content ids

## TDD Evidence

RED then GREEN. Tests written after the code fail G2 — the failure output is the
proof, and `final_checklist.py` checks for it.

| | |
|---|---|
| **RED - command** | Backend: `.venv/Scripts/python.exe -m pytest -q tests/test_api.py::test_content_returns_all_five_validated_content_areas tests/test_content_service.py::test_invalid_skill_evidence_reference_raises_a_clear_error`; Frontend: `npm.cmd test -- <six Phase 2 test files>` |
| **RED - failed for the right reason** | Yes. Backend: `/api/content` was 404 and invalid evidence did not raise. Frontend: four absent modules plus aggregate page/Profile behaviour absent; 6 suites failed, 6 new-behaviour tests failed. One pre-existing privacy invariant passed. Full evidence in `handoffs/3-test.md`. |
| **GREEN - result** | Backend: `16 passed`; `ruff check .` passed. Frontend: `17 passed`; ESLint, `tsc --noEmit`, and production build passed. Exact browser viewports at 375px and 1440px rendered cleanly; `scrollWidth` equalled `clientWidth` at both widths. |

---

# 5 · Gates

See `harness/QUALITY-GATES.md`. `PARTIAL`/`SKIPPED` are honest; a check reported
`PASS` without running is not.

| Gate | When | Result | Date | Note |
|---|---|---|---|---|
| **G0** branch | before `/build` writes | PASS | 2026-08-29 | `feature/02-portfolio-ui`; clean; rebased onto `origin/main`; 1 commit ahead |
| **G1** design | Design → Plan | PASS | 2026-08-29 | 7 questions answered; no dependency; `1-design.md` 39 lines; content/filter decision resolved |
| **G2** test (RED) | Test → Develop | PASS | 2026-08-29 | backend 2/2 RED; frontend 6 suites RED for expected absent endpoint/components/behaviour |
| **G3** build (GREEN) | Develop → Review | PASS | 2026-08-29 | backend 16; frontend 17; ruff/lint/typecheck/build pass; API and browser path pass; 375px + desktop visually checked |
| **G4** review | Review → Complete | PASS | 2026-08-29 | fresh backend 16 + frontend 17; lint/typecheck; secrets; exact-width visual + live keyboard pass; 1 LOW non-blocking test-coverage finding |
| **G5** completion | before archive + PR | PASS | 2026-08-29 | final checklist passed with repository venv; completion, learning, manifests and PR body updated |

## Final Checklist  *(`/complete`)*

`python harness/scripts/final_checklist.py --slug 02-portfolio-ui` — must exit 0.
Paste the result table, then confirm by hand:

- [x] content traces to the resume; no invented experience
- [x] AI checks are not applicable — Phase 2 contains no AI behavior
- [x] works at 375px and desktop
- [x] loading, error and empty states reachable
- [x] keyboard navigable; no images are present

---

# 6 · Record

## Decisions Taken

| Date | Decision | Reason |
|---|---|---|
| 2026-08-29 | One aggregate `/api/content` response | All data is already cached together; avoids repeated endpoints, requests, and loading state |
| 2026-08-29 | Omit empty Building/Learning/Beyond sections | User approved; the resume supplies no narrative content and TODO strings are not portfolio copy |
| 2026-08-29 | Derive project filters from existing technologies | User approved; fixed categories are unsupported presentation claims and mostly empty for two projects |
| 2026-08-29 | No new UI or motion dependency | Existing React, Tailwind, semantic HTML, and `motion-safe` CSS cover the behaviour |
| 2026-08-29 | Resolve and validate skill evidence across all content types | Phase 1 deferred ref integrity; evidence UI must never link to a nonexistent item |
| 2026-08-29 | Omit Resume CTA until a public asset exists | `docs/resume.md` is source material, not a served/downloadable resume; do not fabricate an asset |
| 2026-08-29 | Add existing `Profile.test.tsx` to the planned file list | Planning named a `Profile.tsx` refactor but omitted its existing contract test; corrected before RED rather than widening scope silently |
| 2026-08-29 | Add `backend/app/services/content.py` to the planned file list | RED proved cross-file evidence integrity cannot live in a thin router; user approved correcting the service-file omission before GREEN |

## User Overrides

Every entry must end in a promoted rule. Promoted to
`harness/learning/user-overrides.md` at `/complete`.

| Date | Agent proposed | User chose | Why | Rule now |
|---|---|---|---|---|

## Lessons Learned

- **Worked:** One aggregate validated payload plus pure semantic components kept
  state, disclosures, filtering, evidence, and honest empty states straightforward.
- **Cost time:** Edge's minimum headless window mimicked overflow, and the first
  response introduced styling assertions that completion removed.
- **Do differently:** Verify exact browser metrics before diagnosing responsive
  layout and give aggregate fixtures non-empty data for every simple section.

## Known Limitations

- Dedicated non-empty render tests are still absent for Credentials, Contact,
  and Engineering Notes; G4 classified this as LOW and non-blocking.
- AI, live GitHub data, a public resume asset, analytics, and contact submission
  remain deliberately outside Phase 2.

---

# 7 · Validation & PR  *(`/complete`)*

## Validation

Real results only. Not run = `SKIPPED`, never `PASS`.

| Check | Result |
|---|---|
| backend tests | PASS — 16 passed |
| frontend tests | PASS — 16 passed |
| lint | PASS — ruff + ESLint |
| typecheck | PASS — `tsc --noEmit` |
| manual check | PASS — API + UI served; exact 375px and 1440px screenshots inspected; no horizontal overflow |

All sections render real resume content; filters and expanders work; 375px and
desktop clean.

## PR Summary

| | |
|---|---|
| **Title** | `feat: build resume-backed portfolio UI` |
| **URL** | https://github.com/shefali289/portfolio_ai/pull/2 |
| **Merged** | yes - 2026-08-30 |

**What it adds:** A complete resume-backed portfolio UI with aggregate content
loading, semantic experience disclosures, project filters, skill evidence,
credentials, optional engineering notes, contact links, and honest states.

**Why:** Makes the portfolio presentable before later AI phases while keeping
all claims grounded in validated content.

## Suggested Commit Message

```
docs(harness): complete 02-portfolio-ui
```
