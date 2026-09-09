# Step 03 — Audit source assessments

*(**OPTIONAL** — brownfield only)* · Run-sheet: [process-assessment.md](../../../docs/process-assessment.md)

Surface reusable pre-existing assessment material so the human can weigh reuse when building the cluster
plan. Read-only: it authors nothing, persists nothing, and decides nothing — it brings options to the
surface.

## Applies when — ask the operator

This is the one **optional** step in the factory. It depends on how the courseware is being developed,
which the tooling cannot infer:

- **Greenfield** — the units are being authored from scratch, with no pre-existing assessment materials.
  Nothing to audit. **Skip the step entirely** and proceed to step 04.
- **Brownfield** — standalone assessment materials already exist for the cluster's units (typically in
  `original_materials/`) and might be reusable.

**Ask the operator which it is** before starting the step; do not infer it from whether a folder happens
to exist. Greenfield is the common case for new courseware.

## Tooling

- agent `evaluate-legacy-materials` — `.claude/agents/evaluate-legacy-materials.md`

*(Brownfield only. On a greenfield build nothing here runs.)*

## Gate

**Gate 03 → 04** · *not a correctness check.*

- **Greenfield:** proceed.
- **Brownfield:** the `evaluate-legacy-materials` agent has been run and its surfaced candidates are in
  hand as an input to step 04, where the human decides what (if anything) to reuse. Reusable scenario
  assets carry forward to the scenario plan at step 06.

## Status

**Not ported** — the agent still lives at its legacy location. Converting it is done on request,
test-first; see [factory/README.md](../../README.md).
