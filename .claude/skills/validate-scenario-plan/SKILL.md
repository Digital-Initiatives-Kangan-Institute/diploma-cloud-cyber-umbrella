---
name: validate-scenario-plan
version: 1.1.0
updated: 2026-06-22
model: claude-haiku-4-5-20251001
description: >-
  This skill should be used to confirm a scenario plan satisfies its scenario's assessment contract —
  e.g. "validate the scenario plan", "does the scenario cover every SR", "run the scenario cross-check", or
  at run-sheet Gate 6→7. It runs validate_scenario_plan.py: it lints the two-part scenario plan against the
  format standard (Part 1 narrative + Part 2 build checklist present; header binding; each '#### SE-NN'
  checklist item carries 'Satisfies:' + 'Keynotes:' fields) and cross-checks Part 2 against the consolidated
  assessment plan's SR-* register — asserting every SR-* is satisfied by at least one checklist item
  (UNCOVERED → fail) and no item claims a non-existent SR-* (PHANTOM → fail). Use it whenever a scenario plan
  must be confirmed against its SR-* contract.
---

# Validate scenario plan

The scenario plan (`scenario-plans/<SEMESTER>.md`) has two parts (see `docs/scenario-plan-format.md`):
**Part 1** the scenario narrative (the human-led story bible) and **Part 2** the forward build checklist —
`SE-NN` items, each binding the `SR-*` it provides and carrying keynotes on what to build. It is the seam
between the **consolidated assessment plan** (`assessment-plans/<SEMESTER>.md`, the contract) and the website
(built from it). This skill is the machine condition for run-sheet **Gate 6→7**.

## When to use

- After authoring/updating a scenario plan, to confirm Part 2 satisfies the whole `SR-*` contract (Gate 6→7).
- Whenever the consolidated assessment plan changed (an `SR-*` was added/removed), to catch a scenario plan
  that no longer covers the contract.
- To detect a checklist item claiming a stale or mistyped `SR-*` (phantom).

## The validator

`validate_scenario_plan.py` (bundled at `.claude/skills/scripts/`) runs two phases:

- **FORMAT** — required sections present + in order (title, Part 1 — Scenario narrative, Part 2 — Build
  checklist, SR coverage, Open questions, Changelog); header carries STATUS + Assessment-binding; Part 2 has
  `#### SE-NN` item blocks each with a `Satisfies:` and a `Keynotes:` field; SE ids well-formed. (Part 1 is
  linted for presence only — the narrative is the human creative part.)
- **CROSS-CHECK** — reads the `SR-*` register from the consolidated assessment plan and the `Satisfies:`
  lines from Part 2, then asserts bidirectionally: every register `SR-*` is satisfied by ≥1 item
  (**UNCOVERED** otherwise), and every claimed `SR-*` exists in the register (**PHANTOM** otherwise). An item
  satisfying no `SR-*` is reported **info** (allowed world-building).

Stdlib only.

## How to run it

```bash
python3 .claude/skills/scripts/validate_scenario_plan.py --semester S1
```

- `--semester` — defaults the plan to `scenario-plans/<SEMESTER>.md` and the contract to
  `assessment-plans/<SEMESTER>.md` (override with `--plan` / `--consolidated`).

Exit `0` on PASS (format valid AND every `SR-*` satisfied, no phantoms), `1` otherwise. On an UNCOVERED
failure, add or bind a checklist item; on PHANTOM, fix the `Satisfies:` id (or regenerate the consolidated
plan if the register genuinely changed).

## Portability

Self-contained: stdlib-only, in `.claude/skills/scripts/`; needs only the scenario plan + the consolidated
assessment plan.
