---
name: generate-consolidated-plan
version: 1.0.0
updated: 2026-06-22
model: claude-haiku-4-5-20251001
description: >-
  This skill should be used to (re)generate a scenario's consolidated assessment plan — e.g. "build the
  consolidated assessment plan", "regenerate the S1 consolidated plan", "aggregate the cluster plans", or
  at run-sheet step 5 once every cluster's assessment plan is authored. It runs the deterministic
  generator (generate_consolidated_plan.py), which derives one cross-cluster plan from the per-cluster
  assessment_plan.md files: the AT roster, the whole-of-scenario UoC coverage rollup, and the unioned
  scenario-requirements (SR-*) register — the single contract the scenario plan is validated against. The
  output is DERIVED (never hand-edited); confirm it with the validate-consolidated-plan skill.
---

# Generate consolidated assessment plan

A scenario's per-cluster `assessment_plan.md` files are the authored source of truth. This skill **derives**
the single cross-cluster view a scenario plan is validated against (run-sheet step 5).

## When to use

- Once every cluster in a scenario has an authored, format-valid assessment plan (i.e. each passes
  `validate-assessment-plan`), to produce/refresh the consolidated plan.
- Whenever a per-cluster plan changes — regenerate so the consolidated stays in sync (then run
  `validate-consolidated-plan`).

## The generator

`generate_consolidated_plan.py` (bundled at `.claude/skills/scripts/`) parses each per-cluster plan's §3
(AT roster + per-AT `UoC coverage:` tags) and §6 (`SR-*` register), and writes one consolidated plan:

- **AT roster** — every cluster·AT (mode, unit focus).
- **UoC coverage (whole-of-scenario)** — every consolidated item → the cluster·AT(s) covering it.
- **Scenario requirements register (aggregated)** — the union of every cluster's `SR-*` rows (ids are
  cluster-scoped, so no collisions). This is the contract the scenario plan satisfies.

Deterministic (sorted throughout): same inputs → same output. The output carries a **DERIVED — do not
hand-edit** banner; the per-cluster plans remain the source.

## How to run it

```bash
python3 .claude/skills/scripts/generate_consolidated_plan.py --semester S1
```

- `--semester` — auto-discovers `<SEMESTER>-CL*/assessments/assessment_plan.md`. Default output:
  `assessment-plans/<SEMESTER>.md`. (Or pass explicit `--plan <path>` repeatably + `--out <path>`.)

Then confirm faithfulness with **`validate-consolidated-plan`** (run-sheet Gate 5→6).

## Portability

Self-contained: the generator + the tag helpers it reuses are stdlib-only in `.claude/skills/scripts/`. It
needs only the per-cluster plans (authored to `docs/assessment-plan-format.md`).
