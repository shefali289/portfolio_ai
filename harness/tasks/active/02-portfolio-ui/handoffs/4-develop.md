# Handoff: Developer -> Reviewer

## Done
Implemented the validated aggregate content API and the complete resume-backed
portfolio UI. All planned interactions, honest states, and responsive safeguards
are GREEN. G3 passes.

## You need to know
1. `/api/content` returns all five typed content areas from `ContentService`.
2. `ContentService` now rejects unknown skill evidence refs with a source/ref
   specific `ContentError`; no content or resume claims were added.
3. `App` owns one aggregate loading/error/retry state. Pure components render
   Profile, Experience, Projects, Skills, Credentials, optional Notes, and Contact.
4. Experience uses semantic disclosure buttons; project filters are derived from
   actual technologies; skills resolve human-readable evidence without ratings.
5. Empty collections remain explicit; empty Building/Learning/Beyond sections
   are omitted; raw TODO values never become public evidence.
6. Reduced-motion is honoured, focus is visible, controls meet 44px targets, and
   exact 375px/1440px screenshots were inspected. Browser metrics reported
   `scrollWidth === clientWidth` at both widths.

## Validation
- Backend: `16 passed`; `ruff check .` passed.
- Frontend: `17 passed`; ESLint, `tsc --noEmit`, and Vite build passed.
- Runtime: `/api/content` 200 with 5 roles/2 projects; UI loaded from that API.
- Visual: exact 375px and 1440px emulated viewports passed inspection.

## Deviations
- Added existing `Profile.test.tsx` and `ContentService` to the plan before their
  respective RED/GREEN work; both corrections were user-approved and recorded.
- Windows required `npm.cmd`; Edge's normal headless window has a 492px minimum,
  so exact 375px evidence used DevTools device metrics rather than a cropped image.

## Files
Review the paths in `task.md` under `Files Likely To Change` plus this handoff.

## Open questions
None.

## New learnings
- Verify browser `innerWidth` and `scrollWidth` before diagnosing a narrow Edge
  screenshot; Windows headless minimum-window behaviour can crop a wider viewport.
