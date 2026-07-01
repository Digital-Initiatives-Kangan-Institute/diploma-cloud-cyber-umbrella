---
name: learner-lab-consolidation-pending
description: "DECIDED (boss confirmed 2026-06-29) — ALL lab-packs/activities/assessments move to the AWS Academy Learner Lab, region simulated by a substitution notation; the proven spike, the substitution-standard design (in progress), and the two limits to resolve."
metadata:
  node_type: memory
  type: project
  originSessionId: 5fe40dfd-42a4-49d7-8e7d-5da57c8df524
---

**DECIDED — boss confirmed 2026-06-29.** Every lab-pack, activity and assessment **moves to the AWS
Academy Learner Lab**, with **scenario region simulated by a substitution notation** shown to students.
Drivers: (1) **consistency** — one lab product course-wide instead of per-activity choice between the
Cloud Architecting Sandbox and the Learner Lab; (2) **session persistence** — the Learner Lab persists
state between sessions, the Sandbox does not. This supersedes docs/lab-pack-standard.md's "no single
course-wide lab product / choose per activity" model — that section must be reworked.

**The unblocking spike — PROVEN (2026-06-26), recorded in docs/lab-pack-standard.md.** The CL1 AT3
baseline, hardened to the full multi-AZ end-state (RDS `MultiAZ: true` on `db.t3.medium` + ASG across two
private app subnets), reached `CREATE_COMPLETE` in the **Learner Lab, `us-east-1`**, RDS standby in a
second AZ, no AZ/capacity refusal. So **within-region, cross-AZ HA ports cleanly to the Learner Lab.**

**Substitution notation — being designed (2026-06-29, NOT yet finalised; do not author packs to it yet).**
Goal: one notation, taught from day 1, present in **every** lab/exercise/assessment **even when there is
no substitute**, so students learn it once and adapt automatically. Tim's draft form:
`[scenario: <region> | substitute: <region>]` (delimiter `[]` vs `()` open). **Design points raised:**
1. **Left side should be the REAL AWS region code** (`ap-southeast-2` Sydney, `ap-south-1` Mumbai,
   `ap-southeast-4` Melbourne) — NOT invented names like "sydney-east-1" — so the notation *teaches the
   correct real-world region* while the right side is the lab reality.
2. Operates at **region** level (optionally AZ level when a lab pins specific AZs).
3. **RESOLVED (2026-06-29): the Learner Lab offers only `us-east-1`** (Tim confirmed in the console —
   the region dropdown lists no other selectable region). So lab-pack-standard.md's "`us-east-1` /
   `us-west-2`" claim is now **WRONG and must be corrected**, and Tim's `us-east-2` was a mistake.
4. **RESOLVED (2026-06-29) — the principle: design is multi-region, deployment is single-region.** All
   designs, documents, diagrams and assessments KEEP the real multi-region content (region-choice logic,
   residency = Mumbai `ap-south-1`, DR = Melbourne `ap-southeast-4` — taught + assessed in full, real
   region codes). Only the *physical deploy* collapses to `us-east-1`: deployment is mechanically
   identical in any region (just the console dropdown), so nothing assessable is lost. The substitution
   token lives ONLY on deploy steps, bridging the two layers. Residency/DR "second region" becomes a
   second stack in `us-east-1` + an in-world simulated-geography note; do NOT fake a region with an AZ.
   Full standard authored: **docs/region-substitution-standard.md**. Multi-AZ HA stays REAL (deploys for
   real in us-east-1, no substitution for AZs).

**THE RULE (Tim, 2026-06-30, emphatic): assessments are UNCHANGED from before the Learner Lab move —
the ONLY difference is that deploy steps that can't run in the Learner Lab use the substitution. Nothing
added, nothing removed.** So a cross-region element (DR backup to Melbourne, a residency store) is still
**built and evidenced** — just **deployed to `us-east-1` as a separate stack/vault with the token**
(`[scenario: ap-southeast-4 (Melbourne) | deploy: us-east-1]`); it is NOT "design-only" and NOT dropped.
Assessed on successful deployment **on the substituted region**, not on location. Applied across the S1
deploy-layer builders (CL1 AT2 + AT3 deployment exemplars — incl. the AT3 Melbourne DR backup → us-east-1
DR destination; CL2 AT2 microservice + India store; topic06/07 decks; lab-pack READMEs).

**The ONE deliberate exception — CL3 residency:** the `india-residency.yaml` deploy artefact was retired
as **redundant** (Tim: not needed for a student to do the assessment; the assessor judges residency from
the design). So CL3 residency is assessed at the **DESIGN** level (SR-CL3-04 → ICTCLD504 AC5), not
deployed. Do NOT recreate a CL3 residency deploy artefact. This is a per-cluster call, NOT the general
rule (which is substitute-and-deploy, above).

**Parked ticket:** the CL1 Windows placeholder churns on an ELB health-check replace loop (~6 min) — a
UserData/bootstrap issue, not multi-AZ; fix before any live "lose an AZ, stay up" demo.

**Work the GO triggers:** finalise the substitution standard (format doc + canonical mapping table +
linter/skill, per the project's format-doc-is-source-of-truth pattern), rework lab-pack-standard.md's
environment-selection section, re-target existing packs to the chosen Learner Lab region(s), resolve the
two limits. Related: [[delivery-run-sheet]], [[s1cl3-assessment]].
