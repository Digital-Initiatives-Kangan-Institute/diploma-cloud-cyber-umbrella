"""Which UoC **sections** a Topic teaches, in the institution's Delivery Mapping vocabulary.

USE THIS WHEN you need to know *what kind* of evidence a Topic covers -- performance criteria,
knowledge, skills, conditions -- for a document that asks for a category rather than a citation. The
delivery-plan docx is the case it was built for: its per-session "Delivery Mapping" column is a
five-value dropdown (PC / LO / Know / Skill / Cond), not a list of UoC item references.

DO NOT USE THIS to enumerate individual UoC items. Resolving `[ICTCLD501 PC 1.1-1.3]` into its
members, letting an abbreviated `[PC 2.1]` inherit the preceding unit, or splitting a compound tag on
a middle dot is a different and larger job, already implemented once in
``validate_at_traceability.resolve_tags``. Reach for that; do not re-create it here.

The section codes this reads are the project's canonical **unwrapped** form, ``[UNIT SEC num]``. A
backtick-wrapped tag is a formatting defect the coverage validators report, so it is deliberately not
counted here either -- counting it would let a defect pass unnoticed into a generated document.

Cases: HUS-01 .. HUS-16 in factory/docs/test-plan.md.
"""
from __future__ import annotations

import re

# The "taught / developed" mapping heading, and the markers that end that block.
_MAPPING_HEADING = re.compile(r"^#{1,4}\s.*UoC\s+mapping", re.IGNORECASE)
_APPLIED_MARKER = re.compile(r"applied\b.*\b(earlier|elsewhere|taught)", re.IGNORECASE)
_NEXT_H2 = re.compile(r"^##\s")

# Canonical unwrapped tag: [UNIT SECTION ...]. Only the section is wanted.
_TAG_SECTION = re.compile(r"\[(?:ICT\w+|BSB\w+|VU\d+)\s+(PC|FS|PE|KE|AC)\b")
_BACKTICKED = re.compile(r"`[^`]*`")

# Our section codes as the institutional template's dropdown values. Order follows the template's
# own legend, so a generated document reads the way the institution's reader expects.
_TO_INSTITUTIONAL = {"PC": "PC", "KE": "Know", "PE": "Skill", "FS": "Skill", "AC": "Cond"}
_ORDER = ["PC", "LO", "Know", "Skill", "Cond"]


def taught_block(text: str) -> str:
    """The taught/developed portion of a ``coverage.md``.

    Runs from the "UoC mapping" heading to the next ``##`` heading, and stops early at an
    "applied earlier/elsewhere" marker -- content past that point is taught somewhere else, so
    counting it would credit this Topic with a section it does not teach. Empty string when the
    document has no mapping heading.
    """
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if _MAPPING_HEADING.match(line.strip()):
            start = i + 1
            break
    if start is None:
        return ""
    out = []
    for line in lines[start:]:
        if _NEXT_H2.match(line) or _APPLIED_MARKER.search(line):
            break
        out.append(line)
    return "\n".join(out)


def sections_taught(text: str) -> set[str]:
    """The set of UoC section codes tagged in the document's taught block.

    Returns our own codes (``PC``/``FS``/``PE``/``KE``/``AC``); pass the result through
    :func:`to_delivery_mapping` for the institutional vocabulary.
    """
    block = _BACKTICKED.sub("", taught_block(text))
    return set(_TAG_SECTION.findall(block))


def to_delivery_mapping(sections) -> list[str]:
    """Our section codes as the delivery-plan template's dropdown values.

    ``PE`` and ``FS`` both mean skills to the institution, so they collapse to one ``Skill``.
    Unknown codes are dropped rather than guessed at. Ordering follows the template's legend.
    """
    mapped = {_TO_INSTITUTIONAL[s] for s in sections if s in _TO_INSTITUTIONAL}
    return [v for v in _ORDER if v in mapped]
