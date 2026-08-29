# Handoff: Test -> Developer

## Done
Seven new frontend assertions written before implementation: three for
`useReveal` (new file) and four appended to `SkillsExplorer.test.tsx`. Confirmed
RED, with one honest exception below. No backend file is touched by this task.

## You need to know

1. **`useReveal()` returns `{ ref, visible }`.** `ref` is a callback ref taking
   `Element | null`. `visible` must be **true on the first render** when
   `IntersectionObserver` is absent or `prefers-reduced-motion` matches — the
   tests delete the global and mock `matchMedia` to force both paths.
2. **Content must never be hidden behind an observer that cannot run.** Put the
   hiding class inside `@media (prefers-reduced-motion: no-preference)`.
3. **`data-proven` on each skill button** is the tested hook: `"true"` when the
   skill has evidence, `"false"` when it does not.
4. **A coverage line must read `N of M skills evidenced`** — asserted with
   `/1 of 2 skills evidenced/i` against the fixture.
5. **Evidence must name its source file** — expanding a role-backed skill has to
   render `content/experience.json`.
6. **One test was not RED.** "selecting a second skill closes the first" passed
   immediately — the component already did single-selection. Kept as a
   regression guard; it is **not** TDD evidence.

## Commands
`cd frontend && npm test`

## RED evidence
```
FAIL  src/hooks/useReveal.test.ts
Error: Failed to resolve import "./useReveal". Does the file exist?

FAIL  SkillsExplorer > labels a skill with no evidence as unproven
Error: expect(element).toHaveAttribute("data-proven", "false")

FAIL  SkillsExplorer > summarises how much of the skill set is evidence-backed
Unable to find an element with the text: /1 of 2 skills evidenced/i

FAIL  SkillsExplorer > names the source file the evidence comes from
Unable to find an element with the text: /content\/experience\.json/i

Test Files  2 failed | 5 passed (7)
     Tests  3 failed | 17 passed (20)
```

## Files
- `src/hooks/useReveal.test.ts` (new, 3) · `src/components/SkillsExplorer.test.tsx` (+4)

## Do NOT re-read
`2-plan.md` step 1 is done — tokens and fonts landed. The six other component
test files must stay untouched: a re-skin that breaks a behaviour test has gone
too far into markup.

## Open questions
None.

## New learnings
- A test that passes the moment it is written is not RED — say so in the gate
  rather than letting the pass count imply evidence it lacks.
