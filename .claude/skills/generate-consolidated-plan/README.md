# generate-consolidated-plan · v1.0.0 (updated 2026-06-22)

## Purpose
Deterministically derive a scenario's **consolidated assessment plan** (`assessment-plans/<SEMESTER>.md`)
from its per-cluster `assessment_plan.md` files — the AT roster, the whole-of-scenario UoC coverage rollup,
and the unioned `SR-*` register (the single cross-cluster contract the scenario plan is validated against).
Run-sheet step 5. The output is DERIVED (never hand-edited); the per-cluster plans are the source of truth.

## Prerequisites
- **Python 3** on PATH — standard library only.
- Shared script `.claude/skills/scripts/generate_consolidated_plan.py` (reuses the traceability tag parser).
- The scenario's per-cluster plans, each authored to `docs/assessment-plan-format.md` (ideally each passing
  `validate-assessment-plan`).

## Inputs & outputs
- **In:** `--semester <S>` (auto-discovers `<S>-CL*/assessments/assessment_plan.md`), or explicit `--plan`
  paths; optional `--out`.
- **Out:** `assessment-plans/<S>.md` — AT roster + whole-of-scenario coverage rollup + aggregated `SR-*`
  register, with a DERIVED banner.

## How it works
Parses each per-cluster plan's §3 (AT roster + per-AT UoC-coverage tags) and §6 (SR register), merges and
sorts deterministically, and writes the consolidated plan. Confirm faithfulness with
`validate-consolidated-plan`.

## Version history
- **v1.0.0 (2026-06-22)** — initial version. Proven on S1 (3 clusters, 8 ATs, 284 coverage items, 24 SR).
