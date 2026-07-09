#!/usr/bin/env python3
"""Student-instrument leak-lint — the mechanical half of the assessment run-sheet Gate 9->10.

A student-facing assessment instrument is derived from the assessor version by STRIPPING the
assessor-only content (the Marking Guide's benchmarks, model answers, assessor instructions, and the
UoC mapping). This deterministic, stdlib-only lint proves none of that assessor-only material leaked
into a `*-Student.docx` — the same "no UoC codes on a student-facing artefact" rule already enforced on
student slides, generalised to the assessment instruments.

Two tiers, calibrated against the approved S1 student copies (all clean — 0 hits):
  HARD FAIL (the mapping/benchmark definitively leaked):
    * canonical UoC tags `[UNIT SEC num]` (e.g. [ICTCLD502 PC 1.1]) — the mapping;
    * unambiguous assessor-only labels: Assessor Instructions / Model Answer / Benchmark /
      Marking Criteria.
  WARN (softer VET vocabulary — surface for the human to confirm it isn't a mapping/benchmark leak):
    * Performance Criteria / Performance Evidence / Foundation Skills / Assessment Conditions /
      Unit of Competency / Assessment Mapping.

Deliberately NOT flagged (legitimate on a student copy): the sanctioned **UoC footer** (bare
`UNITCODE Title` lines — the one approved exception), the deliverable name "Knowledge Evidence"
(the student answers KE questions), a "Marking Guide" *reference* (naming the standard, not the
guide's content), and marking-criterion codes (A11, B12 — an intentional what-you're-assessed-on
checklist). What survives HARD/WARN is a real leak or a judgement call, not routine content.

The residual JUDGEMENT — is the student copy self-contained, in-world, complete — stays the human /
an agent check; this lint only proves the assessor-only material is gone.

Usage:
  python validate_student_instrument.py --cluster <SX-CLY dir>   # lint every AT<n>/*Student.docx
  python validate_student_instrument.py --file <one *-Student.docx>
Exit 0 = PASS (no leak), 1 = FAIL (a HARD leak in >=1 file), 2 = usage/error.
"""
from __future__ import annotations

import argparse
import glob
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_uoc import docx_to_text

UOC_TAG = re.compile(r"\[[A-Z]{3,6}\d{3}\s+(?:PC|PE|KE|FS|AC)\b[^\]]*\]")
# assessor-only labels — structural markers of stripped content; verified absent from approved
# student copies, so their presence is a real leak. `s?` allows the plural.
HARD_LABELS = [re.compile(r"\bAssessor Instructions?\b", re.I),
               re.compile(r"\bModel Answers?\b", re.I),
               re.compile(r"\bBenchmarks?\b", re.I),
               re.compile(r"\bMarking Criteria\b", re.I)]
# softer VET vocabulary — usually assessor-side, but could appear legitimately; warn, don't fail.
WARN_TERMS = [re.compile(r"\bPerformance Criteria\b", re.I),
              re.compile(r"\bPerformance Evidence\b", re.I),
              re.compile(r"\bFoundation Skills\b", re.I),
              re.compile(r"\bAssessment Conditions\b", re.I),
              re.compile(r"\bUnit of Competency\b", re.I),
              re.compile(r"\bAssessment Mapping\b", re.I)]


def scan(text: str):
    """Return (uoc_tag_lines, hard_label_lines, warn_lines) — each a list of (marker, line)."""
    tags, hard, warn = [], [], []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        for m in UOC_TAG.findall(line):
            tags.append((m, line))
        for pat in HARD_LABELS:
            hit = pat.search(line)
            if hit:
                hard.append((hit.group(0), line))
        for pat in WARN_TERMS:
            hit = pat.search(line)
            if hit:
                warn.append((hit.group(0), line))
    return tags, hard, warn


def clip(s: str, n: int = 150) -> str:
    s = s.strip()
    return s if len(s) <= n else s[:n - 1] + "…"


def lint_file(path: Path) -> bool:
    """Print a report for one student instrument. Return True if it FAILS (a HARD leak)."""
    tags, hard, warn = scan(docx_to_text(path))
    failed = bool(tags or hard)
    status = "LEAK" if failed else ("clean (warnings)" if warn else "clean")
    print(f"  {path.name}: {status}")
    if tags:
        print(f"    FAIL: {len(tags)} UoC mapping tag(s) — the assessor mapping leaked:")
        for marker, line in tags[:5]:
            print(f"      · {marker}   in: {clip(line)}")
        if len(tags) > 5:
            print(f"      … and {len(tags) - 5} more")
    for marker, line in hard:
        print(f"    FAIL: assessor-only label '{marker}' — in: {clip(line)}")
    for marker, line in warn:
        print(f"    [warn] VET vocabulary '{marker}' — confirm it isn't a mapping/benchmark leak: {clip(line)}")
    return failed


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    ap = argparse.ArgumentParser(description="Student-instrument leak-lint (assessment Gate 9->10).")
    ap.add_argument("--cluster", type=Path, help="a SX-CLY cluster dir; lints every AT<n>/*Student.docx")
    ap.add_argument("--file", type=Path, help="lint a single *-Student.docx")
    args = ap.parse_args()

    if args.file:
        files = [args.file]
    elif args.cluster:
        files = sorted(Path(p) for p in glob.glob(str(args.cluster / "assessments" / "AT*" / "*.docx"))
                       if "student" in Path(p).name.lower())
    else:
        ap.error("give --cluster or --file")

    files = [f for f in files if f.is_file()]
    if not files:
        where = args.file or (args.cluster / "assessments/AT*/*Student.docx")
        print(f"ERROR: no student instrument found: {where}")
        return 2

    label = args.cluster.name if args.cluster else args.file.name
    print(f"Cluster:  {label}")
    print(f"Student instruments: {len(files)}")
    any_fail = False
    for f in files:
        if lint_file(f):
            any_fail = True

    if any_fail:
        print("\nRESULT: FAIL — assessor-only material leaked into a student instrument (strip it).")
        return 1
    print("\nRESULT: PASS — no assessor-only material in the student instrument(s). "
          "(Self-containedness / in-world tone remain the human review.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
