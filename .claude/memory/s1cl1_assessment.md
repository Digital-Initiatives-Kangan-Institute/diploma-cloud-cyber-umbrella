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
- **AT3 Multi-AZ is a real live demo (not a fallback).** The hardened end-state — RDS `MultiAZ: true`
  **and** cross-AZ ASG+ALB — is proven deployable in the **AWS Academy Cloud Architecting Sandbox**
  (`ap-southeast-2`, 2026-06-15). The old "Multi-AZ RDS not supported" reading was wrong for that lab.
  **Required lab for AT3 = the Cloud Architecting Sandbox** (record it in AT3 Resources / Assessment
  Conditions). The design+simulated-failover fallback is NOT needed.

## Open — needed before live delivery

- **Records Management Policy** scenario doc still a placeholder stub on the website
  (`src/content/policies/records-management.md`) — needs drafting; referenced by CL1 AT1/AT2/AT3
  (and CL2/CL3). In-world YAT policy, no course/assessment meta-language.
- **Record the AT3 required lab** (Cloud Architecting Sandbox) in the AT3 assessor `.docx`
  Resources / Assessment Conditions (the Multi-AZ capability is proven — see the settled decision
  above; this is just propagating it into the instrument).
