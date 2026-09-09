"""Cases HDT-01 .. HDT-10 — factory/docs/test-plan.md.

Covers common/helpers/docx_template.py: repeating a heading-plus-table block in an institutional
template, and writing cell values without flattening the template's own formatting.
"""
from docx import Document

import docx_template as DT


def build_doc():
    """A two-block document shaped like the delivery-plan template: heading, table, heading, table."""
    doc = Document()
    p1 = doc.add_paragraph("Session 1")
    t1 = doc.add_table(rows=3, cols=4)
    p2 = doc.add_paragraph("Session 2")
    t2 = doc.add_table(rows=3, cols=4)
    return doc, p1, t1, p2, t2


def body_order(doc):
    """The document body's child element tags, in order — 'p' and 'tbl'."""
    return [el.tag.rsplit("}", 1)[-1] for el in doc.element.body]


# --- clone_block_after (HDT-01 .. HDT-05) ---------------------------------

def test_document_gains_one_paragraph_and_one_table():
    """HDT-01"""
    doc, p1, t1, _p2, _t2 = build_doc()
    before_p, before_t = len(doc.paragraphs), len(doc.tables)
    DT.clone_block_after(p1, t1)
    assert len(doc.paragraphs) == before_p + 1
    assert len(doc.tables) == before_t + 1


def test_clone_sits_immediately_after_the_source_table():
    """HDT-02 — order matters: a session block appended at the end would read out of sequence."""
    doc, p1, t1, _p2, _t2 = build_doc()
    DT.clone_block_after(p1, t1)
    order = body_order(doc)
    assert order[:4] == ["p", "tbl", "p", "tbl"]


def test_clone_paragraph_carries_the_same_text():
    """HDT-03"""
    _doc, p1, t1, _p2, _t2 = build_doc()
    new_p, _new_t = DT.clone_block_after(p1, t1)
    assert new_p.text == "Session 1"


def test_clone_table_has_the_same_shape():
    """HDT-04"""
    _doc, p1, t1, _p2, _t2 = build_doc()
    _new_p, new_t = DT.clone_block_after(p1, t1)
    assert (len(new_t.rows), len(new_t.columns)) == (len(t1.rows), len(t1.columns))


def test_editing_the_clone_leaves_the_source_untouched():
    """HDT-05 — a shallow copy would make every session show the last one's values."""
    _doc, p1, t1, _p2, _t2 = build_doc()
    new_p, new_t = DT.clone_block_after(p1, t1)
    DT.set_cell_text(new_t.rows[0].cells[0], "clone value")
    assert t1.rows[0].cells[0].text == ""
    assert new_p.text == "Session 1"


# --- set_cell_text (HDT-06 .. HDT-10) -------------------------------------

def test_cell_reads_back_the_value_written():
    """HDT-06"""
    _doc, _p1, t1, _p2, _t2 = build_doc()
    cell = t1.rows[0].cells[0]
    DT.set_cell_text(cell, "5 Oct 2026")
    assert cell.text == "5 Oct 2026"


def test_existing_run_formatting_survives_the_write():
    """HDT-07 — the whole point: an institutional template's styling is not ours to discard."""
    _doc, _p1, t1, _p2, _t2 = build_doc()
    cell = t1.rows[0].cells[0]
    run = cell.paragraphs[0].add_run("placeholder")
    run.bold = True
    DT.set_cell_text(cell, "9am - 12pm")
    assert cell.paragraphs[0].runs[0].bold is True
    assert cell.text == "9am - 12pm"


def test_cell_with_no_runs_can_still_be_written():
    """HDT-08"""
    _doc, _p1, t1, _p2, _t2 = build_doc()
    cell = t1.rows[0].cells[1]
    assert cell.paragraphs[0].runs == []
    DT.set_cell_text(cell, "classroom")
    assert cell.text == "classroom"


def test_multiline_value_becomes_one_paragraph_per_line():
    """HDT-09"""
    _doc, _p1, t1, _p2, _t2 = build_doc()
    cell = t1.rows[0].cells[2]
    DT.set_cell_text(cell, "T1 - Web-scale design\n[EX] Record the needs")
    assert len(cell.paragraphs) == 2
    assert cell.paragraphs[1].text == "[EX] Record the needs"


def test_writing_replaces_rather_than_appends():
    """HDT-10"""
    _doc, _p1, t1, _p2, _t2 = build_doc()
    cell = t1.rows[0].cells[3]
    DT.set_cell_text(cell, "first")
    DT.set_cell_text(cell, "second")
    assert cell.text == "second"


# --- ensure_row_cells (HDT-11 .. HDT-13) ----------------------------------

def narrow_row_doc():
    """A table whose header is wider than its data row — the shape a supplied template can ship."""
    doc = Document()
    t = doc.add_table(rows=2, cols=4)
    tr = t.rows[1]._tr
    for tc in list(tr.findall(DT.QN_TC))[2:]:
        tr.remove(tc)
    return t


def test_narrow_row_gains_cells_until_it_matches():
    """HDT-11"""
    t = narrow_row_doc()
    DT.ensure_row_cells(t.rows[1], 4)
    assert len(t.rows[1].cells) == 4


def test_wide_enough_row_is_untouched():
    """HDT-12"""
    t = narrow_row_doc()
    before = len(t.rows[0].cells)
    DT.ensure_row_cells(t.rows[0], 4)
    assert len(t.rows[0].cells) == before


