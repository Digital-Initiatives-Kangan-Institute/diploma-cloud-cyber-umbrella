---
name: learner-lab-consolidation-pending
description: "PENDING boss decision (escalated 2026-06-26) — whether to reframe ALL lab-packs/activities/assessments to run in the Learner Lab with region simulated by substitution; the proven spike that unblocks it, and the two limits the spike does NOT clear."
metadata: 
  node_type: memory
  type: project
  originSessionId: 5fe40dfd-42a4-49d7-8e7d-5da57c8df524
---

**[TBD — awaiting decision]** Tim escalated to his boss (2026-06-26) the question of **reframing every
lab-pack, activity and assessment so they all run in the AWS Academy Learner Lab**, accepting that
**region is simulated by a substitution convention** (e.g. `scenario: Sydney → substitute: us-east-1a`,
`scenario: Mumbai → substitute: us-east-1b`). **Not decided** — do not write it as settled anywhere or
start reframing artefacts until the boss confirms.

**Why it's on the table:** (1) **consistency** — one lab product for the whole course instead of
per-activity choice between the Cloud Architecting Sandbox and the Learner Lab (the current model in
docs/lab-pack-standard.md "Choosing the lab environment"); (2) **session persistence** — the Learner Lab
persists state between work sessions, which the Sandbox does not.

**The unblocking spike — PROVEN (2026-06-26), recorded in docs/lab-pack-standard.md.** The CL1 AT3
baseline, hardened to the full multi-AZ end-state (RDS `MultiAZ: true` on `db.t3.medium` + ASG across two
private app subnets), reached `CREATE_COMPLETE` in the **Learner Lab, `us-east-1`**, with the **RDS
standby in a second AZ** and **no AZ/capacity refusal** in the ASG activity log. So **within-region,
cross-AZ HA ports cleanly to the Learner Lab** — the part the substitution faithfully serves.

**Two limits the spike does NOT clear (decide these as part of the reframe):**
1. **Cross-region residency / DR is not rescued.** Mumbai/Melbourne (CL3 India slice + DR copy) are
   genuinely separate *regions*; collapsing them to two *AZs* of `us-east-1` erases the jurisdictional
   boundary. That material would become **notional** (mechanics-only, per the existing "geography is
   simulated" stance) or **stay in the Sandbox** — a conscious call, not free.
2. **The CL1 Windows placeholder churns on an ELB health-check replace loop (~6 min)** in this env — a
   UserData/bootstrap issue, NOT a multi-AZ one, but it must be fixed before any live "lose an AZ, stay
   up" demo. Separate ticket.

**If the boss says yes,** the work is: adopt the substitution convention as a documented standard (land
it once in every lab-pack README), rework docs/lab-pack-standard.md's environment-selection section,
re-target the existing packs to `us-east-1`, and resolve the two limits above. Related:
[[delivery-run-sheet]], [[s1cl3-assessment]].
