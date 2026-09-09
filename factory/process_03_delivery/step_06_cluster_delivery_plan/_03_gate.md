# Step 06 — Gate

**Exit condition.** What must hold before step 07 starts. The step's *entry* condition is a different
thing — see [`_00_prerequisites.md`](_00_prerequisites.md).

## Gate 06 → 07

All conditions must hold:

| # | Kind | Condition | Status |
|---|---|---|---|
| 1 | script | `scripts/validate_cluster_delivery_plan.py` passes: every built Topic and every assessment is placed in the grid; sessions numbered contiguously with every cell decided; `Mode` and `Activity` in vocabulary; the grid reconciles with the frame | **built + ported**, 27 cases (CDP-01…29) green |
| 2 | human | the **sequence** is sound — spacing, catch-up placement, and the online/classroom mix | no validator, by design |

Run the script condition per [`_01_execution.md` § H](_01_execution.md#h--running-the-validator).

## What the validator does not check

`[TBD — needs discussion: ordering]` — it confirms every Topic and assessment is **placed**, not that
the order is workable. A plan putting a build Topic before the design-approval assessment it depends on
passes today. Either the validator learns the constraint from each Topic's `coverage.md` AT marker plus
the assessment plan's thread, or it stays part of condition 2 above.

## On condition 2

Whether the sequence is *good* is human judgement made live in the juggling session, and there is
deliberately no agent validator second-guessing it. Condition 1 answers "is this complete enough to
generate the document"; condition 2 answers "is this a term worth teaching".
