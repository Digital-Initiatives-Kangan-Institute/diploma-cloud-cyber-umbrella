---
name: assessment-run-sheet
description: The assessment process is now a formalised step→gate run-sheet (docs/process-assessment.md); we are validating it gate-by-gate against S1 and building a validator/agent for each gateless gate. In-flight workstream — next is Gate 6 (scenario plan tooling).
metadata:
  type: project
---

The cluster **assessment process is a formalised step→gate run-sheet** —
[process-assessment.md](../../docs/process-assessment.md), the **assessment run-sheet** (one of two; the
**delivery run-sheet** = process-delivery.md, to get the same treatment later). 11 steps; each **gate** =
a deterministic **validator** (where one exists) **+ human review**, with the human check removable per-gate
as a step earns confidence. The active workstream is **walking the gates against S1 (CL1/CL2/CL3)**: run the
validator where one exists; at a gateless gate, build a tool/agent for it.

**Gate-walk state (2026-06-22):**
- **Gate 1 transcribe / 2 consolidate-UoC** — existing validators, PASS on all 3 clusters.
- **Gate 3 audit** — reframed as **brownfield-only / optional** (skip if greenfield); built the read-only
  **`evaluate-legacy-materials` agent** (`.claude/agents/`) that surfaces reuse candidates, authors/decides
  nothing. Not a validation gate. Can't run on S1 (no `original_materials/` in repo).
- **Gate 4 plan** — built the **assessment-plan format standard** (docs/assessment-plan-format.md) +
  **`validate-assessment-plan`** (format linter + UoC-coverage). **All 3 S1 plans retrofitted** to the
  format (per-AT UoC coverage as canonical tags derived from the AT benchmarks; per-cluster **`SR-*`**
  scenario-requirements register; substance preserved). All PASS (CL1 106, CL2 105, CL3 72).
- **Gate 5 consolidate plans** *(per scenario)* — built **`generate-consolidated-plan`** (deterministic) +
  **`validate-consolidated-plan`** (independent faithful-union tester). Generated `assessment-plans/S1.md`
  (the cross-cluster AT roster + coverage rollup + **unioned SR-* register** = the single contract the
  scenario validates against). PASS.
- **Gates 7 assessor (validate-at-traceability) / 9 mapping (validate-mapping-doc) / 10 cluster-coverage
  (validate-cluster-coverage)** — validators already exist + passed earlier this session; back-test in the
  walk if needed. **Gate 8 student / Gate 11 pre-validation** — human.

**Architecture (decided):** per-cluster `assessment_plan.md` = **authored source of truth**; the
**consolidated plan = derived** (generated, never hand-edited); the **scenario plan** (next) validates
against the consolidated **SR-*** register. `SR-*` ids are **cluster-scoped** (`SR-CL3-01`) so registers
union without collision. AC items are discharged via the SR register's **AC-link** column.

**NEXT (post-compaction):** **Gate 6 — scenario** tooling — author the **scenario-plan format spec** +
**scenario-plan linter** + **scenario cross-check** (every `SR-*` in `assessment-plans/S1.md` satisfied by a
scenario-plan element; bidirectional). That's the open item flagged in assessment-plan-format.md ("scenario-
plan format — to be written"). Then revisit gates 7/9/10 in the walk, then give **process-delivery.md** the
run-sheet treatment. Related: [[mapping-pipeline]] (same derived-artefact + validator pattern).
