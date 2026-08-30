"""Tests for validate_consolidated.py — the Gate 2→3 oracle.

`consolidated_uoc.md` is the last point in the run-sheet where the source of truth is still
checkable. Nothing downstream reads the units again: the assessment plan's coverage rollup, every
AT's traceability tags, the mapping documents and the cluster-coverage capstone all build their
expected item set from this one document. An item lost here does not surface later as a gap — it
surfaces as 100% coverage of a set that is quietly short.

So the gate has to prove four things about the item layer, and stay indifferent to the editorial
layer around it (topic headings, rationale, assessment ideas — legitimately not in any unit):

  MISSING        every assessable item from every unit is present
  UNEXPECTED     nothing is present that no unit contains
  DUPLICATED     each item appears exactly once
  MISTRANSCRIBED each item's text is the source's text, under the tag that identifies it

Fixtures are unit .md and consolidated .md written by hand here, so the expectations are
independent of the parsers under test.
"""
import re
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "validate_consolidated.py"

UNIT_A = """# ICTTEST101 Configure cloud services

# Elements and Performance Criteria

| ELEMENTS | PERFORMANCE CRITERIA |
| --- | --- |
| Elements describe the essential outcomes. | Performance criteria describe the performance. |
| 1. Prepare | 1.1 Confirm cloud service requirements with the client<br>1.2 Identify security and access requirements |

# Foundation Skills

| SKILL | DESCRIPTION |
| --- | --- |
| Oral communication | Presents information using clear language |

# Performance Evidence

The candidate must demonstrate the ability to:

- configure two cloud services
- document the configuration

# Knowledge Evidence

- industry standards used in cloud computing
- functions and differences of cloud models, including:
  - public cloud
  - private cloud

# Assessment Conditions

- cloud vendor service provider

Assessors of this unit must satisfy the requirements for assessors.

# Links

Companion volume implementation guides are found at the link.
"""

UNIT_B = """# ICTTEST202 Monitor cloud services

# Elements and Performance Criteria

| ELEMENTS | PERFORMANCE CRITERIA |
| --- | --- |
| Elements describe the essential outcomes. | Performance criteria describe the performance. |
| 1. Monitor | 1.1 Review service metrics against agreed targets |

# Foundation Skills

| SKILL | DESCRIPTION |
| --- | --- |
| Reading | Interprets technical documentation |

# Performance Evidence

- report on service performance

# Knowledge Evidence

- monitoring tools available on a cloud platform

# Assessment Conditions

- access to monitoring tooling

Assessors of this unit must satisfy the requirements for assessors.

# Links

Companion volume implementation guides are found at the link.
"""

# The faithful consolidation: the editorial layer, with every item line as the extractor emits it.
ITEMS = [
    "- 1.1 Confirm cloud service requirements with the client [ICTTEST101 PC 1.1]",
    "- 1.2 Identify security and access requirements [ICTTEST101 PC 1.2]",
    "- **Oral communication** — Presents information using clear language [ICTTEST101 FS Oral communication]",
    "- configure two cloud services [ICTTEST101 PE 1]",
    "- document the configuration [ICTTEST101 PE 2]",
    "- industry standards used in cloud computing [ICTTEST101 KE 1]",
    "- functions and differences of cloud models, including: [ICTTEST101 KE 2]\n"
    "  - public cloud\n  - private cloud",
    "- cloud vendor service provider [ICTTEST101 AC 1]",
    "- Assessors of this unit must satisfy the requirements for assessors. [ICTTEST101 AC 2]",
    "- 1.1 Review service metrics against agreed targets [ICTTEST202 PC 1.1]",
    "- **Reading** — Interprets technical documentation [ICTTEST202 FS Reading]",
    "- report on service performance [ICTTEST202 PE 1]",
    "- monitoring tools available on a cloud platform [ICTTEST202 KE 1]",
    "- access to monitoring tooling [ICTTEST202 AC 1]",
    "- Assessors of this unit must satisfy the requirements for assessors. [ICTTEST202 AC 2]",
]

