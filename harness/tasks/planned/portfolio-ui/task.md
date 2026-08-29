# Task: Portfolio UI

`/plan portfolio-ui`  ·  branch `feature/portfolio-ui`  ·  Phase 2

> **Brief only.** `/plan` fills in Design, Implementation Steps and Tests First.
> Do not implement from this file alone.

## Feature

Every portfolio section, rendered from `content/*.json`, with no AI in it yet:
Hero, Experience timeline, Projects, Skills, What I'm Building & Learning,
Beyond Engineering, Contact.

## Goal

A portfolio that stands on its own and is presentable as-is. If the day runs
short, everything after this phase is additive rather than load-bearing.

## User Experience

- Hero states the positioning, with Explore Work / Ask My AI / Resume / GitHub / Contact
- Experience is a timeline; each role expands for detail rather than a wall of text
- Projects are case-study cards - problem, solution, approach, tech, impact - filterable
  by AI / Automation / Backend / Cloud / Frontend
- Skills are grouped, never percentages; clicking one shows where it was used
- Notes and Beyond Engineering render as cards
- Works at 375px and desktop

## Reuses

`ContentService` and the API client from `foundation`. New endpoints only if a
section needs data not already served.

## Tests First (outline)

- each section renders content from mocked API data, not hardcoded copy
- experience item expands and collapses
- project filter narrows the visible set; clearing restores it
- skill click reveals its evidence list
- loading, error and empty states for every data-driven section

## Skills

`react-component`, `tdd-cycle`, `a11y-responsive`

## Validation

All sections render real resume content; filters and expanders work; 375px and
desktop clean; `npm test` and `tsc --noEmit` green.

## Out of Scope

Any AI feature. Ask My Portfolio, Why Me?, GitHub, Engineer Mode.

## Gate Log

_(filled during the lifecycle - see `harness/QUALITY-GATES.md`)_

- G0 branch  ·  G1 design  ·  G2 test  ·  G3 build  ·  G4 review  ·  G5 done

## Decisions Taken

_(appended as the lifecycle runs: what was decided and why)_

## PR

_(written at `/complete` from `harness/templates/pull-request.md`)_
