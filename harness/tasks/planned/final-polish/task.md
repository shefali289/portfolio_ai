# Task: Final Polish + Deploy

`/plan final-polish`  ·  branch `feature/final-polish`  ·  Phase 6

> **Brief only.** `/plan` fills in Design, Implementation Steps and Tests First.
> Do not implement from this file alone.

## Feature

Engineer Mode, state coverage, mobile and accessibility passes, README,
architecture diagram, screenshots, and deployment to Vercel.

## Goal

Reach the Definition of Done: a portfolio ready to publish and demonstrate.

## User Experience

An Engineer Mode toggle reveals, per AI response: endpoint, chunks retrieved,
vector search ms, generation ms, sources used, and tool used where applicable.

## Reuses

Metrics already returned by the Phase 3 and 4 endpoints - this phase displays
them, it does not add new measurement.

## Tests First (outline)

- Engineer Mode toggles and renders real metrics from the response
- metrics absent from a response degrade gracefully
- every AI surface has loading, error and empty states
- full suite green across backend and frontend

## Skills

`react-component`, `a11y-responsive`, `tdd-cycle`

## Validation

Every Definition of Done item satisfied. Deployed site reachable, AI features
working against Gemini in production.

## Out of Scope

New AI capabilities. Custom domain, analytics.

## Gate Log

_(filled during the lifecycle - see `harness/QUALITY-GATES.md`)_

- G0 branch  ·  G1 design  ·  G2 test  ·  G3 build  ·  G4 review  ·  G5 done

## Decisions Taken

_(appended as the lifecycle runs: what was decided and why)_

## PR

_(written at `/complete` from `harness/templates/pull-request.md`)_
