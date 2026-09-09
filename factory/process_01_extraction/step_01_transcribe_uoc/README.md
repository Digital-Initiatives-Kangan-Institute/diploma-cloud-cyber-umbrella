# Step 01 — Transcribe the units of competency

*(loop per unit)* · Run-sheet: [process-assessment.md](../../../docs/process-assessment.md)

Lift each official UoC Word document into Markdown **verbatim** — reconstructed from the document XML, never retyped.

## Tooling

- skill `transcribe-uoc` — `.claude/skills/transcribe-uoc/`
- script `transcribe_uoc.py` — `.claude/skills/scripts/`
- validator `validate_uoc.py` — `.claude/skills/scripts/`

## Gate

**Gate 01 → 02** · *validator* `validate-uoc-transcription` (`validate_uoc.py`) = **EXACT MATCH** for every unit.

## Status

**Not ported** — the tooling above still lives at its legacy location. Converting it is done on request,
test-first; see [factory/README.md](../../README.md).
