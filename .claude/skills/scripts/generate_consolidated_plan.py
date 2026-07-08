#!/usr/bin/env python3
"""Deterministically generate a scenario's consolidated assessment plan from its per-cluster plans.

The per-cluster `assessment_plan.md` files are the authored source of truth; this DERIVES the
single cross-cluster view a scenario plan is validated against (see docs/assessment-plan-format.md):

  - AT roster — every AT across all the scenario's clusters.
  - Whole-of-scenario UoC coverage rollup — every consolidated item → the cluster+AT(s) that cover it.
  - Aggregated scenario-requirements register — the union of every cluster's SR-* rows (cluster-scoped
    ids, so no collisions). This is the contract the scenario plan satisfies.

It is deterministic (sorted throughout): same inputs → same output. The output carries a "DO NOT
hand-edit" banner; faithfulness is confirmed separately by validate_consolidated_plan.py.

Usage:
  generate_consolidated_plan.py --semester S1 [--repo <content repo root>] [--out <path>]
  generate_consolidated_plan.py --plan <assessment_plan.md> --plan ... --out <path>

Default output: <repo>/assessment-plans/<SEMESTER>.md
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_at_traceability import resolve_tags

REPO = Path(__file__).resolve().parents[3]  # .claude/skills/scripts/ -> content repo root
SEC_ORDER = {"PC": 0, "PE": 1, "KE": 2, "FS": 3, "AC": 4}


def cluster_token(path: Path) -> str:
    m = re.search(r"(CL\d+)", str(path))
    return m.group(1) if m else path.parent.parent.name


def _strip(cell: str) -> str:
    return cell.replace("**", "").replace("`", "").strip()


def _section(text, num):
    """Text of '## <num>. …' up to the next '## '."""
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines) if re.match(rf"^##\s+{num}\.", ln)), None)
    if start is None:
        return ""
    end = next((j for j in range(start + 1, len(lines)) if re.match(r"^##\s", lines[j])), len(lines))
    return "\n".join(lines[start:end])


def parse_plan(path: Path):
    """{cluster, ats:[(id,title,mode,unit)], coverage:{item_tag:set(cluster·AT)}, srs:[(id,desc,ats,ac)]}."""
    text = path.read_text(encoding="utf-8")
    cl = cluster_token(path)
    sec3 = _section(text, 3)

    # AT roster — the table rows before the first '### ' detail block
    ats = []
    table_part = re.split(r"^###\s", sec3, maxsplit=1, flags=re.MULTILINE)[0]
    for ln in table_part.splitlines():
        if not ln.strip().startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) >= 5 and re.match(r"\**AT\d+\**$", cells[0].strip()):
            at = _strip(cells[0])
            ats.append((at, _strip(cells[1]), _strip(cells[2]), _strip(cells[4])))

    # per-AT UoC coverage — from each '### ATn' block's 'UoC coverage:' line
    coverage = {}
    blocks = re.split(r"^###\s+(AT\d+)\b", sec3, flags=re.MULTILINE)
    for i in range(1, len(blocks), 2):
        at, body = blocks[i], blocks[i + 1]
        for line in body.splitlines():
            if "UoC coverage:" in line:
                for tag, form in resolve_tags(line):
                    if form != "unresolved" and not tag.startswith("?? "):
                        coverage.setdefault(tag, set()).add(f"{cl}·{at}")

    # SR register — §6 table rows
    srs = []
    for ln in _section(text, 6).splitlines():
        if not ln.strip().startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) >= 4 and re.match(r"\**SR-[A-Z]+\d+-\d+\**", cells[0]):
            srs.append((_strip(cells[0]), cells[1].strip(), cells[2].strip(), cells[3].strip()))

    return {"cluster": cl, "ats": ats, "coverage": coverage, "srs": srs}


def _item_key(tag):
    parts = tag.split()
    unit, sec, num = parts[0], parts[1], " ".join(parts[2:])
    nk = tuple(int(x) for x in num.split(".")) if re.match(r"^\d+(\.\d+)?$", num) else (999, num)
    return (unit, SEC_ORDER.get(sec, 9), nk)


def _sr_key(sr):
    m = re.match(r"SR-([A-Z]+)(\d+)-(\d+)", sr[0])
    return (m.group(1), int(m.group(2)), int(m.group(3))) if m else (sr[0],)


def build_consolidated(plans, semester):
    plans = sorted(plans, key=lambda p: p["cluster"])
    lines = [f"# {semester} — Consolidated Assessment Plan",
             "",
             "> **DERIVED — do not hand-edit.** Generated from the per-cluster assessment plans by",
             "> `generate_consolidated_plan.py`; faithfulness is checked by `validate_consolidated_plan.py`.",
             "> The per-cluster `assessment_plan.md` files are the authored source of truth.",
             ">",
             "> **Scenario binding:** the single cross-cluster contract the scenario plan is validated",
             "> against — every `SR-*` below must be satisfied by the scenario plan.",
             ">",
             "> **Source plans:** " + ", ".join(f"`{p['cluster']}`" for p in plans) + ".",
             "",
             "## AT roster", "",
             "| Cluster | AT | Mode | Unit focus |", "|---|---|---|---|"]
    for p in plans:
        for at, title, mode, unit in p["ats"]:
            lines.append(f"| {p['cluster']} | {at} — {title} | {mode} | {unit} |")

    # coverage rollup (merge across plans)
    coverage = {}
    for p in plans:
        for tag, where in p["coverage"].items():
            coverage.setdefault(tag, set()).update(where)
    lines += ["", "## UoC coverage (whole-of-scenario)", "",
              "| UoC item | Covered by |", "|---|---|"]
    for tag in sorted(coverage, key=_item_key):
        lines.append(f"| [{tag}] | {', '.join(sorted(coverage[tag]))} |")

    # aggregated SR register (union; ids are cluster-scoped so unique)
    srs = sorted({sr for p in plans for sr in p["srs"]}, key=_sr_key)
    lines += ["", "## Scenario requirements register (aggregated)", "",
              "| SR | Condition the scenario must enable | AT(s) | AC link |", "|---|---|---|---|"]
    for sr_id, desc, ats, ac in srs:
        lines.append(f"| {sr_id} | {desc} | {ats} | {ac} |")
    lines.append("")
    return "\n".join(lines)


def discover_plans(repo: Path, semester: str):
    return sorted(repo.glob(f"{semester}-CL*/assessments/assessment_plan.md"))


def main():
    ap = argparse.ArgumentParser(description="Generate a scenario's consolidated assessment plan.")
    ap.add_argument("--semester", help="e.g. S1 (auto-discovers <SEMESTER>-CL*/assessments/…)")
    ap.add_argument("--repo", type=Path, default=REPO)
    ap.add_argument("--plan", action="append", type=Path, default=[], help="explicit per-cluster plan(s)")
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()

    paths = args.plan or (discover_plans(args.repo, args.semester) if args.semester else [])
    if not paths:
        print("No per-cluster plans found (give --semester or --plan)."); sys.exit(2)
    plans = [parse_plan(p) for p in paths]
    out = args.out or (args.repo / "assessment-plans" / f"{args.semester}.md")
    md = build_consolidated(plans, args.semester or "Consolidated")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    n_ats = sum(len(p["ats"]) for p in plans)
    n_cov = len({t for p in plans for t in p["coverage"]})
    n_sr = len({sr for p in plans for sr in p["srs"]})
    print(f"Wrote {out} — {len(plans)} clusters, {n_ats} ATs, {n_cov} UoC items, {n_sr} SR.")


if __name__ == "__main__":
    main()
