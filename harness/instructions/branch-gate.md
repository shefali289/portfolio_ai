# Branch Gate (G0) — Policy

Enforced by `harness/scripts/branch_gate.py`. This file is the *why*; the
script is the *what*.

## Rules

1. **Never commit to `main`.** `main` holds the scaffold and merged work only.
2. **Branch name is `feature/<slug>`**, or `fix/<slug>` / `improvement/<slug>`.
   Lowercase, hyphenated.
3. **The slug equals the task directory name.** Task, branch and PR are
   therefore trivially traceable to each other — this replaces the work-item ID
   a production setup would carry.
4. **A branch may not exist without a task.** `/plan <slug>` first.
5. **Rebase onto `origin/main` before opening a PR**, so review sees the code as
   it will land.

## Rebase safety

- Refuses on a dirty tree — commit or stash first.
- Aborts cleanly on conflict, leaving the tree untouched.
- **Never force-pushes.** Rebasing an already-pushed branch rewrites history, so
  the script tells you to push with `--force-with-lease` rather than doing it.
  Force-pushing is an approval-gate action.

## Run

```bash
python harness/scripts/branch_gate.py --slug <slug> --rebase
```

Exit 0 = gate open. Record the result in the task's gate table.
