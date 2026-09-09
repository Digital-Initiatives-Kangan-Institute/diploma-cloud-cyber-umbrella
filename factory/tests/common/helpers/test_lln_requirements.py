"""Cases HLLN-01 .. HLLN-11 — factory/docs/test-plan.md.

Covers common/helpers/lln_requirements.py: deriving a cluster's LLN section from the Foundation
Skills its units declare.
"""
import lln_requirements as LLN

CONSOLIDATED = """\
# S1-CL9 Test Cluster — Consolidated UoC

## Foundation skills

- **Reading** — Interprets complex technical and operational documentation to determine and confirm job requirements [ICTCLD501 FS Reading]
- **Reading** — Interprets complex technical and operational documentation to determine and confirm job requirements [ICTCLD503 FS Reading]
- **Reading** — Analyses and consolidates information from a range of sources [ICTCLD505 FS Reading]
- **Writing** — Develops complex documentation in required formats using clear and detailed language [ICTCLD503 FS Writing]
- **Oral communication** — Uses listening and questioning techniques to articulate complex concepts [ICTCLD501 FS Oral communication]
- **Numeracy** — Performs calculations to assess the financial implications of a proposed change [ICTCLD501 FS Numeracy]
- **Planning and organising** — Uses a broad range of strategies to evaluate and resolve risk events [ICTCLD501 FS Planning and organising]
- **Problem solving** — Uses a mix of intuitive and formal processes to identify key information [ICTCLD503 FS Problem solving]
- **Self-management** — Demonstrates a sophisticated knowledge of principles and practices [ICTCLD505 FS Self-management]
"""


def collected():
    return LLN.collect(CONSOLIDATED)


# --- what is collected (HLLN-01 .. HLLN-04) -------------------------------

def test_reading_is_collected():
    """HLLN-01"""
    assert any("Interprets complex technical" in i for i in collected()["Literacy — Reading"])


def test_oral_communication_is_collected():
    """HLLN-02"""
    assert any("listening and questioning" in i
               for i in collected()["Language / Oral communication"])


def test_writing_is_collected():
    """HLLN-03"""
    assert any("Develops complex documentation" in i for i in collected()["Literacy — Writing"])


def test_numeracy_is_collected():
    """HLLN-04"""
    assert any("financial implications" in i for i in collected()["Numeracy"])


# --- what is excluded (HLLN-05, HLLN-06) ----------------------------------

def test_planning_and_organising_is_excluded():
    """HLLN-05 — a Foundation Skill, but not a language, literacy or numeracy demand."""
    assert not any("resolve risk events" in i for items in collected().values() for i in items)


def test_problem_solving_and_self_management_are_excluded():
    """HLLN-06"""
    joined = " ".join(i for items in collected().values() for i in items)
    assert "intuitive and formal processes" not in joined
    assert "sophisticated knowledge of principles" not in joined


# --- amalgamation across units (HLLN-07 .. HLLN-09) -----------------------

def test_skills_from_every_unit_are_amalgamated():
    """HLLN-07 — Reading appears in three units; both distinct demands must survive."""
    reading = collected()["Literacy — Reading"]
    assert any("Interprets complex" in i for i in reading)
    assert any("Analyses and consolidates" in i for i in reading)


def test_item_repeated_across_units_is_listed_once():
    """HLLN-08 — 501 and 503 declare the same Reading demand verbatim."""
    reading = collected()["Literacy — Reading"]
    assert sum("Interprets complex technical" in i for i in reading) == 1


def test_source_unit_tag_is_stripped():
    """HLLN-09 — the tag is traceability for us, not content for a compliance document."""
    assert not any("FS Reading]" in i for i in collected()["Literacy — Reading"])


# --- shape of the result (HLLN-10, HLLN-11) -------------------------------

def test_headings_are_ordered_and_empty_ones_omitted():
    """HLLN-10"""
    assert list(collected()) == [
        "Language / Oral communication", "Literacy — Reading", "Literacy — Writing", "Numeracy",
    ]
    assert "Numeracy" not in LLN.collect("- **Reading** — Something [ICTCLD501 FS Reading]")


def test_rendering_produces_one_bullet_per_item():
    """HLLN-11"""
    sections = collected()
    text = LLN.render(sections)
    assert "Literacy — Reading" in text
    assert text.count("\n- ") + text.startswith("- ") == sum(len(v) for v in sections.values())


def test_br_joined_demands_become_separate_items():
    """HLLN-12 — the consolidated UoC joins sub-demands with <br>; each is its own demand."""
    got = LLN.collect(
        "- **Writing** — Develops complex documentation<br>Writes and edits code "
        "[ICTCLD503 FS Writing]"
    )
    items = got["Literacy — Writing"]
    assert items == ["Develops complex documentation", "Writes and edits code"]


def test_no_markup_survives_into_a_demand():
    """HLLN-13 — <br> was the tag that bit us; this guards against the next one.

    Markup in the source is a transcription artefact, not content. A compliance document showing a
    literal tag is a visible defect, so nothing angle-bracketed may reach a collected demand.
    """
    got = LLN.collect(
        "- **Reading** — First demand<br>Second demand [ICTCLD501 FS Reading]\n"
        "- **Writing** — Uses <em>clear</em> language<br/>And correct syntax [ICTCLD503 FS Writing]\n"
    )
    for items in got.values():
        for demand in items:
            assert "<" not in demand and ">" not in demand, demand
