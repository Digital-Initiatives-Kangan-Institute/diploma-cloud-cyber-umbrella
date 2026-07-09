#!/usr/bin/env python3
"""Deck reproduction check — does a regenerated .pptx reproduce the committed one?

The gate for migrating a hand-scripted teaching deck to the generic slide-plan builder: build the deck
from a content-complete slide_plan.md and prove it reproduces the committed deck at content level —
per-slide **body text** (titles + bullets, in order), **teacher notes**, and per-slide **image count**.
Byte/XML identity is impossible (different builders author different markup), so the bar is content +
order equivalence. The .pptx analogue of validate_instrument_reproduction.py.

Extraction (stdlib zipfile + ElementTree): slides are read in numeric part order (slide1.xml, slide2.xml,
…); each slide's paragraphs (`<a:p>` → concatenated `<a:t>`) are the body lines; its linked notesSlide's
paragraphs are the notes (a trailing bare slide-number line dropped); `<a:blip>` count = images.

Usage:
  python validate_deck_reproduction.py --candidate <regen.pptx> --reference <committed.pptx>
  python validate_deck_reproduction.py --candidate a.pptx --reference b.pptx --no-notes --sub 'OLD::NEW'
Exit 0 = PASS (reproduces), 1 = FAIL (content differs), 2 = usage/error.
"""
from __future__ import annotations

import argparse
import difflib
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
RELNS = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def _paras(root) -> list[str]:
    out = []
    for p in root.iter(A + "p"):
        s = "".join(t.text or "" for t in p.iter(A + "t"))
        s = re.sub(r"\s+", " ", s).strip()
        if s:
            out.append(s)
    return out


def _slide_parts(z: zipfile.ZipFile) -> list[str]:
    names = [n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)]
    return sorted(names, key=lambda n: int(re.search(r"slide(\d+)\.xml", n).group(1)))


def _notes_for(z: zipfile.ZipFile, slide_part: str) -> list[str]:
    rels = "ppt/slides/_rels/" + slide_part.split("/")[-1] + ".rels"
    if rels not in z.namelist():
        return []
    root = ET.fromstring(z.read(rels))
    tgt = next((r.get("Target") for r in root.iter(RELNS + "Relationship")
                if "notesSlide" in (r.get("Type") or "")), None)
    if not tgt:
        return []
    part = "ppt/" + tgt.replace("../", "")
    if part not in z.namelist():
        return []
    lines = _paras(ET.fromstring(z.read(part)))
    if lines and lines[-1].isdigit():   # drop the slide-number placeholder
        lines = lines[:-1]
    return lines


def extract(path: Path) -> list[dict]:
    with zipfile.ZipFile(path) as z:
        out = []
        for sp in _slide_parts(z):
            root = ET.fromstring(z.read(sp))
            out.append({"body": _paras(root),
                        "notes": _notes_for(z, sp),
                        "images": sum(1 for _ in root.iter(A + "blip"))})
        return out


def _flat(slides, key):
    # pure text in document order (no per-slide index prefix) so difflib aligns across an
    # inserted/removed slide — e.g. a deliberately-added section divider shows as one clean
    # insertion, not a cascade of index-shifted "changes".
    return [ln for s in slides for ln in s[key]]


def _diff(ref, cand, label):
    if ref == cand:
        return True, ""
    d = [x for x in difflib.unified_diff(ref, cand, n=0, lineterm="") if not x.startswith(("---", "+++", "@@"))]
    body = "\n".join(f"  {x}" for x in d[:40])
    if len(d) > 40:
        body += "\n  … (truncated)"
    return False, body


def main() -> int:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Does a regenerated deck reproduce the committed one?")
    ap.add_argument("--candidate", required=True, type=Path)
    ap.add_argument("--reference", required=True, type=Path)
    ap.add_argument("--no-notes", action="store_true", help="skip the teacher-notes comparison")
    ap.add_argument("--sub", action="append", default=[], metavar="OLD::NEW",
                    help="rewrite OLD->NEW in the REFERENCE text before diffing (absorb a deliberate change)")
    args = ap.parse_args()
    for p in (args.candidate, args.reference):
        if not p.is_file():
            print(f"ERROR: not found: {p}"); return 2

    cand, ref = extract(args.candidate), extract(args.reference)
    rb, cb = _flat(ref, "body"), _flat(cand, "body")
    rn, cn = _flat(ref, "notes"), _flat(cand, "notes")
    for rule in args.sub:
        if "::" not in rule:
            print(f"ERROR: --sub must be OLD::NEW, got {rule!r}"); return 2
        old, new = rule.split("::", 1)
        rb = [x.replace(old, new) for x in rb]; rn = [x.replace(old, new) for x in rn]

    print(f"Candidate: {args.candidate.name}  ({len(cand)} slides, {sum(s['images'] for s in cand)} images, {len(cn)} note lines)")
    print(f"Reference: {args.reference.name}  ({len(ref)} slides, {sum(s['images'] for s in ref)} images, {len(rn)} note lines)")

    ok_body, dbody = _diff(rb, cb, "body")
    ok_notes, dnotes = (True, "") if args.no_notes else _diff(rn, cn, "notes")
    ok_img = sum(s["images"] for s in cand) == sum(s["images"] for s in ref)

    print(f"  body text:  {'PASS' if ok_body else 'FAIL'}   notes: {'skipped' if args.no_notes else ('PASS' if ok_notes else 'FAIL')}   image count: {'match' if ok_img else 'DIFFERS'}")
    if not ok_body:
        print("Body differences (- committed / + regenerated):\n" + dbody)
    if not ok_notes:
        print("Notes differences (- committed / + regenerated):\n" + dnotes)

    if ok_body and ok_notes:
        print("\nRESULT: PASS — the regenerated deck reproduces the committed one"
              + ("" if ok_img else " (⚠ image count differs — check placement)") + ".")
        return 0
    print("\nRESULT: FAIL — deck content differs.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
