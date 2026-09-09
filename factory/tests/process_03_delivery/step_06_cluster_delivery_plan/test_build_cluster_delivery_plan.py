"""Cases CDG-01 .. CDG-14 — factory/docs/test-plan.md.

The step-6 generator: a validated outline plus the institutional template becomes a filled
Delivery Plan .docx.
"""
from docx import Document

import build_cluster_delivery_plan as B
from conftest import FORMAT_DOC, TEMPLATE


R_DATA_PROBE = 3  # the first data row of a session block


def sessions(doc):
    """The per-session tables — the 6-column blocks, ignoring the summary tables at the top."""
    return [t for t in doc.tables if len(t.columns) == 6]


def cell(table, row, col):
    return table.rows[row].cells[col].text.strip()


def build(cluster_fixture, tmp_path, plan=None):
    root, write_plan = cluster_fixture
    plan_path = write_plan(plan) if plan else write_plan()
    out = tmp_path / "out.docx"
    code = B.build(plan_path, TEMPLATE, out, fmt_doc=FORMAT_DOC)
    return code, out


# --- refusing to run (CDG-01, CDG-02) -------------------------------------

def test_invalid_outline_is_refused(cluster, tmp_path, plan_text, capsys):
    """CDG-01 — a PASS is what 'ready to generate' means; generating from a FAIL invents content."""
    code, out = build(cluster, tmp_path, plan_text.replace("| spare      | —      |",
                                                           "| spare      |        |"))
    assert code == 1
    assert not out.exists()


def test_source_template_is_not_modified(cluster, tmp_path):
    """CDG-02"""
    before = TEMPLATE.read_bytes()
    build(cluster, tmp_path)
    assert TEMPLATE.read_bytes() == before


# --- session blocks (CDG-03 .. CDG-06) ------------------------------------

def test_one_session_block_per_grid_row(cluster, tmp_path):
    """CDG-03 — the template ships with three; the intake decides how many there really are."""
    code, out = build(cluster, tmp_path)
    assert code == 0
    assert len(sessions(Document(str(out)))) == 3


def test_session_blocks_appear_in_grid_order(cluster, tmp_path):
    """CDG-04"""
    _code, out = build(cluster, tmp_path)
    blocks = sessions(Document(str(out)))
    dates = [cell(b, 1, 1) for b in blocks]
    assert dates == ["2026-10-08", "2026-10-08", "2026-10-09"]


def test_session_date_comes_from_the_date_column(cluster, tmp_path):
    """CDG-05"""
    _code, out = build(cluster, tmp_path)
    assert cell(sessions(Document(str(out)))[0], 1, 1) == "2026-10-08"


def test_time_comes_from_the_time_column(cluster, tmp_path):
    """CDG-06"""
    _code, out = build(cluster, tmp_path)
    assert cell(sessions(Document(str(out)))[1], 3, 0) == "1pm-4pm"


# --- institutional vocabulary (CDG-07 .. CDG-11) --------------------------

def test_mode_is_translated_to_institutional_codes(cluster, tmp_path):
    """CDG-07 — the outline says online/classroom; the template's dropdown is O/FTF/WP."""
    _code, out = build(cluster, tmp_path)
    assert cell(sessions(Document(str(out)))[0], 3, 1) == "O"


def test_assessment_session_carries_its_declared_type(cluster, tmp_path):
    """CDG-08 — from the outline's 'Assessment types:' field, not inferred from the instrument."""
    _code, out = build(cluster, tmp_path)
    assert cell(sessions(Document(str(out)))[1], 3, 2) == "Project"


def test_non_assessment_session_leaves_assessment_empty(cluster, tmp_path):
    """CDG-09"""
    _code, out = build(cluster, tmp_path)
    assert cell(sessions(Document(str(out)))[0], 3, 2) == ""


def test_delivery_mapping_carries_the_topics_sections(cluster, tmp_path):
    """CDG-10 — session 1 runs T1, whose coverage.md teaches PC and KE."""
    _code, out = build(cluster, tmp_path)
    mapping = cell(sessions(Document(str(out)))[0], 3, 5)
    assert "PC" in mapping and "Know" in mapping


def test_session_placing_nothing_has_empty_mapping(cluster, tmp_path):
    """CDG-11 — the spare session places '—'."""
    _code, out = build(cluster, tmp_path)
    assert cell(sessions(Document(str(out)))[2], 3, 5) == ""


# --- content and fidelity (CDG-12 .. CDG-14) ------------------------------

def test_topic_column_names_what_the_session_runs(cluster, tmp_path):
    """CDG-12 — a bare 'T1' tells a reader nothing; the title is in the Topic's coverage.md."""
    _code, out = build(cluster, tmp_path)
    assert cell(sessions(Document(str(out)))[0], 3, 3) == "Topic 01 — Test topic"


