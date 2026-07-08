#!/usr/bin/env python3
"""Delivery coverage — do a cluster's TEACHING Topics, taken together, teach EVERY UoC item the
assessment assesses? This is the delivery-side analogue of validate_cluster_coverage: the assessment
side proves every consolidated item is *assessed*; this proves every assessed item is *taught*.

It builds the expected item set from the cluster's consolidated_uoc.md and collects the UoC references
from each Topic's coverage.md — specifically the "taught / developed" mapping (NOT the 'applied earlier'
or 'out of scope' sections, so an item only-ever-applied or deferred surfaces as a genuine gap).

CRUCIALLY it uses the SAME tag standard as the assessment side: it imports valid_tag_set + resolve_tags
from validate_at_traceability (the one shared parser the assessment validators use) and strips code
spans before scanning, so a tag counts here exactly when it would count in an AT — full [UNIT SEC num],
unwrapped (backtick-wrapped tags are prose, not counted), ranges/lists expanded. See
docs/cluster-authoring-conventions.md §1.

Reports:
  * MISSING   — assessed items no Topic teaches (the gap to close).
  * PHANTOM   — coverage refs that are not real consolidated items.
  * NON-CONFORMING (diagnostic) — tags present but not to standard (backtick-wrapped, or bare
    section-only with no number) — these don't count, and usually explain a MISSING; the retrofit list.

Usage:
  validate_delivery_coverage.py --cluster <dir> [--consolidated <path>] [--include-fs] [--include-ac]

Exit 0 = PASS (every required item is taught; no phantom).
"""
import argparse
import glob
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_at_traceability import valid_tag_set, resolve_tags

# the "taught / developed" mapping heading, and the markers that END it
MAPPING_HEADING = re.compile(r"^#{1,4}\s.*UoC\s+mapping", re.IGNORECASE)
APPLIED_MARKER = re.compile(r"applied\b.*\b(earlier|elsewhere|taught)", re.IGNORECASE)
NEXT_H2 = re.compile(r"^##\s")
WRAPPED_TAG = re.compile(r"`\[(?:ICT\w+|BSB\w+|VU\d+)\s+(?:PC|FS|PE|KE|AC)\b[^\]]*\]`")
BARE_TAG = re.compile(r"\[(?:ICT\w+|BSB\w+|VU\d+)\s+(?:PC|FS|PE|KE|AC)\]")


def taught_block(text: str) -> str:
    """The 'taught / developed' portion of a coverage.md: from the 'UoC mapping' heading to the next
    '## ' heading, truncated at any 'applied earlier' marker so only taught-here tags are scanned."""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if MAPPING_HEADING.match(ln.strip()):
            start = i + 1
            break
    if start is None:
        return ""
    out = []
    for ln in lines[start:]:
        if NEXT_H2.match(ln) or APPLIED_MARKER.search(ln):
            break
        out.append(ln)
    return "\n".join(out)


def topic_tags(path: Path):
    """(resolved taught tags, wrapped-count, bare-count) for one coverage.md."""
    text = path.read_text(encoding="utf-8")
    block = taught_block(text)
    wrapped = len(WRAPPED_TAG.findall(block))
    bare = len(BARE_TAG.findall(block))
    stripped = re.sub(r"`[^`]*`", "", block)  # enforce unwrapped — same rule as valid_tag_set
    tags = set()
    for line in stripped.splitlines():
        for tag, _form in resolve_tags(line):
            if not tag.startswith("?? "):
                tags.add(tag)
    return tags, wrapped, bare


def by_section(tags):
    out = {}
    for t in sorted(tags):
        sec = t.split()[1] if len(t.split()) > 1 else "?"
        out.setdefault(sec, []).append(t)
    return out


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    ap = argparse.ArgumentParser(description="Delivery coverage: do the Topics teach every assessed UoC item?")
    ap.add_argument("--cluster", required=True, type=Path)
    ap.add_argument("--consolidated", type=Path, help="defaults to <cluster>/consolidated_uoc.md")
    ap.add_argument("--include-fs", action="store_true",
                    help="require FS (foundation skills) too; off by default (FS is embedded, rarely tagged in teaching)")
    ap.add_argument("--include-ac", action="store_true",
                    help="require AC too; off by default (AC is an assessment condition, not taught content)")
    args = ap.parse_args()

    consolidated = args.consolidated or (args.cluster / "consolidated_uoc.md")
    if not consolidated.is_file():
        print(f"ERROR: consolidated_uoc.md not found: {consolidated}")
        sys.exit(2)
    expected = valid_tag_set(consolidated)

    covers = sorted(glob.glob(str(args.cluster / "delivery" / "topic_*" / "coverage.md")))
    if not covers:
        print(f"ERROR: no delivery/topic_*/coverage.md under {args.cluster}")
        sys.exit(2)

    per_topic, all_refs = {}, Counter()
    wrapped_total = bare_total = 0
    for c in covers:
        p = Path(c)
        tags, wrapped, bare = topic_tags(p)
        per_topic[p.parent.name] = (tags, wrapped, bare)
        all_refs.update(tags)
        wrapped_total += wrapped
        bare_total += bare
    covered = set(all_refs)

    secof = lambda t: t.split()[1] if len(t.split()) > 1 else "?"
    def required_section(sec):
        if sec == "AC":
            return args.include_ac
        if sec == "FS":
            return args.include_fs
        return sec in ("PC", "PE", "KE")
    required = {t for t in expected if required_section(secof(t))}

    missing = sorted(required - covered)
    phantom = sorted(covered - expected)

    print(f"Cluster:   {args.cluster.name}")
    print(f"Topics:    {len(per_topic)} coverage.md")
    print(f"Required:  {len(required)} items (PC/PE/KE"
          + ("/FS" if args.include_fs else "") + ("/AC" if args.include_ac else "") + ")")
    print(f"Taught:    {len(covered & required)} / {len(required)} "
          f"({100 * len(covered & required) // max(len(required), 1)}%)")
    print()
    for name, (tags, wrapped, bare) in per_topic.items():
        flags = []
        if wrapped:
            flags.append(f"{wrapped} backtick-wrapped")
        if bare:
            flags.append(f"{bare} bare/un-numbered")
        note = f"   [non-conforming: {', '.join(flags)}]" if flags else ""
        print(f"  {name}: {len(tags & expected)} taught{note}")
    print()

    if wrapped_total or bare_total:
        print(f"NON-CONFORMING TAGS (do not count under the standard — retrofit to [UNIT SEC num], "
              f"unwrapped): {wrapped_total} backtick-wrapped, {bare_total} bare/un-numbered.")
        print()

    if phantom:
        print(f"PHANTOM ({len(phantom)}) — coverage refs not in the consolidated UoC:")
        for sec, tags in by_section(phantom).items():
            for t in tags:
                print(f"  - {t}")
        print()

    if missing:
        print(f"MISSING ({len(missing)}) — assessed items no Topic teaches:")
        for sec, tags in by_section(missing).items():
            print(f"  {sec}:")
            for t in tags:
                print(f"    - {t}")
        print()

    if not missing and not phantom:
        print("RESULT: PASS - every assessed item is taught by at least one Topic.")
        sys.exit(0)
    print("RESULT: FAIL"
          + (" - untaught items remain" if missing else "")
          + (" - phantom references present" if phantom else "") + ".")
    sys.exit(1)


if __name__ == "__main__":
    main()
