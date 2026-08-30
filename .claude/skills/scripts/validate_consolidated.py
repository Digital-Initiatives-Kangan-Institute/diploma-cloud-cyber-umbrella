#!/usr/bin/env python3
"""Validate that a cluster's consolidated_uoc.md references every PC/FS/PE/KE/AC
from each source UoC exactly once.

General, argument-driven version of validate_consolidated_uoc.py (which is
hardcoded to S1-CL2). Parsing logic is identical; the cluster directory, the
source unit files, and the trailing-assessor-AC behaviour are all parameters,
so the same tool validates any cluster.

Usage:
  validate_consolidated.py --cluster <CLUSTER_DIR> \
      --unit ICTCLD504=units_of_competency/ICTCLD504_Complete_R1.md \
      --unit BSBXTW401=units_of_competency/BSBXTW401_Complete_R2.md \
      [--assessor-ac]

  --cluster        path to the cluster dir (contains consolidated_uoc.md)
  --unit CODE=PATH  a source unit: its tag code and its .md path (relative to
                    the cluster dir, or absolute). Repeatable.
  --assessor-ac     count the trailing "Assessors of this unit must satisfy..."
                    paragraph as one extra AC item per unit. Omit for clusters
                    that do not tag it.

Exit 0 = PASS (every expected item present exactly once, nothing extra).
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import inventory_uoc  # noqa: E402
from validate_uoc import normalise_cosmetic  # noqa: E402


TAG_RE = r"\[(ICT\w+|BSB\w+|VU\d+) (PC|FS|PE|KE|AC) ([^\]]+)\]"


def build_inventory(units: list[tuple[str, Path]], assessor_ac: bool) -> dict[str, str]:
    """The expected items, {tag: verbatim item block}, from the source UoCs.

    Itemisation is delegated to inventory_uoc — the same extractor that produces the item lines
    in the first place. There is deliberately no second copy of the parsing rules here: two
    mirrored parsers that must agree are a maintenance hazard, not independent evidence. The
    independent check on the .md's structure lives upstream at Gate 1, where the .docx is the
    oracle.
    """
    expected = {}
    for unit, md_path in units:
        md = md_path.read_text(encoding="utf-8")
        for _header, items in inventory_uoc.inventory(unit, md, assessor_ac):
            for block in items:
                m = re.search(TAG_RE, block)
                expected[f"{m.group(1)} {m.group(2)} {m.group(3).strip()}"] = block
    return expected


def extract_refs(text: str) -> list[tuple[str, str, str]]:
    """Pull every reference tag from the consolidated doc, skipping code spans."""
    cleaned = re.sub(r"`[^`]*`", "", text)
    return re.findall(TAG_RE, cleaned)


def item_blocks(text: str) -> dict[str, str]:
    """{tag: item block} for the consolidated doc's tagged bullet lines.

    An item line is a bullet carrying its tag OUTSIDE a code span — editorial prose cites tags in
    backticks, and must not be mistaken for an item. The block runs on through any following
    indented, untagged sub-bullets, which belong to that item.
    """
    lines = text.splitlines()
    out = {}
    for i, line in enumerate(lines):
        bare = re.sub(r"`[^`]*`", "", line)
        if not re.match(r"^[-*] ", line):
            continue
        m = re.search(TAG_RE, bare)
        if not m:
            continue
        block = [line]
        for nxt in lines[i + 1:]:
            if re.match(r"^\s+[-*] ", nxt) and not re.search(TAG_RE, re.sub(r"`[^`]*`", "", nxt)):
                block.append(nxt)
            else:
                break
        out.setdefault(f"{m.group(1)} {m.group(2)} {m.group(3).strip()}", "\n".join(block))
    return out


def item_words(block: str) -> list[str]:
    """An item's text as a word sequence, for comparison against its source.

    Everything that is rendering rather than content is removed: the tag, bullet markers and
    indentation, bold markers, and <br> cell separators. Word's cosmetic substitutions are
    normalised with the same rule Gate 1 uses, so a smart quote is not a mistranscription.
    """
    text = re.sub(TAG_RE, "", block)
    text = re.sub(r"<br\s*/?>", " ", text).replace("**", "")
    text = re.sub(r"^\s*[-*]\s+", "", text, flags=re.M)
    return normalise_cosmetic(text).split()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cluster", required=True, type=Path)
    ap.add_argument("--unit", required=True, action="append",
                    help="CODE=relative/or/abs/path.md")
    ap.add_argument("--assessor-ac", action="store_true",
                    help="count trailing assessor-requirements paragraph as an AC item")
    args = ap.parse_args()

    cluster_dir = args.cluster
    units = []
    for spec in args.unit:
        code, _, path = spec.partition("=")
        if not code or not path:
            ap.error(f"--unit must be CODE=PATH, got {spec!r}")
        p = Path(path)
        if not p.is_absolute():
            p = cluster_dir / p
        units.append((code, p))

    consolidated_path = cluster_dir / "consolidated_uoc.md"

    try:
        expected = build_inventory(units, args.assessor_ac)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)
    consolidated = consolidated_path.read_text(encoding="utf-8")
    raw_refs = extract_refs(consolidated)
    found = [f"{u} {s.strip()} {n.strip()}" for u, s, n in raw_refs]
    counts = Counter(found)

    found_set = set(found)
    missing = sorted(set(expected) - found_set)
    unexpected = sorted(found_set - set(expected))
    duplicated = sorted([(ref, c) for ref, c in counts.items() if c > 1])

    # Every item present under the right tag must also still say what the source says.
    blocks = item_blocks(consolidated)
    mistranscribed = []
    for ref in sorted(set(expected) & found_set):
        block = blocks.get(ref)
        if block is None:
            mistranscribed.append((ref, "no item line carries this tag (cited in prose only)"))
        elif item_words(block) != item_words(expected[ref]):
            mistranscribed.append((ref, "text differs from the source unit"))

    print(f"Cluster:          {cluster_dir.name}")
    print(f"Units:            {', '.join(u for u, _ in units)}")
    print(f"Assessor-AC mode: {'on' if args.assessor_ac else 'off'}")
    print(f"Expected items:   {len(expected)}")
    print(f"Found references: {len(found)} ({len(found_set)} unique)")
    print()

    if missing:
        print(f"MISSING ({len(missing)}):")
        for ref in missing:
            print(f"  - {ref}")
        print()

    if unexpected:
        print(f"UNEXPECTED ({len(unexpected)}):")
        for ref in unexpected:
            print(f"  - {ref}  (count={counts[ref]})")
        print()

    if duplicated:
        print(f"DUPLICATED ({len(duplicated)}):")
        for ref, c in duplicated:
            print(f"  - {ref}  ({c} times)")
        print()

    if mistranscribed:
        print(f"MISTRANSCRIBED ({len(mistranscribed)}):")
        for ref, why in mistranscribed:
            print(f"  - {ref}  ({why})")
            src = " ".join(item_words(expected[ref]))
            got = " ".join(item_words(blocks[ref])) if ref in blocks else ""
            print(f"      source: {src[:160]}")
            print(f"      doc:    {got[:160]}")
        print()

    if not missing and not unexpected and not duplicated and not mistranscribed:
        print("RESULT: PASS — every expected item appears exactly once, verbatim, nothing extra.")
        sys.exit(0)
    else:
        print("RESULT: FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
