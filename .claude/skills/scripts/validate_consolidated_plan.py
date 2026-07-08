#!/usr/bin/env python3
"""Validate that a consolidated assessment plan faithfully reflects its per-cluster source plans.

The separate tester for generate_consolidated_plan.py. It re-reads the per-cluster `assessment_plan.md`
files (the authored source of truth) and **independently** parses the generated consolidated doc, then
asserts the consolidated is an exact faithful union of the sources:

  - AT roster — every cluster·AT (mode, unit focus) present, none extra;
  - UoC coverage rollup — every item maps to exactly the cluster·AT set the sources cover it with;
  - aggregated SR register — every SR-* row (id, condition, AT(s), AC link) present, none extra.

This catches a stale consolidated (a per-cluster plan changed, the aggregate wasn't regenerated), a
hand-edit, or a generator bug — without trusting the generator's writer.

Usage:
  validate_consolidated_plan.py --semester S1 [--repo <content repo root>] [--consolidated <path>]

Exit 0 = PASS (consolidated is an exact, faithful union of the per-cluster plans).
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_consolidated_plan as gen


def _rows(text, header_kw):
    """Yield cell-lists of the table whose header line contains header_kw."""
    lines, intable = text.splitlines(), False
    for ln in lines:
        s = ln.strip()
        if s.startswith("|") and header_kw in s:
            intable = True
            continue
        if intable:
            if not s.startswith("|"):
                intable = False
                continue
            if re.fullmatch(r"\|[\s|:-]+\|?", s):  # separator row
                continue
            yield [c.strip() for c in s.strip("|").split("|")]


def parse_consolidated(path: Path):
    text = path.read_text(encoding="utf-8")
    ats, coverage, srs = set(), {}, set()
    for c in _rows(text, "Cluster |"):
        if len(c) >= 4:
            m = re.match(r"(AT\d+)\s+—\s+(.*)", c[1])
            if m:
                ats.add((c[0], m.group(1), m.group(2).strip(), c[2], c[3]))
    for c in _rows(text, "UoC item |"):
        if len(c) >= 2:
            tag = c[0].strip().strip("[]").strip()
            coverage[tag] = {w.strip() for w in c[1].split(",") if w.strip()}
    for c in _rows(text, "Condition the scenario"):
        if len(c) >= 4 and c[0].startswith("SR-"):
            srs.add((c[0], c[1], c[2], c[3]))
    return ats, coverage, srs


def expected_from_sources(plans):
    ats = {(p["cluster"], at, title, mode, unit)
           for p in plans for (at, title, mode, unit) in p["ats"]}
    coverage = {}
    for p in plans:
        for tag, where in p["coverage"].items():
            coverage.setdefault(tag, set()).update(where)
    srs = {sr for p in plans for sr in p["srs"]}
    return ats, coverage, srs


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description="Validate a consolidated assessment plan vs its sources.")
    ap.add_argument("--semester", required=True)
    ap.add_argument("--repo", type=Path, default=gen.REPO)
    ap.add_argument("--consolidated", type=Path)
    args = ap.parse_args()

    consolidated = args.consolidated or (args.repo / "assessment-plans" / f"{args.semester}.md")
    paths = gen.discover_plans(args.repo, args.semester)
    if not consolidated.exists():
        print(f"No consolidated plan at {consolidated} — run generate_consolidated_plan.py first."); sys.exit(2)
    if not paths:
        print(f"No per-cluster source plans for {args.semester}."); sys.exit(2)

    plans = [gen.parse_plan(p) for p in paths]
    exp_ats, exp_cov, exp_srs = expected_from_sources(plans)
    act_ats, act_cov, act_srs = parse_consolidated(consolidated)

    print(f"=== {consolidated} vs {len(plans)} source plan(s) ===")
    problems = []

    for label, exp, act in (("AT roster", exp_ats, act_ats), ("SR register", exp_srs, act_srs)):
        for miss in sorted(exp - act):
            problems.append(f"{label}: MISSING from consolidated — {miss}")
        for extra in sorted(act - exp):
            problems.append(f"{label}: EXTRA in consolidated (not in sources) — {extra}")

    for tag in sorted(set(exp_cov) | set(act_cov), key=lambda t: t):
        e, a = exp_cov.get(tag), act_cov.get(tag)
        if e is None:
            problems.append(f"coverage: EXTRA item in consolidated — [{tag}] ({sorted(a)})")
        elif a is None:
            problems.append(f"coverage: MISSING item in consolidated — [{tag}] (sources: {sorted(e)})")
        elif e != a:
            problems.append(f"coverage: [{tag}] sources={sorted(e)} consolidated={sorted(a)}")

    if not problems:
        print(f"  PASS — faithful union: {len(exp_ats)} ATs, {len(exp_cov)} UoC items, {len(exp_srs)} SR")
        print("\nRESULT: PASS"); sys.exit(0)
    print(f"  FAIL — {len(problems)} discrepancy(ies):")
    for p in problems[:40]:
        print(f"    [FAIL] {p}")
    if len(problems) > 40:
        print(f"    … and {len(problems) - 40} more")
    print("\nRESULT: FAIL"); sys.exit(1)


if __name__ == "__main__":
    main()
