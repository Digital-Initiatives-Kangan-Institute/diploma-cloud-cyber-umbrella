#!/usr/bin/env python3
"""Validate a Topic's slide_plan.md — the gate before the deck is built.

Deterministic, stdlib-only. The slide plan is the kept, validated source the deck is built from;
this checks it conforms to the format AND covers what its sibling coverage.md requires.

FORMAT:
  - header (# ... Slide plan + '> **Covers:**') and a '## Slides' section present;
  - every '### C<n>' component section carries a non-empty 'Teaches:' line;
  - every slide carries a recognised [<TYPE>] tag and a mandatory 'image:' field whose value is one of
    none / reuse / diagram / gen / placeholder.

RENDER SAFETY (mirrors build_topic_deck.py's line grammar — both found only at the visual pass on CL1):
  - no wrapped/stray line inside a slide block: a line that is not a bullet, a field, a table row or
    notes-block content is rendered as its own level-0 bullet, splitting a sentence mid-clause.
    Every bullet goes on ONE line, however long;
  - no markdown in rendered text (titles, kickers, bullets): the deck engine has no markdown support,
    so `**bold**`, `*italic*` and `backticks` come out literally. Plain text only.

BACKWARDS COVERAGE (vs the sibling coverage.md):
  - every component coverage.md declares has a '### C<n>' section;
  - the union of the slide plan's 'Teaches:' tags covers every UoC item coverage.md teaches
    (MISSING otherwise); no Teaches tag is a phantom (PHANTOM); a Teaches tag the topic spec does
    not claim is reported EXTRA (advisory).

Uses the SAME tag machinery as the assessment validators (valid_tag_set / resolve_tags) and the same
taught-table reader as validate_delivery_coverage, so a tag counts here exactly as anywhere else.

Usage:  validate_slide_plan.py --plan <topic_NN>/slide_plan.md   (coverage.md auto-found alongside)
Exit 0 = PASS.
"""
# --- FACTORY MIGRATION NOTE --------------------------------------------------
# Before migrating this script into factory/, CHECK factory/common/helpers/ and
# prefer what is there over writing your own. Relevant to this file:
#   md_table        - markdown tables: split_row / is_separator / rows_under_heading.
#                     Rows keep their source line number so a failure can cite a line.
#   uoc_sections    - which UoC SECTIONS a Topic teaches (PC/KE/PE/FS/AC), plus
#                     taught_block(). Section presence only - NOT item enumeration.
#
# Enumerating individual UoC items - expanding ranges, abbreviated tags inheriting a
# unit, compound tags - already has ONE home: validate_at_traceability.resolve_tags.
# uoc_sections deliberately does not repeat it. Use resolve_tags; do not fork it.
# Every helper is covered by cases in factory/docs/test-plan.md. If one is wrong,
# fix it there and add the case - never fork a local copy.
# -----------------------------------------------------------------------------

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_at_traceability import valid_tag_set, resolve_tags
from validate_delivery_coverage import taught_block

TYPES = {"PRIMER", "BESPOKE", "AWS", "DEMO", "EX", "TABLE", "TAKEAWAYS", "TITLE", "DIVIDER"}
IMG_KEYWORDS = {"none", "reuse", "diagram", "gen", "placeholder"}
SLIDE_LINE = re.compile(r"^\s*-\s*\**\s*`?\s*\[([^\]]+)\]")   # - **`[TYPE ...]`** title
TEACHES_LINE = re.compile(r"^\s*-?\s*Teaches:\s*(.+)$", re.IGNORECASE)
IMAGE_LINE = re.compile(r"^\s*image:\s*(\S+)", re.IGNORECASE)
COMP_HEADING = re.compile(r"^###\s+(C\d+)\b", re.IGNORECASE)

# --- render safety: mirror build_topic_deck.py's line grammar ---
FIELD_LINE = re.compile(r"^\s*(image|kicker|timer|source|note):\s*", re.IGNORECASE)
NOTES_LINE = re.compile(r"^(\s*)notes:\s*", re.IGNORECASE)
BULLET_LINE = re.compile(r"^(\s*)-\s+(.*)$")
MARKDOWN = re.compile(r"\*\*|`|(?<![\w*])\*[^*\s][^*]*\*(?![\w*])")   # **bold** / `code` / *italic*


