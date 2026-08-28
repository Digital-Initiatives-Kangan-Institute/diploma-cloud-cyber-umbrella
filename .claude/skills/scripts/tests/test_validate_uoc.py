"""Tests for validate_uoc.py — the Gate 1→2 transcription oracle.

The gate's job is to prove a `.md` transcription is verbatim against its source `.docx`. Three
failure modes must be caught: content in the source that is MISSING from the transcription,
content in the transcription that is NOT IN the source, and content that is MISTRANSCRIBED
(changed, renumbered, re-cased, re-ordered, duplicated). It must equally NOT cry wolf on the
things that are legitimately different — markdown syntax, page furniture, whitespace, and the
cosmetic character substitutions Word makes.

**Independence.** Every fixture is built from literal Python strings, and the expected `.md` is
written by hand here — never produced by `transcribe_uoc.py`. That matters: the transcriber and
the validator implement the same Word-XML extraction twice, so a test that fed the transcriber's
own output back in would only prove the two agree with each other. These fixtures are the
independent ground truth.

The fixture builder writes only the zip parts under test (`word/document.xml`, plus header/footer
parts where a test needs them) — enough for a zip-reading extractor, not a Word-openable file.
"""
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate_uoc as V  # noqa: E402

SCRIPT = Path(__file__).resolve().parents[1] / "validate_uoc.py"

DOC_OPEN = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    "<w:body>"
)
DOC_CLOSE = "</w:body></w:document>"


# ---------------------------------------------------------------------------
# Fixture builders — Word XML from literal text
# ---------------------------------------------------------------------------

def _runs(text: str) -> str:
    """Text → run XML. A tab character becomes <w:tab/>, a newline becomes <w:br/>."""
    out = []
    for i, line in enumerate(text.split("\n")):
        if i:
            out.append("<w:br/>")
        for j, chunk in enumerate(line.split("\t")):
            if j:
                out.append("<w:tab/>")
            if chunk:
                out.append(f'<w:t xml:space="preserve">{escape(chunk)}</w:t>')
    return f"<w:r>{''.join(out)}</w:r>"


def p(text: str, style: str | None = None) -> str:
    """A paragraph, optionally carrying a paragraph style."""
    pPr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    return f"<w:p>{pPr}{_runs(text)}</w:p>"


def h(level: int, text: str) -> str:
    return p(text, style=f"Heading{level}")


def bullet(text: str) -> str:
    return p(text, style="ListBullet")


def raw_p(inner: str) -> str:
    """A paragraph whose run XML is supplied verbatim — for elements _runs cannot express."""
    return f"<w:p><w:r>{inner}</w:r></w:p>"


def tbl(rows: list[list[str]]) -> str:
    """A table. A newline inside a cell starts a new paragraph in that cell."""
    out = ["<w:tbl>"]
    for row in rows:
        out.append("<w:tr>")
        for cell in row:
            paras = "".join(p(part) for part in cell.split("\n"))
            out.append(f"<w:tc>{paras}</w:tc>")
        out.append("</w:tr>")
    out.append("</w:tbl>")
    return "".join(out)


def make_docx(tmp_path: Path, blocks: list[str], furniture: bool = False, name="unit.docx") -> Path:
    """Zip the given body blocks into a .docx. `furniture` adds header/footer parts with content."""
    path = tmp_path / name
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("word/document.xml", DOC_OPEN + "".join(blocks) + DOC_CLOSE)
        if furniture:
            for part, text in (
                ("word/header1.xml", "ICTCLD501 Configure cloud services"),
                ("word/footer1.xml", "Approved Page 3 of 5 IT Training Package"),
            ):
                z.writestr(part, DOC_OPEN.replace("w:document", "w:hdr") + p(text) + "</w:body></w:hdr>")
    return path


def verdict(tmp_path: Path, docx: Path, md_text: str) -> str:
    """Run the gate over a pair and reduce it to its verdict: exact | cosmetic | substantive."""
    md = tmp_path / "unit.md"
    md.write_text(md_text, encoding="utf-8")
    f = V.diff_report("fixture", V.docx_to_text(docx), V.md_to_text(md))
    if f["exact_match"]:
        return "exact"
    if f["cosmetic_match"]:
        return "cosmetic"
    return "substantive"


