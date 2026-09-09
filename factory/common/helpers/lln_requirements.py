"""Deriving a cluster's LLN requirements from its units' Foundation Skills.

USE THIS WHEN a document needs the language, literacy and numeracy demands a cluster places on
learners -- the institutional delivery plan has such a section. The demands are already written, in
the units of competency themselves, so this reads them rather than asking anyone to compose them.

**Only the LLN-relevant Foundation Skills count.** A unit's Foundation Skills also cover planning and
organising, problem solving, self-management and the like: real skills, but not language, literacy or
numeracy, and including them would overstate what the section is claiming.

Amalgamates across however many units the cluster has, de-duplicating: units routinely declare the
same demand in identical words, and a compliance document should say it once. Source-unit tags are
stripped -- they are traceability for us, not content for the reader.

Cross-process by nature: the source is extraction's ``consolidated_uoc.md``, the consumer is a
delivery document. That is why it lives in ``common/`` rather than in either step.

Cases: HLLN-01 .. HLLN-11 in factory/docs/test-plan.md.
"""
from __future__ import annotations

import re

# A Foundation Skill bullet: "- **<Skill>** — <demand> [UNIT FS <Skill>]"
_FS_BULLET = re.compile(r"^-\s+\*\*([^*]+?)\*\*\s+[—-]\s+(.+)$", re.MULTILINE)

# Trailing traceability tag on a demand.
_SOURCE_TAG = re.compile(r"\s*\[[A-Z]{3}[A-Z0-9]*\s+FS\b[^\]]*\]\s*$")

# The consolidated UoC joins several demands within one bullet using a literal <br>.
_SUBDEMAND = re.compile(r"\s*<br\s*/?>\s*", re.IGNORECASE)

# Any other markup that survived transcription. It is a source artefact, never content: a compliance
# document showing a literal tag is a visible defect, so strip whatever the source happens to carry.
_MARKUP = re.compile(r"<[^>]*>")

# The LLN-relevant Foundation Skills, as the institution's headings. Anything not named here is a
# Foundation Skill but not an LLN demand, and is deliberately dropped.
_HEADINGS = {
    "Oral communication": "Language / Oral communication",
    "Reading": "Literacy — Reading",
    "Writing": "Literacy — Writing",
    "Numeracy": "Numeracy",
}

# Emission order, following the institution's own sequence.
_ORDER = ["Language / Oral communication", "Literacy — Reading", "Literacy — Writing", "Numeracy"]


def collect(consolidated_text: str) -> dict[str, list[str]]:
    """LLN demands grouped by heading, in the institution's order.

    De-duplicated within a heading and stripped of source-unit tags. A bullet joining several demands
    with ``<br>`` is split -- each is a separate demand and reads as one in a document -- and any other
    markup the source carries is stripped. A heading with
    no demands is omitted rather than emitted empty: the cluster genuinely places no such demand.
    """
    found: dict[str, list[str]] = {}
    for skill, demand in _FS_BULLET.findall(consolidated_text):
        heading = _HEADINGS.get(skill.strip())
        if heading is None:
            continue
        bucket = found.setdefault(heading, [])
        for text in _SUBDEMAND.split(_SOURCE_TAG.sub("", demand.strip())):
            text = _MARKUP.sub("", text).strip()
            if text and text not in bucket:
                bucket.append(text)
    return {h: found[h] for h in _ORDER if h in found}


def render(sections: dict[str, list[str]]) -> str:
    """The collected demands as headed bullet lists, ready to place in a document."""
    out = []
    for heading, items in sections.items():
        out.append(heading)
        out.extend(f"- {item}" for item in items)
        out.append("")
    return "\n".join(out).strip()
