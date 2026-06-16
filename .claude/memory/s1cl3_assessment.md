---
name: s1cl3-assessment
description: S1-CL3 (Cloud Infrastructure Improvement, ICTCLD504 + BSBXTW401) assessment workstream — assess Ledgerline / practice website, the 3-AT individual→group→individual rhythm, owned-dimension + team-leadership evidence model.
metadata:
  type: project
---

CL3 = **Cloud Infrastructure Improvement**: **ICTCLD504** (improve cloud infrastructure) + **BSBXTW401**
(lead and facilitate a team) — assessment workstream. The **lightest** cluster (~56h, weeks 9–18,
parallel with CL2). Decisions + open questions only — what is built lives in
`S1-CL3-Cloud-Infrastructure-Improvement/`. Delivery workstream: [[s1cl3-delivery]]. General authoring
rules: docs/cluster-authoring-conventions.md.

**Identity:** *lead a team to improve a cloud system's infrastructure* — **CL1 AT3's improve-loop
widened** (security + reliability + scalability + cost, not just HA), **team-led**.

**Vehicle (per docs/scenario-flow.md):** **assesses on Ledgerline** (single-AZ cloud — mirrors
the LMS: on-prem → single-AZ cloud by end of CL1), **practises on the website**. `[ICTCLD504 KE 6]`
(object storage for static web sites) is evidenced as a **contextual knowledge question** contrasting
Ledgerline with an object-storage-dependent system — not an applied task on Ledgerline.

## AT structure (settled): three ATs, individual → group → individual
- **AT1 (individual) — Engagement Setup:** the **team plan / Role Brief** (401 el 1) + **requirements &
  analysis** of the baseline (504 el 1). The docs we pre-populate for lower clusters — here the
  student-as-lead authors them.
- **AT2 (group) — Improvement Design via led meetings:** 504 el 2 (each student **owns one dimension**:
  security / reliability / scalability / cost) + 401 el 2–4. **Collaboration is assessed here** (the
  design), not the point-and-click implementation.
- **AT3 (individual) — Implement / test / finalise their owned dimension** (504 el 3–4).
- Two approval moments: deploy sign-off at AT2 (`504 PC 2.5`); final sign-off at AT3 (`504 PC 4.3`).

## Evidence model
- **Owned-dimension model** → each student gets individual **504** evidence inside a group effort.
- **Team-leadership (401):** each student **leads ≥1 meeting** → **assessor observation checklist**
  (primary evidence, incl. *managed a conflict*) + **reflection** appendix on 2 conflicts (secondary;
  carries 401 KE 5/10) + **performance review** (el 4). How the assessor stimulates a conflict is the
  assessor's conduct — out of the instrument's scope.

## Reuse / new authoring
**Heavy reuse:** the improve-loop + lab-pack pattern from CL1 AT3 (docs/lab-pack-standard.md — now pointed
at Ledgerline's single-AZ cloud infra); the Solution Design + Deployment Report templates + generators +
scenario world from CL2 ([[s1cl2-assessment]]). **New** = the 401 instruments (team plan / Role Brief,
led-meeting observation checklist, reflection, performance review), the Ledgerline baseline lab-pack,
the Ledgerline scenario context.

## Open — authoring only (design is settled; no blocking TBDs)
Design fully resolved (team model = teams of 4 / assessor-formed / rotating-chair; vehicle;
author-fresh accepted; scenario built). **AT1 (Team Setup) is built** — assessor + student +
team-plan exemplar + generators. Coverage 10/72 until AT2/AT3 land. Remaining:
- **AT2 (group) — Analyse, Design & Approve** (the heaviest AT; both units integrate here): the new
  **Architecture Analysis** doc type (template + exemplar), the owned-dimension Solution Design
  exemplar, the new **led-meeting observation checklist**, **reflection prompt** + **performance-review
  template**, the approval presentation + sign-off record, and the AT2 student/assessor instruments.
- **AT3 (individual) — Implement:** as-deployed Deployment Report exemplar, AT3 student/assessor
  instruments, and the **Ledgerline baseline lab-pack**.
- **`mappings/`** — per-unit Assessment Mapping docs (504 + 401), generated as CL1/CL2's were.
- Downstream external gate (as CL1/CL2): institutional **Pre-Validation**.
