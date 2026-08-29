# Harness Scripts

The mechanical half of the harness. Each runs identically **locally and in CI**,
so a green local run means a green pipeline.

| Script | Gate | Run when |
|---|---|---|
| `branch_gate.py` | G0 | before `/build` writes anything, and before a PR |
| `health_check.py` | — | between features, via `/health` |
| `final_checklist.py` | G5 | at `/complete`, before archiving and the PR |

## `branch_gate.py` — G0

```bash
python harness/scripts/branch_gate.py                 # check only
python harness/scripts/branch_gate.py --rebase        # also rebase onto main
python harness/scripts/branch_gate.py --slug 01-foundation
```

Checks: not on `main` · branch matches `feature|fix|improvement/<slug>` · a task
directory exists for the slug · working tree clean · branch not behind
`origin/main`.

**Rebase safety.** It refuses to rebase a dirty tree, aborts cleanly on conflict
leaving the tree untouched, and **never force-pushes**. Rebasing an
already-pushed branch rewrites history, so it tells you to push with
`--force-with-lease` rather than doing it for you.

## `health_check.py`

13 structural checks on the harness itself: learning caps, handoff caps, task
briefs, gate-log sections, skills indexed both ways, links, file references,
override follow-through, learning velocity, drift.

Exit 0 healthy, 1 unhealthy. WARNs do not fail.

## `final_checklist.py` — G5

```bash
python harness/scripts/final_checklist.py             # the active task
python harness/scripts/final_checklist.py --slug 01-foundation
```

Every box must tick before a task is complete:

- harness health, and the branch gate
- **TDD evidence** — `3-test.md` records real failure output (RED), and
  `4-develop.md` exists (GREEN). Tests written after the fact fail this.
- backend `pytest` + `ruff`; frontend `vitest` + lint + `tsc`
- `content/*.json` parses; TODO placeholders reported, not penalised
- gate log records G0-G4 with no `FAIL`
- `lessons-learned.md` has an entry for this slug; every override is promoted
- `completion.md` and `pull-request.md` written, not left as templates

Then it prints the checks that **cannot** be automated — content traces to the
resume, sources cited, 375px, states reachable, keyboard — for confirmation by
hand.

## Rules

- A check that cannot run yet is `SKIPPED`, never `PASS`. Skips do not block.
- Never relax a check to make a pipeline green. Fix the cause, or record the
  skip honestly.