def test_added_cells_copy_the_last_cells_formatting():
    """HDT-13 — a bolted-on cell must not look bolted on."""
    t = narrow_row_doc()
    DT.set_cell_text(t.rows[1].cells[1], "styled")
    t.rows[1].cells[1].paragraphs[0].runs[0].bold = True
    DT.ensure_row_cells(t.rows[1], 4)
    DT.set_cell_text(t.rows[1].cells[3], "new")
    assert t.rows[1].cells[3].paragraphs[0].runs[0].bold is True


# --- set_cell_block (HDT-14 .. HDT-17) ------------------------------------

BLOCKS = [("Intro line", False), ("A Heading", True), ("- an item", False)]


def styled_placeholder_cell():
    """A cell whose paragraph STYLE carries a colour, as an institutional template's prompt does.

    The colour lives on the style, not the run — which is why clearing a run-level override is not
    enough to make filled content black.
    """
    from docx.shared import RGBColor
    doc = Document()
    style = doc.styles.add_style("Prompt text", 1)
    style.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
    t = doc.add_table(rows=1, cols=1)
    cell = t.rows[0].cells[0]
    cell.paragraphs[0].style = style
    cell.paragraphs[0].add_run("Enter the requirements here.")
    return cell


def test_each_block_becomes_its_own_paragraph():
    """HDT-14"""
    cell = styled_placeholder_cell()
    DT.set_cell_block(cell, BLOCKS)
    assert [p.text for p in cell.paragraphs] == ["Intro line", "A Heading", "- an item"]


def test_heading_block_is_bold():
    """HDT-15"""
    cell = styled_placeholder_cell()
    DT.set_cell_block(cell, BLOCKS)
    assert cell.paragraphs[1].runs[0].bold is True


def test_non_heading_block_is_not_bold():
    """HDT-16"""
    cell = styled_placeholder_cell()
    DT.set_cell_block(cell, BLOCKS)
    assert cell.paragraphs[0].runs[0].bold is not True
    assert cell.paragraphs[2].runs[0].bold is not True


def test_placeholder_colour_is_cleared():
    """HDT-17 — inheriting the prompt's colour makes real content read as an unfilled prompt."""
    cell = styled_placeholder_cell()
    DT.set_cell_block(cell, BLOCKS)
    for p in cell.paragraphs:
        assert str(p.runs[0].font.color.rgb) == "000000", p.text


def cell_with_dropdown():
    """A cell holding a content control, as the delivery-plan template's Delivery/Assessment cells do."""
    from docx.oxml import parse_xml
    from docx.oxml.ns import nsdecls
    doc = Document()
    t = doc.add_table(rows=1, cols=1)
    cell = t.rows[0].cells[0]
    cell._tc.append(parse_xml(
        f'<w:sdt {nsdecls("w")}><w:sdtPr/><w:sdtContent>'
        f'<w:p><w:r><w:t>Select</w:t></w:r></w:p></w:sdtContent></w:sdt>'
    ))
    return cell


def sdt_count(cell):
    from docx.oxml.ns import qn
    return len(cell._tc.findall(".//" + qn("w:sdt")))


def test_writing_removes_a_content_control():
    """HDT-18 — the dropdown is a placeholder; a filled cell must not still offer it."""
    cell = cell_with_dropdown()
    assert sdt_count(cell) == 1
    DT.set_cell_text(cell, "O")
    assert sdt_count(cell) == 0
    assert "Select" not in cell._tc.xml


def test_writing_a_block_removes_a_content_control():
    """HDT-18 — same for the block writer."""
    cell = cell_with_dropdown()
    DT.set_cell_block(cell, [("Real content", False)])
    assert sdt_count(cell) == 0


# --- unwrap_content_controls (HDT-19 .. HDT-21) ---------------------------

def row_with_wrapped_cells():
    """A row whose middle cells are wrapped in content controls.

    This is the delivery-plan template's real shape: `tc, sdt, sdt, tc`. python-docx sees only the
    direct `w:tc` children, so such a row reports fewer cells than it has and writes land in the
    wrong columns.
    """
    from docx.oxml import parse_xml
    from docx.oxml.ns import nsdecls, qn
    doc = Document()
    t = doc.add_table(rows=1, cols=4)
    tr = t.rows[0]._tr
    tcs = tr.findall(qn("w:tc"))
    for i in (1, 2):
        tc = tcs[i]
        sdt = parse_xml(f'<w:sdt {nsdecls("w")}><w:sdtPr/><w:sdtContent/></w:sdt>')
        tr.replace(tc, sdt)
        sdt.find(qn("w:sdtContent")).append(tc)
    return t


def test_wrapped_cell_is_promoted_to_a_real_cell():
    """HDT-19"""
    t = row_with_wrapped_cells()
    assert len(t.rows[0].cells) == 2
    DT.unwrap_content_controls(t.rows[0])
    assert len(t.rows[0].cells) == 4


def test_promoting_preserves_left_to_right_order():
    """HDT-20 — order is the whole point: a shifted cell writes a value into the wrong column."""
    t = row_with_wrapped_cells()
    DT.unwrap_content_controls(t.rows[0])
    for i, cell in enumerate(t.rows[0].cells):
        DT.set_cell_text(cell, f"col{i}")
    assert [c.text for c in t.rows[0].cells] == ["col0", "col1", "col2", "col3"]


def test_every_cell_is_writable_after_promoting():
    """HDT-21"""
    t = row_with_wrapped_cells()
    DT.unwrap_content_controls(t.rows[0])
    from docx.oxml.ns import qn
    assert t.rows[0]._tr.findall(qn("w:sdt")) == []
