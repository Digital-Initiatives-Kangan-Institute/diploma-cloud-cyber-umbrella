#!/usr/bin/env python3
"""build_topic_deck — generate a Kangan teaching deck FROM a Topic's slide_plan.md.

The factory step 4 builder: one generic, deterministic script that reads the kept+validated
`slide_plan.md` (slide-plan-format.md) and produces `Topic_NN_Slides.pptx` — replacing the
hand-written per-topic build scripts. It maps each slide's [TYPE] tag to a kangan_deck layout and
resolves each slide's `image:` directive in-pipeline (draw-diagram for diagrams; image-gen, gated, for
generated art; placeholder for AWS-reuse).

Slide-plan content the builder reads (an extension of the format's skeleton — full content, not briefs):

  ## Slides
  ### Opener
  - [BESPOKE] Continuing the build
    - a top-level bullet
      - a sub-bullet
    image: none
  ### C1 — Virtual network & subnets
  - Teaches: [ICTCLD401 PC 2.2]          (coverage mapping — not a slide)
  - Kicker: the fabric the workload lives in   (optional divider kicker)
  - [PRIMER] Networking, the essentials
    - what a network/subnet/IP/CIDR is
    image: diagram net-basics
  - [EX] Build the design's VPC
    - stand up the VPC + subnets in the lab
    timer: ~25 min
    image: none
  ### Close
  - [BESPOKE] Next: Topic 8
    - the workload tier moves in
    image: none

Per-slide fields: `image:` (required by the format), and optional `kicker:` / `timer:` (EX) /
`source:` (DEMO recorded-demo ref) / `note:` (TABLE). A TABLE slide carries markdown `| a | b |` rows.

Usage:  python scripts/build_topic_deck.py <slide_plan.md> [out.pptx] [--allow-gen]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "helpers"))   # engine helpers (co-located)


def _brand_dir(argv):
    """The course brand pack (brand.py) lives in the CONTENT repo; the engine is course-agnostic.
    Resolve it via --brand <dir|file>, else walk up from the slide-plan path to the content repo's
    scripts/, else fall back to the engine's own dir (works when engine + brand are co-located)."""
    for i, a in enumerate(argv):
        if a == "--brand" and i + 1 < len(argv):
            p = Path(argv[i + 1]).resolve()
            return p.parent if p.is_file() else p
    for a in argv[1:]:
        if not a.startswith("-"):
            for d in Path(a).resolve().parents:
                if (d / "scripts" / "brand.py").exists():
                    return d / "scripts"
            break
    return Path(__file__).resolve().parent


sys.path.insert(0, str(_brand_dir(sys.argv)))   # content-repo scripts/ — the course brand pack
import kangan_deck as k          # noqa: E402
from deck_images import resolve_image   # noqa: E402

# per-component divider accents (cycled), matching the CL1 look (section colours)
ACCENTS = [k.MAGENTA, k.SKY, k.GREEN, k.NAVY]

SLIDE_RE = re.compile(r"^-\s+((?:\[[^\]]+\]\s*)+)(.*)$")   # "- [TYPE] [TYPE2] Title"
TYPE_RE = re.compile(r"\[([^\]]+)\]")
FIELD_RE = re.compile(r"^\s*(image|kicker|timer|source|note):\s*(.*)$", re.IGNORECASE)
BULLET_RE = re.compile(r"^(\s*)-\s+(.*)$")
COMP_RE = re.compile(r"^###\s+(.*)$")


