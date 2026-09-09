#!/usr/bin/env python3
"""Generate a cluster's institutional Delivery Plan .docx from its validated outline.

Step 6, execution item 13. Everything written here is DERIVED -- from the outline's session grid, the
cluster's frame, and each placed Topic's coverage.md. Nothing is invented and nothing is asked for a
second time; if a value is missing, that is a gap in the outline and the gate should have caught it.

REFUSES TO RUN on an outline that does not pass the step-6 gate. A PASS is precisely what "ready to
generate" means, so generating from a FAIL would fabricate content for undecided cells.

The template ships with three example session blocks; an intake needs one per session, so blocks are
cloned via docx_template. The template's own formatting is preserved throughout -- a filled
institutional document must still look like the institution's document.

Behaviour is specified by cases CDG-01 .. CDG-14 in factory/docs/test-plan.md.

Usage:
  python build_cluster_delivery_plan.py --plan <cluster>/delivery/delivery-plan.md \\
      --template <Delivery_Plan_Template_v0.1.docx> --out <S1_CLn_Delivery_Plan.docx>

Exit 0 on success, 1 if the outline does not validate.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common" / "helpers"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from docx_template import (clone_block_after, ensure_row_cells, set_cell_block,  # noqa: E402
                           set_cell_text, unwrap_content_controls)
from format_contract import parse_labelled_fields  # noqa: E402
from lln_requirements import collect as collect_lln  # noqa: E402
from md_table import rows_under_heading  # noqa: E402
from uoc_sections import sections_taught, to_delivery_mapping  # noqa: E402
import validate_cluster_delivery_plan as gate  # noqa: E402

# The outline's Mode vocabulary as the template's Delivery dropdown.
MODE_TO_DELIVERY = {"online": "O", "classroom": "FTF", "workplace": "WP"}

# Where a value goes inside one 6-column session block.
R_DATE, C_DATE = 1, 1        # the "Session date" row
R_DATA = 3                   # the first data row under the column headers
C_TIME, C_DELIVERY, C_ASSESSMENT, C_TOPIC, C_RESOURCES, C_MAPPING = 0, 1, 2, 3, 4, 5


# The outline's Document details fields, and the template row each one fills:
#   (outline field label, table title prefix, row index in that table)
HEADER_FIELDS = [
    ("Qualification code and title", "Details", 1),
    ("Unit code and title", "Details", 2),
    ("Cohort description", "Details", 3),
]

# Fields whose template cell holds a STYLED PLACEHOLDER rather than real content. Writing these with
# set_cell_text would inherit the prompt's colour and the filled cell would still read as unfilled.
PLACEHOLDER_FIELDS = [
    ("Materials and resources", "General Learning Materials", 1),
]


LLN_INTRO = ("This cluster places the following language, literacy and numeracy demands on learners. "
             "Trainers should identify and support any learner who may need assistance to meet them.")


def _derive_lln(cluster: Path) -> list[tuple[str, bool]]:
    """The LLN section as (text, is_heading) blocks, read from the cluster's own units.

    Derived rather than carried in the outline: it has no per-instance variation, so a copy in the
    outline could only go stale when the units change. Contrast Date and Time, which are derived with
    an override and therefore do live in the grid.
    """
    consolidated = cluster / "consolidated_uoc.md"
    if not consolidated.is_file():
        return []
    sections = collect_lln(consolidated.read_text(encoding="utf-8", errors="ignore"))
    if not sections:
        return []
    blocks = [(LLN_INTRO, False)]
    for heading, items in sections.items():
        blocks.append((heading, True))
        blocks += [(f"- {i}", False) for i in items]
    return blocks


def _fill_header(doc, header: dict, cluster: Path) -> None:
    """Fill the Details / Materials / LLN tables above the session blocks.

    Copied straight across from the outline -- these are composed once, in the plan, so the docx step
    has nothing left to decide. The gate has already refused a plan with any of them empty.
    """
    by_title = {t.rows[0].cells[0].text.strip(): t for t in doc.tables if len(t.columns) == 2}
    for label, title_prefix, row in HEADER_FIELDS:
        table = next((t for k, t in by_title.items() if k.startswith(title_prefix)), None)
        if table is not None and row < len(table.rows):
            set_cell_text(table.rows[row].cells[1], header.get(label, ""))

    for label, title_prefix, row in PLACEHOLDER_FIELDS:
        table = next((t for k, t in by_title.items() if k.startswith(title_prefix)), None)
        if table is not None and row < len(table.rows):
            set_cell_block(table.rows[row].cells[1], [(header.get(label, ""), False)])

    lln = next((t for k, t in by_title.items() if k.startswith("LLN")), None)
    if lln is not None:
        set_cell_block(lln.rows[1].cells[1], _derive_lln(cluster))


def _session_blocks(doc):
    """The per-session tables -- the 6-column blocks, not the summary tables above them."""
    return [t for t in doc.tables if len(t.columns) == 6]


def _block_paragraph(doc, table):
    """The 'Session N' paragraph immediately preceding ``table`` in document order."""
    from docx.text.paragraph import Paragraph
    prev = table._tbl.getprevious()
    while prev is not None and not prev.tag.endswith("}p"):
        prev = prev.getprevious()
    return Paragraph(prev, doc) if prev is not None else None


def _assessment_types(header_fields: dict) -> dict:
    """``{'AT1': 'Project', 'AT2': 'Project'}`` from the outline's 'Assessment types:' field."""
    raw = header_fields.get("Assessment types", "")
    return {m.group(1).upper(): m.group(2).strip()
            for m in re.finditer(r"(AT\d+)\s*:\s*([A-Za-z0-9]+)", raw)}


