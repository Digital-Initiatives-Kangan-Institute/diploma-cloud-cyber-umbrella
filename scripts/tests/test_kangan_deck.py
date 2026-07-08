"""Smoke tests for helpers.kangan_deck (Kangan teaching-deck base)."""
import pathlib
import sys

sys.path.insert(0, str(next(
    d for d in pathlib.Path(__file__).resolve().parents
    if (d / "helpers" / "__init__.py").exists()
)))

from helpers.kangan_deck import (  # noqa: E402
    new_deck, title_slide, divider_slide, content_slide, close_slide, GOLD,
)


def test_new_deck_starts_empty():
    assert len(new_deck().slides) == 0


def test_build_a_small_teaching_deck():
    prs = new_deck()
    title_slide(prs, 1, "Cloud Foundations", "Topic 1")
    divider_slide(prs, "1", "Concepts", "What you'll learn", GOLD)
    content_slide(prs, 2, "Regions and AZs", "Concepts", [(0, "A region has AZs"), (0, "AZs are isolated")])
    close_slide(prs, "Wrap up", ["See you next session"])
    assert len(prs.slides) == 4
