"""Filling an **institutional** .docx template without disturbing its formatting.

USE THIS WHEN you are populating a document somebody else designed -- a Kangan delivery plan, an
assessment mapping tool, any supplied .docx whose fonts, shading and column widths must survive
untouched, and whose repeating section has to be repeated more times than the template ships with.

DO NOT USE THIS to build a table from nothing. ``scripts/helpers/docx_tables.py`` does that, and the
distinction is the whole point: there the styling is ours to set, so a fresh run per cell is correct;
here the styling is the institution's, so the existing run must be *reused* or its font, size and
colour are silently lost. Both behaviours are right for their own job -- neither is a duplicate of
the other, and they are deliberately kept apart.

Requires python-docx (see factory/requirements.txt). The rest of the factory's helpers are
stdlib-only; this one cannot be.

Cases: HDT-01 .. HDT-10 in factory/docs/test-plan.md.
"""
from __future__ import annotations

import copy


def clone_block_after(paragraph, table):
    """Duplicate a heading-plus-table block, inserting the copy directly after ``table``.

    An institutional template ships with a few example blocks -- the delivery plan has three
    "Session N" headings each followed by its own table -- and a real document needs as many as the
    plan has sessions. Cloning is a **deep** copy: a shallow one would leave every block sharing the
    same underlying XML, so filling the last would overwrite all of them.

    Insertion is positional rather than appended, because a block added at the end of the document
    would read out of sequence.

    Returns ``(new_paragraph, new_table)`` as python-docx objects, ready to fill.
    """
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    new_p_el = copy.deepcopy(paragraph._p)
    new_t_el = copy.deepcopy(table._tbl)

    table._tbl.addnext(new_t_el)
    table._tbl.addnext(new_p_el)

    return Paragraph(new_p_el, paragraph._parent), Table(new_t_el, table._parent)


def _drop_content_controls(cell) -> None:
    """Remove any content control (``w:sdt``) the cell holds.

    An institutional template uses these for its dropdown prompts -- the delivery plan's Delivery and
    Assessment cells each hold one showing "Select". They are invisible to ``cell.paragraphs``, so
    writing a value would leave the prompt in place and the cell would render both. A filled cell must
    not still offer its dropdown.
    """
    from docx.oxml.ns import qn
    for sdt in cell._tc.findall(qn("w:sdt")) + cell._tc.findall(".//" + qn("w:sdt")):
        parent = sdt.getparent()
        if parent is not None:
            parent.remove(sdt)


def set_cell_text(cell, text: str) -> None:
    """Write ``text`` into ``cell``, keeping the formatting the template already had.

    The first existing run is **reused** rather than replaced, so its font, size, weight and colour
    carry over to the new value -- that is what keeps a filled template looking like the template.
    A cell with no runs yet gets one.

    Newlines become one paragraph per line, matching how these templates express multi-line cell
    content. Any previous content is replaced, so writing twice leaves only the second value, and any
    content control the cell held is removed.
    """
    _drop_content_controls(cell)
    for p in cell.paragraphs[1:]:
        p._element.getparent().remove(p._element)

    first = cell.paragraphs[0]
    lines = (text or "").split("\n")

    keep = first.runs[0] if first.runs else first.add_run("")
    for extra in list(first.runs[1:]):
        extra._element.getparent().remove(extra._element)
    keep.text = lines[0]

    for line in lines[1:]:
        para = cell.add_paragraph()
        para.style = first.style
        run = copy.deepcopy(keep._element)
        para._p.append(run)
        para.runs[0].text = line


# python-docx exposes no public constant for a table-cell element name.
QN_TC = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tc"


def ensure_row_cells(row, n: int) -> None:
    """Widen ``row`` to ``n`` cells, copying the last cell so additions match the row's styling.

    A supplied template can ship rows narrower than its own header -- the Kangan delivery plan's
    session blocks declare six columns but their data rows carry only four, so the last two columns
    have no cell to write into at all. Widening is the honest fix: the header says those columns
    exist, so the document should be able to hold their values.

    Does nothing when the row is already wide enough. A row with no cells is left alone -- there is
    nothing to copy formatting from, and inventing one would guess at the template's intent.
    """
    tr = row._tr
    cells = tr.findall(QN_TC)
    if not cells or len(cells) >= n:
        return
    for _ in range(n - len(cells)):
        clone = copy.deepcopy(cells[-1])
        for p in clone.findall(
            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"
        )[1:]:
            clone.remove(p)
        tr.append(clone)


def set_cell_block(cell, blocks) -> None:
    """Write ``blocks`` -- ``(text, is_heading)`` pairs -- one paragraph each, as real content.

    The sibling of :func:`set_cell_text`, and deliberately different. ``set_cell_text`` PRESERVES the
    template's formatting, which is right when the cell already holds real content. This one is for a
    cell holding a styled **placeholder** -- "Enter the LLN requirements of the unit." -- where the
    styling is the prompt's, not the document's. Inheriting it makes filled content read as an
    unfilled prompt, so the text colour is set to black explicitly -- the colour sits on the
    paragraph style, so clearing a run-level override would leave it in place.

    Headings are bolded so a long structured value stays scannable rather than becoming a wall.
    """
    from docx.shared import RGBColor

    _drop_content_controls(cell)
    for p in cell.paragraphs[1:]:
        p._element.getparent().remove(p._element)
    first = cell.paragraphs[0]
    for r in list(first.runs):
        r._element.getparent().remove(r._element)

    for i, (text, is_heading) in enumerate(blocks):
        para = first if i == 0 else cell.add_paragraph()
        para.style = first.style
        run = para.add_run(text)
        run.bold = bool(is_heading)
        # Set black EXPLICITLY. Merely clearing a run-level override is not enough: the colour lives
        # on the paragraph style, so the placeholder's colour would still apply and the filled cell
        # would still read as an unfilled prompt.
        run.font.color.rgb = RGBColor(0, 0, 0)


def unwrap_content_controls(row) -> None:
    """Promote any cell wrapped in a content control to a real cell on ``row``.

    An institutional template may wrap a cell in a ``w:sdt`` to attach a dropdown -- the delivery
    plan's Delivery and Assessment cells are wrapped this way, giving a row whose children are
    ``tc, sdt, sdt, tc, tc, tc``. python-docx only sees the direct ``w:tc`` children, so the row
    reports four cells where it has six, and every write lands in the wrong column.

    Unwrapping restores the row to plain cells **in their original order**, which is what makes the
    columns line up again. Call it before reading or writing a row that a template supplied.
    """
    from docx.oxml.ns import qn

    tr = row._tr
    for child in list(tr):
        if child.tag != qn("w:sdt"):
            continue
        content = child.find(qn("w:sdtContent"))
        cells = content.findall(qn("w:tc")) if content is not None else []
        if not cells:
            continue
        index = list(tr).index(child)
        for offset, tc in enumerate(cells):
            tr.insert(index + offset, tc)
        tr.remove(child)