def _topics_in(placed: str) -> list[int]:
    return [int(n) for n in re.findall(r"\bT0*(\d+)\b", placed)]


def _topic_title(n: int, cluster: Path) -> str:
    """``Topic 01 — Web-scale architecture design``, read from the Topic's own coverage.md.

    A bare ``T1`` in a delivery plan tells a reader nothing about what the session covers. The title
    is already written, once, in the Topic's coverage heading -- so it is read rather than restated,
    and cannot drift from the Topic it names. Falls back to the plain reference when there is no
    readable heading: an unreadable title is not a reason to write nothing.
    """
    cov = cluster / "delivery" / f"topic_{n:02d}" / "coverage.md"
    if cov.is_file():
        m = re.search(r"^#\s+(Topic\s+\d+\s+[—-]\s+.+?)\s*(?:·.*)?$",
                      cov.read_text(encoding="utf-8", errors="ignore"), re.MULTILINE)
        if m:
            return m.group(1).strip()
    return f"T{n}"


def _assessment_title(n: int, cluster: Path) -> str:
    """``AT1 — Cloud Expansion: Design & DR Plan``, read from the cluster's assessment plan.

    An assessment has no coverage.md, so its title comes from the plan that named it -- authored once
    there, rather than inferred from an instrument's filename. Falls back to the plain reference when
    the plan has no heading for it.
    """
    plan = cluster / "assessments" / "assessment_plan.md"
    if plan.is_file():
        m = re.search(rf"^#{{1,4}}\s+(AT{n}\s+[—-]\s+.+?)\s*$",
                      plan.read_text(encoding="utf-8", errors="ignore"), re.MULTILINE)
        if m:
            return m.group(1).strip()
    return f"AT{n}"


# What a session reads as when it places nothing. A reserved session is a decision, and a blank row
# reads as an oversight rather than as a reservation.
ACTIVITY_LABELS = {
    "spare": "Spare / contingency — catch-up, or assessment overflow",
    "onboarding": "Onboarding",
    "practice": "Practice",
}


def _placed_label(placed: str, activity: str, cluster: Path) -> str:
    """The Placed value as it should read in the document -- Topics and assessments by title.

    A bare ``T1`` or ``AT1`` tells a reader nothing about what the session covers, and this document
    is read by people who were not in the planning conversation.

    When nothing is placed, the session is labelled from its Activity instead. The plan already
    decided the session is spare; leaving the cell blank throws that decision away and the row reads
    as an oversight. The label never displaces real content -- it applies only to an empty cell.
    """
    if placed in ("", "—"):
        return ACTIVITY_LABELS.get(activity.strip().lower(), "")
    out = re.sub(r"\bAT0*(\d+)\b", lambda m: _assessment_title(int(m.group(1)), cluster), placed)
    return re.sub(r"\bT0*(\d+)\b(?![^—]*—)", lambda m: _topic_title(int(m.group(1)), cluster), out)


