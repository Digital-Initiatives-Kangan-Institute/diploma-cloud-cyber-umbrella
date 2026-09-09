# Step 05 — Consolidate the assessment plans

*(per scenario — after every cluster's step 04)* · Run-sheet: [process-assessment.md](../../../docs/process-assessment.md)

Derive one cross-cluster plan from the per-cluster plans: the AT roster, the coverage rollup, and the unioned `SR-*` register. Generated, never hand-edited.

## Tooling

- skill `generate-consolidated-plan` — `.claude/skills/generate-consolidated-plan/`
- engine `generate_consolidated_plan.py` — `.claude/skills/scripts/`
- validator `validate_consolidated_plan.py` — `.claude/skills/scripts/`

## Gate

**Gate 05 → 06** · *validator* `validate-consolidated-plan` = **PASS** — an exact, faithful union of the source plans.

## Status

**Not ported** — the tooling above still lives at its legacy location. Converting it is done on request,
test-first; see [factory/README.md](../../README.md).
