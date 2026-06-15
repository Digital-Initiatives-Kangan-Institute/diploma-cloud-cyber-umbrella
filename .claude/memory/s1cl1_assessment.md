---
name: s1cl1-assessment
description: S1-CL1 (Cloud Design and Build) pilot cluster, assessment workstream — COMPLETE (2026-06-15): AT shape, settled cross-AT design decisions, and the now-closed pre-delivery items.
metadata:
  node_type: memory
  type: project
---

> **STATUS: COMPLETE (2026-06-15).** The CL1 assessment workstream is done — all instruments
> finalised, the Multi-AZ risk resolved, the Records Management Policy authored. See **Status** at the
> foot of this entry. Don't reopen unless something material changes.

S1-CL1 (Cloud Design and Build) is the **pilot cluster**, developed end-to-end. This entry holds the
**assessment workstream**: the cluster's **AT shape**, its **settled design decisions**, and its
**completion status**. Delivery-planning (sessions/teaching materials) is a separate workstream — see
[[s1cl1-delivery]]. General authoring rules live in docs/cluster-authoring-conventions.md.

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
  **Required lab for AT3 = the Cloud Architecting Sandbox** — recorded in the AT3 assessment conditions
  (C1 names AWS Academy Cloud Architecting [172221] + Cloud Foundations [104469] and RDS access). The
  design+simulated-failover fallback is NOT needed.

## Status — COMPLETE (2026-06-15)

The CL1 assessment workstream is complete. Nothing outstanding blocks live delivery:

- **9 instruments** (AT1/AT2/AT3 × assessor / student / exemplar) — finalised. The assessor + student
  instruments are **hand-authored, version-controlled, known-good** `.docx`. Generators for them were
  explored and **deliberately not pursued** — the CL1 assessors carry a much richer marking benchmark
  (per-section Satisfactory/NYS guidance + worked CBA examples + benchmark tables) than the CL2/CL3
  *generated* assessors, so forcing them into the generated structure would lose that content. Future
  changes are deliberate **manual edits** to the known-good `.docx`. (The **exemplars** do have
  generators: `scripts/s1_cl1/build_s1_cl1_at*_*_exemplar.py`.)
- **Multi-AZ RDS** resolved and recorded (see the settled decision above); **AT2 baseline
  CloudFormation** + **AT3 lab-pack** proven live in the Cloud Architecting Sandbox.
- **Records Management Policy** authored on the website (`src/content/policies/records-management.md`).
- Delivery workstream: see [[s1cl1-delivery]] (also complete).
