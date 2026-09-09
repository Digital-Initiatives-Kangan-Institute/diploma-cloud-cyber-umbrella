# Step 06 — Cluster delivery plan

*(per cluster, per intake)* · Run-sheet: [process-delivery.md](../../../docs/process-delivery.md)

Lay one cluster's Topics and assessments onto a concrete session grid for a specific intake, validate it,
and generate the institutional `…_Delivery_Plan.docx`. The plan is a **semester-instance artefact** —
disposable per intake; the course it is built from is not.

## Contents

Numbered in the order they are needed, working through the step.

| | Document | |
|---|---|---|
| `_00` | [prerequisites](_00_prerequisites.md) | **entry condition** — the previous gate, plus the instance facts only the operator holds |
| `_01` | [execution](_01_execution.md) | the step performed, item by item, with the detail each item links to |
| `_02` | [delivery-plan-format](_02_delivery-plan-format.md) | the format standard the outline is written to — first needed at execution item 11 |
| `_03` | [gate](_03_gate.md) | **exit condition** — what must hold before step 07 starts |
| | [`scripts/`](scripts/) | the step's own code, linked from the execution items that run it |

## Tooling

| What | Where |
|---|---|
| format standard | [`_02_delivery-plan-format.md`](_02_delivery-plan-format.md) — **in this folder** |
| validator [`scripts/validate_cluster_delivery_plan.py`](scripts/validate_cluster_delivery_plan.py) | **in this folder** — ported, on the shared helpers |
| institutional template `Delivery_Plan_Template_v0.1.docx` | content repo `kangan-templates/` |
| docx generator `build_delivery_plan.py` | **not yet built** |

## Status

**Ported, except the docx generator.** The format standard and the validator both live here; the
validator was rebuilt test-first onto `common/helpers/` (27 cases, `CDP-01…29`, all green) rather than
carrying its own copies of the contract-parsing logic. The legacy script and its skill have been **deleted** — the gate is purely mechanical, so under the
factory's boundary it needs no skill wrapper.

Still missing: the docx generator (CL1's plan was hand-filled in Word, ~2.5 hours across three passes).

Live work: the 2026 Term 2 intake, CL2 and CL3 co-delivered. The step cannot currently run for CL2 —
prerequisites P4 (cohort size) and P5 (online/classroom split) are unknown.
