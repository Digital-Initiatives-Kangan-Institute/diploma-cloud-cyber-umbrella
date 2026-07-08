# validate-consolidated-plan · v1.0.0 (updated 2026-06-22)

## Purpose
Prove a scenario's **consolidated assessment plan** is an exact, faithful union of its per-cluster source
plans — the independent tester for `generate-consolidated-plan` and the machine condition for run-sheet
**Gate 5→6**. Catches a stale aggregate (a per-cluster plan changed, the consolidated wasn't regenerated),
a hand-edit of the derived doc, or a generator bug.

## Prerequisites
- **Python 3** on PATH — standard library only.
- Shared scripts `.claude/skills/scripts/validate_consolidated_plan.py` (+ `generate_consolidated_plan.py`,
  whose source parser it reuses).
- The per-cluster `assessment_plan.md` files + the consolidated `assessment-plans/<SEMESTER>.md`.

## Inputs & outputs
- **In:** `--semester <S>` (discovers the sources + defaults the consolidated path; override with
  `--consolidated`).
- **Out:** PASS, or `MISSING` / `EXTRA` discrepancies across the AT roster, the UoC-coverage rollup, and the
  `SR-*` register. **Exit 0** when the consolidated is an exact faithful union.

## How it works
Re-reads the per-cluster plans and **independently** parses the consolidated doc, comparing the AT roster,
coverage map, and SR register as sets. It does not trust the generator's writer — it verifies the written
doc parses back to exactly the source union.

## Version history
- **v1.0.0 (2026-06-22)** — initial version. Proven on S1 (PASS on the generated plan; correctly FAILs a
  tampered copy).
