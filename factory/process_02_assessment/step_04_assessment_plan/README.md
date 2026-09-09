# Step 04 — Assessment plan

*(per cluster)* · Run-sheet: [process-assessment.md](../../../docs/process-assessment.md)

Decide the cluster's AT roster: what each AT evidences (UoC coverage tags) and what the scenario must supply (the `SR-*` register).

## Tooling

- validator `validate_assessment_plan.py` — `.claude/skills/scripts/`
- format standard `assessment-plan-format.md` — `docs/`

## Gate

**Gate 04 → 05** · *validator* `validate-assessment-plan` = **PASS** — conforms to the format and every consolidated item is covered.

## Status

**Not ported** — the tooling above still lives at its legacy location. Converting it is done on request,
test-first; see [factory/README.md](../../README.md).
