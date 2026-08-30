"""Tests for inventory_uoc.py — the mechanical extractor behind step 2.

It is now the sole producer of every item line in every cluster's consolidated_uoc.md, so its
output IS the assessable item register. Three properties have to hold: every assessable item in
the unit becomes exactly one tagged item, nothing that is not an assessable item becomes one, and
each item's text is the source's text unaltered.

The numbering rules it must implement (they are what every downstream tag depends on):
  PC  — the source's own numbering, from the performance-criteria column, split on <br>
  FS  — the skill name verbatim, case and spaces included
  PE/KE/AC — 1..N in source order, EXCEPT a section whose only top-level bullet ends in ':',
        whose immediate sub-bullets are the items; nested sub-bullets under a normal item stay
        folded into that one item
  the trailing "Assessors of this unit must satisfy..." paragraph is one extra AC only with
        --assessor-ac

Fixtures are unit .md text written by hand here, so the expectations are independent of the
parser under test.
"""
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import inventory_uoc as I  # noqa: E402

TAG = re.compile(r"\[((?:ICT|BSB|VU)\w+ (?:PC|FS|PE|KE|AC) [^\]]+)\]")


# ---------------------------------------------------------------------------
# A representative unit
# ---------------------------------------------------------------------------

UNIT = """# ICTTEST101 Configure cloud services

# Application

This unit describes the skills required to configure cloud services.

# Elements and Performance Criteria

| ELEMENTS | PERFORMANCE CRITERIA |
| --- | --- |
| Elements describe the essential outcomes. | Performance criteria describe the performance needed. |
| 1. Prepare to configure | 1.1 Confirm cloud service requirements with the client<br>1.2 Identify security and access requirements |
| 2. Configure services | 2.1 Configure services according to organisational procedures |

# Foundation Skills

This section describes those language, literacy and numeracy skills.

| SKILL | DESCRIPTION |
| --- | --- |
| Oral communication | Presents information using clear language |
| Problem solving | Evaluates alternative strategies and anticipates consequences |

# Unit Mapping Information

Supersedes ICTTEST100.

# Performance Evidence

The candidate must demonstrate the ability to complete the tasks outlined in the elements.

- configure two cloud services
- document the configuration

In the course of the above, the candidate must:

- record the deployment steps

# Knowledge Evidence

The candidate must demonstrate knowledge of:

- industry standards used in cloud computing
- functions and differences of cloud models, including:
  - public cloud
  - private cloud

# Assessment Conditions

Skills must be demonstrated in a workplace.

- cloud vendor service provider
- industry software packages

Assessors of this unit must satisfy the requirements for assessors in applicable vocational education and training legislation.

# Links

Companion Volume implementation guides are found at the link.
"""

# The items this unit contains, written out by hand: (tag, the text of the item's first line).
EXPECTED = [
    ("ICTTEST101 PC 1.1", "1.1 Confirm cloud service requirements with the client"),
    ("ICTTEST101 PC 1.2", "1.2 Identify security and access requirements"),
    ("ICTTEST101 PC 2.1", "2.1 Configure services according to organisational procedures"),
    ("ICTTEST101 FS Oral communication", "**Oral communication** — Presents information using clear language"),
    ("ICTTEST101 FS Problem solving", "**Problem solving** — Evaluates alternative strategies and anticipates consequences"),
    ("ICTTEST101 PE 1", "configure two cloud services"),
    ("ICTTEST101 PE 2", "document the configuration"),
    ("ICTTEST101 PE 3", "record the deployment steps"),
    ("ICTTEST101 KE 1", "industry standards used in cloud computing"),
    ("ICTTEST101 KE 2", "functions and differences of cloud models, including:"),
    ("ICTTEST101 AC 1", "cloud vendor service provider"),
    ("ICTTEST101 AC 2", "industry software packages"),
]

ASSESSOR_PARA = ("ICTTEST101 AC 3",
                 "Assessors of this unit must satisfy the requirements for assessors in "
                 "applicable vocational education and training legislation.")


