# Process 03 — Delivery

Turning a cluster's completed assessment into the teaching that prepares students for it: the delivery
frame, the Topic breakdown and specs, the teaching decks, the practice tasks that mirror each assessment,
and the per-intake delivery plan. Consumes `process_02_assessment`'s outputs.

Run-sheet: [docs/process-delivery.md](../../docs/process-delivery.md). A separate run-sheet, so its steps
number from 01.

The last two steps mirror assessment's 04 → 05: **step 06 plans one cluster**, **step 07 consolidates the
intake's cluster plans** into a single timeline — the view that matters when clusters are co-delivered to
one cohort. Step 07 is new and **not yet in the run-sheet**, which still ends at step 06.

## Steps

| Step | Name | Legacy location of its tooling |
|---|---|---|
| 01 | Cluster specification (delivery frame) | `.claude/skills/setup-cluster-spec/`, `.claude/skills/scripts/validate_cluster_spec.py` |
| 02 | Topic breakdown | `.claude/skills/scripts/validate_topic_breakdown.py` |
| 03 | Topic spec (`coverage.md`) | `scripts/generate_topic_coverage.py`, `.claude/skills/scripts/validate_delivery_coverage.py` |
| 04 | Slide plan → Topic deck | `scripts/build_topic_deck.py`, `.claude/skills/draw-diagram/`, `image-gen/`, `review-slides/`; `validate_slide_plan.py`, `validate_deck_reproduction.py` |
| 05 | Practice tasks | `scripts/helpers/run_sheet.py`; content repo `scripts/s1_cl*/*_practice_run_sheet.py` |
| 06 | Cluster delivery plan | **ported** — `step_06_cluster_delivery_plan/scripts/validate_cluster_delivery_plan.py`; the docx generator is **not yet built** |
| 07 | Consolidated delivery plan | **new step — nothing built**; not yet in the run-sheet |

## Status

**Step 06 is partly ported** — its format standard and validator now live in its step folder, the
validator rebuilt test-first on `common/helpers/` (cases `CDP-01…29`). Its docx generator is still to
build. Every other step is structure only; step folders gain their tooling as each step's work comes up.

Live work: the 2026 Term 2 intake (CL2 + CL3 co-delivered).
