---
name: validate-student-instrument
version: 1.0.0
updated: 2026-07-09
model: claude-haiku-4-5-20251001
description: >-
  This skill should be used whenever a student-facing assessment instrument needs a leak check — e.g.
  "lint the student instrument", "did any assessor-only content leak into the student copy", "check the
  student docx for UoC codes / benchmarks", or after deriving a *-Student.docx from its assessor
  companion (assessment run-sheet Step 9). It runs a deterministic check (the bundled
  validate_student_instrument.py) over each AT's `*-Student.docx`: HARD-FAILS on the assessor mapping /
  benchmark leaking in (canonical UoC tags `[UNIT SEC num]`, and the labels Assessor Instructions /
  Model Answer / Benchmark / Marking Criteria), and WARNS on softer VET vocabulary (Performance
  Criteria/Evidence, Foundation Skills, Assessment Conditions, Unit of Competency, Assessment Mapping).
  It is the mechanical half of the Gate 9->10 check; whether the student copy is self-contained,
  in-world, and complete stays the human's review.
---

# Validate a student instrument (assessment Gate 9→10 leak-lint)

Step 9 of the assessment run-sheet derives the **student-facing** instrument from the assessor version by
**stripping the assessor-only content** — the Marking Guide's benchmarks, model answers, assessor
instructions, and the UoC mapping (see [process-assessment.md §9](../../../docs/process-assessment.md)).
This skill is the **mechanical half of Gate 9→10**: it proves none of that assessor-only material leaked
into the `*-Student.docx`. It is the same "no UoC codes on a student-facing artefact" rule already
enforced on student slides, generalised to the assessment instruments.

## When to use

- After a `*-Student.docx` is derived from its `*-Assessor.docx` (Step 9), before the human review.
- Any time a student instrument is edited, as a cheap re-check.

It checks *leakage*, not *quality* — whether the student copy is **self-contained, in-world, and
complete** stays the human half of the gate (a natural spot for a later agent check).

## What it flags

**HARD FAIL** — the mapping/benchmark definitively leaked (verified absent from the approved S1 student
copies, so a hit is real):
- **canonical UoC tags** `[UNIT SEC num]` (e.g. `[ICTCLD502 PC 1.1]`) — the mapping;
- **assessor-only labels** — *Assessor Instructions*, *Model Answer*, *Benchmark*, *Marking Criteria*.

**WARN** (surfaced, human confirms — could be legitimate): softer VET vocabulary — *Performance
Criteria*, *Performance Evidence*, *Foundation Skills*, *Assessment Conditions*, *Unit of Competency*,
*Assessment Mapping*.

**Deliberately NOT flagged** (legitimate on a student copy, so no false positives):
- the sanctioned **UoC footer** (bare `UNITCODE Title` lines — the one approved meta exception);
- the deliverable name **"Knowledge Evidence"** (the student answers KE questions);
- a **"Marking Guide" reference** (naming the standard the student must meet, not the guide's content);
- **marking-criterion codes** (A11, B12 — the intentional "what you're assessed on" checklist).

## How to run it

> **Python:** use whatever Python 3 launcher you have — `python`, `python3`, or `py -3`.

```bash
python .claude/skills/scripts/validate_student_instrument.py --cluster <SX-CLY-dir>   # every AT<n>/*Student.docx
python .claude/skills/scripts/validate_student_instrument.py --file <one *-Student.docx>
```

Exit `0` = PASS (no HARD leak; WARNs may be present), `1` = FAIL (a HARD leak in ≥1 file), `2` =
usage/error. WARNs do **not** fail the gate — they are for the human to confirm.

## Interpreting the result

Goal: `RESULT: PASS`. Each file reports `clean`, `clean (warnings)`, or `LEAK` with the offending
line(s) quoted.

**Hard failures (must fix):** strip the leaked content back to the assessor copy —
- **UoC mapping tags** → remove them; the mapping belongs only in the Assessor doc + the Mapping doc.
- **Assessor-only label** (Model Answer / Benchmark / Assessor Instructions / Marking Criteria) → that
  block is assessor-only; delete it from the student copy.

Re-run until PASS. A WARN is a prompt to look, not a failure — confirm the term is student-appropriate.

## Portability

Self-contained + stdlib-only (`validate_student_instrument.py` in `.claude/skills/scripts/`); it reuses
the pack's `docx_to_text` extractor. The HARD/WARN vocabulary is VET-standard, so it lifts into any
course repo whose ATs follow the `AT<n>/*-Student.docx` / `*-Assessor.docx` convention.
