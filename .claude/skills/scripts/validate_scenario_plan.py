#!/usr/bin/env python3
"""Validate a scenario plan against the scenario-plan format standard + the SR-* contract.

The scenario plan has two parts (see docs/scenario-plan-format.md): Part 1 is the human-led narrative
(story bible — linted for presence only); Part 2 is the forward build checklist (contract-bound).

Two checks:

  FORMAT (linter — deterministic): the required sections are present and in order; the header carries a
    STATUS + Assessment-binding line; Part 2 has at least one '#### SE-NN' checklist-item block, and every
    such block carries a 'Satisfies:' field and a 'Keynotes:' field; every SE id is well-formed (SE-NN).

  CROSS-CHECK (bidirectional, against the consolidated assessment plan's SR-* register): every SR-* in
    assessment-plans/<SEMESTER>.md is satisfied by at least one checklist item (else UNCOVERED -> FAIL);
    no item claims an SR-* that is not in the register (else PHANTOM -> FAIL). An item that satisfies no
    SR-* is reported as info (allowed world-building, but a forgotten binding is visible).

Stdlib only.

Usage:
  validate_scenario_plan.py --semester S1 [--repo <content repo root>]
  validate_scenario_plan.py --plan <scenario plan> --consolidated <assessment-plans/S1.md>

Exit 0 = PASS (format valid AND every SR-* satisfied, no phantoms).
"""
import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]  # .claude/skills/scripts/ -> content repo root
SR_RE = re.compile(r"\bSR-[A-Z]+\d+-\d+\b")

# (regex for the heading, human label) in required order
REQUIRED = [
    (r"^#\s+.*Scenario Plan\b", "title — '# … Scenario Plan'"),
    (r"^##\s+Part 1\b.*Scenario narrative\b", "## Part 1 — Scenario narrative"),
    (r"^##\s+Part 2\b.*Build checklist\b", "## Part 2 — Build checklist"),
    (r"^##\s+SR coverage\b", "## SR coverage"),
    (r"^##\s+Open questions\b", "## Open questions"),
    (r"^##\s+Changelog\b", "## Changelog"),
]


def section_span(lines, start_pat, end_pats):
    start = next((i for i, ln in enumerate(lines) if re.match(start_pat, ln)), None)
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if any(re.match(p, lines[j]) for p in end_pats):
            end = j
            break
    return "\n".join(lines[start:end])


def check_format(text):
    """Return (problems, advisories, satisfied) — satisfied: {SR-id: set(SE-id)}."""
    lines = text.splitlines()
    problems, advisories = [], []

    # 1) required sections present + in order
    last_idx = -1
    for pat, label in REQUIRED:
        idx = next((i for i, ln in enumerate(lines) if re.match(pat, ln)), None)
        if idx is None:
            problems.append(f"missing required section: {label}")
        elif idx < last_idx:
            problems.append(f"section out of order: {label}")
        else:
            last_idx = idx

    # 2) header fields
    if not re.search(r"^>\s*\*\*STATUS", text, re.MULTILINE):
        problems.append("header missing a '> **STATUS** …' line")
    if "Assessment binding" not in text:
        problems.append("header missing an 'Assessment binding' line")

    # 3) Part 2 — checklist items: '#### SE-NN' blocks, each with Satisfies + Keynotes
    part2 = section_span(lines, r"^##\s+Part 2\b", [r"^##\s+SR coverage\b"]) or ""
    se_labels = re.findall(r"^####\s+(SE-\d+)\b", part2, re.MULTILINE)
    if not se_labels:
        problems.append("Part 2 has no '#### SE-NN' checklist-item blocks")
    chunks = re.split(r"^####\s+SE-\d+\b.*$", part2, flags=re.MULTILINE)[1:]
    satisfied = {}
    for label, chunk in zip(se_labels, chunks):
        if "Keynotes:" not in chunk:
            problems.append(f"{label} block missing a 'Keynotes:' field")
        sat_line = next((ln for ln in chunk.splitlines() if "Satisfies:" in ln), None)
        if sat_line is None:
            problems.append(f"{label} block missing a 'Satisfies:' field")
            continue
        srs = SR_RE.findall(sat_line)
        if not srs:
            advisories.append(f"{label} satisfies no SR-* (world-building — confirm intended)")
        for sr in srs:
            satisfied.setdefault(sr, set()).add(label)

    return problems, advisories, satisfied


def consolidated_srs(consolidated: Path):
    """The set of SR-* ids defined in the consolidated assessment plan's register."""
    text = consolidated.read_text(encoding="utf-8")
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines)
                  if re.match(r"^##\s+Scenario requirements register", ln)), None)
    span = "\n".join(lines[start:]) if start is not None else text
    return set(SR_RE.findall(span))


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description="Validate a scenario plan (format + SR cross-check).")
    ap.add_argument("--semester", help="e.g. S1 (defaults the plan + consolidated paths)")
    ap.add_argument("--repo", type=Path, default=REPO)
    ap.add_argument("--plan", type=Path, help="default <repo>/scenario-plans/<SEMESTER>.md")
    ap.add_argument("--consolidated", type=Path, help="default <repo>/assessment-plans/<SEMESTER>.md")
    args = ap.parse_args()

    if not args.plan and not args.semester:
        print("Give --semester or --plan."); sys.exit(2)
    plan = args.plan or (args.repo / "scenario-plans" / f"{args.semester}.md")
    consolidated = args.consolidated or (args.repo / "assessment-plans" / f"{args.semester}.md")
    if not plan.exists():
        print(f"No scenario plan at {plan}"); sys.exit(2)

    text = plan.read_text(encoding="utf-8")
    print(f"=== {plan} ===")

    problems, advisories, satisfied = check_format(text)
    if not problems:
        print(f"  FORMAT: PASS — all sections present; {len(satisfied)} distinct SR-* satisfied")
    else:
        print(f"  FORMAT: FAIL — {len(problems)} issue(s)")
        for p in problems:
            print(f"    [FAIL] {p}")
    for a in advisories:
        print(f"    [info] {a}")

    cross_fail = False
    if consolidated.exists():
        contract = consolidated_srs(consolidated)
        uncovered = sorted(contract - satisfied.keys())
        phantom = sorted(satisfied.keys() - contract)
        if not uncovered and not phantom:
            print(f"  CROSS-CHECK: PASS — all {len(contract)} SR-* in {consolidated.name} satisfied by an item")
        else:
            cross_fail = True
            print(f"  CROSS-CHECK: FAIL — {len(uncovered)} uncovered, {len(phantom)} phantom (of {len(contract)} SR-*)")
            for sr in uncovered:
                print(f"    [UNCOVERED] {sr} — no checklist item satisfies it")
            for sr in phantom:
                print(f"    [PHANTOM] {sr} — claimed by {', '.join(sorted(satisfied[sr]))} but not in the register")
    else:
        print(f"  CROSS-CHECK: SKIPPED — no consolidated assessment plan at {consolidated}")

    ok = not problems and not cross_fail
    print("\nRESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
