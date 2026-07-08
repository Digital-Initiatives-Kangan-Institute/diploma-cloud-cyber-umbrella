#!/usr/bin/env python3
"""Validate a cluster-specification.md (the delivery-run-sheet Step-1 frame).

Deterministic, stdlib-only. The CONTRACT is not hard-coded here: the linter reads the
format document's ``## Skeleton`` block (docs/cluster-specification-format.md) to learn the
required headings and field labels, so the format doc is the single source of truth. On top
of that structural check it verifies the deterministic arithmetic.

Checks:
  - every heading + field NAMED IN THE SKELETON is present and non-empty;
  - frame arithmetic reconciles (total sessions, delivered hours, variance);
  - topic-budget arithmetic reconciles (reserved + available = total);
  - over-nominal hours carry a recorded authorisation.

Anything requiring JUDGMENT (is the variance acceptable, is the topic count sensible) is NOT
here — that is the human's acceptance call (and, at later delivery steps, an agent validator).
Variance is REPORTED, never failed on its own.

Usage:
  python validate_cluster_spec.py --spec <cluster>/cluster-specification.md
  python validate_cluster_spec.py --cluster <S1-CLx dir>      # finds the spec inside
  [--format <path to cluster-specification-format.md>]        # auto-located if omitted

Exit 0 on PASS, 1 otherwise.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Arithmetic relationships are intrinsic (not expressible as mere field presence), so they
# live in code. Field *names* come from the format doc. Keep these labels matching the doc.
F_NOMINAL = "Nominal hours"
F_WEEKS = "Weeks"
F_SPW = "Sessions per week"
F_LENGTH = "Session length (hours)"
F_TOTAL = "Total sessions"
F_DELIVERED = "Delivered hours"
F_VARIANCE = "Variance (nominal − delivered)"
F_AUTH = "Over-nominal authorisation"
B_ONB = "Onboarding sessions"
B_SPARE = "Spare sessions"
B_ASSESS = "Dedicated assessment sessions"
B_AVAIL = "Teaching/practice sessions available"


def find_format_doc(explicit: str | None) -> Path | None:
    if explicit:
        p = Path(explicit)
        return p if p.is_file() else None
    name = "cluster-specification-format.md"
    here = Path(__file__).resolve()
    candidates = [
        Path("docs") / name,                 # cwd = umbrella root
        Path("..") / "docs" / name,          # cwd = content repo
        Path("..") / ".." / "docs" / name,
    ]
    # walk up from the script too (umbrella/diploma-cloud-cyber-content/.claude/skills/scripts)
    for parent in here.parents:
        candidates.append(parent / "docs" / name)
    for c in candidates:
        if c.is_file():
            return c
    return None


def parse_contract(format_text: str) -> tuple[list[str], list[str]]:
    """Extract (headings, field-labels) from the format doc's ``## Skeleton`` code block."""
    m = re.search(r"##\s+Skeleton\s*\n+```[a-zA-Z]*\n(.*?)\n```", format_text, re.DOTALL)
    if not m:
        return [], []
    block = m.group(1)
    headings = re.findall(r"^(##\s+.+?)\s*$", block, re.MULTILINE)
    fields = [lbl.strip() for lbl in re.findall(r"^-\s*([^:\n]+?):", block, re.MULTILINE)]
    # de-dupe, preserve order
    headings = list(dict.fromkeys(headings))
    fields = list(dict.fromkeys(fields))
    return headings, fields


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
    m = re.search(r"[-+]?\d+(?:\.\d+)?", value.replace("−", "-"))
    return float(m.group(0)) if m else None


def fmt(x) -> str:
    return str(int(x)) if x is not None and float(x).is_integer() else str(x)


