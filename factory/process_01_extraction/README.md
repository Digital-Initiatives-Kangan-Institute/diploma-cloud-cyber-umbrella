# Process 01 — Extraction

Getting source material into validated, machine-readable form. Everything here is **faithful lifting**,
not editorial judgement: the unit-of-competency documents are transcribed verbatim, every assessable item
is extracted pre-tagged, and — where any exists — pre-existing assessment material is surveyed. Nothing
in this process *decides* anything; that starts at `process_02_assessment`.

Steps 01 and 02 run on every build. Step 03 runs only on a brownfield build (see below).

Run-sheet: [docs/process-assessment.md](../../docs/process-assessment.md) (its first three steps).

## Steps

| Step | Name | Legacy location of its tooling |
|---|---|---|
| 01 | Transcribe the units of competency | `.claude/skills/transcribe-uoc/`, `.claude/skills/scripts/transcribe_uoc.py`, `validate_uoc.py` |
| 02 | Consolidate the cluster's UoCs | `.claude/skills/consolidate-uocs/`, `.claude/skills/scripts/inventory_uoc.py`, `validate_consolidated.py` |
| 03 | Audit source assessments — **OPTIONAL, brownfield only** | `.claude/agents/evaluate-legacy-materials.md` (agent-only; no script) |

**Step 03 is the factory's one optional step.** It runs only when pre-existing assessment materials
exist and might be reused. Greenfield — the common case for new courseware — skips it entirely and goes
straight to step 04. Which it is cannot be inferred, so **ask the operator** rather than guessing from
whether a folder happens to be present.

## Status

Structure only — **nothing ported**. Step folders are created as each step's work comes up.
