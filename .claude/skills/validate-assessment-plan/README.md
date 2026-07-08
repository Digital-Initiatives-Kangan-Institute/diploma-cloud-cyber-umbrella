# validate-assessment-plan · v1.0.0 (updated 2026-06-22)

## Purpose
Prove a cluster's `assessment_plan.md` is **well-formed** (conforms to the assessment-plan format standard)
and **complete** (every consolidated PC/PE/KE/FS item is referenced by at least one AT's UoC coverage). The
machine condition for run-sheet **Gate 4**; the plan-time counterpart to `validate-cluster-coverage` (which
checks the *authored instruments* at Gate 9).

## Prerequisites
- A **Python 3 interpreter** on PATH (`python3`, or `python` / `py -3` on Windows) — standard library only.
- Shared script in `.claude/skills/scripts/`: **`validate_assessment_plan.py`** (reuses the traceability
  validator's tag machinery).
- A cluster directory with **`assessments/assessment_plan.md`** (to the format standard) and
  **`consolidated_uoc.md`**.

## Inputs & outputs
- **In:** `--cluster <dir>` (optional `--plan` / `--consolidated` overrides).
- **Out:** a **FORMAT** result (sections present + ordered; per-AT `UoC coverage:` + `Scenario
  requirements:` fields; well-formed cross-referenced `SR-*` register) and a **COVERAGE** result (`MISSING`
  unplanned items, `PHANTOM` bad refs; AC informational). **Exit 0** when format valid and coverage complete.

## How it works
Parses the plan's structure deterministically for the format check, and collects the canonical
`[UNIT SEC num]` tags from each AT's `UoC coverage:` field for the coverage check, comparing against the
items in `consolidated_uoc.md`. The format it enforces is `docs/assessment-plan-format.md`.

## Version history
- **v1.0.0 (2026-06-22)** — initial documented version. Proven on the S1-CL3 plan (the first authored to the
  format standard).
