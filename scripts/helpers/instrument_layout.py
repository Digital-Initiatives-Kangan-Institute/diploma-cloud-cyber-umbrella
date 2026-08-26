"""Readability layout for Kangan assessment instruments (.docx).

The instrument generators hold their content as flat lists of strings/tuples. These helpers
turn that flat content into something a person can navigate — real headings, bold labels,
bulleted lists, spacing, and clickable links into the scenario site — without the content
itself carrying formatting.

Three entry points:
  ``render_prose``      — the shared Instructions-to-Student prose (student + assessor copies)
  ``set_cell_rich``     — an instruction-table cell built from ``(text, kind)`` blocks
  ``render_benchmark``  — the assessor-only benchmark body, whose shape is inferred from the text

plus ``add_hyperlink``, which python-docx has no native support for.
"""
import re

from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

BODY = "Assessor text"  # the Kangan body style both instrument templates carry
MUTED = RGBColor(0x59, 0x59, 0x59)
LINK_BLUE = "0563C1"


def add_hyperlink(paragraph, text, url, colour=LINK_BLUE, size_pt=None):
    """Append a clickable hyperlink run to ``paragraph``."""
    r_id = paragraph.part.relate_to(url, RT.HYPERLINK, is_external=True)
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    props = OxmlElement("w:rPr")
    if size_pt is not None:
        sz = OxmlElement("w:sz")
        sz.set(qn("w:val"), str(int(size_pt * 2)))
        props.append(sz)
    colour_el = OxmlElement("w:color")
    colour_el.set(qn("w:val"), colour)
    props.append(colour_el)
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    props.append(underline)
    run.append(props)
    t = OxmlElement("w:t")
    t.text = text
    run.append(t)
    link.append(run)
    paragraph._p.append(link)
    return paragraph


def _bulleted(doc, indent=18, space_after=6):
    p = doc.add_paragraph(style=BODY)
    p.paragraph_format.left_indent = Pt(indent)
    p.paragraph_format.space_after = Pt(space_after)
    return p


def render_prose(doc, prose):
    """Render Instructions-to-Student prose from ``(text, style)`` pairs.

    Style tags beyond the Word style names:
      'item'       — a list entry whose lead-in (up to the first ' — ') is bolded
      'bullet'     — a plain list entry
      'link|<url>' — a list entry whose text is a clickable link to <url>
    """
    for text, style in prose:
        if style.startswith("link|"):
            p = _bulleted(doc, space_after=8)
            p.add_run("• ")
            add_hyperlink(p, text, style.split("|", 1)[1])
        elif style in ("item", "bullet"):
            p = _bulleted(doc)
            lead, sep, rest = text.partition(" — ") if style == "item" else ("", "", text)
            if style == "item" and sep:
                p.add_run("• ")
                p.add_run(lead).bold = True
                p.add_run(sep + rest)
            else:
                p.add_run("• " + (rest or text))
        else:
            p = doc.add_paragraph(text, style=style)
            if style.startswith("Heading"):
                p.paragraph_format.space_before = Pt(12)
                p.paragraph_format.space_after = Pt(4)
            else:
                p.paragraph_format.space_after = Pt(8)


def set_cell_rich(cell, blocks):
    """Fill an instruction-table cell from ``(text, kind)`` blocks, spaced so a long cell reads.

    Kinds: 'p' a paragraph · 'h' a bold sub-heading · 'b' a bulleted entry ·
    'link|<url>' a bulleted clickable link.
    """
    for p in cell.paragraphs[1:]:
        p._element.getparent().remove(p._element)
    first = cell.paragraphs[0]
    for r in list(first.runs):
        r._element.getparent().remove(r._element)
    style = first.style
    for i, (text, kind) in enumerate(blocks):
        p = first if i == 0 else cell.add_paragraph()
        p.style = style
        p.paragraph_format.space_after = Pt(4 if kind != "p" else 8)
        if kind == "h":
            p.paragraph_format.space_before = Pt(8)
            p.add_run(text).bold = True
        elif kind.startswith("link|"):
            p.paragraph_format.left_indent = Pt(14)
            p.add_run("• ")
            add_hyperlink(p, text, kind.split("|", 1)[1])
        elif kind == "b":
            p.paragraph_format.left_indent = Pt(14)
            p.add_run("• " + text)
        else:
            p.add_run(text)


