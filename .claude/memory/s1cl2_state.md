---
name: s1-cl2-cluster-state
description: S1-CL2 (Cloud Disaster Recovery, ICTCLD501/503/505) durable design decisions — vehicle, AT structure, the DR≠design≠residency reframe, scenario spine, DR/microservice/residency calls, AWS Academy constraints. Build artefacts live in the repo (git authoritative), not here.
metadata:
  type: project
---

S1-CL2 (Cloud Disaster Recovery) = **ICTCLD501 · ICTCLD503 · ICTCLD505**. Decisions + open questions only — for what is *built* (instruments, exemplars, generators) read the repo: `S1-CL2-Cloud-Disaster-Recovery/` + main `scripts/`. CL1 is the done pilot ([[s1-cl1-cluster-current-state]]).

**Vehicle (per [[scenario-flow-convention]]):** assesses on the **website** (`website-global-expansion`), practises on the **LMS** (`lms-global-expansion`). Plan + consolidated_uoc re-pointed. **AT1 fully re-pointed to the website + committed (`b70e556`, unpushed)**; **AT2 exemplar/instruments are still LMS-framed → next** (the substance transfers unchanged except the contrast below).

## AT structure (settled)
- **AT1 — Design & DR Plan, three parts:** **A** Solution Design (503 *design*: web-scale + the microservice) · **B** DR Plan (501, pure recovery) · **C** presentation of A+B for approval (501 element 5 = the design-approval gate, and the verbal KE Q&A). A and B are **separate documents**.
- **AT2 — single Deployment Report** (503 *build* + 505 IaC + monitoring), implementing the AT1 design.
- **Two approval moments:** design approval at AT1 (501 el 5); build sign-off at AT2 (503/505 el 4).
- **KE evidencing (settled):** a written **Knowledge Evidence appendix** per report is the *mandatory* location — KE is OUT of the report bodies. The **instrument** carries the contextual KE *questions* (student answers them in the appendix); Part C re-covers them verbally (C5). Templates are **KE-free** (instrument-driven + shown in the exemplar's appendix). Allocation: **A12 = 503 KE 3/4/6** (Solution Design); **B15 = 501 KE 1–6** (DR Plan). **`501 KE 6` (monitor/alerts) moved AT2→AT1 Part B** (disaster detection — all of 501 now in AT1).

## Key reframe — three separate concerns (Tim's; do NOT re-tangle)
*Disaster recovery* (501) = "what if the system goes down" → DR Plan. *Design* (503: web-scale + the microservice) → Solution Design. *Data residency* = an **input constraint**, NOT a deliverable (no compliance-plan artefact — no UoC asks for one). **The microservice lives in the Solution Design, never the DR plan.**

## Scenario spine
- **Offshore-India partnership** (GIFT City, a *single* partner) → the assessed system must serve a global user base + be region-recoverable + be provisioned as code. **One event drives all 3 units.**
- **Depth = "serve multiple regions," NOT multi-region data replication** — met by global serving (CloudFront) + a DR *plan* + *parameterised* IaC.
- **Practice↔assessment contrast:** LMS practice = **authenticated cohort**; website assessment = **anonymous public** (pulls in CDN / WAF / bot-mitigation / SEO). Applied only as far as natural — nothing else contrived.

## DR / microservice / residency design calls
- **DR = backup-and-restore.** Recovery region = a second **Australian** region (Melbourne `ap-southeast-4`), **NOT India** — recovering AU data into India would itself be a new cross-border transfer; staying onshore keeps the DR plan clean. RTO 4h / RPO 1h (adjustable). Web-scale = CloudFront + the existing ASG.
- **Microservice (503):** a **webhook-driven, serverless, append-only audit/access-log service**. The assessed task is designing the webhook payload contract; the source system is a generic webhook producer (no live system needed).
- **Residency:** mock requirements docs *grounded in real law*, **light dial** (a bounded India slice). Drivers: **DPDP Act 2023** (permissive — main data may stay in AU) + **CERT-In 2022** (operational logs in India 180 days). Accounting's analogue = **Companies Act** (books-of-account backup in India), *not* RBI.
- **DR-plan document model:** one DR Plan format throughout (existing → student-produced share it). In-world: a DR plan was omitted from the cloud cutover contract → it is deprecated → this engagement rectifies it; students recreate the cloud DR plan as the deliverable.
- **CL2 baseline = a provided HA-hardened website snapshot** ([[website-current-state]]).

## AWS Academy (Learner Lab) constraints — verified
- Learner Lab confirmed; **`us-east-1` + `us-west-2` only** (no Mumbai `ap-south-1`); **RDS Multi-AZ unsupported**. `us-west-2` is the **India stand-in** (primary `us-east-1` = AU). No IAM-role creation → reuse the fixed **`LabRole`**.
- **Serverless on `LabRole` PROVEN LIVE (2026-06-09):** API-GW → SQS → Lambda → DynamoDB deploys + runs via CloudFormation, `LabRole` serving as both Lambda execution role and API-GW→SQS credentials. Build ATs can be hands-on (joins the EC2/RDS baseline proven at CL1 AT3, [[lab-pack-standard]]).
- **Template↔exemplar parity:** the exemplar's body shape MUST equal the template's; the only exemplar-extra is the KE appendix (instrument-driven). Keep the report **validation/approval sections** in the exemplars (DR §7, SD §11) to match the templates — el-5/approval is the Part C *activity*, the section is its written *record*. The **Solution Design + Deployment Report templates are SHARED with CL1** (forked into web-scale / serverless variants, state-gated by slug) → do NOT strip them; the **DR-plan template is CL2-only**. See [[document-template-system]].

## Open
- **AT1 — DONE & committed `b70e556` (unpushed):** all three exemplars + assessor + student instruments re-pointed to the website, KE appendices added, KE 6 → Part B. End-to-end complete.
- **AT2 — NEXT:** re-point LMS→website (microservice build + IaC + monitoring); **drop `501 KE 6`** (now in AT1 B15); add the KE-appendix structure (503 KE 1/2/5 + 505 KE 1–11) with the KE questions in the instrument; same template-parity approach as AT1.
- **501/503 standalone source assessments not in repo** → Step-3 reuse audit blocked; **505 is greenfield** — author fresh meanwhile.
- Per-AT delivery TBDs (time allowed, location); cluster closeout (per-unit Assessment Mapping docs, a UoC-coverage validator, institutional **Pre-Validation**); **[VERIFY]** legal/residency wording before it reaches students.
- Lab-pack **format** choice (separate runnable pack vs `.docx` appendices) — a format call now, not a capability one.
