#!/usr/bin/env python3
"""Instrument reproduction check — does a regenerated instrument .docx reproduce the committed one?

The gate for retro-fitting a generator to an authored assessment instrument: build the generator, emit
a candidate .docx, and prove it reproduces the committed reference at the CONTENT level (every heading,
paragraph, and table cell — in order). Byte/XML identity is impossible (python-docx vs Word author
different markup), so the bar is content + order equivalence of the document body.

Comparison:
  * body text of both docs is extracted in document order (paragraphs + table cells) via the pack's
    docx_to_text, normalised (per-line strip; runs of whitespace collapsed; blank lines dropped);
  * optional `--sub OLD::NEW` rewrites OLD->NEW in the REFERENCE before diffing, to absorb a DELIBERATE
    change (e.g. a URL update) so the check still passes when the only intended difference is applied;
  * the two normalised line-sequences are diffed (difflib). PASS = identical.

Usage:
  python validate_instrument_reproduction.py --candidate <regen.docx> --reference <committed.docx>
  python validate_instrument_reproduction.py --candidate a.docx --reference b.docx --sub 'www.placeholder.com.au::yat.timbaird.com'
Exit 0 = PASS (reproduces), 1 = FAIL (content differs), 2 = usage/error.
"""
from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_uoc import docx_to_text


def normalise(text: str) -> list[str]:
    out = []
    for raw in text.splitlines():
        line = re.sub(r"\s+", " ", raw).strip()
        if line:
            out.append(line)
    return out


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    ap = argparse.ArgumentParser(description="Does a regenerated instrument reproduce the committed one?")
    ap.add_argument("--candidate", required=True, type=Path, help="the regenerated .docx")
    ap.add_argument("--reference", required=True, type=Path, help="the committed .docx to reproduce")
    ap.add_argument("--sub", action="append", default=[], metavar="OLD::NEW",
                    help="rewrite OLD->NEW in the REFERENCE before diffing (absorbs a deliberate change)")
    ap.add_argument("--context", type=int, default=1, help="diff context lines (default 1)")
    args = ap.parse_args()

    for p in (args.candidate, args.reference):
        if not p.is_file():
            print(f"ERROR: not found: {p}")
            return 2

    cand = normalise(docx_to_text(args.candidate))
    # Normalise FIRST, then apply subs — so a plain-space rule matches a non-breaking space (or any
    # whitespace) in the source, then re-normalise to tidy any doubled space / emptied line a sub left.
    ref = normalise(docx_to_text(args.reference))
    if args.sub:
        joined = "\n".join(ref)
        for rule in args.sub:
            if "::" not in rule:
                print(f"ERROR: --sub must be OLD::NEW, got {rule!r}")
                return 2
            old, new = rule.split("::", 1)
            joined = joined.replace(old, new)
        ref = normalise(joined)

    print(f"Candidate: {args.candidate.name}  ({len(cand)} content lines)")
    print(f"Reference: {args.reference.name}  ({len(ref)} content lines)")
    if args.sub:
        print(f"Applied {len(args.sub)} deliberate substitution(s) to the reference before diffing.")

    if cand == ref:
        print("\nRESULT: PASS — the regenerated instrument reproduces the committed one "
              "(content + order identical" + (", after the deliberate change" if args.sub else "") + ").")
        return 0

    sm = difflib.SequenceMatcher(a=ref, b=cand, autojunk=False)
    ratio = sm.ratio()
    diff = list(difflib.unified_diff(ref, cand, fromfile="committed", tofile="regenerated",
                                     n=args.context, lineterm=""))
    adds = sum(1 for d in diff if d.startswith("+") and not d.startswith("+++"))
    dels = sum(1 for d in diff if d.startswith("-") and not d.startswith("---"))
    print(f"\nRESULT: FAIL — content differs ({ratio*100:.1f}% similar; {dels} removed, {adds} added).")
    print("First differences (- committed / + regenerated):")
    shown = 0
    for d in diff:
        if d.startswith(("---", "+++")):
            continue
        print(f"  {d}")
        shown += 1
        if shown >= 60:
            print("  … (truncated)")
            break
    return 1


if __name__ == "__main__":
    sys.exit(main())
