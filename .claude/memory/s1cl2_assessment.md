---
name: s1cl2-assessment
description: S1-CL2 (Cloud Disaster Recovery, ICTCLD501/503/505) assessment workstream — durable design decisions: vehicle, AT structure, the DR≠design≠residency reframe, scenario spine, DR/microservice/residency calls, lab usage, template parity.
metadata:
  type: project
---

S1-CL2 (Cloud Disaster Recovery) = **ICTCLD501 · ICTCLD503 · ICTCLD505** — assessment workstream.
Decisions + open questions only; for what is *built* read the repo
(`S1-CL2-Cloud-Disaster-Recovery/` + main `scripts/`). Delivery workstream: [[s1cl2-delivery]]. General
authoring rules: docs/cluster-authoring-conventions.md.

**Vehicle (per docs/scenario-flow.md):** assesses on the **website** (`website-global-expansion`),
practises on the **LMS** (`lms-global-expansion`). **AT1** = Design + DR Plan; **AT2** = implement the
website's audit-log microservice (503 build + 505 IaC + monitoring). The practice↔assessment contrast
below applies.

## AT structure (settled)
- **AT1 — Design & DR Plan, three parts:** **A** Solution Design (503 design: web-scale + the
  microservice) · **B** DR Plan (501, pure recovery) · **C** presentation of A+B for approval (501
  element 5 = design-approval gate + verbal KE Q&A). A and B are **separate documents**.
- **AT2 — single Deployment Report** (503 build + 505 IaC + monitoring), implementing the AT1 design.
- **Two approval moments:** design approval at AT1 (501 el 5); build sign-off at AT2 (503/505 el 4).
- **KE evidencing (settled):** a written **Knowledge Evidence appendix** per report is the *mandatory*
  location — KE is OUT of report bodies; the **instrument** carries the contextual KE *questions*
  (answered in the appendix); Part C re-covers them verbally (C5); templates are **KE-free**. CL2
  allocation: **A12 = 503 KE 3/4/6** (Solution Design); **B15 = 501 KE 1–6** (DR Plan); **`501 KE 6`
  (monitor/alerts) in AT1 Part B**.
- **Coverage:** AT1 + AT2 together evidence every PC/FS/PE/KE in `consolidated_uoc.md` — the
  cluster-coverage validator passes (105/105). Foundation Skills are **co-evidenced** through the
  technical deliverables and troubleshooting (assessment plan G11), noted in the marking guides rather
  than assessed as separate criteria.

## Key reframe — three separate concerns (Tim's; do NOT re-tangle)
*Disaster recovery* (501) = "what if the system goes down" → DR Plan. *Design* (503: web-scale + the
microservice) → Solution Design. *Data residency* = an **input constraint**, NOT a deliverable (no UoC
asks for a compliance-plan artefact). **The microservice lives in the Solution Design, never the DR
plan.**

## Scenario spine
- **Offshore-India partnership** (GIFT City, a *single* partner) → the assessed system must serve a
  global user base + be region-recoverable + be provisioned as code. **One event drives all 3 units.**
- **Depth = "serve multiple regions," NOT multi-region data replication** — met by global serving
  (CloudFront) + a DR *plan* + *parameterised* IaC.
- **Practice↔assessment contrast:** LMS practice = **authenticated cohort**; website assessment =
  **anonymous public** (pulls in CDN / WAF / bot-mitigation / SEO). Applied only as far as natural.

## DR / microservice / residency design calls
- **DR = backup-and-restore.** Recovery region = a second **Australian** region (Melbourne
  `ap-southeast-4`), **NOT India** (recovering AU data into India = a new cross-border transfer; onshore
  keeps the DR plan clean). RTO 4h / RPO 1h (adjustable). Web-scale = CloudFront + the existing ASG.
- **Microservice (503):** a **webhook-driven, serverless, append-only audit/access-log service**.
  Assessed task = designing the webhook payload contract; source = a generic webhook producer (no live
  system needed).
- **Residency:** mock requirements docs *grounded in real law*, **light dial** (a bounded India slice).
  Drivers: **DPDP Act 2023** (permissive — main data may stay in AU) + **CERT-In 2022** (operational
  logs in India 180 days). Accounting's analogue = **Companies Act** (books-of-account backup in India),
  not RBI.
- **DR-plan document model:** one DR Plan format throughout. In-world: a DR plan was omitted from the
  cloud cutover contract → deprecated → this engagement rectifies it; students recreate the cloud DR
  plan as the deliverable.
- **CL2 baseline = a provided HA-hardened website snapshot** (docs/website-architecture.md).

## Lab (AWS Academy Learner Lab) — CL2 usage
- **`us-west-2` is the India stand-in** (primary `us-east-1` = AU); Mumbai `ap-south-1` is not available
  in the Learner Lab. (General Learner Lab constraints + the serverless-on-`LabRole` capability live in
  docs/lab-pack-standard.md.)

## Template parity
The exemplar's body shape MUST equal the template's; the only exemplar-extra is the KE appendix
(instrument-driven). Keep the report validation/approval sections in the exemplars (DR §7, SD §11) to
match templates. The **Solution Design + Deployment Report templates are SHARED with CL1** (forked into
web-scale / serverless variants, state-gated by slug) → do NOT strip them; the **DR-plan template is
CL2-only**. See docs/document-template-system.md.

## Open — external gates only (authoring + coverage are complete: 105/105)
Nothing further is authorable here; the only remaining gate is the **institutional Pre-Validation**
meeting (the colleague validation Tim will arrange). Minor: AT1 working title / website `s1-cl2-at1`
label may broaden to "Design & DR Plan"; per-AT time/location conditions sit with [[s1cl2-delivery]].

**Residency/legal content — settled, do NOT re-flag.** The India residency/legal framing (DPDP Act,
CERT-In, the Companies Act analogue) is LLM-grounded and accepted as-is: this is an imaginary
pre-university case study, not a real compliance deliverable, so no legal review is engaged. Applies
across clusters (CL2 + CL3). Don't reopen it as a `[VERIFY]`.
