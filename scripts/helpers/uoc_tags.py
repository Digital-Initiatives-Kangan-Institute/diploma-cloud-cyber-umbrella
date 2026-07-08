"""UoC traceability tag for assessor artefacts.

Renders the small italic teal "Evidences: ..." line used in assessor exemplars and
instruments to tie a section to the units of competency it evidences. Assessment
artefacts only — never used in in-world / student-facing documents.
"""
from docx.shared import Pt, RGBColor

from brand import TEAL

#: Run size (points) for the UoC evidence tag.
UOC_TAG_FONT_SIZE_PT = 8.5


def add_uoc_evidence_tag(doc, text):
    """Append an "Evidences: <text>" tag (small italic teal). Returns the paragraph."""
    p = doc.add_paragraph()
    r = p.add_run("Evidences: " + text)
    r.italic = True
    r.font.size = Pt(UOC_TAG_FONT_SIZE_PT)
    r.font.color.rgb = RGBColor.from_string(TEAL)
    p.paragraph_format.space_after = Pt(6)
    return p
