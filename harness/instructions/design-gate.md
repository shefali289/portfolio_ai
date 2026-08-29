# Design Gate (G1) — Policy

The only gate with no script — design quality is a judgement, so the check is a
checklist the Design Agent applies to its own output before handing over.

## Blocks unless

- [ ] All seven design questions answered, one or two sentences each
- [ ] Acceptance criteria are **testable** — each maps to something observable
- [ ] Reuse identified: what existing service/component this extends
- [ ] Rejected alternatives recorded, one line each with the reason
- [ ] **No new dependency**, or one justified in writing
- [ ] **No new top-level system**, or a strong stated reason
- [ ] `handoffs/1-design.md` is under 60 lines
- [ ] Empty, loading and error states described for any UI

## Two valid outcomes that are not "proceed"

- **"This is designed wrong."** Say so and re-open design rather than planning
  around a known flaw.
- **"This adds little value."** Recommending against a feature is a legitimate
  Design Agent result.

## Then

Record `G1` in the task's gate table with the result, and append anything
consequential to `## Decisions Taken`.
