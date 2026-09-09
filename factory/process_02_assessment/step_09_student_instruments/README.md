# Step 09 — Student instruments

*(loop per AT)* · Run-sheet: [process-assessment.md](../../../docs/process-assessment.md)

Render the student copy of each AT from the same authored source — blank, self-contained, and free of assessor-only content.

## Tooling

- generators — content repo `scripts/s1_cl*/build_*_student.py`
- validator `validate_student_instrument.py` — `.claude/skills/scripts/`
- validator `validate_instrument_reproduction.py` — `.claude/skills/scripts/`

## Gate

**Gate 09 → 10** · *validator* `validate-student-instrument` — the student copy leaks no UoC tags, benchmark or assessor instructions. Human review: self-contained + in-world.

## Status

**Not ported** — the tooling above still lives at its legacy location. Converting it is done on request,
test-first; see [factory/README.md](../../README.md).