def render_safety_issues(block: list) -> list:
    """Issues in one slide block (block[0] = the '- [TYPE] title' line) that would render wrongly:
    ('stray', line) — a line the builder would treat as its own level-0 bullet (a wrapped bullet);
    ('markdown', line) — markdown in text the deck renders literally (titles/kickers/bullets)."""
    issues = []
    title = block[0].split("]", 1)[-1]
    if MARKDOWN.search(title):
        issues.append(("markdown", block[0].strip()))
    notes_indent = None
    for raw in block[1:]:
        if notes_indent is not None:
            if raw.strip() == "" or len(raw) - len(raw.lstrip()) > notes_indent:
                continue                      # notes-block content — not rendered on the slide
            notes_indent = None
        nm = NOTES_LINE.match(raw)
        if nm:
            notes_indent = len(nm.group(1))
            continue
        if FIELD_LINE.match(raw):
            if raw.lower().lstrip().startswith("kicker:") and MARKDOWN.search(raw):
                issues.append(("markdown", raw.strip()))
            continue
        if raw.strip().startswith("|"):
            continue
        bm = BULLET_LINE.match(raw)
        if bm:
            if MARKDOWN.search(bm.group(2)):
                issues.append(("markdown", raw.strip()))
            continue
        if raw.strip():
            issues.append(("stray", raw.strip()))
    return issues


def tags_from(text: str) -> set:
    stripped = re.sub(r"`[^`]*`", "", text)
    out = set()
    for line in stripped.splitlines():
        for tag, _f in resolve_tags(line):
            if not tag.startswith("?? "):
                out.add(tag)
    return out


def coverage_components(text: str):
    comps = []
    for m in re.finditer(r"^-\s*\*\*\s*(C\d+)\b", text, re.MULTILINE):
        if m.group(1) not in comps:
            comps.append(m.group(1))
    return comps


def _cell_components(cell: str) -> set:
    """The C-ids a taught-table component cell names, expanding a 'C1–C4' range."""
    comps = set()
    for a, b in re.findall(r"C(\d+)\s*[–-]\s*C?(\d+)", cell):     # ranges: C1–C4
        comps |= {f"C{n}" for n in range(int(a), int(b) + 1)}
    comps |= set(re.findall(r"C\d+", cell))                       # singletons: C1 · C3
    return comps


