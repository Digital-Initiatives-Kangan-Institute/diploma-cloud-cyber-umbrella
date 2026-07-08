# validate-scenario-plan · v1.0.0 (2026-06-22)

## Purpose
Prove a scenario's **scenario plan** satisfies its **assessment contract** — the machine condition for
run-sheet **Gate 6→7**. The consolidated assessment plan ends in an `SR-*` register (everything the world
must provide); this confirms the scenario plan's Part-2 build checklist binds an item to every one of them,
and that no item points at an `SR-*` that does not exist. (The scenario plan has two parts: Part 1 the
human-led narrative — linted for presence only — and Part 2 the contract-bound build checklist.)

## Prerequisites
- **Python 3** on PATH — standard library only.
- Shared script `.claude/skills/scripts/validate_scenario_plan.py`.
- The scenario plan `scenario-plans/<SEMESTER>.md` + the consolidated `assessment-plans/<SEMESTER>.md`.

## Inputs & outputs
- **In:** `--semester <S>` (defaults both paths; override with `--plan` / `--consolidated`).
- **Out:** PASS, or FORMAT issues + `UNCOVERED` / `PHANTOM` cross-check discrepancies. **Exit 0** when the
  format is valid and every `SR-*` is satisfied with no phantom.

## How it works
Lints the scenario plan against `docs/scenario-plan-format.md` (Part 1 + Part 2 sections present, header
binding, per-item `Satisfies:` + `Keynotes:` fields, SE-NN ids), then reads the `SR-*` register from the
consolidated assessment plan and the items' `Satisfies:` lines and compares them as sets, both directions.

## Version history
- **v1.1.0 (2026-06-22)** — two-part format (Part 1 narrative + Part 2 build checklist); items are `#### SE-NN`
  blocks requiring `Satisfies:` + `Keynotes:`. Proven on S1.
- **v1.0.0 (2026-06-22)** — initial version (single-part element list). Built for run-sheet Gate 6.
