---
name: validate-delivery-plan
version: 1.0.0
updated: 2026-07-02
model: claude-haiku-4-5-20251001
description: >-
  This skill should be used whenever a cluster's delivery-plan outline needs checking — e.g. "validate
  the delivery plan", "is the delivery plan complete", "can we generate the delivery-plan docx yet",
  "check the session grid", or during/after the human-AI juggling session that produces a
  delivery/delivery-plan.md for a specific intake. It runs a deterministic check (the bundled
  validate_delivery_plan.py): the outline conforms to the format (header fields + session-grid columns
  named in the skeleton), the grid is internally consistent (numbered 1..N, every cell decided, Mode +
  Activity in vocabulary), every built Topic (delivery/topic_NN/) and every assessment (assessments/AT<n>/)
  is placed, and the grid reconciles with the frame (cluster-specification.md). It is the gate for Step 6
  — the terminal, per-instance step of the delivery run-sheet. A PASS means the outline holds every
  decision the docx generator needs; each failure is a decision still to be made. It checks completeness,
  not whether the sequence is good (that is the human call made live in the juggling session).
---

# Validate a cluster's delivery plan (Step 6)

A cluster's `delivery/delivery-plan.md` is a **semester-instance** artefact — the session grid produced
in a human-AI juggling session once the intake's concrete shape is known (session count, days,
online/classroom split). It is **not** a course artefact: re-run the step for a different intake and you
get a different plan from the same course (see
[delivery-plan-format.md](../../../docs/delivery-plan-format.md)). This skill proves the outline is
**complete enough to generate the institutional `…_Delivery_Plan.docx`** — so the producing session knows
when it is done, and can keep prompting the human for any decision still missing.

## When to use

- **During** the juggling session — run it repeatedly; each FAIL names a decision still to make.
- As the **Step-6 gate**, before the delivery-plan docx is generated from the outline.

It checks *completeness and internal/​frame consistency*, **not** whether the sequence is good — the
spacing, catch-up cadence and online/classroom mix are the human's call made live in the session, and
there is deliberately **no** agent validator second-guessing them.

## The validator

The engine is **`validate_delivery_plan.py`**, bundled at `.claude/skills/scripts/`, stdlib-only. It is
**driven by the format document**: it reads the `## Skeleton` block of `docs/delivery-plan-format.md` to
learn the required headings, header fields and **grid columns**, so the format doc is the single source
of truth (change the skeleton, the check follows). It enumerates the cluster's built Topics
(`delivery/topic_NN/`) and assessments (`assessments/AT<n>/`) as the authoritative "must be placed" sets,
and reads the sibling `cluster-specification.md` for the frame reconciliation.

## How to run it

> **Python:** use whatever Python 3 launcher you have — `python`, `python3`, or `py -3`.

```bash
python .claude/skills/scripts/validate_delivery_plan.py --cluster <SX-CLY-dir>
# or
python .claude/skills/scripts/validate_delivery_plan.py --plan <SX-CLY-dir>/delivery/delivery-plan.md
# the format doc is auto-located in the umbrella docs/; override with --format <path> if needed
```

Exit `0` on PASS, `1` otherwise.

## Interpreting the result

Goal: `RESULT: PASS — … is complete enough to generate the delivery-plan docx.` The `[plan]` lines
always **report** the intake-vs-frame session divergence, the reservations, and the mode split — that is
information, not failure.

**Hard failures (each is a decision still to be made — fix in the juggling session and re-run):**
- **missing heading / header field / grid column** — a part of the contract is absent. Add it.
- **empty cell (undecided)** — a session's `Week`/`Day`/`Mode`/`Activity` is blank, or `Placed` is
  blank (write `—` for an intentionally-empty session). Decide it.
- **invalid `Mode` / `Activity`** — use `online`/`classroom` and one of the seven activities.
- **session numbers not contiguous `1…N`** — a gap, duplicate or out-of-range session number.
- **Topic `T<n>` not placed / assessment `AT<n>` not placed** — the plan dropped it. Place it.
- **row count ≠ declared `Total sessions available`** — reconcile the grid with the header.
- **frame budgets an onboarding/spare session but the grid has none** — add the reserved session.

Fix and re-run until PASS. Whether the sequence is a *good* plan is the human half — settled in the
session, not by this gate.

## Portability

Self-contained and stdlib-only; the only external inputs are the cluster's `cluster-specification.md`,
its `delivery/topic_NN/` and `assessments/AT<n>/` folders, and the format doc it enforces. Lifts into any
course repo that carries the umbrella `docs/` tooling layer.
