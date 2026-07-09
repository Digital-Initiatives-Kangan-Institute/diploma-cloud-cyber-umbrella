#!/usr/bin/env python3
"""Validate a cluster's TOPIC BREAKDOWN — the delivery run-sheet Gate 2->3 structural lint.

Deterministic, stdlib-only. Confirms the AT -> Topic decomposition is structurally sound (the light
structural check the run-sheet names) BEFORE the Topic specs and decks are built. It reads the
breakdown as recorded in each Topic's coverage.md, and checks:

  A. every AT (a `assessments/AT<n>/` folder) is covered by >=1 Topic;
  B. every Topic (a `delivery/topic_NN/` folder) declares its AT via the canonical coverage.md intro
     marker `**AT<n> content Topic**`, and that AT is a real one (no phantom AT); where the Topic also
     carries an `## N. AT<n> equivalence/alignment` heading, it must AGREE with the intro marker;
  C. the Topic count fits the frame — it must be <= the cluster-specification's
     `Teaching/practice sessions available` (each Topic needs at least one session). Divergence from the
     `Nominal topic count` is REPORTED, never failed (the nominal count is an estimate, confirmed here).

What it does NOT do: judge whether these are the RIGHT Topics or whether the split is pedagogically
sound — that stays the human's acceptance call. This is structure, not quality (the UoC-coverage depth
is the separate Gate 3->4 check, validate_delivery_coverage.py).

Usage:
  python validate_topic_breakdown.py --cluster <S1-CLx dir>
Exit 0 = PASS, 1 = FAIL, 2 = usage/error.
"""
from __future__ import annotations

import argparse
import glob
import re
import sys
from pathlib import Path

INTRO_AT = re.compile(r"\*\*AT(\d+)\s+content Topic\*\*")
SECTION_AT = re.compile(r"^#{2,4}\s*\d*\.?\s*AT(\d+)\s+(?:equivalence|alignment)", re.IGNORECASE | re.MULTILINE)
AT_DIR = re.compile(r"^AT\d+$")

F_AVAIL = "Teaching/practice sessions available"
F_NOMINAL = "Nominal topic count"


def parse_fields(text: str) -> dict:
    fields = {}
    for line in text.splitlines():
        m = re.match(r"\s*-\s*([^:]+?):\s*(.*?)\s*$", line)
        if m:
            fields[m.group(1).strip()] = m.group(2).strip()
    return fields


def num(value):
    if value is None:
        return None
    m = re.search(r"[-+]?\d+", value.replace("−", "-"))
    return int(m.group(0)) if m else None


def topic_at(coverage_text: str):
    """(intro_at, section_at) as strings 'AT<n>' or None each, read from a coverage.md."""
    mi = INTRO_AT.search(coverage_text)
    ms = SECTION_AT.search(coverage_text)
    return (f"AT{mi.group(1)}" if mi else None, f"AT{ms.group(1)}" if ms else None)


def main() -> int:
    # ASCII-safe even when stdout is a pipe (Windows cp1252 would otherwise crash on the box glyphs).
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    ap = argparse.ArgumentParser(description="Validate a cluster's Topic breakdown (delivery Gate 2->3).")
    ap.add_argument("--cluster", required=True, type=Path, help="an S1-CLx cluster dir")
    args = ap.parse_args()

    cluster = args.cluster
    if not cluster.is_dir():
        print(f"ERROR: cluster dir not found: {cluster}")
        return 2

    # --- the AT set (assessments/AT<n>/) ---
    assess = cluster / "assessments"
    ats = sorted(d.name for d in assess.iterdir() if d.is_dir() and AT_DIR.match(d.name)) \
        if assess.is_dir() else []
    if not ats:
        print(f"ERROR: no assessments/AT<n>/ folders under {cluster}")
        return 2

    # --- the Topic folders (delivery/topic_NN/) ---
    topic_dirs = sorted(Path(p) for p in glob.glob(str(cluster / "delivery" / "topic_*"))
                        if Path(p).is_dir())
    if not topic_dirs:
        print(f"ERROR: no delivery/topic_*/ folders under {cluster}")
        return 2

    errors, warnings = [], []
    at_topics = {a: [] for a in ats}     # AT -> [topic names]
    for td in topic_dirs:
        cov = td / "coverage.md"
        if not cov.is_file():
            errors.append(f"{td.name}: no coverage.md — Topic does not declare its AT")
            continue
        intro, section = topic_at(cov.read_text(encoding="utf-8"))
        if intro is None:
            errors.append(f"{td.name}: no '**AT<n> content Topic**' marker — Topic does not declare its AT")
            continue
        if intro not in ats:
            errors.append(f"{td.name}: declares {intro}, which is not a real AT (have {', '.join(ats)})")
            continue
        if section is not None and section != intro:
            errors.append(f"{td.name}: AT mismatch — intro says {intro} but the alignment heading says {section}")
            continue
        at_topics[intro].append(td.name)

    # --- Check A: every AT has >=1 Topic ---
    for a in ats:
        if not at_topics[a]:
            errors.append(f"{a}: no Topic is assigned to it (every AT needs >=1 Topic)")

    # --- Check C: Topic count fits the frame ---
    spec = cluster / "cluster-specification.md"
    n_topics = len(topic_dirs)
    if spec.is_file():
        fields = parse_fields(spec.read_text(encoding="utf-8"))
        avail = num(fields.get(F_AVAIL))
        nominal = num(fields.get(F_NOMINAL))
        if avail is not None and n_topics > avail:
            errors.append(f"{n_topics} Topics > {avail} teaching/practice sessions available — cannot fit the frame")
        if nominal is not None and n_topics != nominal:
            warnings.append(f"{n_topics} Topics != nominal topic count {nominal} (estimate) — confirm the divergence is intended")
    else:
        warnings.append("no cluster-specification.md — skipped the frame-fit check (Check C)")

    # --- report ---
    print(f"Cluster:  {cluster.name}")
    print(f"ATs:      {len(ats)} ({', '.join(ats)})")
    print(f"Topics:   {n_topics} (delivery/topic_*/)")
    for a in ats:
        ts = at_topics[a]
        print(f"  {a}: {len(ts)} Topic(s){' — ' + ', '.join(ts) if ts else ''}")
    for w in warnings:
        print(f"  [warn]  {w}")

    if errors:
        print()
        for e in errors:
            print(f"  FAIL: {e}")
        print(f"\nRESULT: FAIL — {len(errors)} structural issue(s) in the Topic breakdown of {cluster.name}")
        return 1

    print(f"\nRESULT: PASS — every AT has a Topic, every Topic declares a valid AT, "
          f"and {n_topics} Topics fit the frame.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
