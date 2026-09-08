"""Tests for validate_slide_plan.render_safety_issues — the two deck-builder gotchas
(a wrapped bullet becomes its own level-0 bullet; markdown renders literally).

The function mirrors build_topic_deck.py's line grammar: within a slide block, a line that is not a
bullet / field / table row / notes-block content falls through to "tolerate a plain brief line as a
level-0 bullet". These tests pin both checks so neither silently stops firing.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from validate_slide_plan import render_safety_issues


def block(*lines):
    return list(lines)


def kinds(issues):
    return [k for k, _ in issues]


# --- clean blocks -------------------------------------------------------------

def test_clean_block_passes():
    issues = render_safety_issues(block(
        "- [BESPOKE] A clean slide",
        "  - one bullet on one line, however long it happens to run on and on and on",
        "  kicker: plain text kicker",
        "  timer: ~20 min",
        "  image: none",
    ))
    assert issues == []


def test_notes_block_content_is_not_a_stray_line():
    issues = render_safety_issues(block(
        "- [EX] Activity",
        "  - do the task",
        "  image: none",
        "  notes:",
        "    A plain notes line, not rendered on the slide.",
        "    Another one, wrapped over",
        "    several lines quite happily.",
    ))
    assert issues == []


def test_notes_block_ends_on_dedent():
    # after the notes block dedents, a stray line is a stray line again
    issues = render_safety_issues(block(
        "- [EX] Activity",
        "  image: none",
        "  notes:",
        "    inside the notes block",
        "  this line has dedented out of the notes block",
    ))
    assert kinds(issues) == ["stray"]


def test_table_rows_are_not_stray_lines():
    issues = render_safety_issues(block(
        "- [TABLE] A comparison",
        "  | left | right |",
        "  | --- | --- |",
        "  | a | b |",
        "  image: none",
    ))
    assert issues == []


# --- stray / wrapped lines ----------------------------------------------------

def test_wrapped_bullet_is_flagged():
    issues = render_safety_issues(block(
        "- [BESPOKE] A slide",
        "  - a bullet that was wrapped by an editor onto",
        "    a second line without a dash",
        "  image: none",
    ))
    assert kinds(issues) == ["stray"]
    assert "second line" in issues[0][1]


# --- markdown -----------------------------------------------------------------

def test_bold_in_bullet_is_flagged():
    issues = render_safety_issues(block(
        "- [BESPOKE] A slide",
        "  - this renders **literally** in the deck",
        "  image: none",
    ))
    assert kinds(issues) == ["markdown"]


def test_backticks_in_bullet_are_flagged():
    issues = render_safety_issues(block(
        "- [BESPOKE] A slide",
        "  - run `terraform apply` to proceed",
        "  image: none",
    ))
    assert kinds(issues) == ["markdown"]


def test_italic_in_kicker_is_flagged():
    issues = render_safety_issues(block(
        "- [BESPOKE] A slide",
        "  - a clean bullet",
        "  kicker: security *of* the cloud, security *in* it",
        "  image: none",
    ))
    assert kinds(issues) == ["markdown"]


def test_markdown_in_title_is_flagged():
    issues = render_safety_issues(block(
        "- [BESPOKE] The **big** picture",
        "  - a clean bullet",
        "  image: none",
    ))
    assert kinds(issues) == ["markdown"]


def test_markdown_in_notes_is_not_flagged():
    # notes go to the speaker-notes pane, not the slide — out of scope for this check
    issues = render_safety_issues(block(
        "- [EX] Activity",
        "  - a clean bullet",
        "  image: none",
        "  notes:",
        "    teacher hint with **emphasis** and `code` is tolerated",
    ))
    assert issues == []


def test_bare_asterisk_arithmetic_is_not_markdown():
    issues = render_safety_issues(block(
        "- [BESPOKE] A slide",
        "  - capacity is 5 * 3 instances across zones",
        "  image: none",
    ))
    assert issues == []