PREAMBLE = """# S1-CL9 Test Cluster — Consolidated UoC

> **STATUS: DRAFT.** Every assessable item quoted verbatim and tagged `[UNIT SECTION numbering]` —
> for example `[ICTTEST101 PC 1.1]` or `[ICTTEST202 KE 1]`.

## Group 1 — Preparing and configuring

**Why grouped:** one artefact could plausibly evidence the whole group.

"""


def consolidated(items=None) -> str:
    return PREAMBLE + "\n".join(ITEMS if items is None else items) + "\n"


def build(tmp_path, doc=None, unit_a=UNIT_A, unit_b=UNIT_B) -> Path:
    """A cluster laid out the way the validator expects to find one."""
    cluster = tmp_path / "S1-CL9-Test"
    (cluster / "units_of_competency").mkdir(parents=True)
    (cluster / "units_of_competency/ICTTEST101.md").write_text(unit_a, encoding="utf-8")
    (cluster / "units_of_competency/ICTTEST202.md").write_text(unit_b, encoding="utf-8")
    (cluster / "consolidated_uoc.md").write_text(consolidated() if doc is None else doc, encoding="utf-8")
    return cluster


def run(cluster: Path, assessor_ac=True) -> subprocess.CompletedProcess:
    args = [sys.executable, str(SCRIPT), "--cluster", str(cluster),
            "--unit", "ICTTEST101=units_of_competency/ICTTEST101.md",
            "--unit", "ICTTEST202=units_of_competency/ICTTEST202.md"]
    if assessor_ac:
        args.append("--assessor-ac")
    return subprocess.run(args, capture_output=True, text=True)


def without(tag: str) -> list[str]:
    """The item list with the item carrying `tag` removed."""
    return [i for i in ITEMS if f"[{tag}]" not in i]


def replace(tag: str, new_line: str) -> list[str]:
    return [new_line if f"[{tag}]" in i else i for i in ITEMS]


# ---------------------------------------------------------------------------
# Baseline
# ---------------------------------------------------------------------------

def test_a_faithful_consolidation_passes(tmp_path):
    """If this fails, every FAIL-side test below proves nothing."""
    r = run(build(tmp_path))
    assert r.returncode == 0, r.stdout


def test_editorial_prose_is_not_treated_as_items(tmp_path):
    """Topic headings, rationale and status notes appear in no unit and must not be UNEXPECTED."""
    r = run(build(tmp_path))
    assert "UNEXPECTED" not in r.stdout, r.stdout


def test_backticked_example_tags_in_the_preamble_are_not_items(tmp_path):
    """The preamble cites two real tags inside code spans; they must not count as occurrences."""
    r = run(build(tmp_path))
    assert "DUPLICATED" not in r.stdout, r.stdout


def test_an_editorial_bullet_citing_a_tag_is_not_an_item(tmp_path):
    """Editorial bullets cite tags in backticks — an AT summary, a grouping note.

    They are prose about an item, not the item, and their text is not the unit's text. Reading
    one as an item line makes it the register's entry for that tag, and the real item becomes a
    duplicate of itself. It is placed BEFORE the items here so it would win if it were counted.
    """
    doc = (PREAMBLE
           + "- **AT1 — Design** — evidences `[ICTTEST101 PC 1.1]` and `[ICTTEST101 PE 1]`.\n\n"
           + "\n".join(ITEMS) + "\n")
    r = run(build(tmp_path, doc))
    assert r.returncode == 0, r.stdout


# ---------------------------------------------------------------------------
# MISSING — nothing lost
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tag", ["ICTTEST101 PC 1.2", "ICTTEST101 FS Oral communication",
                                 "ICTTEST101 PE 2", "ICTTEST101 KE 1", "ICTTEST101 AC 1"])