def taught_rows(text: str):
    """From coverage.md's taught block, each table row as (tag_set, component_set) — so a slide plan
    that owns only a subset of the topic's components (a split topic) can be scoped to its slice."""
    rows = []
    for ln in taught_block(text).splitlines():
        if not ln.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 2 or all(set(c) <= set("-: ") for c in cells):   # header separator
            continue
        rows.append((tags_from(" ".join(cells[:-1])), _cell_components(cells[-1])))
    return rows


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    ap = argparse.ArgumentParser(description="Validate a Topic slide_plan.md.")
    ap.add_argument("--plan", required=True, type=Path)
    args = ap.parse_args()
    plan = args.plan
    if not plan.is_file():
        print(f"ERROR: slide plan not found: {plan}")
        return 1
    coverage = plan.parent / "coverage.md"
    if not coverage.is_file():
        print(f"ERROR: sibling coverage.md not found: {coverage}")
        return 1
    consolidated = plan.parent.parent.parent / "consolidated_uoc.md"
    valid = valid_tag_set(consolidated) if consolidated.is_file() else set()

    text = plan.read_text(encoding="utf-8")
    cov_text = coverage.read_text(encoding="utf-8")
    errors, advisories = [], []

    # --- header + Slides section ---
    if not re.search(r"^#\s+.*Slide plan\s*$", text, re.MULTILINE):
        errors.append("missing title '# Topic <NN> <Title> — Slide plan'")
    if not re.search(r"^>\s*\*\*Covers:", text, re.MULTILINE):
        errors.append("missing '> **Covers:** …' line")
    if "## Slides" not in text:
        errors.append("missing '## Slides' section")

    # --- walk sections under ## Slides ---
    lines = text.splitlines()
    sections = {}          # heading -> list of lines
    cur = None
    in_slides = False
    for ln in lines:
        if ln.strip() == "## Slides":
            in_slides = True
            continue
        if in_slides and re.match(r"^##\s", ln):   # next H2 ends Slides
            in_slides = False
        if in_slides and ln.startswith("### "):
            cur = ln.strip()
            sections[cur] = []
            continue
        if in_slides and cur:
            sections[cur].append(ln)

    plan_components = []
    teaches_tags = set()
    for heading, body in sections.items():
        cm = COMP_HEADING.match(heading)
        body_text = "\n".join(body)
        # Teaches line — required on component sections (not Opener/Close)
        tm = None
        for b in body:
            tm = TEACHES_LINE.match(b)
            if tm:
                break
        if cm:
            plan_components.append(cm.group(1).upper())
            if not tm or not tm.group(1).strip():
                errors.append(f"component section '{heading}' has no non-empty 'Teaches:' line")
            else:
                teaches_tags |= tags_from(tm.group(1))

        # slides in this section: each slide block needs a type + an image: field
        idx = [i for i, b in enumerate(body) if SLIDE_LINE.match(b)]
        for k, start in enumerate(idx):
            end = idx[k + 1] if k + 1 < len(idx) else len(body)
            block = body[start:end]
            tag = SLIDE_LINE.match(block[0]).group(1)
            first_tok = tag.strip().split()[0].upper()
            if first_tok not in TYPES:
                errors.append(f"{heading}: slide '[{tag}]' has unrecognised type '{first_tok}'")
            img = None
            for b in block:
                im = IMAGE_LINE.match(b)
                if im:
                    img = im.group(1).lower()
                    break
            title = block[0].split("]", 1)[-1].strip()[:40]
            if img is None:
                errors.append(f"{heading}: slide '[{tag}] {title}' has no 'image:' field (mandatory)")
            elif img not in IMG_KEYWORDS:
                errors.append(f"{heading}: slide '[{tag}] {title}' image: '{img}' not a valid keyword")
            for kind_, line_ in render_safety_issues(block):
                if kind_ == "stray":
                    errors.append(f"{heading}: slide '[{tag}] {title}' — line would render as its own "
                                  f"bullet (wrapped bullet? join onto one line): '{line_[:60]}'")
                else:
                    errors.append(f"{heading}: slide '[{tag}] {title}' — markdown renders literally "
                                  f"(plain text only): '{line_[:60]}'")

    # --- backwards coverage vs coverage.md (scoped to a declared subset for a split-deck topic) ---
    cov_components = coverage_components(cov_text)
    cc_m = re.search(r"^>.*Covers-components:(.+)$", text, re.MULTILINE)   # C-ids anywhere after the label
    declared = set(re.findall(r"C\d+", cc_m.group(1).upper())) if cc_m else None
    if declared is not None:
        missing_comp = [c for c in sorted(declared) if c not in plan_components]
        cov_taught = set().union(*[tags for tags, comps in taught_rows(cov_text) if comps & declared]) \
            if taught_rows(cov_text) else set()
        scope_note = f" (Covers-components: {', '.join(sorted(declared))})"
    else:
        missing_comp = [c for c in cov_components if c not in plan_components]
        cov_taught = tags_from(taught_block(cov_text))
        scope_note = ""
    if missing_comp:
        errors.append(f"components with no slide-plan section: {', '.join(missing_comp)}")
    missing_tags = sorted(cov_taught - teaches_tags)
    phantom = sorted(t for t in teaches_tags if valid and t not in valid)
    extra = sorted(t for t in teaches_tags if t in valid and t not in cov_taught)

    if missing_tags:
        errors.append(f"{len(missing_tags)} UoC item(s) coverage.md teaches but no slide plans to teach:\n    "
                      + "\n    ".join(missing_tags))
    if phantom:
        errors.append(f"{len(phantom)} Teaches tag(s) not a real consolidated UoC item:\n    "
                      + "\n    ".join(phantom))
    if extra:
        advisories.append(f"{len(extra)} Teaches tag(s) not in coverage.md's taught set (verify):\n    "
                          + "\n    ".join(extra))

    # --- report ---
    print(f"Plan:      {plan}")
    print(f"Coverage:  {coverage.name}  ({len(cov_taught)} taught items, {len(cov_components)} components)")
    print(f"Slide plan: {len(plan_components)} component sections, {len(teaches_tags)} Teaches tags")
    print()
    for a in advisories:
        print(f"ADVISORY: {a}\n")
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        print(f"\nRESULT: FAIL - {len(errors)} issue(s) in {plan}")
        return 1
    print(f"RESULT: PASS - slide plan conforms and covers coverage.md{scope_note}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