# ---------- parse ----------
def parse_slide_plan(text: str) -> dict:
    lines = text.splitlines()
    m = re.match(r"#\s+Topic\s+(\S+)\s+(.*?)\s+[—-]\s+Slide plan", lines[0]) if lines else None
    topic_no = m.group(1) if m else "?"
    title = m.group(2).strip() if m else "Topic"
    sub = next((re.sub(r"^>.*?:\**\s*", "", l).strip()
                for l in lines if re.match(r">\s*\*\*Subtitle", l, re.IGNORECASE)), "")

    # isolate the ## Slides section
    start = next((i for i, l in enumerate(lines) if l.strip() == "## Slides"), None)
    if start is None:
        raise ValueError("slide_plan.md has no '## Slides' section")
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"^##\s", lines[i])), len(lines))
    body = lines[start + 1:end]

    components, comp, slide = [], None, None

    def close_slide():
        nonlocal slide
        if slide is not None:
            comp["slides"].append(slide)
            slide = None

    for raw in body:
        cm = COMP_RE.match(raw)
        if cm:
            close_slide()
            head = cm.group(1).strip()
            if head.lower().startswith("opener"):
                kind, num, ctitle = "opener", None, "Opener"
            elif head.lower().startswith("close"):
                kind, num, ctitle = "close", None, "Close"
            else:
                cmn = re.match(r"C(\d+)\s*[—-]?\s*(.*)$", head)
                kind, num, ctitle = "component", (cmn.group(1) if cmn else None), \
                    (cmn.group(2).strip() if cmn and cmn.group(2) else head)
            comp = {"kind": kind, "num": num, "title": ctitle, "kicker": "", "slides": []}
            components.append(comp)
            continue
        if comp is None:
            continue
        sm = SLIDE_RE.match(raw)
        if sm:
            types = TYPE_RE.findall(sm.group(1))
            rest = sm.group(2).strip()
            # component metadata lines (Teaches:/Kicker:) are "- Word:" not "- [TYPE]"
            if not types and ":" in rest:
                continue
            if types and types[0].lower() == "teaches":
                continue
            close_slide()
            slide = {"types": types, "title": rest, "bullets": [], "image": "none",
                     "kicker": "", "timer": "", "source": "", "note": "", "table": []}
            continue
        # a "- Teaches:" / "- Kicker:" component line (no [TYPE])
        meta = re.match(r"^-\s+(Teaches|Kicker):\s*(.*)$", raw, re.IGNORECASE)
        if meta and slide is None:
            if meta.group(1).lower() == "kicker":
                comp["kicker"] = meta.group(2).strip()
            continue
        if slide is None:
            continue
        # within a slide: fields, table rows, or bullets
        fm = FIELD_RE.match(raw)
        if fm:
            slide[fm.group(1).lower()] = fm.group(2).strip()
            continue
        if raw.strip().startswith("|"):
            cells = [c.strip() for c in raw.strip().strip("|").split("|")]
            if not all(set(c) <= set("-: ") for c in cells):   # skip the |---| separator row
                slide["table"].append(cells)
            continue
        bm = BULLET_RE.match(raw)
        if bm:
            indent = len(bm.group(1))
            level = min(2, max(0, (indent - 2) // 2)) if indent >= 2 else 0
            slide["bullets"].append((level, bm.group(2).strip()))
            continue
        if raw.strip():   # tolerate a plain brief line as a level-0 bullet
            slide["bullets"].append((0, raw.strip()))
    close_slide()
    return {"topic_no": topic_no, "title": title, "subtitle": sub, "components": components}


# ---------- build ----------
def _primary(types):
    return (types[0].split()[0].upper() if types else "BESPOKE")


def build(plan: dict, topic_dir: Path, out: Path, allow_gen: bool = False):
    prs = k.new_deck()
    page = [0]

    def pg():
        page[0] += 1
        return page[0]

    k.title_slide(prs, plan["topic_no"], plan["title"], plan["subtitle"])
    ai = 0
    for comp in plan["components"]:
        accent = k.GOLD
        if comp["kind"] == "component":
            accent = ACCENTS[ai % len(ACCENTS)]
            ai += 1
            num = (comp["num"] or str(ai)).zfill(2)
            k.divider_slide(prs, num, comp["title"], comp["kicker"], accent)
        for sl in comp["slides"]:
            kind = _primary(sl["types"])
            bullets = [(lvl, txt) for lvl, txt in sl["bullets"]]
            if comp["kind"] == "close" or kind == "CLOSE":
                k.close_slide(prs, sl["title"], [t for _, t in sl["bullets"]], accent=k.GOLD)
                continue
            if kind == "EX":
                k.activity_slide(prs, pg(), sl["title"], bullets, sl["timer"] or "~15 min", accent=accent)
            elif kind == "DEMO":
                k.demo_slide(prs, pg(), sl["title"], bullets, accent=accent, source=sl["source"] or None)
            elif kind == "TAKEAWAYS":
                k.takeaways_slide(prs, pg(), sl["title"], [t for _, t in sl["bullets"]], accent=accent)
            elif kind == "TABLE":
                headers = sl["table"][0] if sl["table"] else []
                rows = sl["table"][1:] if len(sl["table"]) > 1 else []
                k.table_slide(prs, pg(), sl["title"], sl["kicker"], headers, rows,
                              accent=accent, note=sl["note"] or None)
            else:   # PRIMER / BESPOKE / AWS / other -> content or visual
                img = resolve_image(sl["image"], topic_dir, allow_gen=allow_gen)
                if img is None:
                    k.content_slide(prs, pg(), sl["title"], sl["kicker"], bullets, accent=accent)
                else:
                    k.visual_slide(prs, pg(), sl["title"], sl["kicker"], bullets, [img], accent=accent)
    k.save(prs, out)


def main(argv=None) -> int:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Build a Kangan deck from a Topic's slide_plan.md.")
    ap.add_argument("slide_plan", help="path to delivery/topic_NN/slide_plan.md")
    ap.add_argument("out", nargs="?", help="output .pptx (default: Topic_NN_Slides.pptx beside the plan)")
    ap.add_argument("--allow-gen", action="store_true", help="enable image-gen (paid) for image: gen slides")
    ap.add_argument("--brand", metavar="PATH", help="course brand pack (brand.py); default: found from the slide-plan path")
    args = ap.parse_args(argv)

    plan_path = Path(args.slide_plan).resolve()
    topic_dir = plan_path.parent
    plan = parse_slide_plan(plan_path.read_text(encoding="utf-8"))
    out = Path(args.out) if args.out else topic_dir / f"Topic_{str(plan['topic_no']).zfill(2)}_Slides.pptx"
    build(plan, topic_dir, out, allow_gen=args.allow_gen)
    return 0


if __name__ == "__main__":
    sys.exit(main())
