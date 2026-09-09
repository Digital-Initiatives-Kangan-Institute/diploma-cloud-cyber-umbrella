#!/usr/bin/env python3
"""Generate each Topic's coverage.md from its slide_plan.md — the delivery run-sheet's Step 3
artefact, derived from the Step 4 one.

The redraft workflow authors slide plans against the assessment workbook's task order; coverage.md is
then REGENERATED from the plans (never hand-edited) so the Gate 3->4 / 4->5 validators check a contract
that matches reality. Parses each plan's `### C<n> — <title>` sections, their `Teaches:` tags and the
workbook tasks their `[EX]` slides culminate in; descriptors come verbatim from consolidated_uoc.md.

Course-agnostic, stdlib-only. The per-cluster input is the AT map — which topics carry which AT:

  scripts/generate_topic_coverage.py --cluster <cluster-dir> --at-map 1-5:AT1,6-9:AT2

Emits the structure the validators require: the `**AT<n> content Topic**` marker
(validate-topic-breakdown), `- **C<n> …` component declarations and the `UoC mapping` table whose last
cell is the component (validate-slide-plan), with canonical unwrapped tags.
"""
import argparse
import re
import sys
from pathlib import Path

TAG = re.compile(r"\[([A-Z]{3,}[A-Z0-9]* (?:PC|PE|KE|FS|AC) [^\]]+)\]")


def parse_at_map(spec: str) -> dict:
    out = {}
    for part in spec.split(","):
        rng, at = part.split(":")
        a, _, b = rng.partition("-")
        for n in range(int(a), int(b or a) + 1):
            out[n] = at
    return out


def descriptors(consolidated: Path) -> dict:
    """Item lines are '- <num> descriptor [TAG]' — tag at end of line."""
    desc = {}
    for ln in consolidated.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^-\s*(?:[\d.]+\s+)?(.+?)\s*\[([^\]]+)\]\s*$", ln)
        if m:
            d = re.sub(r"\s+", " ", re.sub(r"^\*\*|\*\*$", "", m.group(1))).strip(" .*")
            desc.setdefault(m.group(2).strip(), d)
    return desc


def parse_plan(plan_path: Path):
    plan = plan_path.read_text(encoding="utf-8")
    title = re.match(r"#\s+Topic \d+\s+(.+?)\s+— Slide plan", plan.splitlines()[0]).group(1)
    depth = re.search(r"## Depth ceiling\n(.+?)\n\n", plan, re.S).group(1).strip().split("\n\n")[0]
    comps, cur = [], None
    for ln in plan.splitlines():
        m = re.match(r"^###\s+(C\d+)\s*—\s*(.+)$", ln)
        if m:
            cur = {"id": m.group(1), "title": m.group(2).strip(), "tags": [], "culm": None}
            comps.append(cur)
            continue
        if re.match(r"^###\s", ln):
            cur = None
            continue
        if cur is None:
            continue
        if re.match(r"^-\s*Teaches:", ln):
            for t in TAG.findall(ln):
                if t not in cur["tags"]:
                    cur["tags"].append(t)
        wm = re.match(r"^\s+-\s+(Workbook — task[^.]+|The assessment's question[^.]+)\.", ln)
        if wm and cur["culm"] is None:
            cur["culm"] = wm.group(1).replace("Workbook — ", "")
    return title, depth, comps


def main():
    ap = argparse.ArgumentParser(description="Regenerate coverage.md files from slide plans.")
    ap.add_argument("--cluster", required=True, type=Path, help="cluster dir (holds consolidated_uoc.md + delivery/)")
    ap.add_argument("--at-map", required=True, help="topic->AT ranges, e.g. 1-5:AT1,6-9:AT2")
    args = ap.parse_args()

    deliv = args.cluster / "delivery"
    at_of = parse_at_map(args.at_map)
    desc = descriptors(args.cluster / "consolidated_uoc.md")
    total = len(at_of)
    missing_any = False

    for n in sorted(at_of):
        topic = deliv / f"topic_{n:02d}"
        title, depth, comps = parse_plan(topic / "slide_plan.md")
        at = at_of[n]
        out = [f"# Topic {n:02d} — {title} · Coverage", ""]
        out.append(f"**Topic {n:02d} of {total}** · **{at} content Topic** — the slides and the {at} "
                   "workbook advance together: each component ends in the workbook task it prepares.")
        out.append("")
        out.append("The coverage spec — what this Topic must cover, in UoC and AT terms. "
                   "`slide_plan.md` and the deck are built to satisfy it.")
        out.append("")
        out.append("## Depth ceiling")
        out.append(depth)
        out.append("")
        out.append("## What this Topic must cover")
        out.append("")
        for c in comps:
            culm = f" Culminates in the workbook: **{c['culm']}**." if c["culm"] else ""
            out.append(f"- **{c['id']} — {c['title']}.**{culm}")
        out.append("")
        out.append("## 1. UoC mapping")
        out.append("")
        out.append("UoC **taught / developed** in this Topic:")
        out.append("")
        out.append("| UoC item | Descriptor | Component |")
        out.append("|---|---|---|")
        missing = []
        for c in comps:
            for t in c["tags"]:
                d = desc.get(t)
                if d is None:
                    missing.append(t)
                    d = "??"
                out.append(f"| [{t}] | {d} | {c['id']} |")
        out.append("")
        out.append("## Changelog")
        out.append("- regenerated from the slide plan by scripts/generate_topic_coverage.py; "
                   "components re-cut so each one ends in a workbook task.")
        out.append("")
        (topic / "coverage.md").write_text("\n".join(out), encoding="utf-8")
        tagn = sum(len(c["tags"]) for c in comps)
        note = f"  MISSING DESCRIPTOR: {missing}" if missing else ""
        missing_any = missing_any or bool(missing)
        print(f"topic_{n:02d}: {len(comps)} components, {tagn} tag rows{note}")

    return 1 if missing_any else 0


if __name__ == "__main__":
    sys.exit(main())