def test_a_dropped_item_is_missing(tmp_path, tag):
    """One item lost from each section — each is a different parse path."""
    r = run(build(tmp_path, consolidated(without(tag))))
    assert r.returncode == 1
    assert "MISSING" in r.stdout and tag in r.stdout


def test_a_dropped_unit_is_missing(tmp_path):
    """A whole unit left out of the consolidation."""
    r = run(build(tmp_path, consolidated([i for i in ITEMS if "ICTTEST202" not in i])))
    assert r.returncode == 1
    assert r.stdout.count("ICTTEST202") >= 6


def test_the_assessor_paragraph_is_required_when_the_flag_is_set(tmp_path):
    r = run(build(tmp_path, consolidated(without("ICTTEST101 AC 2"))))
    assert r.returncode == 1 and "ICTTEST101 AC 2" in r.stdout


def test_a_backticked_item_tag_does_not_count_as_present(tmp_path):
    """Tags only count unwrapped — a code-spanned item tag must read as MISSING, not present."""
    doc = consolidated(replace("ICTTEST101 PE 1", "- configure two cloud services `[ICTTEST101 PE 1]`"))
    r = run(build(tmp_path, doc))
    assert r.returncode == 1 and "ICTTEST101 PE 1" in r.stdout


def test_an_empty_consolidation_is_not_a_pass(tmp_path):
    r = run(build(tmp_path, PREAMBLE))
    assert r.returncode == 1 and "MISSING" in r.stdout


# ---------------------------------------------------------------------------
# UNEXPECTED — nothing invented
# ---------------------------------------------------------------------------

def test_a_phantom_item_number_is_unexpected(tmp_path):
    r = run(build(tmp_path, consolidated(ITEMS + ["- invented criterion [ICTTEST101 PC 9.9]"])))
    assert r.returncode == 1 and "UNEXPECTED" in r.stdout and "PC 9.9" in r.stdout


def test_an_item_from_a_unit_outside_the_cluster_is_unexpected(tmp_path):
    r = run(build(tmp_path, consolidated(ITEMS + ["- borrowed item [ICTCLD999 KE 1]"])))
    assert r.returncode == 1 and "UNEXPECTED" in r.stdout


# ---------------------------------------------------------------------------
# DUPLICATED — exactly once
# ---------------------------------------------------------------------------

def test_the_same_item_in_two_groups_is_duplicated(tmp_path):
    doc = consolidated(ITEMS + ["\n## Group 2 — Also relevant\n",
                                "- configure two cloud services [ICTTEST101 PE 1]"])
    r = run(build(tmp_path, doc))
    assert r.returncode == 1 and "DUPLICATED" in r.stdout


# ---------------------------------------------------------------------------
# MISTRANSCRIBED — the item's text is the source's text
# ---------------------------------------------------------------------------

def test_a_reworded_item_fails(tmp_path):
    """Present, exactly once, correctly tagged — and no longer what the unit says."""
    doc = consolidated(replace("ICTTEST101 PC 1.1",
                               "- 1.1 Check the client's cloud requirements [ICTTEST101 PC 1.1]"))
    r = run(build(tmp_path, doc))
    assert r.returncode == 1, r.stdout
    assert "ICTTEST101 PC 1.1" in r.stdout


def test_a_truncated_item_fails(tmp_path):
    doc = consolidated(replace("ICTTEST101 PC 1.1", "- 1.1 Confirm cloud service [ICTTEST101 PC 1.1]"))
    r = run(build(tmp_path, doc))
    assert r.returncode == 1, r.stdout


def test_dropped_sub_bullets_fail(tmp_path):
    """The defect found in CL1: the parent kept, its children dropped, the item left on a colon."""
    doc = consolidated(replace("ICTTEST101 KE 2",
                               "- functions and differences of cloud models, including: [ICTTEST101 KE 2]"))
    r = run(build(tmp_path, doc))
    assert r.returncode == 1, r.stdout
    assert "ICTTEST101 KE 2" in r.stdout


