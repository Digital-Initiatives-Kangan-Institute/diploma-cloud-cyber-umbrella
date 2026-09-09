"""Reading a format document's machine-readable contract.

The factory's gate architecture rests on one idea: **the format document is the single source of
truth**. A format standard carries a ``## Skeleton`` fenced block showing the artefact's shape, and the
validator *parses that block* to learn what to check rather than hard-coding a field list — change the
skeleton and the checks follow.

Two validators grew their own copies of this machinery and had already drifted before extraction --
one returned two values, the other three. This is the one copy, carrying the superset behaviour;
``validate_cluster_spec.py`` still has its own and should adopt this when it ports.

``find_format_doc`` also understands the factory's step-folder convention, where a step's documents are
number-prefixed for reading order (``_02_delivery-plan-format.md``), so a validator living in a step's
``scripts/`` folder finds the document beside it.

Cases: HFC-01 .. HFC-17 in factory/docs/test-plan.md.
"""
from __future__ import annotations

import re
from pathlib import Path

# A step folder numbers its documents for reading order: _00_prerequisites.md, _02_<name>.md, ...
_NUMBER_PREFIX = re.compile(r"^_\d+_")


def find_format_doc(name: str, explicit: str | None = None, start: Path | None = None) -> Path | None:
    """Locate the format document called ``name``.

    ``explicit`` wins outright when it points at a real file (and yields None when it does not, so a
    mistyped ``--format`` fails loudly instead of silently falling back). Otherwise the search walks up
    from ``start`` (defaulting to the caller's own directory), and at each level looks for the document
    beside that directory, as a number-prefixed variant, or inside a ``docs/`` subdirectory. Nearest
    match wins.
    """
    if explicit:
        p = Path(explicit)
        return p if p.is_file() else None

    here = Path(start).resolve() if start else Path(__file__).resolve().parent
    for d in [here, *here.parents]:
        direct = d / name
        if direct.is_file():
            return direct
        numbered = sorted(
            c for c in d.glob(f"_*_{name}") if _NUMBER_PREFIX.match(c.name)
        )
        if numbered:
            return numbered[0]
        in_docs = d / "docs" / name
        if in_docs.is_file():
            return in_docs
    return None


def parse_contract(format_text: str) -> tuple[list[str], list[str], list[str]]:
    """Extract ``(headings, field-labels, grid-column-names)`` from the ``## Skeleton`` block.

    Everything outside the block is prose about the format, not the contract itself, and is ignored.
    Returns three empty lists when there is no skeleton to read.
    """
    m = re.search(r"##\s+Skeleton\s*\n+```[a-zA-Z]*\n(.*?)\n```", format_text, re.DOTALL)
    if not m:
        return [], [], []
    block = m.group(1)

    headings = list(dict.fromkeys(re.findall(r"^(##\s+.+?)\s*$", block, re.MULTILINE)))
    fields = list(dict.fromkeys(
        lbl.strip() for lbl in re.findall(r"^-\s*([^:\n]+?):", block, re.MULTILINE)
    ))

    # Grid columns come from the first real table header row; the |---| separator is not one.
    columns: list[str] = []
    for line in block.splitlines():
        if line.lstrip().startswith("|") and re.search(r"[A-Za-z#]", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if any(re.search(r"-{3,}", c) for c in cells):
                continue
            columns = [c for c in cells if c]
            break

    return headings, fields, columns


def parse_labelled_fields(text: str) -> dict[str, str]:
    """Read ``- Label: value`` lines into a mapping.

    A value may run over several lines: any **indented** line following a field continues it, and the
    line breaks are kept. Some values are structured -- a headed list of LLN demands, say -- and
    flattening them onto one line turns a readable section into an unreadable paragraph, so the
    structure is preserved as written. Continuation ends at the next unindented line.

    Table rows are skipped: a grid row can contain a colon and would otherwise be read as a field.
    A repeated label keeps the last value.
    """
    fields: dict[str, str] = {}
    current: str | None = None
    for line in text.splitlines():
        if line.lstrip().startswith("|"):
            current = None
            continue
        m = re.match(r"-\s*([^:]+?):\s*(.*?)\s*$", line.lstrip()) if not line[:1].isspace() else None
        if m:
            current = m.group(1).strip()
            fields[current] = m.group(2).strip()
            continue
        if current and line[:1].isspace() and line.strip():
            extra = line.strip()
            fields[current] = f"{fields[current]}\n{extra}".lstrip("\n")
            continue
        if not line[:1].isspace():
            current = None
    return fields
