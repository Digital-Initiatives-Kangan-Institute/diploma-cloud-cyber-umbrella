"""Cases HUS-01 .. HUS-16 — factory/docs/test-plan.md.

Covers common/helpers/uoc_sections.py: which UoC sections a Topic teaches, in the institutional
Delivery Mapping vocabulary.
"""
import uoc_sections as US

COVERAGE = """\
# Topic 03 — DR: requirements & impact analysis · Coverage

**Topic 03 of 9** · **AT1 content Topic**

Some intro prose mentioning [ICTCLD501 PC 1.1] which must NOT count — it is before the mapping heading.

### UoC mapping — taught / developed

| Component | Teaches |
|---|---|
| C1 | [ICTCLD501 PC 1.1] |
| C2 | [ICTCLD501 KE 2] and [ICTCLD503 PE 1] |
| C3 | [ICTCLD501 PC 1.2] |
| C4 | a component with no tag at all |
| C5 | a `[ICTCLD505 AC 1]` wrapped tag, which is not the canonical form |
| C6 | a malformed [bracket with no unit] |

## 4. Next section

| Component | Teaches |
|---|---|
| C9 | [ICTCLD505 AC 1] |
"""

TRUNCATED = """\
### UoC mapping — taught / developed

| C1 | [ICTCLD501 PC 1.1] |
Items applied earlier in the cluster:
| C2 | [ICTCLD501 KE 2] |
"""


# --- taught_block (HUS-01 .. HUS-04) --------------------------------------

def test_block_runs_from_mapping_heading_to_next_h2():
    """HUS-01"""
    block = US.taught_block(COVERAGE)
    assert "ICTCLD501 PC 1.1" in block
    assert "Next section" not in block


def test_applied_earlier_marker_truncates_the_block():
    """HUS-02"""
    block = US.taught_block(TRUNCATED)
    assert "PC 1.1" in block
    assert "KE 2" not in block


def test_content_before_the_mapping_heading_is_excluded():
    """HUS-03"""
    block = US.taught_block(COVERAGE)
    assert "must NOT count" not in block


def test_absent_mapping_heading_yields_an_empty_block():
    """HUS-04"""
    assert US.taught_block("# A topic\n\nNo mapping heading here.\n") == ""


# --- sections_taught (HUS-05 .. HUS-10) -----------------------------------

def test_section_is_collected_from_a_canonical_tag():
    """HUS-05"""
    assert "PC" in US.sections_taught(COVERAGE)


def test_wrapped_tag_is_not_counted():
    """HUS-06 — the canonical form is unwrapped; a backticked tag is a formatting defect."""
    assert "AC" not in US.sections_taught(COVERAGE)


def test_repeated_section_is_reported_once():
    """HUS-07 — PC appears twice in the block."""
    assert sorted(US.sections_taught(COVERAGE)).count("PC") == 1


def test_tags_outside_the_taught_block_are_not_counted():
    """HUS-08 — the '## 4. Next section' table carries an AC tag that must not leak in."""
    assert "AC" not in US.sections_taught(COVERAGE)


def test_line_without_a_tag_contributes_nothing():
    """HUS-09"""
    assert US.sections_taught("### UoC mapping\n\n| C1 | no tags here |\n") == set()


def test_malformed_bracket_is_ignored():
    """HUS-10 — '[bracket with no unit]' must not raise or become a section."""
    got = US.sections_taught(COVERAGE)
    assert got <= {"PC", "KE", "PE", "FS", "AC"}


# --- to_delivery_mapping (HUS-11 .. HUS-16) -------------------------------

def test_pc_maps_to_pc():
    """HUS-11"""
    assert US.to_delivery_mapping({"PC"}) == ["PC"]


def test_ke_maps_to_know():
    """HUS-12"""
    assert US.to_delivery_mapping({"KE"}) == ["Know"]


def test_pe_and_fs_both_map_to_skill():
    """HUS-13"""
    assert US.to_delivery_mapping({"PE"}) == ["Skill"]
    assert US.to_delivery_mapping({"FS"}) == ["Skill"]


def test_ac_maps_to_cond():
    """HUS-14"""
    assert US.to_delivery_mapping({"AC"}) == ["Cond"]


def test_result_is_deduplicated_and_stably_ordered():
    """HUS-15 — PE and FS collapse to one 'Skill'; order follows the template's legend."""
    assert US.to_delivery_mapping({"AC", "PE", "PC", "FS", "KE"}) == ["PC", "Know", "Skill", "Cond"]


def test_section_with_no_institutional_equivalent_is_dropped():
    """HUS-16"""
    assert US.to_delivery_mapping({"PC", "ZZ"}) == ["PC"]