# ---------------------------------------------------------------------------
# A representative source unit + its faithful transcription
# ---------------------------------------------------------------------------

BLOCKS = [
    h(1, "ICTCLD501 Configure cloud services"),
    h(2, "Elements and Performance Criteria"),
    tbl([
        ["Element", "Performance Criteria"],
        ["1. Prepare to configure", "1.1 Confirm cloud service requirements with the client\n"
                                    "1.2 Identify security and access requirements"],
        ["2. Configure services", "2.1 Configure services according to organisational procedures"],
    ]),
    h(2, "Performance Evidence"),
    p("The candidate must demonstrate the ability to complete the tasks outlined in the "
      "elements, performance criteria and knowledge evidence of this unit."),
    bullet("configure two cloud services"),
    bullet("document the configuration"),
    h(2, "Foundation Skills"),
    tbl([
        ["Skill", "Description"],
        ["Oral communication", "Presents information using clear language"],
    ]),
]

MD = """# ICTCLD501 Configure cloud services

## Elements and Performance Criteria

| Element | Performance Criteria |
| --- | --- |
| 1. Prepare to configure | 1.1 Confirm cloud service requirements with the client<br>1.2 Identify security and access requirements |
| 2. Configure services | 2.1 Configure services according to organisational procedures |

## Performance Evidence

The candidate must demonstrate the ability to complete the tasks outlined in the elements, performance criteria and knowledge evidence of this unit.

- configure two cloud services
- document the configuration

## Foundation Skills

| Skill | Description |
| --- | --- |
| Oral communication | Presents information using clear language |
"""


@pytest.fixture
def source(tmp_path):
    return make_docx(tmp_path, BLOCKS)


# ---------------------------------------------------------------------------
# The gate must not cry wolf — legitimate differences pass
# ---------------------------------------------------------------------------

def test_faithful_transcription_is_exact(tmp_path, source):
    """The baseline. If this ever fails, every FAIL-side test below is meaningless."""
    assert verdict(tmp_path, source, MD) == "exact"


def test_page_furniture_is_excluded(tmp_path):
    """Headers/footers carry unit codes and attribution that are deliberately not transcribed.

    They live in separate zip parts, so the gate must never see them as missing content.
    """
    docx = make_docx(tmp_path, BLOCKS, furniture=True)
    assert verdict(tmp_path, docx, MD) == "exact"


def test_tabs_and_line_breaks_are_whitespace(tmp_path):
    """A w:tab between words and a w:br inside a paragraph are structure, not content."""
    docx = make_docx(tmp_path, [p("PC\t1.1\tConfirm requirements"), p("first line\nsecond line")])
    assert verdict(tmp_path, docx, "PC 1.1 Confirm requirements\n\nfirst line<br>second line\n") == "exact"


def test_multi_paragraph_cell_joins_with_br(tmp_path):
    """Two paragraphs in one cell transcribe as `a<br>b` — the same content, not an insertion."""
    docx = make_docx(tmp_path, [tbl([["Element", "PC"], ["1. Prepare", "1.1 Confirm\n1.2 Identify"]])])
    md = "| Element | PC |\n| --- | --- |\n| 1. Prepare | 1.1 Confirm<br>1.2 Identify |\n"
    assert verdict(tmp_path, docx, md) == "exact"


def test_word_cosmetics_pass_as_cosmetic(tmp_path):
    """Smart quotes, en dashes, non-breaking spaces and ellipses are Word's, not the author's."""
    docx = make_docx(tmp_path, [p("The candidate’s work – as scoped – must… continue")])
    assert verdict(tmp_path, docx, "The candidate's work - as scoped - must... continue\n") == "cosmetic"


# ---------------------------------------------------------------------------
# Failure mode 1 — content in the source is MISSING from the transcription
# ---------------------------------------------------------------------------

def test_dropped_word_fails(tmp_path, source):
    assert verdict(tmp_path, source, MD.replace("clear language", "language")) == "substantive"


def test_dropped_negation_fails(tmp_path):
    """The smallest possible omission that inverts an assessment requirement."""
    docx = make_docx(tmp_path, [p("The candidate must not use a pre-built template")])
    assert verdict(tmp_path, docx, "The candidate must use a pre-built template\n") == "substantive"


