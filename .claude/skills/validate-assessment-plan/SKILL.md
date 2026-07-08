---
name: validate-assessment-plan
version: 1.0.0
updated: 2026-06-22
model: claude-haiku-4-5-20251001
description: >-
  This skill should be used to check a cluster's assessment plan — e.g. "validate the assessment plan",
  "is the assessment plan complete/well-formed", "does the plan cover every UoC item", "check the plan
  format", or before treating a cluster's assessment plan as ready (run-sheet Gate 4). It runs a
  deterministic check (the bundled validate_assessment_plan.py): a FORMAT linter that the plan conforms to
  the assessment-plan format standard (required sections, per-AT UoC-coverage + scenario-requirements
  fields, a well-formed SR-* register, cross-referenced), and a COVERAGE check that every consolidated
  PC/PE/KE/FS item is referenced by at least one AT's UoC coverage. Use it whenever a cluster assessment
  plan must be confirmed, even if the user does not name the script.
---

# Validate assessment plan

A cluster's `assessment_plan.md` is the authored source of truth for that cluster's assessments. This skill
proves it is **well-formed** and **complete** before the downstream authoring keys off it (run-sheet Gate 4).

## When to use

- Before treating a cluster's assessment plan as ready (the Gate 4 machine condition).
- After (re)writing a plan, to confirm it conforms to the format standard and leaves no UoC item unplanned.
- To find which consolidated items a plan hasn't yet assigned to an AT, or which scenario requirements it
  references but hasn't defined.

## The validator

The engine is **`validate_assessment_plan.py`**, bundled at `.claude/skills/scripts/`. Two checks:

- **FORMAT (linter — deterministic):** the required sections are present and in order; the header carries a
  STATUS + Scenario-binding line; §3 has an AT table and a per-AT block with both a `UoC coverage:` and a
  `Scenario requirements:` field; §6 is a register of well-formed cluster-scoped `SR-<CL>-NN` rows; every
  `SR-*` referenced in §3 is defined in §6 (unreferenced defs are advisory).
- **COVERAGE:** every PC/PE/KE/FS item in the cluster's `consolidated_uoc.md` is referenced by at least one
  AT's `UoC coverage:` (canonical `[UNIT SEC num]` tags, reusing the bundled tag parser). AC items are
  discharged via the SR register, so they are informational here; phantom refs (tags that are not real UoC
  items) fail.

The format it enforces is **`docs/assessment-plan-format.md`**. Stdlib only; reuses the traceability
validator's tag machinery.

## How to run it

> **Python interpreter:** `python3`, `python`, or `py -3` (on Windows, `python3` may be the Store alias).

```bash
python3 .claude/skills/scripts/validate_assessment_plan.py --cluster <S1-CLx dir>
```

- `--cluster` — the cluster directory (it contains `assessments/assessment_plan.md` and
  `consolidated_uoc.md`).
- `--plan` / `--consolidated` — override the defaults if either lives elsewhere.

Exit `0` on PASS (format valid **and** every required item covered, no phantoms), `1` otherwise.

## Interpreting the result

- **FORMAT: FAIL** — a missing/out-of-order section, a per-AT block missing its `UoC coverage:` /
  `Scenario requirements:` field, an `SR-*` referenced but not defined, or an SR id that isn't
  cluster-scoped. Fix the plan's structure.
- **COVERAGE: MISSING** — a consolidated item no AT's UoC coverage references: an unplanned requirement.
  Assign it to the AT that should evidence it.
- **COVERAGE: PHANTOM** — a tag in the plan that is not a real UoC item (typo / wrong unit / stale number).
- This is the **plan-time** coverage check (intent). The **realisation** check — that the authored AT
  benchmarks actually evidence every item — is `validate-cluster-coverage` (Gate 9).

## Portability

Self-contained: the validator and the tag helpers it reuses live in `.claude/skills/scripts/` and are
stdlib-only, so it runs in any course repo from just the cluster directory. The format it checks is defined
in `docs/assessment-plan-format.md`.
