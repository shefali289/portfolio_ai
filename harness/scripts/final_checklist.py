#!/usr/bin/env python3
"""Gate G5 - Final Checklist.

Every box must tick before a task is deemed complete. Run at /complete, before
archiving the task and opening the PR.

    python harness/scripts/final_checklist.py            # active task
    python harness/scripts/final_checklist.py --slug foo

Covers: harness health · branch gate · TDD evidence (RED then GREEN) · backend
tests+lint · frontend tests+lint+typecheck · content parses · gate log · learning
updated · PR body ready.

Exit 0 = completable. Exit 1 = not complete, whatever the report says.

A check that cannot run yet is SKIPPED, never PASS. Skips do not block; failures
do. Nothing here is ever reported as passing without actually running.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "harness" / "scripts"

SEC = chr(10) + "## "
TOP = chr(10) + "# "
DASH = chr(8212)

results: list[tuple[str, str, str]] = []


def record(status: str, check: str, detail: str = "") -> None:
    results.append((status, check, detail))


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def tail(proc: subprocess.CompletedProcess, n: int = 1) -> str:
    lines = [l for l in (proc.stdout + proc.stderr).strip().splitlines() if l.strip()]
    return " | ".join(lines[-n:]) if lines else "no output"


# --------------------------------------------------------------------------
def find_task(slug: str | None) -> Path | None:
    tasks = ROOT / "harness" / "tasks"
    if slug:
        hits = list(tasks.glob(f"*/{slug}"))
        return hits[0] if hits else None
    active = [d for d in (tasks / "active").iterdir() if d.is_dir()] \
        if (tasks / "active").exists() else []
    return active[0] if len(active) == 1 else None


def check_harness() -> None:
    p = run([sys.executable, str(SCRIPTS / "health_check.py")], ROOT)
    if p.returncode == 0:
        record("PASS", "harness health", "all structural checks pass")
    else:
        fails = [l.strip() for l in p.stdout.splitlines() if l.strip().startswith("- ")]
        record("FAIL", "harness health", "; ".join(fails[:3]) or "see health_check output")


def check_branch() -> None:
    p = run([sys.executable, str(SCRIPTS / "branch_gate.py")], ROOT)
    if p.returncode == 0:
        record("PASS", "branch gate (G0)", "on a valid feature branch, current with main")
    else:
        fails = [l.strip() for l in p.stdout.splitlines() if l.strip().startswith("- ")]
        record("FAIL", "branch gate (G0)", "; ".join(fails[:3]) or "see branch_gate output")


def check_tdd(task: Path) -> None:
    """RED evidence is what separates TDD from tests written afterwards."""
    ho = task / "handoffs"
    red = ho / "3-test.md"
    green = ho / "4-develop.md"
    if not red.exists():
        record("FAIL", "TDD - RED evidence", "handoffs/3-test.md missing")
        return
    text = red.read_text(encoding="utf-8").lower()
    markers = ("fail", "error", "red")
    if not any(m in text for m in markers):
        record("FAIL", "TDD - RED evidence",
               "3-test.md records no failure output - tests must fail first")
    else:
        record("PASS", "TDD - RED evidence", "failing-test output recorded")
    if not green.exists():
        record("FAIL", "TDD - GREEN", "handoffs/4-develop.md missing")
    else:
        record("PASS", "TDD - GREEN", "implementation handoff present")


def check_backend() -> None:
    be = ROOT / "backend"
    if not (be / "app" / "main.py").exists():
        record("SKIP", "backend tests", "backend not built yet")
        record("SKIP", "backend lint", "backend not built yet")
        return
    p = run([sys.executable, "-m", "pytest", "-q"], be)
    record("PASS" if p.returncode == 0 else "FAIL", "backend tests", tail(p))
    p = run([sys.executable, "-m", "ruff", "check", "."], be)
    record("PASS" if p.returncode == 0 else "FAIL", "backend lint", tail(p))


def check_frontend() -> None:
    fe = ROOT / "frontend"
    if not (fe / "package.json").exists():
        for c in ("frontend tests", "frontend lint", "frontend typecheck"):
            record("SKIP", c, "frontend not built yet")
        return
    npm = "npm.cmd" if sys.platform == "win32" else "npm"
    npx = "npx.cmd" if sys.platform == "win32" else "npx"
    p = run([npm, "test", "--", "--run"], fe)
    record("PASS" if p.returncode == 0 else "FAIL", "frontend tests", tail(p))
    p = run([npm, "run", "lint"], fe)
    record("PASS" if p.returncode == 0 else "FAIL", "frontend lint", tail(p))
    p = run([npx, "tsc", "--noEmit"], fe)
    record("PASS" if p.returncode == 0 else "FAIL", "frontend typecheck", tail(p))


def check_content() -> None:
    import json
    files = sorted((ROOT / "content").glob("*.json"))
    if not files:
        record("SKIP", "content parses", "no content files yet")
        return
    bad, todos = [], 0
    for f in files:
        try:
            todos += f.read_text(encoding="utf-8").count("TODO")
            json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            bad.append(f"{f.name}: {e}")
    if bad:
        record("FAIL", "content parses", "; ".join(bad))
    else:
        note = f"{len(files)} files valid"
        if todos:
            note += f", {todos} TODO placeholder(s) - expected where the resume is silent"
        record("PASS", "content parses", note)


def check_gate_log(task: Path) -> None:
    """Every gate must carry a real result. FAIL blocks; PARTIAL/SKIPPED do not."""
    t = task / "task.md"
    if not t.exists():
        record("FAIL", "gate log", "task.md missing")
        return
    text = t.read_text(encoding="utf-8")

    rows = re.findall(r"^\|\s*\*\*(G[0-5])\*\*[^|]*\|[^|]*\|([^|]*)\|",
                      text, re.M)
    if not rows:
        record("FAIL", "gate log", "no G0-G5 results table in task.md")
        return

    blank, failed, recorded = [], [], []
    for gate, result in rows:
        r = result.strip().strip("*` ")
        if not r or r == DASH:
            blank.append(gate)
        elif r.upper() == "FAIL":
            failed.append(gate)
        else:
            recorded.append(gate + "=" + r.upper())

    if failed:
        record("FAIL", "gate log", "recorded FAIL: " + ", ".join(failed))
    elif blank:
        record("FAIL", "gate log", "no result for " + ", ".join(blank))
    else:
        record("PASS", "gate log", ", ".join(recorded))


def check_task_record(task: Path) -> None:
    """The task doc is the durable artefact - it must hold the whole story."""
    t = task / "task.md"
    if not t.exists():
        record("FAIL", "task record", "task.md missing")
        return
    text = t.read_text(encoding="utf-8")

    ac = text.split("## Acceptance Criteria", 1)
    if len(ac) < 2:
        record("FAIL", "acceptance criteria", "no ## Acceptance Criteria section")
    else:
        block = ac[1].split(SEC, 1)[0]
        done = len(re.findall(r"- \[x\]", block, re.I))
        todo = len(re.findall(r"- \[ \]", block))
        if done + todo == 0:
            record("FAIL", "acceptance criteria", "section is empty")
        elif todo:
            record("FAIL", "acceptance criteria", f"{todo} of {done + todo} unticked")
        else:
            record("PASS", "acceptance criteria", f"all {done} ticked")

    for head, label in (("## TDD Evidence", "TDD evidence in task"),
                        ("## PR Summary", "PR summary in task")):
        if head not in text:
            record("FAIL", label, "no " + head + " section")
            continue
        block = text.split(head, 1)[1].split(SEC, 1)[0].split(TOP, 1)[0]
        cells = re.findall(r"^\|\s*\*\*([^*]+)\*\*\s*\|([^|]*)\|", block, re.M)
        if not cells:
            record("FAIL", label, "no filled table rows")
            continue
        empty = [k.strip() for k, v in cells
                 if not v.strip().strip("*` ") or v.strip().strip("*` ") == DASH]
        if empty:
            record("FAIL", label, "not filled in: " + ", ".join(empty))
        else:
            record("PASS", label, str(len(cells)) + " rows recorded")

    lessons = text.split("## Lessons Learned", 1)
    if len(lessons) < 2:
        record("FAIL", "lessons in task", "no ## Lessons Learned section")
    else:
        block = lessons[1].split(SEC, 1)[0].split(TOP, 1)[0]
        bullets = [l for l in block.splitlines()
                   if l.strip().startswith("- **") and len(l.split(":**", 1)[-1].strip()) > 3]
        if len(bullets) < 3:
            record("FAIL", "lessons in task",
                   str(len(bullets)) + "/3 filled (Worked / Cost time / Do differently)")
        else:
            record("PASS", "lessons in task", "all 3 recorded")


def check_learning(slug: str) -> None:
    """Learning is what makes the next feature cheaper - it is not optional."""
    lp = ROOT / "harness" / "learning"
    lessons = (lp / "lessons-learned.md").read_text(encoding="utf-8")
    if slug in lessons:
        record("PASS", "learning updated", "lessons-learned has an entry for " + slug)
    else:
        record("FAIL", "learning updated",
               "no " + slug + " entry in lessons-learned.md - /complete step 3")

    overrides = (lp / "user-overrides.md").read_text(encoding="utf-8")
    entries = len(re.findall(r"^### ", overrides, re.M))
    promoted = overrides.count("**Rule now:**")
    if promoted < entries:
        record("FAIL", "overrides promoted",
               str(entries) + " recorded, " + str(promoted) + " promoted - each needs a rule")
    else:
        record("PASS", "overrides promoted", str(entries) + " recorded, all promoted")


def check_completion_docs(task: Path) -> None:
    for name, label in (("completion.md", "completion report"),
                        ("pull-request.md", "PR body")):
        p = task / name
        if not p.exists():
            record("FAIL", label, f"{name} not written")
        elif len(p.read_text(encoding="utf-8").strip()) < 200:
            record("FAIL", label, f"{name} looks like an unfilled template")
        else:
            record("PASS", label, name)


# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description="Gate G5 - Final Checklist")
    ap.add_argument("--slug", help="task slug (default: the single active task)")
    args = ap.parse_args()

    task = find_task(args.slug)
    if task is None:
        print("\nNo task to check. Pass --slug, or ensure exactly one task "
              "is in harness/tasks/active/.\n")
        return 1
    slug = task.name

    check_harness()
    check_branch()
    check_tdd(task)
    check_backend()
    check_frontend()
    check_content()
    check_gate_log(task)
    check_task_record(task)
    check_learning(slug)
    check_completion_docs(task)

    width = max(len(c) for _, c, _ in results)
    print(f"\nG5 - Final Checklist  ({slug})\n" + "=" * (width + 40))
    for status, check, detail in results:
        box = {"PASS": "[x]", "FAIL": "[ ]", "SKIP": "[-]"}[status]
        print(f"  {box} {status:4}  {check:<{width}}  {detail}")

    fails = [r for r in results if r[0] == "FAIL"]
    skips = [r for r in results if r[0] == "SKIP"]
    print("=" * (width + 40))
    print(f"  {len(results) - len(fails) - len(skips)} passed, "
          f"{len(skips)} skipped, {len(fails)} failed\n")

    if fails:
        print(f"'{slug}' is NOT complete. Outstanding:")
        for _, check, detail in fails:
            print(f"  - {check}: {detail}")
        print()
        return 1

    print("Not automatable - confirm by hand before archiving:")
    for line in ("content traces to the resume; no invented experience",
                 "AI answers cite sources; out-of-scope questions refused",
                 "works at 375px and desktop",
                 "loading, error and empty states reachable",
                 "keyboard navigable; images have alt text"):
        print(f"  [ ] {line}")
    print(f"\n'{slug}' passes G5 - safe to archive and open the PR.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
