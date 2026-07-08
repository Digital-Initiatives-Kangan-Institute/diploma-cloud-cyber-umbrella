---
name: validate-consolidated-plan
version: 1.0.0
updated: 2026-06-22
model: claude-haiku-4-5-20251001
description: >-
  This skill should be used to confirm a scenario's consolidated assessment plan faithfully reflects its
  per-cluster source plans — e.g. "validate the consolidated plan", "is the consolidated assessment plan in
  sync", "did the consolidator do its job", or at run-sheet Gate 5→6. It runs the independent tester
  (validate_consolidated_plan.py): it re-reads the per-cluster assessment_plan.md files and independently
  parses the generated consolidated doc, asserting the consolidated is an exact, faithful union (AT roster,
  whole-of-scenario coverage, and unioned SR-* register) — catching a stale aggregate, a hand-edit, or a
  generator bug. Use it whenever a consolidated assessment plan must be confirmed.
---

# Validate consolidated assessment plan

The consolidated assessment plan is a **derived** artefact (see `generate-consolidated-plan`); the
per-cluster `assessment_plan.md` files are the source of truth. This skill is the **independent tester**
that the consolidated is an exact, faithful union of those sources — the machine condition for run-sheet
**Gate 5→6**.

## When to use

- After (re)generating the consolidated plan, to confirm it is in sync (Gate 5→6).
- Whenever a per-cluster plan has changed, to catch a **stale** consolidated that wasn't regenerated.
- To detect a hand-edit of the (derived) consolidated, or a generator bug.

## The validator

`validate_consolidated_plan.py` (bundled at `.claude/skills/scripts/`) re-reads the per-cluster plans (via
the generator's source parser) **and independently parses the consolidated doc**, then asserts they match
exactly:

- **AT roster** — every cluster·AT (mode, unit focus) present; none extra.
- **UoC coverage rollup** — every item maps to exactly the cluster·AT set the sources cover it with.
- **Aggregated `SR-*` register** — every `SR-*` row (id, condition, AT(s), AC link) present; none extra.

Any `MISSING` (in the sources, absent from the consolidated) or `EXTRA` (in the consolidated, not in the
sources) is a discrepancy → FAIL. Stdlib only.

## How to run it

```bash
python3 .claude/skills/scripts/validate_consolidated_plan.py --semester S1
```

- `--semester` — discovers the per-cluster sources + defaults the consolidated to
  `assessment-plans/<SEMESTER>.md` (override with `--consolidated`).

Exit `0` on PASS (exact faithful union), `1` otherwise. On FAIL, regenerate with
`generate-consolidated-plan` (drift is almost always a stale aggregate).

## Portability

Self-contained: stdlib-only, in `.claude/skills/scripts/`; needs only the per-cluster plans + the
consolidated doc.