def _mapping_for(placed: str, cluster: Path) -> str:
    """The Delivery Mapping value for a session -- the sections its placed Topics teach."""
    sections = set()
    for n in _topics_in(placed):
        cov = cluster / "delivery" / f"topic_{n:02d}" / "coverage.md"
        if cov.is_file():
            sections |= sections_taught(cov.read_text(encoding="utf-8"))
    return ", ".join(to_delivery_mapping(sections))


def build(plan: Path, template: Path, out: Path, fmt_doc: Path | None = None) -> int:
    """Fill ``template`` from ``plan`` and write ``out``. Returns 0 on success, 1 if the gate fails."""
    from docx import Document

    argv = ["--plan", str(plan)]
    if fmt_doc:
        argv += ["--format", str(fmt_doc)]
    saved, sys.argv = sys.argv, ["validate_cluster_delivery_plan.py", *argv]
    try:
        if gate.main() != 0:
            print("REFUSED: the outline does not pass the step-6 gate - fix it and re-run.")
            return 1
    finally:
        sys.argv = saved

    text = plan.read_text(encoding="utf-8")
    header = parse_labelled_fields(text)
    at_types = _assessment_types(header)
    cluster = plan.parent.parent

    rows = rows_under_heading(text, "Session grid")
    cols = {name.strip().lower(): i for i, name in enumerate(rows[0][0])}
    data = [cells for cells, _ in rows[1:]]

    doc = Document(str(template))
    _fill_header(doc, header, cluster)
    blocks = _session_blocks(doc)

    # The template ships with a few example blocks; make the count match the intake.
    while len(blocks) < len(data):
        last = blocks[-1]
        para = _block_paragraph(doc, last)
        _new_p, new_t = clone_block_after(para, last)
        blocks.append(new_t)
    for extra in blocks[len(data):]:
        extra._tbl.getparent().remove(extra._tbl)
    blocks = blocks[:len(data)]

    for cells, block in zip(data, blocks):
        get = lambda name: cells[cols[name]].strip() if name in cols else ""  # noqa: E731
        placed = get("placed")
        at = re.search(r"\bAT\d+\b", placed, re.IGNORECASE)

        # The template wraps its Delivery and Assessment cells in dropdown content controls, which
        # hides them from python-docx: the row reports four cells where it has six, and writes land
        # one or two columns left of where they belong. Unwrap first, then widen if still short.
        unwrap_content_controls(block.rows[R_DATA])
        ensure_row_cells(block.rows[R_DATA], 6)

        set_cell_text(block.rows[R_DATE].cells[C_DATE], get("date"))
        set_cell_text(block.rows[R_DATA].cells[C_TIME], get("time"))
        set_cell_text(block.rows[R_DATA].cells[C_DELIVERY],
                      MODE_TO_DELIVERY.get(get("mode").lower(), ""))
        set_cell_text(block.rows[R_DATA].cells[C_ASSESSMENT],
                      at_types.get(at.group(0).upper(), "") if at else "")
        set_cell_text(block.rows[R_DATA].cells[C_TOPIC],
                      _placed_label(placed, get("activity"), cluster))
        set_cell_text(block.rows[R_DATA].cells[C_MAPPING], _mapping_for(placed, cluster))

        # The template ships four data rows per block; a session fills one. Leaving the rest would
        # put three blank rows under every session across the whole document.
        for spare in block.rows[R_DATA + 1:]:
            spare._tr.getparent().remove(spare._tr)

    out.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out))
    print(f"WROTE: {out} ({len(data)} sessions)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a cluster's Delivery Plan docx (Step 6, item 13).")
    ap.add_argument("--plan", required=True, type=Path)
    ap.add_argument("--template", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--format", dest="fmt_doc", type=Path)
    a = ap.parse_args()
    return build(a.plan, a.template, a.out, a.fmt_doc)


if __name__ == "__main__":
    sys.exit(main())
