"""Tests for helpers.docx_code."""
import pathlib
import sys

sys.path.insert(0, str(next(
    d for d in pathlib.Path(__file__).resolve().parents
    if (d / "helpers" / "__init__.py").exists()
)))

from docx import Document  # noqa: E402
from docx.shared import Pt  # noqa: E402

from helpers.docx_code import add_code_block, CODE_FONT, CODE_FONT_SIZE_PT  # noqa: E402


def test_one_paragraph_per_line_monospaced():
    paras = add_code_block(Document(), ["line one", "line two", "line three"])
    assert len(paras) == 3
    run = paras[0].runs[0]
    assert run.font.name == CODE_FONT
    assert run.font.size == Pt(CODE_FONT_SIZE_PT)


def test_blank_line_renders_as_space():
    paras = add_code_block(Document(), [""])
    assert paras[0].runs[0].text == " "
