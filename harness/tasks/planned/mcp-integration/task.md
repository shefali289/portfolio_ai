# Task: MCP + GitHub Context

| | |
|---|---|
| **Slug** | `mcp-integration` |
| **Branch** | `feature/mcp-integration` |
| **Phase** | Phase 5 |
| **Status** | brief — not started |
| **Started / Completed** | — |

> **Brief only.** `/plan mcp-integration` fills in Design, Plan and the rest. Every stage
> writes back here, so this file ends up holding the whole story. Do not
> implement from this file alone.

---

# 1 · Intent

## Feature

GitHub public API integration, a small portfolio MCP server, a From My GitHub
section, and answers combining stored knowledge with live tool data.

## Goal

Show the distinction between RAG (stored knowledge) and MCP/tools (external,
live capability) - and that they can answer one question together.

## Acceptance Criteria

Refined at `/plan`, checked off at `/review`.

- [ ] the From My GitHub section renders live public repositories
- [ ] it degrades gracefully when the GitHub API is rate-limited or unreachable
- [ ] the MCP server exposes and answers its tools
- [ ] one question returns both portfolio and GitHub evidence, **attributed
      separately**
- [ ] the RAG implementation is unchanged by this phase

## User Experience

A From My GitHub section shows selected repositories. Asking "What Python
projects has she built?" returns portfolio evidence and live repositories,
attributed separately.

## Out of Scope

Authenticated GitHub features, write operations, other MCP servers.

---

# 2 · Design  *(Design Agent, `/plan`)*

_(seven questions — unanswered until `/plan`)_

## Existing Components Reused

RAG service unchanged - adding a tool must not reshape retrieval.
`ContentService` backs the MCP tools.

## Rejected Alternatives

_(filled at `/plan`)_

---

# 3 · Plan  *(Planning Agent, `/plan`)*

## Implementation Steps

_(4–10 steps — filled at `/plan`)_

## Files Likely To Change

_(filled at `/plan`)_

## Skills Used

`api-endpoint`, `react-component`, `tdd-cycle`, `a11y-responsive`

---

# 4 · Tests  *(Test Agent, `/build`)*

## Tests First

- GitHub client parses repo data; handles rate limit and network failure
- the section renders repos and degrades when the API is unavailable
- MCP server exposes the tools and returns valid results
- a combined answer attributes stored vs live evidence separately

## TDD Evidence

RED then GREEN. Tests written after the code fail G2 — the failure output is the
proof, and `final_checklist.py` checks for it.

| | |
|---|---|
| **RED - command** | — |
| **RED - failed for the right reason** | — |
| **GREEN - result** | — |

---

# 5 · Gates

See `harness/QUALITY-GATES.md`. `PARTIAL`/`SKIPPED` are honest; a check reported
`PASS` without running is not.

| Gate | When | Result | Date | Note |
|---|---|---|---|---|
| **G0** branch | before `/build` writes | — | | `branch_gate.py` |
| **G1** design | Design → Plan | — | | |
| **G2** test (RED) | Test → Develop | — | | failure output recorded |
| **G3** build (GREEN) | Develop → Review | — | | |
| **G4** review | Review → Complete | — | | tests · lint · typecheck · a11y |
| **G5** completion | before archive + PR | — | | `final_checklist.py` |

## Final Checklist  *(`/complete`)*

`python harness/scripts/final_checklist.py --slug mcp-integration` — must exit 0.
Paste the result table, then confirm by hand:

- [ ] content traces to the resume; no invented experience
- [ ] AI answers cite sources; out-of-scope questions refused
- [ ] works at 375px and desktop
- [ ] loading, error and empty states reachable
- [ ] keyboard navigable; images have alt text

---

# 6 · Record

## Decisions Taken

| Date | Decision | Reason |
|---|---|---|

## User Overrides

Every entry must end in a promoted rule. Promoted to
`harness/learning/user-overrides.md` at `/complete`.

| Date | Agent proposed | User chose | Why | Rule now |
|---|---|---|---|---|

## Lessons Learned

- **Worked:**
- **Cost time:**
- **Do differently:**

## Known Limitations

_(filled at `/complete`)_

---

# 7 · Validation & PR  *(`/complete`)*

## Validation

Real results only. Not run = `SKIPPED`, never `PASS`.

| Check | Result |
|---|---|
| backend tests | — |
| frontend tests | — |
| lint | — |
| typecheck | — |
| manual check | — |

Repos render live; MCP tools callable and listed.

## PR Summary

| | |
|---|---|
| **Title** | — |
| **URL** | — |
| **Merged** | — |

**What it adds:** —

**Why:** —

## Suggested Commit Message

```
<type>: <description>
```
