#!/usr/bin/env python3
"""Harness health check.

Structural validation of the harness itself - not the application. Runs
identically locally (`python harness/scripts/health_check.py`, or `/health`) and in CI.

Exit 0 = healthy, 1 = at least one FAIL. WARNs do not fail the build.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
H = ROOT / "harness"

LEARNING_CAPS = {
    "architecture-map.md": 150,
    "conventions.md": 150,
    "decisions.md": 150,
    "gotchas.md": 150,
    "lessons-learned.md": 100,
    "user-overrides.md": 80,
}
HANDOFF_CAP = 60
TASK_SECTIONS = ["## Gate Log", "## Decisions Taken", "## PR"]

results: list[tuple[str, str, str]] = []


def record(status: str, check: str, detail: str = "") -> None:
    results.append((status, check, detail))


def lines(p: Path) -> int:
    return len(p.read_text(encoding="utf-8").splitlines())


# --------------------------------------------------------------------------
def check_layout() -> None:
    """The files the harness cannot run without."""
    required = [
        "AGENT-MANIFEST.md",
        "HARNESS-RULES.md",
        "HANDOFF-PROTOCOL.md",
        "QUALITY-GATES.md",
        "README.md",
        "learning/README.md",
        "skills/README.md",
        "templates/task.md",
        "templates/completion.md",
        "templates/pull-request.md",
    ]
    missing = [f for f in required if not (H / f).exists()]
    if missing:
        record("FAIL", "layout", "missing: " + ", ".join(missing))
    else:
        record("PASS", "layout", f"{len(required)} core files present")

    agents = sorted(p.stem for p in (H / "agents").glob("*-agent.md"))
    expected = ["design-agent", "developer-agent", "planning-agent",
                "review-agent", "test-agent"]
    if agents != expected:
        record("FAIL", "agents", f"expected {expected}, found {agents}")
    else:
        record("PASS", "agents", "5 agent roles defined")


def check_learning_caps() -> None:
    """Learning that is not pruned is learning that is not read."""
    over = []
    for name, cap in LEARNING_CAPS.items():
        p = H / "learning" / name
        if not p.exists():
            record("FAIL", "learning", f"missing {name}")
            return
        n = lines(p)
        if n > cap:
            over.append(f"{name} {n}/{cap}")
    if over:
        record("FAIL", "learning caps", "over cap (prune): " + ", ".join(over))
    else:
        total = sum(lines(H / "learning" / n) for n in LEARNING_CAPS)
        record("PASS", "learning caps", f"6 files within cap, {total} lines total")


def check_handoff_caps() -> None:
    """A handoff over cap means an agent transcribed instead of briefing."""
    over = []
    count = 0
    for p in H.glob("tasks/*/*/handoffs/*.md"):
        count += 1
        n = lines(p)
        if n > HANDOFF_CAP:
            over.append(f"{p.parent.parent.name}/{p.name} {n}")
    if over:
        record("FAIL", "handoff caps", f"over {HANDOFF_CAP} lines: " + ", ".join(over))
    elif count == 0:
        record("PASS", "handoff caps", "no handoffs yet")
    else:
        record("PASS", "handoff caps", f"{count} handoffs within {HANDOFF_CAP} lines")


def check_active_tasks() -> None:
    """Normally exactly one feature in flight."""
    active = [d.name for d in (H / "tasks" / "active").iterdir()
              if d.is_dir()] if (H / "tasks" / "active").exists() else []
    if len(active) > 1:
        record("FAIL", "active tasks", f"{len(active)} active: {active} - expected 0 or 1")
    else:
        record("PASS", "active tasks", active[0] if active else "none in flight")


def check_manifest_tasks() -> None:
    """Every /plan-able task name needs a brief to start from."""
    mf = H / "AGENT-MANIFEST.md"
    text = mf.read_text(encoding="utf-8")
    slugs = set(re.findall(r"^\| `([a-z0-9-]+)` \| \d \|", text, re.M))
    planned = {d.name for d in (H / "tasks" / "planned").iterdir() if d.is_dir()}
    done = {d.name for d in (H / "tasks" / "completed").iterdir() if d.is_dir()}
    active = {d.name for d in (H / "tasks" / "active").iterdir() if d.is_dir()} \
        if (H / "tasks" / "active").exists() else set()
    have = planned | done | active

    missing = sorted(slugs - have)
    orphan = sorted(planned - slugs)
    if missing:
        record("FAIL", "task briefs", "manifest slug with no brief: " + ", ".join(missing))
    else:
        record("PASS", "task briefs", f"{len(slugs)} phase slugs all have a task dir")
    if orphan:
        record("WARN", "task briefs", "brief not in manifest: " + ", ".join(orphan))


def check_task_sections() -> None:
    """Gate log, decisions and PR sections must exist to be filled in."""
    bad = []
    n = 0
    for d in H.glob("tasks/*/*"):
        t = d / "task.md"
        if not t.is_file():
            continue
        n += 1
        text = t.read_text(encoding="utf-8")
        miss = [s for s in TASK_SECTIONS if s not in text]
        if miss:
            bad.append(f"{d.name} missing {','.join(s[3:] for s in miss)}")
    if bad:
        record("FAIL", "task sections", "; ".join(bad))
    else:
        record("PASS", "task sections", f"{n} tasks have Gate Log/Decisions/PR")


def check_skills_index() -> None:
    """A skill nobody indexes is a skill nobody uses."""
    text = (H / "AGENT-MANIFEST.md").read_text(encoding="utf-8")
    indexed = set(re.findall(r"\[`([a-z0-9-]+)`\]\(skills/", text))
    on_disk = {p.stem for p in (H / "skills").glob("*.md")} - {"README"}
    if on_disk - indexed:
        record("FAIL", "skills index", "on disk, not indexed: " + ", ".join(sorted(on_disk - indexed)))
    elif indexed - on_disk:
        record("FAIL", "skills index", "indexed, missing file: " + ", ".join(sorted(indexed - on_disk)))
    else:
        record("PASS", "skills index", f"{len(on_disk)} skills indexed both ways")


def check_links() -> None:
    """Broken links make the harness unnavigable."""
    bad = []
    for p in ROOT.rglob("*.md"):
        if ".git" in p.parts or "node_modules" in p.parts:
            continue
        for m in re.finditer(r"\[[^\]]+\]\(([^)#]+)\)", p.read_text(encoding="utf-8")):
            link = m.group(1).strip()
            if link.startswith(("http", "mailto", "#")):
                continue
            if not (p.parent / link).resolve().exists():
                bad.append(f"{p.relative_to(ROOT)} -> {link}")
    if bad:
        record("FAIL", "links", f"{len(bad)} broken: " + "; ".join(bad[:5]))
    else:
        record("PASS", "links", "all relative links resolve")


def check_referenced_files() -> None:
    """Backticked harness paths must exist."""
    pat = re.compile(r"`((?:harness|\.claude)/[A-Za-z0-9_./-]+\.(?:md|py))`")
    missing = set()
    for p in ROOT.rglob("*.md"):
        if ".git" in p.parts or "node_modules" in p.parts:
            continue
        for m in pat.finditer(p.read_text(encoding="utf-8")):
            if not (ROOT / m.group(1)).exists():
                missing.add(m.group(1))
    if missing:
        record("FAIL", "file refs", "referenced but absent: " + ", ".join(sorted(missing)))
    else:
        record("PASS", "file refs", "all referenced harness files exist")


def check_override_followthrough() -> None:
    """An override recorded but not promoted will be made again."""
    p = H / "learning" / "user-overrides.md"
    text = p.read_text(encoding="utf-8")
    entries = re.findall(r"^### .+$", text, re.M)
    promoted = text.count("**Rule now:**")
    if not entries:
        record("PASS", "overrides", "none recorded")
    elif promoted < len(entries):
        record("FAIL", "overrides",
               f"{len(entries)} recorded, only {promoted} promoted to a rule")
    else:
        record("PASS", "overrides", f"{len(entries)} recorded, all promoted")


def check_learning_velocity() -> None:
    """Zero learnings from a real feature means /complete was skipped."""
    done = [d for d in (H / "tasks" / "completed").iterdir() if d.is_dir()]
    if not done:
        record("PASS", "velocity", "no features completed yet")
        return
    lessons = (H / "learning" / "lessons-learned.md").read_text(encoding="utf-8")
    entries = len(re.findall(r"^### ", lessons, re.M))
    if entries < len(done):
        record("WARN", "velocity",
               f"{len(done)} features completed but {entries} lesson entries")
    else:
        record("PASS", "velocity", f"{entries} lessons / {len(done)} features")


def check_drift() -> None:
    """Planned markers left behind after the thing exists."""
    amap = (H / "learning" / "architecture-map.md").read_text(encoding="utf-8")
    planned = len(re.findall(r"\(planned\)", amap))
    backend_built = (ROOT / "backend" / "app" / "main.py").exists()
    if planned and backend_built:
        record("WARN", "drift", f"{planned} (planned) markers but backend exists - refresh")
    elif planned:
        record("PASS", "drift", f"{planned} (planned) markers, nothing built yet")
    else:
        record("PASS", "drift", "no stale planned markers")


# --------------------------------------------------------------------------
def main() -> int:
    for fn in (check_layout, check_learning_caps, check_handoff_caps,
               check_active_tasks, check_manifest_tasks, check_task_sections,
               check_skills_index, check_links, check_referenced_files,
               check_override_followthrough, check_learning_velocity,
               check_drift):
        try:
            fn()
        except Exception as exc:  # a check that crashes is a failing check
            record("FAIL", fn.__name__, f"check errored: {exc}")

    width = max(len(c) for _, c, _ in results)
    print("\nHarness Health\n" + "=" * (width + 34))
    for status, check, detail in results:
        mark = {"PASS": "PASS", "WARN": "WARN", "FAIL": "FAIL"}[status]
        print(f"  {mark:4}  {check:<{width}}  {detail}")

    fails = [r for r in results if r[0] == "FAIL"]
    warns = [r for r in results if r[0] == "WARN"]
    print("=" * (width + 34))
    print(f"  {len(results) - len(fails) - len(warns)} passed, "
          f"{len(warns)} warned, {len(fails)} failed\n")

    if fails:
        print("Harness is UNHEALTHY. Fix:")
        for _, check, detail in fails:
            print(f"  - {check}: {detail}")
        print()
        return 1
    print("Harness is healthy.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
