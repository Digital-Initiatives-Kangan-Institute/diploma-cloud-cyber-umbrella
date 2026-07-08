"""Smoke tests for helpers.pptx_brand (YAT/MTS presentation brand)."""
import pathlib
import sys

sys.path.insert(0, str(next(
    d for d in pathlib.Path(__file__).resolve().parents
    if (d / "helpers" / "__init__.py").exists()
)))

from helpers.pptx_brand import (  # noqa: E402
    new_deck, add_title_slide, add_content_slide, add_statement_slide,
    add_table_slide, add_closing_slide,
)


def test_new_deck_starts_empty():
    assert len(new_deck().slides) == 0


def test_build_a_small_branded_deck():
    prs = new_deck()
    add_title_slide(prs, "Design Review", "YAT LMS", ["Prepared by MTS", "v1.0"])
    add_content_slide(prs, "Agenda", [("Scope", 0), ("Approach", 0), ("Risks", 1)])
    add_statement_slide(prs, "Key point", "Availability is the driver", "99.9% target")
    add_table_slide(prs, "Costs", ["Item", "Year 1"], [["Compute", "$100"]])
    add_closing_slide(prs, "Questions", "thank you")
    assert len(prs.slides) == 5
