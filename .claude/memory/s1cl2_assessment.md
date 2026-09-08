---
name: s1cl2-assessment
description: S1-CL2 (Cloud Disaster Recovery, ICTCLD501/503/505) assessment workstream — durable design decisions: vehicle, the workbook AT structure, the DR≠design≠residency reframe, scenario spine, DR/microservice/residency calls, lab usage, and which template survives.
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

## AT structure (settled — converted to the workbook format 2026-09-01)
Both instruments are **guided workbooks** per docs/assessment-workbook-format.md: one document the
student works through task by task, authored once and rendered blank for the student / worked for the
assessor. Task numbering is **continuous across an instrument** and criterion codes are **unique across
the cluster** — both are tooling requirements, not style (see the format doc).
- **AT1 — Design & DR Plan, three parts, 43 tasks + 7 knowledge questions, one continuous sequence:**
  **A** design (503: web-scale + the microservice, tasks 1–19) · **B** DR plan (501 el 1–4, tasks
  20–37) · **C** approval (501 el 5, tasks 38–43; the first two are unmarked preparation).
- **AT2 — the microservice + IaC build**, 22 tasks + 3 knowledge questions (503 build + 505 + monitoring).
- **Two approval moments:** design approval at AT1 (501 el 5); build sign-off at AT2 (503/505 el 4).
- **KE evidencing:** a **knowledge-questions section in each workbook**, asked about the student's own
  design and build; Part C re-covers them verbally. (Superseded the per-document KE appendix, which went
  with the deliverable templates.)
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

## Which template survives, and why (settled 2026-09-01)
**One: the DR Plan.** `[ICTCLD501 AC 3]` names "reporting standards for documenting and communicating
disaster recovery plan", so the plan is a real document — AT1 task 37 assembles the worksheet's answers
into the YAT template, and **both the workbook and the plan are submitted**; the plan is what is marked
for `[ICTCLD501 PC 4.3]`. Its exemplar survives with it.

**Nothing else.** ICTCLD503's and ICTCLD505's assessment conditions are environment conditions and name
no document format, so their "document and justify" criteria are met by the worksheet. `[ICTCLD501 PC
5.1]` asks for a **verbal** walkthrough, so Part C needs no deck. The Solution Design, Deployment Report
and presentation templates and their exemplars are retired. See docs/assessment-workbook-format.md for
the quote-the-AC test.

## Open — external gates only (authoring + coverage are complete: 105/105)
Nothing further is authorable here; the only remaining gate is the **institutional Pre-Validation**
meeting (the colleague validation Tim will arrange). Minor: AT1 working title / website `s1-cl2-at1`
label may broaden to "Design & DR Plan"; per-AT time/location conditions sit with [[s1cl2-delivery]].

**Residency/legal content — settled, do NOT re-flag.** The India residency/legal framing (DPDP Act,
CERT-In, the Companies Act analogue) is LLM-grounded and accepted as-is: this is an imaginary
pre-university case study, not a real compliance deliverable, so no legal review is engaged. Applies
across clusters (CL2 + CL3). Don't reopen it as a `[VERIFY]`.


## Done, don't redo
The rework to the workbook format is **complete** for both ATs. Gates 1, 2, 4, 8, 9, 10 and 11 all pass;
the mapping documents are regenerated and machine-validated. What remains is human: the institutional
Pre-Validation meeting, and the 34 FS/AC closest-fit cells in the mapping documents that the validator
flags as advisory because they are not benchmark-traceable.
