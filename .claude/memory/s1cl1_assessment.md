---
name: s1cl1-assessment
description: S1-CL1 (Cloud Design and Build) pilot cluster, assessment workstream — AT shape, settled cross-AT design decisions, and open items needed before live delivery.
metadata:
  node_type: memory
  type: project
---

S1-CL1 (Cloud Design and Build) is the **pilot cluster**, developed end-to-end. This entry holds the
**assessment workstream**: the cluster's **AT shape**, its **settled design decisions**, and the **open
items** still needed before live delivery. Delivery-planning (sessions/teaching materials) is a
separate workstream — see [[s1cl1-delivery]]. General authoring rules live in
docs/cluster-authoring-conventions.md.

## Cluster shape

| AT | Title | Format | Primary unit |
|---|---|---|---|
| AT1 | Business Case: YAT LMS Cloud Migration | Project Assessment — Part A (BC written) + Part B (board presentation) | ICTICT517 |
| AT2 | Cloud Foundation Build: YAT LMS | Project Assessment — single-task; deliverable = Deployment Report + appendices | ICTCLD401 |
| AT3 | High Availability: YAT LMS | Project Assessment — Part A (HA Design) + Part B (HA Deployment Report) | ICTCLD502 |

Scenario: the **YAT College (RTO)** world is single-sourced on the **website**
(diploma-cloud-cyber-website) — see docs/website-architecture.md. Cluster artefacts reference it
**abstractly** (e.g. "the YAT intranet"), never by path; the old `<repo_root>/scenario/` folder is no
longer the source of truth.

## Settled cross-AT design decisions (won't re-litigate unless new evidence)

- **Project Assessment template for all three ATs** — even AT2 (single-task): "implementation is a
  project even if the deliverable is written." (General rule: docs/cluster-authoring-conventions.md §7.)
- **502 PC reassignment AT3 → AT2:** PCs 1.3, 4.1, 4.2, 4.3 moved (UoC text analysis — not HA-specific).
  AT3 owns all HA-design / -evaluation / -simulation / -closure PCs.
- **MTS scope = cloud infrastructure only.** YAT IT (in-scenario) handles LMS app deployment, MySQL
  migration, cutover, change management. Single source: the AT1 role-brief § Scope; cross-referenced
  from AT2 + AT3.
- **AT3 is post-cutover** — LMS already deployed by YAT IT after AT2; AT3 hardens running infrastructure
  in place (no re-deploy, no data migration, no cutover for AT3).
- **AT3 has no standalone closure pack / observation event / Security Responsibilities Matrix.** Closure
  PCs (5.1–5.3) evidenced in HA Deployment Report §6.6 + §7.5 + §7.6; FS Oral Communication in AT1's
  presentation.
- **AT2 → AT3 thread loose by design.** AT2 implements a supplied baseline design; AT3 hardens it. The
  assessor distributes an AT2 baseline CloudFormation template so every student starts AT3 consistent.
- **AT3 maintenance-window framing:** simulated Saturday late-night ~3.5h window; brief blips
  acceptable; must end HA-done or rolled back.

## Open — needed before live delivery

- **⚠️ AWS Academy lab — Multi-AZ RDS for AT3.** The Learner Lab (Foundation Services) documents
  "Multi-AZ deployments not supported" — conflicts with AT3's "convert the DB to Multi-AZ + trigger
  failover" build. **Only the live Multi-AZ DB is at risk** — compute HA (cross-AZ ASG + ALB) is fully
  supported. **Resolution (per Tim):** make the correct AWS Academy enrolment an AT3 condition/resource
  rather than changing content — (a) confirm which enrolment gives an open-build env that also permits
  Multi-AZ RDS; (b) smoke-test it; (c) record the required course/lab in AT3 Resources + Assessment
  Conditions + assessor notes. **Fallback:** reframe DB-HA as design+template (`Multi-AZ: true`) +
  simulated failover (reboot/terminate).
- **AT2 baseline CloudFormation YAML** still to author (placeholder spec exists; ~400–600 lines).
- **Records Management Policy** scenario doc still to author (placeholder exists).
