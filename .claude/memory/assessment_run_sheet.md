---
name: assessment-run-sheet
description: The assessment process is now a formalised step→gate run-sheet (docs/process-assessment.md); we are validating it gate-by-gate against S1 and building a validator/agent for each gateless gate. In-flight workstream — gates 1–7 validated on S1; NEXT is walking gates 8–12 (assessor/student instruments → mapping → cluster coverage → pre-validation).
metadata:
  type: project
---

The cluster **assessment process is a formalised step→gate run-sheet** —
[process-assessment.md](../../docs/process-assessment.md), the **assessment run-sheet** (one of two; the
**delivery run-sheet** = process-delivery.md, to get the same treatment later). 12 steps; each **gate** =
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
- **Gate 6 scenario** — built the **scenario-plan format standard** (docs/scenario-plan-format.md) +
  **`validate-scenario-plan`** (format linter + bidirectional SR cross-check). The **scenario plan**
  (`scenario-plans/<S>.md`) is the *authored* counterpart of the *derived* consolidated plan: in-world
  **`SE-NN`** elements, each `Satisfies:` the `SR-*` it provides. Authored **`scenario-plans/S1.md`** (22
  elements binding all 24 `SR-*`); cross-check **PASS** (negative-tested: catches UNCOVERED + PHANTOM).
- **Gate 7 scenario materials / website** — built the read-only **`verify-scenario-realisation` agent**
  (`.claude/agents/`); proven on S1's built website. Its worklist is now **CLOSED** (see
  [[scenario-plan-reverse-mapping]]): 3 of 4 "gaps" were SR-wording mis-statements (SE-05/10/11), SE-16 a
  generator fix, and `website-improvement` (CL3 practice) was kept + refreshed.
- **⚠ Run-sheet was RELINEARISED — it is now 12 steps** (scenario **plan** = step 6, scenario
  **materials/website** = step 7, then **8 assessor / 9 student / 10 mapping / 11 cluster-coverage / 12
  pre-validation**). Older notes used the 11-step numbering — ignore those numbers.
- **Gates 8 assessor (`validate-at-traceability`) / 10 mapping (`validate-mapping-doc`) / 11 cluster-coverage
  (`validate-cluster-coverage`)** — validators exist but are **not yet back-tested on the *current* S1
  artefacts** (much changed since — that's the NEXT work). **Gate 9 student / Gate 12 pre-validation** — human.

**Architecture (decided):** per-cluster `assessment_plan.md` = **authored source of truth**; the
**consolidated plan = derived** (generated, never hand-edited); the **scenario plan** (next) validates
against the consolidated **SR-*** register. `SR-*` ids are **cluster-scoped** (`SR-CL3-01`) so registers
union without collision. AC items are discharged via the SR register's **AC-link** column.

**NEXT (post-compaction):** resume the assessment walk at **Gate 8** — run `validate-at-traceability` across
all **8 assessor instruments** (CL1×3, CL2×2, CL3×3) against each cluster's `consolidated_uoc.md`; then
**Gate 9** student instruments (human check), **Gate 10** `validate-mapping-doc` (every unit), **Gate 11**
`validate-cluster-coverage` (per cluster), **Gate 12** institutional pre-validation (human). Goal: confirm
the run-sheet takes S1 to "everything placed, only human pre-validation remaining." *(A Gate-8 sweep was
about to run when the website thread interrupted.)* After that: give **process-delivery.md** the run-sheet
treatment (the delivery run-sheet). **Deferred follow-up:** generate the branded
`YAT-Website-Improved-Solution-Design` download asset (delivery-side parity; non-blocking). Related:
[[mapping-pipeline]], [[scenario-plan-model]], [[scenario-plan-reverse-mapping]].