def main() -> int:
    # Output ASCII-safe even when stdout is a pipe (Windows cp1252 would otherwise crash).
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    ap = argparse.ArgumentParser(description="Validate a cluster-specification.md delivery frame.")
    ap.add_argument("--spec", help="path to cluster-specification.md")
    ap.add_argument("--cluster", help="an S1-CLx dir; finds cluster-specification.md inside")
    ap.add_argument("--format", dest="fmt_doc", help="path to cluster-specification-format.md")
    args = ap.parse_args()

    if args.spec:
        spec = Path(args.spec)
    elif args.cluster:
        spec = Path(args.cluster) / "cluster-specification.md"
    else:
        ap.error("give --spec or --cluster")
    if not spec.is_file():
        print(f"ERROR: spec not found: {spec}")
        return 1

    fmt_doc = find_format_doc(args.fmt_doc)
    if fmt_doc is None:
        print("ERROR: format doc not found - pass --format <cluster-specification-format.md>")
        return 1
    req_headings, req_fields = parse_contract(fmt_doc.read_text(encoding="utf-8"))
    if not req_headings or not req_fields:
        print(f"ERROR: could not parse a contract from {fmt_doc} (## Skeleton block)")
        return 1

    text = spec.read_text(encoding="utf-8")
    errors, warnings, notes = [], [], []

    # --- structure from the format contract ---
    if not re.search(r"^#\s+.+Cluster Specification\s*$", text, re.MULTILINE):
        errors.append("missing title '# <cluster> — Cluster Specification'")
    if not re.search(r"^>\s*\*\*STATUS:", text, re.MULTILINE):
        errors.append("missing '> **STATUS:** …' banner line")
    for h in req_headings:
        if h not in text:
            errors.append(f"missing required heading: {h}")

    fields = parse_fields(text)
    for label in req_fields:
        if label not in fields:
            errors.append(f"missing field: '{label}'")
        elif fields[label] == "":
            errors.append(f"empty field: '{label}'")

    # --- frame arithmetic ---
    nominal = num(fields.get(F_NOMINAL))
    weeks = num(fields.get(F_WEEKS))
    spw = num(fields.get(F_SPW))
    length = num(fields.get(F_LENGTH))
    total = num(fields.get(F_TOTAL))
    delivered = num(fields.get(F_DELIVERED))
    variance = num(fields.get(F_VARIANCE))
    auth = fields.get(F_AUTH, "").strip().lower()

    if None not in (weeks, spw, total) and weeks * spw != total:
        errors.append(
            f"total sessions {fmt(total)} != weeks x sessions/week "
            f"({fmt(weeks)} x {fmt(spw)} = {fmt(weeks*spw)})"
        )
    if None not in (total, length, delivered) and total * length != delivered:
        errors.append(
            f"delivered hours {fmt(delivered)} != total sessions x length "
            f"({fmt(total)} x {fmt(length)} = {fmt(total*length)})"
        )
    if None not in (nominal, delivered, variance) and nominal - delivered != variance:
        errors.append(
            f"variance {fmt(variance)} != nominal - delivered "
            f"({fmt(nominal)} - {fmt(delivered)} = {fmt(nominal-delivered)})"
        )

    # --- over-nominal authorisation rule ---
    if None not in (nominal, delivered):
        overage = delivered - nominal
        if overage > 0:
            if auth in ("", "n/a", "na", "none", "no"):
                errors.append(
                    f"over nominal by {fmt(overage)}h but '{F_AUTH}' is "
                    f"'{fields.get(F_AUTH,'')}' — record who authorised it"
                )
            else:
                notes.append(f"runs {fmt(overage)}h OVER nominal - authorised: {fields.get(F_AUTH)}")
        elif overage < 0:
            notes.append(f"runs {fmt(-overage)}h UNDER nominal (unused budget)")
        else:
            notes.append("delivers exactly the nominal hours")

    # --- topic-budget arithmetic ---
    onb = num(fields.get(B_ONB))
    spare = num(fields.get(B_SPARE))
    dass = num(fields.get(B_ASSESS))
    avail = num(fields.get(B_AVAIL))
    if None not in (onb, spare, dass, avail, total) and onb + spare + dass + avail != total:
        errors.append(
            f"topic-budget sessions don't reconcile: onboarding+spare+assessment+available "
            f"({fmt(onb)}+{fmt(spare)}+{fmt(dass)}+{fmt(avail)} = {fmt(onb+spare+dass+avail)}) "
            f"!= total sessions {fmt(total)}"
        )

    # --- soft cross-check: declared units vs consolidated_uoc.md ---
    cons = spec.parent / "consolidated_uoc.md"
    banner = re.search(r"^>\s*\*\*STATUS:.*$", text, re.MULTILINE)
    if cons.is_file() and banner:
        declared = set(re.findall(r"[A-Z]{3,}[A-Z0-9]+\d", banner.group(0)))
        if declared:
            ctext = cons.read_text(encoding="utf-8", errors="ignore")
            missing = sorted(u for u in declared if u not in ctext)
            if missing:
                warnings.append(
                    f"unit(s) in banner not found in consolidated_uoc.md: {', '.join(missing)}"
                )

    # --- report ---
    name = spec.parent.name
    print(f"  contract: {fmt_doc}  ({len(req_headings)} headings, {len(req_fields)} fields)")
    for n in notes:
        print(f"  [frame] {name}: {n}")
    for w in warnings:
        print(f"  [warn]  {w}")

    if errors:
        print()
        for e in errors:
            print(f"  FAIL: {e}")
        print(f"\nRESULT: FAIL — {len(errors)} issue(s) in {spec}")
        return 1

    print(f"\nRESULT: PASS — {spec} is a complete, internally-consistent delivery frame.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
