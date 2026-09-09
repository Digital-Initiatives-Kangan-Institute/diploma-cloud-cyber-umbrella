# Step 03 — Topic spec (`coverage.md`)

*(loop per Topic — derived, not hand-authored)* · Run-sheet: [process-delivery.md](../../../docs/process-delivery.md)

Generate each Topic's `coverage.md`: the components it teaches and the UoC items each carries.

## Tooling

- engine `generate_topic_coverage.py` — `scripts/`
- validator `validate_delivery_coverage.py` — `.claude/skills/scripts/`

## Gate

**Gate 03 → 04** · *validator* `validate-delivery-coverage` — the union of all Topics' tags covers what the cluster must teach.

## Status

**Not ported** — the tooling above still lives at its legacy location. Converting it is done on request,
test-first; see [factory/README.md](../../README.md).
