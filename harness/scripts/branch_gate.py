#!/usr/bin/env python3
"""Gate G0 - Branch Gate.

Run before /build writes anything, and again before opening a PR.

    python harness/scripts/branch_gate.py              # check only
    python harness/scripts/branch_gate.py --rebase     # also rebase onto main
    python harness/scripts/branch_gate.py --slug foo   # expect this task slug

Checks: not on main · branch matches feature|fix|improvement/<slug> · a task
directory exists for the slug · working tree clean · branch not behind main.

Exit 0 = gate open, 1 = blocked.

Rebase safety: refuses on a dirty tree, aborts cleanly on conflict, and never
force-pushes. After a rebase of an already-pushed branch you must push with
--force-with-lease; this script tells you rather than doing it.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BRANCH_RE = re.compile(r"^(feature|fix|improvement)/[a-z0-9][a-z0-9-]*$")
MAIN = "main"

results: list[tuple[str, str, str]] = []


def record(status: str, check: str, detail: str = "") -> None:
    results.append((status, check, detail))


def git(*args: str, check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                          text=True, check=check)


def out(*args: str) -> str:
    return git(*args).stdout.strip()


# --------------------------------------------------------------------------
def check_branch_name() -> str | None:
    branch = out("rev-parse", "--abbrev-ref", "HEAD")
    if branch == MAIN:
        record("FAIL", "not on main",
               "on main - create feature/<slug> before making changes")
        return None
    if not BRANCH_RE.match(branch):
        record("FAIL", "branch name",
               f"'{branch}' must be feature/<slug>, fix/<slug> or improvement/<slug>")
        return None
    record("PASS", "branch name", branch)
    return branch


def check_task_dir(slug: str, expected: str | None) -> None:
    if expected and slug != expected:
        record("FAIL", "slug match",
               f"branch slug '{slug}' != expected '{expected}'")
        return
    hits = list((ROOT / "harness" / "tasks").glob(f"*/{slug}"))
    if not hits:
        record("FAIL", "task exists",
               f"no harness/tasks/*/{slug} - run /plan {slug} first")
        return
    where = hits[0].parent.name
    if where == "completed":
        record("FAIL", "task exists", f"'{slug}' is already completed")
    else:
        record("PASS", "task exists", f"tasks/{where}/{slug}")


def check_clean_tree() -> bool:
    dirty = out("status", "--porcelain")
    if dirty:
        n = len(dirty.splitlines())
        record("WARN", "clean tree", f"{n} uncommitted change(s) - commit before rebasing")
        return False
    record("PASS", "clean tree", "nothing uncommitted")
    return True


def check_up_to_date(branch: str, do_rebase: bool, clean: bool) -> None:
    """Behind main means the PR is testing stale ground."""
    if not out("remote"):
        record("WARN", "up to date", "no git remote - skipping fetch")
        return

    fetch = git("fetch", "origin", MAIN, "--quiet")
    if fetch.returncode != 0:
        record("WARN", "up to date", "could not fetch origin - offline?")
        return

    base = f"origin/{MAIN}"
    counts = out("rev-list", "--left-right", "--count", f"{base}...HEAD")
    try:
        behind, ahead = (int(x) for x in counts.split())
    except ValueError:
        record("WARN", "up to date", "could not compare with origin/main")
        return

    if behind == 0:
        record("PASS", "up to date", f"{ahead} ahead, 0 behind {base}")
        return

    if not do_rebase:
        record("FAIL", "up to date",
               f"{behind} commit(s) behind {base} - rerun with --rebase")
        return

    if not clean:
        record("FAIL", "rebase", "working tree dirty - commit or stash first")
        return

    rb = git("rebase", base)
    if rb.returncode == 0:
        new = out("rev-list", "--left-right", "--count", f"{base}...HEAD")
        record("PASS", "rebase", f"rebased onto {base} ({new.split()[1]} ahead)")
        if ahead:
            record("WARN", "push",
                   "branch history rewritten - push with --force-with-lease")
    else:
        git("rebase", "--abort")
        first = (rb.stdout + rb.stderr).strip().splitlines()
        record("FAIL", "rebase",
               "conflict - aborted cleanly, tree unchanged. "
               + (first[0] if first else "resolve manually"))


# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description="Gate G0 - Branch Gate")
    ap.add_argument("--rebase", action="store_true",
                    help="rebase onto origin/main when behind")
    ap.add_argument("--slug", help="task slug this branch must match")
    args = ap.parse_args()

    branch = check_branch_name()
    if branch:
        check_task_dir(branch.split("/", 1)[1], args.slug)
        clean = check_clean_tree()
        check_up_to_date(branch, args.rebase, clean)

    width = max(len(c) for _, c, _ in results)
    print("\nG0 - Branch Gate\n" + "=" * (width + 32))
    for status, check, detail in results:
        print(f"  {status:4}  {check:<{width}}  {detail}")

    fails = [r for r in results if r[0] == "FAIL"]
    warns = [r for r in results if r[0] == "WARN"]
    print("=" * (width + 32))
    print(f"  {len(results) - len(fails) - len(warns)} passed, "
          f"{len(warns)} warned, {len(fails)} failed\n")

    if fails:
        print("G0 BLOCKED. Fix:")
        for _, check, detail in fails:
            print(f"  - {check}: {detail}")
        print()
        return 1
    print("G0 open - safe to build.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