def items(md=UNIT, code="ICTTEST101", assessor_ac=False):
    """Flatten inventory() to the list of rendered item blocks, in emission order."""
    out = []
    for _header, block in I.inventory(code, md, assessor_ac):
        out.extend(block)
    return out


def tagged(md=UNIT, code="ICTTEST101", assessor_ac=False):
    """{tag: item block} for the items produced."""
    return {TAG.search(b).group(1): b for b in items(md, code, assessor_ac)}


def first_line_text(block):
    """The item's own text: its first line, with the bullet marker and the tag removed."""
    return TAG.sub("", re.sub(r"^- ", "", block.splitlines()[0])).strip()


# ---------------------------------------------------------------------------
# Completeness and no-invention — the item set is exactly the assessable items
# ---------------------------------------------------------------------------

def test_extracts_exactly_the_expected_items():
    """The baseline: every assessable item, nothing else, in source order."""
    assert [TAG.search(b).group(1) for b in items()] == [t for t, _ in EXPECTED]


def test_every_item_carries_exactly_one_tag():
    for block in items():
        assert len(TAG.findall(block)) == 1, block


def test_no_two_items_share_a_tag():
    tags = [TAG.search(b).group(1) for b in items()]
    assert len(tags) == len(set(tags))


def test_non_assessable_sections_contribute_nothing():
    """Application / Unit Mapping / Links are not assessable and must produce no items."""
    text = " ".join(items())
    for phrase in ("This unit describes", "Supersedes", "Companion Volume"):
        assert phrase not in text


def test_prose_within_an_assessable_section_is_not_an_item():
    """The PE intro paragraph and the 'In the course of the above' lead-in are not items."""
    text = " ".join(items())
    assert "must demonstrate the ability to complete" not in text
    assert "In the course of the above" not in text


# ---------------------------------------------------------------------------
# Verbatim text
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tag,text", EXPECTED)
def test_item_text_is_verbatim(tag, text):
    assert first_line_text(tagged()[tag]) == text


def test_source_punctuation_is_preserved():
    """Smart quotes and trailing full stops belong to the source and must survive extraction."""
    md = UNIT.replace("- configure two cloud services",
                      "- configure the business’s two cloud services.")
    assert first_line_text(tagged(md)["ICTTEST101 PE 1"]) == "configure the business’s two cloud services."


# ---------------------------------------------------------------------------
# Numbering rules
# ---------------------------------------------------------------------------

def test_pc_keeps_source_numbering_across_elements():
    """PC numbers come from the source, not from a counter — 1.1, 1.2 then 2.1, not 1.1..1.3."""
    pcs = [t for t in tagged() if " PC " in t]
    assert pcs == ["ICTTEST101 PC 1.1", "ICTTEST101 PC 1.2", "ICTTEST101 PC 2.1"]


def test_multiple_pcs_in_one_cell_are_split_on_br():
    """Element 1's cell holds two PCs separated by <br>; they are two items, not one."""
    assert "ICTTEST101 PC 1.1" in tagged() and "ICTTEST101 PC 1.2" in tagged()


def test_fs_tag_is_the_skill_name_verbatim():
    """Case and spacing are part of the identity — 'Oral communication', not 'Oral Communication'."""
    assert "ICTTEST101 FS Oral communication" in tagged()


def test_fs_header_row_is_not_an_item():
    assert not any(t.startswith("ICTTEST101 FS SKILL") for t in tagged())


def test_pe_numbered_in_source_order_across_an_intervening_paragraph():
    """The real units split PE into two bullet groups around a lead-in paragraph.

    All the bullets are items of one 1..N sequence — the paragraph does not restart numbering.
    """
    assert first_line_text(tagged()["ICTTEST101 PE 3"]) == "record the deployment steps"


def test_ac_numbered_from_one():
    assert first_line_text(tagged()["ICTTEST101 AC 1"]) == "cloud vendor service provider"


# ---------------------------------------------------------------------------
# The two nesting conventions — the distinction the whole register depends on
# ---------------------------------------------------------------------------

