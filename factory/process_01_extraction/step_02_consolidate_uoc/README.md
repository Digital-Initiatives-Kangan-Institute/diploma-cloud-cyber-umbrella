# Step 02 — Consolidate the cluster's UoCs

*(per cluster)* · Run-sheet: [process-assessment.md](../../../docs/process-assessment.md)

Group every PC/FS/PE/KE/AC from the cluster's units into one `consolidated_uoc.md` — items are *arranged*, never retyped.

## Tooling

- skill `consolidate-uocs` — `.claude/skills/consolidate-uocs/`
- script `inventory_uoc.py` — `.claude/skills/scripts/`
- validator `validate_consolidated.py` — `.claude/skills/scripts/`

## Gate

**Gate 02 → 03** · *validator* `validate-uoc-consolidation` (`validate_consolidated.py`) = **PASS** — every item present exactly once.

## Status

**Not ported** — the tooling above still lives at its legacy location. Converting it is done on request,
test-first; see [factory/README.md](../../README.md).
