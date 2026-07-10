---
name: s1cl1-assessment
description: "S1-CL1 (Cloud Design and Build) pilot cluster, assessment workstream — FINALISED (institutional review PASSED 2026-07-10): AT shape, settled cross-AT design decisions; instruments approved + FROZEN (change-control: warn + new versioned file only)."
metadata: 
  node_type: memory
  type: project
  originSessionId: 5fe40dfd-42a4-49d7-8e7d-5da57c8df524
---

> **STATUS: FINALISED (2026-07-10).** The CL1 assessment workstream is done AND the **institutional
> review / pre-validation gate has now PASSED** — the last gate. CL1's assessments are formally
> **approved for delivery and frozen**. See **Status** at the foot of this entry.
>
> **⚠ CHANGE-CONTROL — CL1 assessments are FINALISED.** Do **not** edit any CL1 instrument in place.
> Any change requires: (1) **warn the user first** + explicit go-ahead; (2) make it on a **new file**
> with the new version in the filename (`…v1.2…` / `…v2.0…`); (3) **bump the footer version**; the
> current approved file is never changed again. Full rule: [[feedback-finalised-assessments-change-control]].

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

## Status — FINALISED (institutional review PASSED 2026-07-10)

The CL1 assessment workstream is complete and has now **passed institutional review — the terminal
gate**. The instruments are approved for delivery and **frozen** (see the change-control banner at the
top). Nothing outstanding blocks live delivery:

- **9 instruments** (AT1/AT2/AT3 × assessor / student / exemplar) are final and approved. All six
  assessor + student instruments now **have generators** (`scripts/s1_cl1/build_s1_cl1_at*_{assessor,student}.py`,
  retrofitted 2026-07-09 → one generator process across all clusters, [[one-course-agnostic-mechanism]]);
  the exemplars too (`…_exemplar.py`).
- **BUT the approved copies are frozen and were hand-finished:** the institutional-review edits +
  the KE/reflection presentation tidy (2026-07-10) were applied to the **`.docx` directly**, so the
  approved `.docx` are **ahead of their generators** — a regenerate would clobber the approved copy and
  fail `validate-instrument-reproduction`. Do **not** regenerate a finalised CL1 instrument. Per the
  change-control rule, changes go to a **new versioned file**, never in place. `[TBD — needs discussion:
  whether/when to reconcile the generators back up to the approved v1.0 baseline, so future versioned
  revisions can be generator-sourced again.]`
- **Version:** the approved baseline is **v1.0** (version shown in the document footer). `[TBD — confirm
  the footer version field is present/reads v1.0 on all six approved instruments.]`
- **AT3 uses a real live Multi-AZ failover demo** (proven in the Cloud Architecting Sandbox); the AT2
  baseline CloudFormation + AT3 lab-pack deploy there.
- The **Records Management Policy** is authored on the website (`src/content/policies/records-management.md`).
- Delivery workstream: see [[s1cl1-delivery]].
