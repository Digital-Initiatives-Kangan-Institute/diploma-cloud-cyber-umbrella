# Step 04 — Slide plan → Topic deck

*(loop per Topic)* · Run-sheet: [process-delivery.md](../../../docs/process-delivery.md)

Author the slide plan, then build the branded deck from it — images resolved in-pipeline, teacher notes carried into the notes pane.

## Tooling

- engine `build_topic_deck.py` — `scripts/`
- engines `kangan_deck.py`, `deck_images.py`, `pptx_brand.py` — `scripts/helpers/`
- skills `draw-diagram`, `image-gen`, `review-slides`, `inspect-file-size`
- brand seam `brand.py` — content repo `scripts/`
- validators `validate_slide_plan.py`, `validate_deck_reproduction.py` — `.claude/skills/scripts/`
- format standard `slide-plan-format.md` — `docs/`

## Gate

**Gate 04 → 05** · *validator* `validate-slide-plan` = **PASS** (conforms + covers `coverage.md`) **before** the deck is built.

## Status

**Not ported** — the tooling above still lives at its legacy location. Converting it is done on request,
test-first; see [factory/README.md](../../README.md).