def test_dropped_bullet_fails(tmp_path, source):
    """A whole PE item lost — the mode that silently reduces what the cluster must assess."""
    assert verdict(tmp_path, source, MD.replace("- document the configuration\n", "")) == "substantive"


def test_dropped_table_cell_fails(tmp_path, source):
    """A PC lost from inside a table cell, where it is easiest to miss by eye."""
    broken = MD.replace("<br>1.2 Identify security and access requirements", "")
    assert verdict(tmp_path, source, broken) == "substantive"


def test_dropped_trailing_section_fails(tmp_path, source):
    """Truncation at the end of the document — the whole Foundation Skills table gone."""
    broken = MD.split("## Foundation Skills")[0]
    assert verdict(tmp_path, source, broken) == "substantive"


# ---------------------------------------------------------------------------
# Failure mode 2 — content in the transcription is NOT IN the source
# ---------------------------------------------------------------------------

def test_added_sentence_fails(tmp_path, source):
    """Invented content is as damaging as lost content: it becomes an item nobody must meet."""
    assert verdict(tmp_path, source, MD + "\nCandidates may resubmit once.\n") == "substantive"


def test_added_bullet_fails(tmp_path, source):
    broken = MD.replace("- document the configuration", "- document the configuration\n- test the configuration")
    assert verdict(tmp_path, source, broken) == "substantive"


def test_added_table_row_fails(tmp_path, source):
    broken = MD.replace(
        "| 2. Configure services | 2.1 Configure services according to organisational procedures |",
        "| 2. Configure services | 2.1 Configure services according to organisational procedures |\n"
        "| 3. Review | 3.1 Review the configuration |",
    )
    assert verdict(tmp_path, source, broken) == "substantive"


def test_duplicated_item_fails(tmp_path, source):
    """Copy-paste during hand-editing: the same PE bullet transcribed twice."""
    broken = MD.replace("- configure two cloud services\n", "- configure two cloud services\n" * 2)
    assert verdict(tmp_path, source, broken) == "substantive"


# ---------------------------------------------------------------------------
# Failure mode 3 — content is MISTRANSCRIBED
# ---------------------------------------------------------------------------

def test_changed_word_fails(tmp_path, source):
    assert verdict(tmp_path, source, MD.replace("Confirm cloud service", "Identify cloud service")) == "substantive"


def test_changed_item_number_fails(tmp_path, source):
    """PC numbering is the identity every downstream UoC tag is built from."""
    assert verdict(tmp_path, source, MD.replace("2.1 Configure", "2.2 Configure")) == "substantive"


def test_changed_quantity_fails(tmp_path, source):
    """`two cloud services` → `three` changes what a candidate must produce."""
    assert verdict(tmp_path, source, MD.replace("configure two cloud", "configure three cloud")) == "substantive"


def test_changed_case_fails(tmp_path, source):
    """Foundation Skills are keyed by the skill name verbatim, case included."""
    assert verdict(tmp_path, source, MD.replace("Oral communication", "Oral Communication")) == "substantive"


def test_reordered_items_fail(tmp_path, source):
    """Order carries meaning here: PE bullets are numbered 1..N in source order downstream."""
    broken = MD.replace(
        "- configure two cloud services\n- document the configuration",
        "- document the configuration\n- configure two cloud services",
    )
    assert verdict(tmp_path, source, broken) == "substantive"


def test_respaced_compound_fails(tmp_path):
    """`IaaS/PaaS/SaaS` retyped as `IaaS / PaaS / SaaS` is a changed token, not whitespace."""
    docx = make_docx(tmp_path, [p("Identify whether the component is IaaS/PaaS/SaaS")])
    assert verdict(tmp_path, docx, "Identify whether the component is IaaS / PaaS / SaaS\n") == "substantive"


# ---------------------------------------------------------------------------
# Blind spots — content-bearing Word elements the extractor must not silently drop
# ---------------------------------------------------------------------------

def test_symbol_character_is_not_lost(tmp_path):
    """A w:sym run carries its character in an attribute, not in w:t.

    The transcriber and the validator share this extraction, so an element neither handles is
    dropped identically on both sides and the diff cancels — a green gate over a transcription
    that is genuinely missing content. The gate must fail loudly instead.
    """
    docx = make_docx(tmp_path, [raw_p(
        '<w:t xml:space="preserve">Deploy </w:t>'
        '<w:sym w:font="Symbol" w:char="F0B3"/>'
        '<w:t xml:space="preserve"> 2 instances</w:t>'
    )])
    assert verdict(tmp_path, docx, "Deploy 2 instances\n") == "substantive"