def test_ke_sub_bullets_stay_folded_into_their_parent_item():
    """A KE parent with children is ONE item, and the children's text is part of it.

    This is the shape CL1's hand extraction lost: the parent kept, the children dropped, leaving
    the item dangling on its colon.
    """
    block = tagged()["ICTTEST101 KE 2"]
    assert "public cloud" in block and "private cloud" in block
    assert "ICTTEST101 KE 3" not in tagged()


def test_parent_bullet_ending_in_colon_makes_its_children_the_items():
    """The ICTICT517 PE shape: one top-level bullet ending ':' — the sub-bullets are the items."""
    md = UNIT.replace(
        "- configure two cloud services\n- document the configuration\n\n"
        "In the course of the above, the candidate must:\n\n- record the deployment steps",
        "- For one organisation:\n  - configure two cloud services\n  - document the configuration")
    pe = {t: b for t, b in tagged(md).items() if " PE " in t}
    assert list(pe) == ["ICTTEST101 PE 1", "ICTTEST101 PE 2"]
    assert first_line_text(pe["ICTTEST101 PE 1"]) == "configure two cloud services"


def test_the_colon_parent_itself_is_not_an_item():
    md = UNIT.replace(
        "- configure two cloud services\n- document the configuration\n\n"
        "In the course of the above, the candidate must:\n\n- record the deployment steps",
        "- For one organisation:\n  - configure two cloud services\n  - document the configuration")
    assert "For one organisation" not in " ".join(items(md))


# ---------------------------------------------------------------------------
# The assessor-AC flag
# ---------------------------------------------------------------------------

def test_assessor_paragraph_omitted_by_default():
    assert ASSESSOR_PARA[0] not in tagged()


def test_assessor_paragraph_emitted_as_the_next_ac_when_requested():
    block = tagged(assessor_ac=True)[ASSESSOR_PARA[0]]
    assert first_line_text(block) == ASSESSOR_PARA[1]


# ---------------------------------------------------------------------------
# Section delimiting
# ---------------------------------------------------------------------------

def test_final_section_without_a_following_heading_is_still_read():
    """Assessment Conditions last in the file — the section regex must not need a trailing '# '."""
    md = UNIT.split("# Links")[0].rstrip() + "\n"
    assert "ICTTEST101 AC 2" in tagged(md)


def test_items_do_not_leak_across_section_boundaries():
    """A PE bullet must never be numbered as a KE item, and vice versa."""
    assert first_line_text(tagged()["ICTTEST101 KE 1"]) == "industry standards used in cloud computing"
    assert first_line_text(tagged()["ICTTEST101 PE 1"]) == "configure two cloud services"


# ---------------------------------------------------------------------------
# Silent zero — the extractor must never quietly report that a section has no items
# ---------------------------------------------------------------------------

def test_a_renamed_section_heading_is_an_error_not_zero_items():
    """If a heading does not match, the section yields nothing and the register silently shrinks.

    Downstream, `validate_consolidated.py` builds its expected set from these same rules, so the
    consolidated doc is then measured against a yardstick that is short by a whole section and
    the gate still passes. Missing an assessable section must be loud.
    """
    md = UNIT.replace("# Knowledge Evidence", "# Knowledge evidence")
    with pytest.raises(Exception):
        items(md)


def test_a_section_with_no_bullets_is_an_error_not_zero_items():
    """Every bullet flattened to a paragraph — the Gate 1 structure blind spot arriving here."""
    md = UNIT.replace(
        "- industry standards used in cloud computing\n"
        "- functions and differences of cloud models, including:\n"
        "  - public cloud\n  - private cloud",
        "industry standards used in cloud computing\n\n"
        "functions and differences of cloud models, including public and private cloud")
    with pytest.raises(Exception):
        items(md)


def test_an_empty_unit_yields_no_items_loudly():
    """A file that is not a UoC at all must fail, not produce an empty register."""
    with pytest.raises(Exception):
        items("# Some other document\n\nNothing assessable here.\n")
