"""Cases HFC-01 .. HFC-17 — factory/docs/test-plan.md.

Covers common/helpers/format_contract.py: locating the format document a validator is driven by,
and parsing the machine-readable contract out of its ``## Skeleton`` block.
"""
import format_contract as FC

NAME = "delivery-plan-format.md"


# --- find_format_doc -------------------------------------------------------

def test_explicit_path_that_exists_is_returned(tmp_path):
    """HFC-01"""
    p = tmp_path / NAME
    p.write_text("x", encoding="utf-8")
    assert FC.find_format_doc(NAME, explicit=str(p)) == p


def test_explicit_path_that_is_missing_returns_none(tmp_path):
    """HFC-02"""
    assert FC.find_format_doc(NAME, explicit=str(tmp_path / "nope.md")) is None


def test_found_beside_the_starting_directory(doc_tree):
    """HFC-03"""
    _root, step, scripts = doc_tree
    target = step / NAME
    target.write_text("x", encoding="utf-8")
    assert FC.find_format_doc(NAME, start=scripts) == target


def test_found_in_a_docs_dir_walking_up(doc_tree):
    """HFC-04"""
    root, _step, scripts = doc_tree
    target = root / "docs" / NAME
    target.write_text("x", encoding="utf-8")
    assert FC.find_format_doc(NAME, start=scripts) == target


def test_number_prefixed_variant_is_found(doc_tree):
    """HFC-05 — the factory step-folder convention names docs `_NN_<name>`."""
    _root, step, scripts = doc_tree
    target = step / f"_02_{NAME}"
    target.write_text("x", encoding="utf-8")
    assert FC.find_format_doc(NAME, start=scripts) == target


def test_returns_none_when_nowhere_on_the_path(doc_tree):
    """HFC-06"""
    _root, _step, scripts = doc_tree
    assert FC.find_format_doc(NAME, start=scripts) is None


def test_nearest_match_wins(doc_tree):
    """HFC-07 — a step-local doc beats one further up the tree."""
    root, step, scripts = doc_tree
    far = root / "docs" / NAME
    far.write_text("far", encoding="utf-8")
    near = step / f"_02_{NAME}"
    near.write_text("near", encoding="utf-8")
    assert FC.find_format_doc(NAME, start=scripts) == near


# --- parse_contract --------------------------------------------------------

SKELETON = """\
# Cluster — Delivery Plan (<intake>)

## 1. Instance prerequisites
- Intake: 2026-S1
- Total sessions available: 24

## 2. Session grid
| #  | Week | Day | Mode      | Activity | Placed |
|----|------|-----|-----------|----------|--------|
| 1  | 9    | Thu | classroom | teach    | T1     |

## 3. Notes / decisions
"""


def test_headings_are_returned_in_order_deduplicated(format_doc):
    """HFC-08"""
    p = format_doc(SKELETON)
    headings, _fields, _cols = FC.parse_contract(p.read_text(encoding="utf-8"))
    assert headings == [
        "## 1. Instance prerequisites",
        "## 2. Session grid",
        "## 3. Notes / decisions",
    ]


def test_labelled_field_names_are_returned(format_doc):
    """HFC-09"""
    p = format_doc(SKELETON)
    _headings, fields, _cols = FC.parse_contract(p.read_text(encoding="utf-8"))
    assert fields == ["Intake", "Total sessions available"]


def test_grid_columns_come_from_the_first_header_row(format_doc):
    """HFC-10"""
    p = format_doc(SKELETON)
    _headings, _fields, cols = FC.parse_contract(p.read_text(encoding="utf-8"))
    assert cols == ["#", "Week", "Day", "Mode", "Activity", "Placed"]


def test_separator_row_is_not_read_as_a_header(format_doc):
    """HFC-11 — the |----| row must not become the column list."""
    p = format_doc(SKELETON)
    _headings, _fields, cols = FC.parse_contract(p.read_text(encoding="utf-8"))
    assert not any(set(c) <= {"-"} for c in cols)


def test_no_skeleton_block_returns_three_empty_lists():
    """HFC-12"""
    assert FC.parse_contract("# A doc\n\nNo skeleton here.\n") == ([], [], [])


def test_content_outside_the_skeleton_is_ignored(format_doc):
    """HFC-13"""
    p = format_doc(SKELETON, preamble="## Not part of the contract\n- Decoy field: value")
    headings, fields, _cols = FC.parse_contract(p.read_text(encoding="utf-8"))
    assert "## Not part of the contract" not in headings
    assert "Decoy field" not in fields


# --- parse_labelled_fields -------------------------------------------------

def test_labelled_lines_are_read_into_a_mapping():
    """HFC-14"""
    got = FC.parse_labelled_fields("- Intake: 2026-S1\n- Weeks: 10\n")
    assert got == {"Intake": "2026-S1", "Weeks": "10"}


def test_table_rows_are_ignored():
    """HFC-15 — a grid row can look like a labelled field; it is not one."""
    text = "- Intake: 2026-S1\n| 1 | 9 | Thu | classroom | teach | T1 |\n"
    assert FC.parse_labelled_fields(text) == {"Intake": "2026-S1"}


def test_repeated_label_keeps_the_last_value():
    """HFC-16"""
    got = FC.parse_labelled_fields("- Weeks: 10\n- Weeks: 8\n")
    assert got == {"Weeks": "8"}


def test_line_without_a_colon_is_ignored():
    """HFC-17"""
    assert FC.parse_labelled_fields("- just a bullet\n") == {}


# --- multi-line field values (HFC-18 .. HFC-20) ---------------------------

MULTILINE = """\
- Intake: 2026-T2
- LLN requirements:
  Literacy — Reading
  - Interprets complex documentation
  - Analyses information from a range of sources
- Cohort description: A small regional cohort
"""


def test_indented_line_continues_the_field():
    """HFC-18 — a value too long or too structured for one line."""
    got = FC.parse_labelled_fields(MULTILINE)
    assert "Literacy — Reading" in got["LLN requirements"]
    assert "Analyses information" in got["LLN requirements"]


def test_continuation_ends_at_the_next_unindented_line():
    """HFC-19 — the following field must not be swallowed into the previous one."""
    got = FC.parse_labelled_fields(MULTILINE)
    assert got["Cohort description"] == "A small regional cohort"
    assert "Cohort description" not in got["LLN requirements"]


def test_continued_value_keeps_its_line_breaks():
    """HFC-20 — the structure is the content; flattening it produces an unreadable paragraph."""
    got = FC.parse_labelled_fields(MULTILINE)
    lines = got["LLN requirements"].split("\n")
    assert lines[0] == "Literacy — Reading"
    assert lines[1].startswith("- Interprets")
