---
name: s1-cl1-cluster-current-state
description: State snapshot of S1-CL1 (Cloud Design and Build) — all three ATs at v1.0; scenario content migration to website in progress (2026-05-27)
metadata: 
  node_type: memory
  type: project
  originSessionId: cecc2119-3823-4017-82e0-21443e608ffd
---

S1-CL1 (Cloud Design and Build) is the pilot cluster being developed end-to-end. **All three ATs are at v1.0 first-draft committed to main as of 2026-05-26.** Scenario-content migration to the YAT mock website is now well underway (see [[website current state]] for the full state of that work). This memory captures cluster-AT **assessment/design** state and known pending items; full design history is in commits + `assessments/assessment_plan.md` changelog. **Delivery-planning** (sessions + teaching/exercise materials) is a separate, active workstream — see [[s1cl1-delivery-state]].

## Cluster shape (settled)

| AT | Title | Format | Primary unit | Status |
|---|---|---|---|---|
| AT1 | Business Case: YAT LMS Cloud Migration | Project Assessment — Part A (BC written) + Part B (board presentation event) | ICTICT517 | ✅ v1.0 docx populated |
| AT2 | Cloud Foundation Build: YAT LMS | Project Assessment — single-task (no Part split); deliverable = Deployment Report with appendices | ICTCLD401 | ✅ v1.0 docx populated |
| AT3 | High Availability: YAT LMS | Project Assessment — Part A (HA Design) + Part B (HA Deployment Report) | ICTCLD502 | ✅ v1.0 docx populated |

Scenario: YAT College (RTO, 175 Cremorne St, Cremorne VIC) at `<repo_root>/scenario/`, shared across the course.

## Settled cross-AT design decisions (won't re-litigate unless new evidence)

- **Project Assessment template chosen for all three ATs** — even AT2 which is single-task (per Tim 2026-05-25: "implementation is a project even if the deliverable is written")
- **502 PC reassignment AT3 → AT2:** PCs 1.3, 4.1, 4.2, 4.3 moved (per UoC text analysis, these are not HA-specific). AT3 still owns all HA-design / -evaluation / -simulation / -closure PCs.
- **MTS scope across the cluster = cloud infrastructure only.** YAT IT (in-scenario) handles LMS app deployment, MySQL data migration, cutover, organisational change management. Single source in `internal-lms-migration-role-brief-S1-CL1-AT1.md` § Scope of the MTS consulting engagement; cross-referenced from AT2 + AT3 docs.
- **AT3 is post-cutover** — LMS app already deployed by YAT IT after AT2; AT3 hardens running infrastructure in-place. No app re-deployment, no data migration, no cutover ceremony for AT3.
- **AT3 has no closure pack / no observation event / no Security Responsibilities Matrix as standalone.** Closure-flavoured PCs (5.1, 5.2, 5.3) evidenced in HA Deployment Report §6.6 + §7.5 + §7.6 (sign-off block). FS Oral Communication already evidenced in AT1's presentation event.
- **AT2 → AT3 thread loose by design.** AT2 implements a supplied baseline design; AT3 hardens it. To get students from "their own AT2 build" to "consistent AT3 starting state", the assessor distributes an AT2 baseline CloudFormation template (placeholder authored; YAML TBD) for deployment in AWS Academy at start of AT3 day.
- **AT3 maintenance window framing:** simulated Saturday late-night ~3.5h window; brief blips acceptable; must end HA-done or rolled back.

## Authored artefacts (paths)

**Per-AT docs (canonical = .docx):**
- `S1-CL1-Cloud-Design-Build/assessments/AT1/AT1-BusinessCase-{Assessor,Student}.docx`
- `S1-CL1-Cloud-Design-Build/assessments/AT2/AT2-Deployment-{Assessor,Student}.docx`
- `S1-CL1-Cloud-Design-Build/assessments/AT3/AT3-High-Availability-{Assessor,Student}.docx`

**Companion .md files in AT2 + AT3 folders** — currently kept pending Tim's review pass; per `cluster_authoring_conventions.md` §3 they get deleted post-paste once Tim accepts the docx.

**Cluster plan + UoC:**
- `S1-CL1-Cloud-Design-Build/consolidated_uoc.md` — verbatim PC/FS/PE/KE/AC with groupings; validator at `<repo_root>/scripts/validate_consolidated_uoc.py`
- `S1-CL1-Cloud-Design-Build/assessments/assessment_plan.md` — group coverage map + decisions changelog; v2 of 2026-05-23, updates through 2026-05-26

**Scenario** (lives at `<repo_root>/scenario/` per `scenario_location.md`):
- 27+ content files (public-/internal-* pages, AT-suffixed state-versioned where needed)
- `scenario/templates/` — student-fillable templates (BC, Deck, Feedback Record placeholders + Deployment Report v1.0 + HA Design v1.0 + HA Deployment Report v1.0)
- `scenario/exemplars/` — past-engagement examples (mostly empty placeholders for the batch-authoring pass)
- `scenario/assessor-resources/` — assessor-only operational artefacts (AT2 baseline CloudFormation template placeholder)
- `scenario/checklist.md` — running authoring inventory