def render_benchmark(doc, blocks, render_table, styles):
    """Render an assessor-only benchmark body, inferring structure from the text itself.

    ``blocks`` are ``(kind, payload)`` where kind is 'tbl' (payload = rows) or a key in
    ``styles``. Plain-text blocks are classified:
      '3. Marking §3 …'    → Heading 2 (a criterion)
      '7.1 Benchmark …'    → Heading 3 (a sub-part)
      'UoC evidenced: …'   → a muted italic attribution line
      'NYS: …' inline      → bold lead-in, plain remainder
      a line ending in ':' → a bold label; what follows becomes bulleted
    """
    bullets = False
    for kind, payload in blocks:
        if kind == "tbl":
            render_table(doc, payload)
            bullets = False
            continue
        if kind != "p":
            p = doc.add_paragraph(payload, style=styles[kind])
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(6)
            bullets = False
            continue

        text = payload
        if re.match(r"^\d+\.\s", text):
            p = doc.add_paragraph(text, style="Heading 2")
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            bullets = False
        elif re.match(r"^\d+\.\d+\s", text):
            p = doc.add_paragraph(text, style="Heading 3")
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            bullets = False
        elif text.startswith("UoC evidenced:"):
            p = doc.add_paragraph(style=BODY)
            run = p.add_run(text)
            run.italic = True
            run.font.color.rgb = MUTED
            run.font.size = Pt(9)
            p.paragraph_format.space_after = Pt(8)
            bullets = False
        elif text.startswith("Note:"):
            p = doc.add_paragraph(style=BODY)
            p.add_run(text).italic = True
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(8)
            bullets = False
        elif text.startswith("NYS: "):
            p = doc.add_paragraph(style=BODY)
            p.add_run("NYS: ").bold = True
            p.add_run(text[5:])
            p.paragraph_format.space_after = Pt(8)
            bullets = False
        elif text.endswith(":"):
            p = doc.add_paragraph(style=BODY)
            p.add_run(text).bold = True
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(4)
            bullets = True
        elif bullets:
            _bulleted(doc, space_after=4).add_run("• " + text)
        else:
            p = doc.add_paragraph(text, style=BODY)
            p.paragraph_format.space_after = Pt(8)


def render_flat_prose(doc, lines, headings):
    """Render instruction prose held as a flat list of strings.

    ``headings`` maps a heading line to whether the block under it is a bulleted list
    (True) or paragraphs (False). Beyond that the shape is inferred:
      '§4 …' / 'Appendix B — …'  → a bold-lead list entry
      a line ending in ':'        → a bold label; what follows becomes bulleted
      ('text', 'link|<url>')      → a clickable link entry
    """
    bullets = False
    for line in lines:
        if isinstance(line, tuple):
            text, kind = line
            p = _bulleted(doc, space_after=8)
            p.add_run("• ")
            add_hyperlink(p, text, kind.split("|", 1)[1])
            continue
        if line in headings:
            p = doc.add_paragraph(line, style="Heading 2")
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            bullets = headings[line]
        elif line.startswith("§") or line.startswith("Appendix "):
            p = _bulleted(doc)
            lead, sep, rest = line.partition(" ")
            p.add_run("• ")
            p.add_run(lead).bold = True
            p.add_run(sep + rest)
            bullets = False
        elif line.endswith(":"):
            p = doc.add_paragraph(style=BODY)
            p.add_run(line).bold = True
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(4)
            bullets = True
        elif bullets:
            _bulleted(doc).add_run("• " + line)
        else:
            p = doc.add_paragraph(line, style=BODY)
            p.paragraph_format.space_after = Pt(8)
