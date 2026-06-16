---
name: s1cl3-assessment
description: S1-CL3 (Cloud Infrastructure Improvement, ICTCLD504 + BSBXTW401) assessment workstream — the write-is-the-seam AT model (504 individual on design+deploy, 401 on the divided YAML write), and why.
metadata:
  type: project
---

CL3 = **Cloud Infrastructure Improvement**: **ICTCLD504** (improve cloud infrastructure) + **BSBXTW401**
(lead and facilitate a team) — assessment workstream. The **lightest** cluster (~56h, weeks 9–18,
parallel with CL2). Decisions + rationale only — built artefacts live in
`S1-CL3-Cloud-Infrastructure-Improvement/`. Delivery: [[s1cl3-delivery]]. Authoring rules:
docs/cluster-authoring-conventions.md.

## The governing insight (write-is-the-seam, 2026-06-16)
504 is a *technical* unit → its evidence must be **individual**. 401 is a *leadership* unit → it needs a
**real team with divided, individually-accountable work**. The tension is resolved by seeing that of the
three jobs — **design / write the IaC / deploy** — only the **write is free to divide**: **design must be
individual** (`504 el 1–2`) and **deploy must be individual** (`504 el 3`), but **writing the
CloudFormation is NOT assessed by 504** — that is ICTCLD505, done in CL2. So the **divided YAML write
(by component) is 401's vehicle**, and it touches no individual 504 evidence. Neither unit is compromised.

## AT model (settled)
- **AT1 (individual) — Design** (`504 el 1–2`): **Part A** Solution Design — analyse the baseline + design
  the whole improvement across all four concerns (reuse CL2 Solution Design type; its *Review of the
  Existing Architecture* section **is** the analysis — no separate "Architecture Analysis" type).
  **Part B** present for review + sign-off-to-proceed (`PC 2.4/2.5`, FS Oral — an observed individual oral).
- **AT2 (group) — Team Implementation** (`401 el 1–4`, entirely): **Part A** project/team plan + allocate
  one IaC **component** to each member. **Part B** the team **writes the CloudFormation for the agreed
  design, divided by component + integrated**, across individually-led meetings; coordinate/support/monitor
  each against the plan/manage conflict; validate the combined template at a team sign-off gate. *(The
  write is the team-work vehicle — NOT 504-assessed.)*
- **AT3 (individual) — Implement** (`504 el 3–4`): each deploys the combined template in their own lab and
  **demonstrates/tests/refines/documents the WHOLE system** (all four concerns) + final sign-off (`PC 4.3`).
  AT3 demonstrates the whole (not a component) — fine, because 401's division already lives in the AT2 write,
  so AT3 is free to be maximal individual 504.

## Key calls
- **No business case** — neither UoC requires one and it would precede the design; the 504 approval gate is
  the **AT1 design presentation**; cost-benefit rides inside the Solution Design (cost is a design concern).
- **The agreed "to be" design is provided** to AT2 (AT1 each designs individually first, assessed; then the
  engagement adopts one agreed design — the provided model the AT1 exemplar doubles as). An assessor
  **reference combined template** is the fallback so a broken team integration can't block AT3 individual
  evidence.
- **Scalability = elastic-capacity-on-demand, demonstrable by test — NOT forecast load growth.** This is
  what lets every component carry a real scalability story on an internal low-load finance system without
  breaching IR-2 (over-provisioning would be the gold-plating IR-2 forbids).
- **Design content (confirmed):** Multi-AZ HA (RDS Multi-AZ + multi-AZ compute); parameterised
  CloudFormation; a **light India residency slice** (CERT-In logs + Companies-Act books-of-account only —
  main system stays in Sydney, DPDP permits). Components = network / compute / database / storage.

## Reuse / build status
**Reuse:** CL1 AT3 improve-loop + lab-pack pattern; CL2 **Solution Design** (AT1) + **Deployment Report**
(AT3) templates/generators + scenario world; students' CL2 (505) IaC skill (the AT2 write reuses it, not
re-assessed). **New:** the AT2 project/team-plan + divided-write spec, the led-meeting observation checklist,
the reflection prompt, the deployable improved lab-pack + reference fallback.
- **Build status:** previously-built AT1 "Team Setup" artefacts → repurposed into **AT2 Part A**. **AT1
  (Solution Design) and AT3 (Deployment Report) are unbuilt.** `scripts/s1_cl3/build_s1_cl3_at1_*` +
  `assessments/AT1/*` need renaming/relocating to AT2.

## Open
- **`[TBD]` component breakdown** — confirm the ~4 IaC modules (network/compute/database/storage) = the
  AT2 write-allocation units. Constraint relaxed vs before: each need only be a separable IaC unit (AT3
  demonstrates the whole), not independently carry all four concerns.
- Downstream: scenario `IR-6` wording (re-point "Improvement Business Case" → the Solution Design); the
  institutional **Pre-Validation** gate.
