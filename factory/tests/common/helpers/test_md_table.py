"""Cases HMDT-01 .. HMDT-12 — factory/docs/test-plan.md.

Covers common/helpers/md_table.py: reading markdown tables out of a document, keeping each row's
source line number so a validator can point a human at the line to fix.
"""
import md_table as MD

DOC = """\
# A document

## 1. Prose section

Some prose, no table here.

## 2. Session grid

A sentence between the heading and the table.

| # | Week | Mode      |
|---|------|-----------|
| 1 | 9    | online    |
| 2 | 9    |           |

## 3. Notes

| Note |
|------|
| n/a  |
"""


# --- split_row (HMDT-01 .. HMDT-03) ---------------------------------------

def test_row_splits_into_stripped_cells():
    """HMDT-01"""
    assert MD.split_row("| 1 | 9 | online |") == ["1", "9", "online"]


def test_outer_pipes_are_not_cells():
    """HMDT-02"""
    assert len(MD.split_row("| a | b |")) == 2


def test_empty_cell_is_preserved():
    """HMDT-03 — a blank cell is a decision not yet made, not an absent column."""
    assert MD.split_row("| 2 | 9 |   |") == ["2", "9", ""]


# --- is_separator (HMDT-04, HMDT-05) --------------------------------------

def test_separator_row_is_recognised():
    """HMDT-04"""
    assert MD.is_separator(MD.split_row("|---|------|-----------|"))


def test_content_row_is_not_a_separator():
    """HMDT-05"""
    assert not MD.is_separator(MD.split_row("| 1 | 9 | online |"))


# --- rows_under_heading (HMDT-06 .. HMDT-12) ------------------------------

def test_rows_are_returned_header_first():
    """HMDT-06"""
    rows = MD.rows_under_heading(DOC, "Session grid")
    assert rows[0][0] == ["#", "Week", "Mode"]


def test_separator_row_is_not_returned():
    """HMDT-07"""
    rows = MD.rows_under_heading(DOC, "Session grid")
    assert not any(MD.is_separator(cells) for cells, _ in rows)
    assert len(rows) == 3  # header + two data rows


def test_each_row_carries_its_source_line_number():
    """HMDT-08"""
    rows = MD.rows_under_heading(DOC, "Session grid")
    header_line = rows[0][1]
    assert DOC.splitlines()[header_line - 1].startswith("| # | Week")


def test_reading_stops_at_the_next_heading():
    """HMDT-09 — the '## 3. Notes' table must not bleed into the grid."""
    rows = MD.rows_under_heading(DOC, "Session grid")
    assert not any("n/a" in c for cells, _ in rows for c in cells)


def test_absent_heading_yields_no_rows():
    """HMDT-10"""
    assert MD.rows_under_heading(DOC, "Nonexistent heading") == []


def test_heading_matches_case_insensitively_on_a_substring():
    """HMDT-11"""
    assert MD.rows_under_heading(DOC, "session GRID") == MD.rows_under_heading(DOC, "Session grid")


def test_prose_between_heading_and_table_is_skipped():
    """HMDT-12"""
    rows = MD.rows_under_heading(DOC, "Session grid")
    assert rows[0][0] == ["#", "Week", "Mode"]