def test_swapped_tags_fail(tmp_path):
    """Both items present, both exactly once — each carrying the other's tag.

    Tag presence alone reports a clean sweep, which is why identity has to be checked.
    """
    doc = consolidated([
        "- configure two cloud services [ICTTEST101 PE 2]" if "[ICTTEST101 PE 1]" in i else
        "- document the configuration [ICTTEST101 PE 1]" if "[ICTTEST101 PE 2]" in i else i
        for i in ITEMS])
    r = run(build(tmp_path, doc))
    assert r.returncode == 1, r.stdout
    # Nothing is missing, extra or doubled — only the pairing is wrong.
    for label in ("MISSING", "UNEXPECTED", "DUPLICATED"):
        assert label not in r.stdout, r.stdout


def test_a_cosmetic_difference_in_item_text_passes(tmp_path):
    """A smart apostrophe or en dash is Word's, not the author's — not a mistranscription."""
    unit = UNIT_A.replace("- configure two cloud services", "- configure the business’s two services")
    doc = consolidated(replace("ICTTEST101 PE 1", "- configure the business's two services [ICTTEST101 PE 1]"))
    r = run(build(tmp_path, doc, unit_a=unit))
    assert r.returncode == 0, r.stdout


# ---------------------------------------------------------------------------
# Grouping-invariance — the judgement layer must not affect the verdict
# ---------------------------------------------------------------------------

def test_regrouping_the_items_does_not_change_the_verdict(tmp_path):
    """Items reordered and split across topics: the same register, differently arranged."""
    shuffled = list(reversed(ITEMS))
    doc = PREAMBLE + "\n".join(shuffled[:5]) + "\n\n## Group 2 — Monitoring\n\n" + "\n".join(shuffled[5:]) + "\n"
    r = run(build(tmp_path, doc))
    assert r.returncode == 0, r.stdout


def test_renaming_topic_headings_does_not_change_the_verdict(tmp_path):
    doc = consolidated().replace("Group 1 — Preparing and configuring", "Topic 4 — Something else entirely")
    r = run(build(tmp_path, doc))
    assert r.returncode == 0, r.stdout


# ---------------------------------------------------------------------------
# Harness
# ---------------------------------------------------------------------------

def test_all_three_classes_are_reported_in_one_run(tmp_path):
    """A run must not stop at the first class — the human fixes the whole document at once."""
    items = without("ICTTEST101 PE 2") + ["- invented [ICTTEST101 PC 9.9]",
                                          "- industry standards used in cloud computing [ICTTEST101 KE 1]"]
    r = run(build(tmp_path, consolidated(items)))
    assert r.returncode == 1
    for label in ("MISSING", "UNEXPECTED", "DUPLICATED"):
        assert label in r.stdout, r.stdout


def test_a_missing_consolidated_file_is_an_error_not_a_pass(tmp_path):
    cluster = build(tmp_path)
    (cluster / "consolidated_uoc.md").unlink()
    assert run(cluster).returncode != 0


def test_a_unit_with_a_renamed_section_is_reported_as_an_error(tmp_path):
    """The expected set must never shrink silently — see inventory_uoc's section check.

    It must surface as an ERROR naming the section, not as a pile of phantom UNEXPECTED tags:
    the message is what tells the human the unit .md is at fault rather than the consolidation.
    """
    r = run(build(tmp_path, unit_a=UNIT_A.replace("# Knowledge Evidence", "# Knowledge evidence")))
    assert r.returncode == 2, r.stdout
    assert "ERROR" in r.stderr and "Knowledge Evidence" in r.stderr


def test_assessor_ac_off_does_not_expect_the_trailing_paragraph(tmp_path):
    doc = consolidated([i for i in ITEMS if "AC 2]" not in i])
    r = run(build(tmp_path, doc), assessor_ac=False)
    assert r.returncode == 0, r.stdout
