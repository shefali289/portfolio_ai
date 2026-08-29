# Task: MCP + GitHub Context

`/plan mcp-integration`  ·  branch `feature/mcp-integration`  ·  Phase 5

> **Brief only.** `/plan` fills in Design, Implementation Steps and Tests First.
> Do not implement from this file alone.

## Feature

GitHub public API integration, a small portfolio MCP server, a From My GitHub
section, and answers that combine stored knowledge with live tool data.

## Goal

Show the distinction between RAG (stored knowledge) and MCP/tools (external,
live capability) - and that they can answer one question together.

## User Experience

A From My GitHub section shows selected repositories. Asking "What Python
projects has she built?" returns portfolio evidence and live repositories,
attributed separately.

## Reuses

RAG service unchanged. Adding a tool must not reshape retrieval. `ContentService`
backs the MCP tools.

## Tests First (outline)

- GitHub client parses repo data; handles rate limit and network failure
- section renders repos, and degrades gracefully when the API is unavailable
- MCP server exposes the tools and returns valid results
- a combined answer attributes stored vs live evidence separately

## Skills

`api-endpoint`, `react-component`, `tdd-cycle`, `a11y-responsive`

## Validation

Repos render live. One question returns both portfolio and GitHub evidence,
clearly attributed. MCP tools callable and listed.

## Out of Scope

Authenticated GitHub features, write operations, other MCP servers.

## Gate Log

_(filled during the lifecycle - see `harness/QUALITY-GATES.md`)_

- G0 branch  ·  G1 design  ·  G2 test  ·  G3 build  ·  G4 review  ·  G5 done

## Decisions Taken

_(appended as the lifecycle runs: what was decided and why)_

## PR

_(written at `/complete` from `harness/templates/pull-request.md`)_
