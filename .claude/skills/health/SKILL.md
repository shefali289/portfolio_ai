---
name: health
description: Harness health check - learning caps, gates, drift, unused skills
when_to_use: Use when asked whether the development harness itself is still healthy.
allowed-tools: Read, Glob, Grep, Bash
disable-model-invocation: true
---

# /health — Harness Health

Is the harness still working, or has it rotted? Reads state, changes nothing.
Cheap — run it between features.

## Step 1 — Run the check

```bash
python harness/scripts/health_check.py
```

This is the **same script CI runs** (`.github/workflows/harness-health.yml`), so
a green local run means a green pipeline. It covers, mechanically:

| Check | Fails when |
|---|---|
| layout · agents | a core harness file or agent role is missing |
| learning caps | a `learning/` file is over cap — unpruned means unread |
| handoff caps | a handoff exceeds 60 lines — transcribing, not briefing |
| active tasks | more than one feature in flight |
| task briefs | a manifest slug has no task directory to start from |
| task sections | a task lacks Gate Log / Decisions Taken / PR |
| skills index | a skill is on disk but unindexed, or indexed but missing |
| links · file refs | a relative link or backticked harness path is broken |
| overrides | an override is recorded but never promoted to a rule |
| velocity | features completed without lessons recorded (WARN) |
| drift | `(planned)` markers left behind after the thing exists (WARN) |

Exit 0 = healthy. Exit 1 = at least one FAIL. WARNs do not fail.

## Step 2 — Judge what the script cannot

Read `harness/learning/` and recent `completion.md` files. **No source files.**

- **Gate history** — across recent completions, how many `SKIPPED`/`PARTIAL`?
  A pattern of skipping the same gate means it is unenforceable. Fix the gate or
  drop it honestly.
- **Learning quality** — are entries genuinely non-obvious, or restating what the
  code already shows? Under cap but useless is still failure.
- **Skill accuracy** — did any completed feature deviate from a skill it used?
  A stale skill gets copied blindly by the next feature.

## Step 3 — Report

Under 25 lines: the script's table, then anything Step 2 surfaced, then the
single smallest fix to make next.

State what is wrong. Do not fix it here — that is a task.
