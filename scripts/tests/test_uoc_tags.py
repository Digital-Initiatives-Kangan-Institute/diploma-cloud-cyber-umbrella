"""Tests for helpers.uoc_tags."""
import pathlib
import sys

sys.path.insert(0, str(next(
    d for d in pathlib.Path(__file__).resolve().parents
    if (d / "helpers" / "__init__.py").exists()
)))

from docx import Document  # noqa: E402
from docx.shared import Pt  # noqa: E402

from helpers.uoc_tags import add_uoc_evidence_tag, UOC_TAG_FONT_SIZE_PT  # noqa: E402
from brand import TEAL  # noqa: E402


def test_evidence_tag_prefixes_text():
    p = add_uoc_evidence_tag(Document(), "[ICTCLD401 PC 4.3]")
    assert p.runs[0].text == "Evidences: [ICTCLD401 PC 4.3]"


def test_evidence_tag_is_small_italic_teal():
    run = add_uoc_evidence_tag(Document(), "x").runs[0]
    assert run.italic is True
    assert run.font.size == Pt(UOC_TAG_FONT_SIZE_PT)
    assert str(run.font.color.rgb) == TEAL
