"""Monospaced code / configuration listings for python-docx.

Renders a block of lines as tight monospaced paragraphs (e.g. a CloudFormation
snippet, a webhook contract, a Lambda handler). No brand palette — plain Consolas.
"""
from docx.shared import Pt

#: Monospace font for code listings.
CODE_FONT = "Consolas"
#: Run size (points) for code listings.
CODE_FONT_SIZE_PT = 8.5


def add_code_block(doc, lines):
    """Append each string in ``lines`` as a tight monospaced paragraph.

    Blank lines render as a single space (preserves vertical spacing). Returns the
    created paragraphs.
    """
    paragraphs = []
    for ln in lines:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        r = p.add_run(ln if ln else " ")
        r.font.name = CODE_FONT
        r.font.size = Pt(CODE_FONT_SIZE_PT)
        paragraphs.append(p)
    return paragraphs
