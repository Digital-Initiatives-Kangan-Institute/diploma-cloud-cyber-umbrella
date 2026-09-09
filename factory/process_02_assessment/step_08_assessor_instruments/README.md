# Step 08 — Assessor instruments

*(loop per AT)* · Run-sheet: [process-assessment.md](../../../docs/process-assessment.md)

Render each AT's authored workbook to the assessor copy — the worked version carrying the marking benchmark and UoC traceability.

## Tooling

- engines `run_sheet.py`, `workbook_instrument.py`, `docx_tables.py` — `scripts/helpers/`
- generators — content repo `scripts/s1_cl*/build_*_assessor.py`
- validator `validate_at_traceability.py` — `.claude/skills/scripts/`
- format standard `assessment-workbook-format.md` — `docs/`

## Gate

**Gate 08 → 09** · *validator* `validate-at-traceability` = **PASS** — no phantom tags, no untagged criteria.

## Status

**Not ported** — the tooling above still lives at its legacy location. Converting it is done on request,
test-first; see [factory/README.md](../../README.md).
