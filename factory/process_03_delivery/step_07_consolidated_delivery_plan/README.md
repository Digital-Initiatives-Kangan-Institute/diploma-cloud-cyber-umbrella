# Step 07 — Consolidated delivery plan

*(per intake — capstone)* · **NEW STEP — not yet in
[process-delivery.md](../../../docs/process-delivery.md)**

Bring the intake's per-cluster delivery plans together into one document showing every cluster's sessions
on a single timeline. Where clusters are **co-delivered** — running in the same weeks, sharing a cohort
and competing for the same days — the individual plans cannot be read against each other, and clashes,
gaps and imbalances are only visible once they are combined.

This step is derived: the consolidated plan is built **from** the validated cluster plans, never
hand-authored alongside them.

## Why it exists

The 2026 Term 2 intake co-delivers CL2 (3 sessions/week) and CL3 (2 sessions/week) to one cohort across
the same ten weeks. Each cluster is planned on its own, and only the consolidated view answers whether
the combined load works: whether two assessment blocks collide in one week, whether one cluster is short
of time while the other has slack to lend, and what the cohort's actual week looks like.

## Mirrors the assessment run-sheet

The same shape as assessment steps 04 → 05: author per cluster, then derive one consolidated artefact
per scenario/intake, generated and validated rather than maintained by hand.

| | Per unit | Consolidated |
|---|---|---|
| Assessment | step 04 — assessment plan (per cluster) | step 05 — consolidate the assessment plans |
| Delivery | step 06 — cluster delivery plan | **step 07 — consolidated delivery plan** |

## Tooling

**Nothing built.** By analogy with step 05, this would want a generator plus an independent validator
confirming the consolidated document is a faithful union of its source plans.

## Gate

`[TBD — needs discussion]` — undefined. By analogy with Gate 05 → 06, a validator confirming the
consolidated plan faithfully reflects every source cluster plan, plus a check that no session slot is
double-booked across clusters.

## Status

**New — nothing exists.** The step is declared so the structure holds a place for it; the run-sheet
([docs/process-delivery.md](../../../docs/process-delivery.md)) still ends at step 06 and needs updating
when this step is built.

`[TBD — needs discussion: borrowing between clusters]` — where one co-delivered cluster needs more time
than it has and another has slack, sessions can be traded. Whether that trade is recorded here or fed
back into the cluster plans at step 06 is open.
