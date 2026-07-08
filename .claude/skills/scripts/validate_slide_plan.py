#!/usr/bin/env python3
"""Validate a Topic's slide_plan.md — the gate before the deck is built.

Deterministic, stdlib-only. The slide plan is the kept, validated source the deck is built from;
this checks it conforms to the format AND covers what its sibling coverage.md requires.

FORMAT:
  - header (# ... Slide plan + '> **Covers:**') and a '## Slides' section present;
  - every '### C<n>' component section carries a non-empty 'Teaches:' line;
  - every slide carries a recognised [<TYPE>] tag and a mandatory 'image:' field whose value is one of
    none / reuse / diagram / gen / placeholder.

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

    # --- backwards coverage vs coverage.md ---
    cov_components = coverage_components(cov_text)
    missing_comp = [c for c in cov_components if c not in plan_components]
    if missing_comp:
        errors.append(f"components in coverage.md with no slide-plan section: {', '.join(missing_comp)}")

    cov_taught = tags_from(taught_block(cov_text))
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
    print(f"RESULT: PASS - slide plan conforms and covers coverage.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