## Pending — operational / pre-delivery

These don't block the v1.0 design but are needed before live delivery:

1. **AT2 baseline CloudFormation YAML** — `scenario/assessor-resources/at2-baseline-cloudformation.md` placeholder authored; the actual `.yaml` needs writing (~400–600 lines per the placeholder's spec)
2. **Records Management Policy** — `internal-records-management-policy.md` placeholder authored; content TBD
3. ✅ **Document templates** (Business Case, Business Case Presentation, Solution Design, Deployment Report) built as branded `.docx`/`.pptx` and live on the intranet Templates page (2026-06-01; see [[document-template-system]]). **Feedback Record: resolved — no standalone template.** Feedback/sign-off is captured in-deliverable via the Solution Design **§9 Review and Approval** block (reviewer feedback + sign-off) and the Business Case sign-off block; the Group 10 feedback PCs ride those, not a separate artefact.
4. 🟡 **Exemplar/model batch** — done: BC assessor exemplar (AT1), AT2 + AT3 deployment-report assessor exemplars, and the AccentLoitte student-model chain (BC + presentation + Solution Design + Deployment Report PDFs). Closure-pack equivalent still TBD.
5. ✅ **Supplied AT2 design** rendered as the branded Solution Design PDF on the intranet (AT2+), replacing the markdown page (draw.io network diagrams done separately).
6. **TBD items inside the docs:** placeholder URL `https://www.placeholder.com.au`, role-played names (Sam Walker / Pat Lin), Second-attempt policy specifics
7. **⚠️ AWS Academy lab — Multi-AZ RDS for AT3 (surfaced 2026-06-06 during CL2 work).** The **Learner Lab (Foundation Services)** documents *"Multi-AZ deployments not supported"* — conflicts with AT3 / Topic 13's *"convert the DB to Multi-AZ + trigger a failover"* build. **Only the live Multi-AZ DB is at risk** — compute HA (cross-AZ ASG + ALB) is fully supported. The **ACA Cloud Architecting** course (CL1's decks are built from it — "ACA M10") *teaches* Multi-AZ, so some AWS Academy environment supports it; the open Learner Lab sandbox blocks it. **Resolution (per Tim):** Kangan can enrol students in any AWS Academy course, so make the **correct enrolment an AT3 condition/resource** rather than changing content. **Actions:** (a) confirm which enrolment gives an **open-build** env that **also** permits Multi-AZ RDS (ACA graded labs are guided/fixed — verify the open lab tier); (b) one smoke test (create a Multi-AZ RDS) confirms; (c) record the required course/lab in **AT3 Resources + Assessment Conditions + assessor delivery notes**. **Fallback** if no open lab allows it: reframe DB-HA as design+template (`Multi-AZ: true`) + simulated failover (reboot/terminate). Verify before CL1 delivery — CL1 is v1.0 drafts, likely not yet run live in the lab.

## Pending — cluster waypoints (per Tim)

1. ✅ AT1 + AT2 + AT3 in institutional templates (all populated as of 2026-05-26)
2. ✅ **Per-UoC mapping documents** populated as of 2026-05-26 (commit `a66963d`). All three (`mappings/ICTCLD401_Assessment_Mapping.docx`, `ICTCLD502_Assessment_Mapping.docx`, `ICTICT517_Assessment_Mapping.docx`) have every UoC item mapped to its evidencing AT criterion code(s). Mapping was populated via `scripts/populate_mapping_docs.py` (idempotent, backs up before edit, handles single-block vs pre-split tables). During this pass, three previously-unmapped 517 FSs were assigned to existing AT1 criteria (no scope change; just claim additions to existing UoC reference columns): A4 + A8 + A12 picked up FS Get the work done; A8 picked up FS Navigate the world of work; B5 + B6 picked up FS Interact with others.
3. 🟡 **Scenario→website migration** in progress (commits `4e830d2` planning evolution, `202b7ab` public-facing pages, `9d90006` policies + references). Subsequent work uncommitted as of 2026-05-27 includes the state-folder intranet refactor, MTS + AccentLoitte MSAs + role briefs + requirements, ICT cost baselines × 3 (year-graded), ICT Strategic Plan, LMS Application Spec, ICT Environment Overview (AT1). Detail in [[website current state]].
4. ⏳ Pre-validation pass (institutional Pre-Validation Tool) on each AT
5. ⏳ Stakeholder review of the full cluster
6. ⏳ Draw.io diagrams (network diagram first; pattern: SVG embed + `.drawio` XML download)

## Reference

- Commits: `a66963d` (per-UoC mapping docs + AT1 FS additions), `38be822` (meta refresh after AT3 v1.0), `b8fc8bc` (AT3 v1.0), `6bac4ec` (AT2 v1.0 + scope clarification + 502 reassignment), `95c2e5c` (AT1 v1.0), …
- Cluster authoring conventions: see memory `cluster_authoring_conventions.md`
- Scope-of-engagement decisions: in `internal-lms-migration-role-brief-S1-CL1-AT1.md` § Scope of the MTS consulting engagement + `internal-cba-cost-inputs-S1-CL1-AT1.md`