def test_topic_without_a_title_falls_back_to_its_reference(cluster, tmp_path, plan_text):
    """CDG-20 — an unreadable title is not a reason to write nothing."""
    root, write_plan = cluster
    cov = root / "delivery" / "topic_01" / "coverage.md"
    cov.write_text(cov.read_text().replace("# Topic 01 — Test topic · Coverage", "no heading here"),
                   encoding="utf-8")
    _code, out = build(cluster, tmp_path)
    assert cell(sessions(Document(str(out)))[0], 3, 3) == "T1"


def test_assessment_session_names_the_assessment(cluster, tmp_path):
    """CDG-21 — named by title, from the assessment plan; an AT has no coverage.md to read."""
    _code, out = build(cluster, tmp_path)
    assert cell(sessions(Document(str(out)))[1], 3, 3) == "AT1 — Cloud Expansion: Design & DR Plan"


def test_assessment_without_a_title_falls_back_to_its_reference(cluster, tmp_path):
    """CDG-22"""
    root, _write = cluster
    plan = root / "assessments" / "assessment_plan.md"
    plan.write_text(plan.read_text().replace("### AT1 — Cloud Expansion: Design & DR Plan", "no heading"),
                    encoding="utf-8")
    _code, out = build(cluster, tmp_path)
    assert cell(sessions(Document(str(out)))[1], 3, 3) == "AT1"


def test_template_cell_formatting_survives(cluster, tmp_path):
    """CDG-13 — a filled institutional document must still look like the institution's document.

    This template carries its formatting through paragraph styles rather than direct run formatting,
    so the style is what has to survive being written to.
    """
    _code, out = build(cluster, tmp_path)
    filled = sessions(Document(str(out)))[0].rows[R_DATA_PROBE].cells[0].paragraphs[0]
    assert filled.style.name == "Heading 3"


def test_document_is_written_where_asked(cluster, tmp_path):
    """CDG-14"""
    _code, out = build(cluster, tmp_path)
    assert out.is_file() and out.stat().st_size > 0


def test_unused_template_rows_are_removed(cluster, tmp_path):
    """CDG-15 — the template ships four data rows per block; a session that fills one keeps one."""
    _code, out = build(cluster, tmp_path)
    for block in sessions(Document(str(out))):
        assert len(block.rows) == R_DATA_PROBE + 1


# --- document header (CDG-16 .. CDG-18) -----------------------------------

def header_tables(doc):
    """The 2-column tables above the session blocks, keyed by their title row."""
    return {t.rows[0].cells[0].text.strip(): t
            for t in doc.tables if len(t.columns) == 2}


def test_details_table_carries_qualification_unit_and_cohort(cluster, tmp_path):
    """CDG-16"""
    _code, out = build(cluster, tmp_path)
    details = header_tables(Document(str(out)))["Details"]
    values = [r.cells[1].text.strip() for r in details.rows[1:]]
    assert "ICT50220" in values[0]
    assert "ICTCLD501" in values[1]
    assert "2026-T2" in values[2]


def test_materials_table_carries_the_materials_value(cluster, tmp_path):
    """CDG-17"""
    _code, out = build(cluster, tmp_path)
    tables = header_tables(Document(str(out)))
    materials = tables["General Learning Materials and Resources"]
    assert "Learner Lab" in materials.rows[1].cells[1].text


def lln_text(out):
    tables = header_tables(Document(str(out)))
    return next(t for k, t in tables.items() if k.startswith("LLN")).rows[1].cells[1].text


def test_lln_table_carries_the_requirements_value(cluster, tmp_path):
    """CDG-18 — derived from the cluster's units, not copied from the outline."""
    _code, out = build(cluster, tmp_path)
    text = lln_text(out)
    assert "Interprets complex technical documentation" in text
    assert "Evaluates and resolves risk events" not in text   # not an LLN demand


def test_changing_the_units_changes_the_generated_lln(cluster, tmp_path):
    """CDG-19 — a derivation tracks its source; a copy in the outline could not."""
    root, _write = cluster
    spec = root / "consolidated_uoc.md"
    spec.write_text(spec.read_text().replace("Interprets complex technical documentation",
                                             "Reads an entirely different thing"), encoding="utf-8")
    _code, out = build(cluster, tmp_path)
    assert "Reads an entirely different thing" in lln_text(out)


def test_spare_session_is_labelled_spare(cluster, tmp_path):
    """CDG-23 — a blank row reads as an oversight; the plan said 'spare', so the document should."""
    _code, out = build(cluster, tmp_path)
    assert cell(sessions(Document(str(out)))[2], 3, 3).lower().startswith("spare")


def test_activity_label_never_displaces_placed_content(cluster, tmp_path):
    """CDG-24 — sessions 1 and 2 place a Topic and an assessment; neither may be relabelled."""
    _code, out = build(cluster, tmp_path)
    blocks = sessions(Document(str(out)))
    assert cell(blocks[0], 3, 3) == "Topic 01 — Test topic"
    assert cell(blocks[1], 3, 3) == "AT1 — Cloud Expansion: Design & DR Plan"