def test_non_breaking_hyphen_is_not_lost(tmp_path):
    """w:noBreakHyphen is a hyphen. Dropping it silently welds two words together."""
    docx = make_docx(tmp_path, [raw_p(
        '<w:t>e</w:t><w:noBreakHyphen/><w:t>learning</w:t>'
    )])
    assert verdict(tmp_path, docx, "elearning\n") == "substantive"


def test_non_breaking_hyphen_transcribed_as_hyphen_is_cosmetic(tmp_path):
    """...but transcribing it as a plain hyphen is the right answer, and must pass."""
    docx = make_docx(tmp_path, [raw_p(
        '<w:t>e</w:t><w:noBreakHyphen/><w:t>learning</w:t>'
    )])
    assert verdict(tmp_path, docx, "e-learning\n") == "cosmetic"


def test_carriage_return_separates_words(tmp_path):
    """w:cr is a line break like w:br. Dropping it welds the words either side together."""
    docx = make_docx(tmp_path, [raw_p('<w:t>first line</w:t><w:cr/><w:t>second line</w:t>')])
    assert verdict(tmp_path, docx, "first line<br>second line\n") == "exact"


def test_empty_source_is_not_a_pass(tmp_path):
    """A source with no extractable words cannot evidence anything.

    An unreadable body, a wrong file, or an extractor that silently returned nothing would
    otherwise agree with an empty `.md` and report a verbatim match over zero content.
    """
    docx = make_docx(tmp_path, [])
    assert verdict(tmp_path, docx, "") == "substantive"


# ---------------------------------------------------------------------------
# Scope boundary — what this gate does NOT prove
# ---------------------------------------------------------------------------

def test_gate_is_structure_blind(tmp_path, source):
    """Documented boundary, not an endorsement: the diff is over words, so structure is invisible.

    A PE bullet transcribed as a plain paragraph keeps the same word sequence and passes here.
    Bullet identity is what step 2's inventory counts, so proving structure belongs to Gate 2→3 —
    which must not assume this gate covered it.
    """
    flattened = MD.replace(
        "- configure two cloud services\n- document the configuration",
        "configure two cloud services document the configuration",
    )
    assert verdict(tmp_path, source, flattened) == "exact"


# ---------------------------------------------------------------------------
# Harness — exit codes are the gate's actual verdict when run from the run-sheet
# ---------------------------------------------------------------------------

def run_cli(*args) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)


def test_cli_exits_zero_on_a_faithful_pair(tmp_path, source):
    md = tmp_path / "unit.md"
    md.write_text(MD, encoding="utf-8")
    r = run_cli(source, md)
    assert r.returncode == 0, r.stdout + r.stderr


def test_cli_exits_one_on_a_substantive_diff(tmp_path, source):
    md = tmp_path / "unit.md"
    md.write_text(MD.replace("- document the configuration\n", ""), encoding="utf-8")
    assert run_cli(source, md).returncode == 1


def test_cli_exits_zero_on_cosmetic_only(tmp_path):
    docx = make_docx(tmp_path, [p("The candidate’s work – as scoped")])
    md = tmp_path / "unit.md"
    md.write_text("The candidate's work - as scoped\n", encoding="utf-8")
    assert run_cli(docx, md).returncode == 0


def test_cli_rejects_an_unpaired_argument(tmp_path, source):
    """Pairs are positional, so a forgotten `.md` must be an error, never a silent skip."""
    assert run_cli(source).returncode == 2


def test_cli_reports_every_pair_before_failing(tmp_path, source):
    """One bad pair must not mask the pairs after it — the run-sheet validates a whole cluster."""
    bad = tmp_path / "bad.md"
    bad.write_text(MD.replace("- document the configuration\n", ""), encoding="utf-8")
    good = tmp_path / "good.md"
    good.write_text(MD, encoding="utf-8")
    r = run_cli(source, bad, source, good)
    assert r.returncode == 1
    assert r.stdout.count("RESULT:") == 2, r.stdout
