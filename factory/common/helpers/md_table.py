"""Reading markdown tables out of a document.

Markdown tables are how this project's artefacts carry structured data -- a delivery plan's session
grid, a slide plan's component table, a consolidated plan's AT roster. Nine scripts across the repo
grew their own copy of this parsing; this is the one implementation.

Rows keep their **1-based source line number**, so a validator reporting a defect can point a human
at the line to fix rather than at the table in general.

Cases: HMDT-01 .. HMDT-12 in factory/docs/test-plan.md.
"""
from __future__ import annotations

import re

_SEPARATOR_CELL = re.compile(r"^:?-{3,}:?$")
_HEADING = re.compile(r"^#{1,6}\s")


def split_row(line: str) -> list[str]:
    """Cells of a pipe-delimited row, stripped. Outer pipes are delimiters, not cells.

    An empty cell is preserved as ``""`` -- in an artefact an empty cell means a decision not yet
    made, which is a thing a validator must be able to see.
    """
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_separator(cells: list[str]) -> bool:
    """True when every cell is a `---` / `:---:` rule, i.e. the row under a table header."""
    return bool(cells) and all(_SEPARATOR_CELL.match(c) for c in cells)


def rows_under_heading(text: str, heading: str) -> list[tuple[list[str], int]]:
    """Rows of the first table beneath ``heading``, as ``(cells, line_no)``, header row first.

    ``heading`` matches case-insensitively as a substring, so "Session grid" finds
    "## 2. Session grid". Reading stops at the next heading of any level, so a later table cannot
    bleed into this one. Separator rows are dropped; prose between the heading and the table is
    skipped. An absent heading yields ``[]``.
    """
    lines = text.splitlines()
    needle = heading.lower()

    start = None
    for i, line in enumerate(lines):
        if _HEADING.match(line) and needle in line.lower():
            start = i + 1
            break
    if start is None:
        return []

    rows: list[tuple[list[str], int]] = []
    for i in range(start, len(lines)):
        line = lines[i]
        if _HEADING.match(line):
            break
        if not line.lstrip().startswith("|"):
            continue
        cells = split_row(line)
        if is_separator(cells):
            continue
        rows.append((cells, i + 1))
    return rows
