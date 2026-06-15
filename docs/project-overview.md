# Project Overview — Diploma of IT (Cloud & Cyber Security) Cluster Refactor

## Background

The Diploma of IT (Cloud and Cyber Security) was originally developed as a **multi-TAFE collaboration**: each participating TAFE authored a different subset of the 21 units, with no shared spine across them. Kangan was a participant in that collaboration. The current state has two problems that flow directly from how it was built:

1. **Significant cross-unit duplication.** Different units assess the same or very similar things, creating wasted assessment effort for both learners and assessors and confusion about which assessment "owns" a competency.
2. **No continuity of narrative or delivery.** Because units were authored independently by different TAFEs, there is no shared spine — context, examples, vocabulary, scenarios, and tooling vary unnecessarily between units that learners experience back-to-back.

The product also includes a mix of authoring styles, document conventions, and folder structures, which itself adds friction for delivery staff and validators.

**Reuse permissions (working assumption, TBD pending legal confirmation).** As a participant in the original multi-TAFE collaboration, Kangan has permission to reuse all materials in `original_materials/` — including content authored by other participating TAFEs (e.g. the YAT College case study attributed to Melbourne Polytechnic). Work is to proceed on that assumption. Tim is double-checking with the Kangan legal team; flag any actions that would be hard to reverse if the assumption turns out to be wrong.

**Fallback if reuse is not permitted.** Tim's standing instruction for this work is to **reuse existing material wherever possible**. If legal advises that specific source content (e.g. the YAT College case study) cannot be reused as-is, the fallback is to **reauthor the affected materials under a different name with equivalent but distinct content** — preserving the structural shape (scenario type, document set, AT mappings) so the rest of the cluster work is unaffected. The architectural decisions (3-AT structure, scenario-spine approach, contextual reflective questions, document inventory) do not depend on any specific source identity and remain stable across this contingency.

## Goal

Reorganise and partially refactor the diploma so that **clusters of related units** become the atomic unit of delivery and assessment. Within each cluster, related content is delivered cohesively and overlapping assessments are merged or remapped. Across clusters, duplication is **explicitly tolerated** — the cluster is the boundary, not the course.

Stated more concretely, by the end of the project we want, for each cluster:

- A clear delivery narrative — what story does this cluster tell, in what order, with what hands-on artefacts?
- A consolidated assessment plan — what is assessed once, what is reused as evidence across units within the cluster, and how do unit assessment mappings tie back to the original training package criteria.
- A set of teaching-and-learning materials that draw on the existing content where viable, refactored where reuse is partial, and freshly authored only where there is a real gap.

## Delivery context

**Preferred cloud platform:** **AWS.** Cloud-bearing clusters target AWS by default, and existing source materials are already AWS-aligned (e.g. ICTCLD401's hands-on practical uses EC2/VPC/RDS/IAM/ASG; ICTCLD502 references the AWS Academy Cloud Architecting course directly). Other vendors are not excluded but require an explicit case.

**Student lab access:** students have access to both **AWS Academy Cloud Foundations [104469]** and **AWS Academy Cloud Architecting [172221]**. These are the authorised lab environments for cluster delivery — assessment design should align to what those courses provide rather than assume access to a free-form personal AWS account.

**Scenario architecture (2026-05-23):** the cluster scenario materials (YAT College) live at `<repo_root>/scenario/` rather than inside any one cluster's folder. Intent: the scenario is **shared across the course** — the same YAT organisation appears in every cluster, with state-versioned documents evolving as the course progresses. Cluster folders reference scenario content abstractly (e.g. "the YAT intranet's ICT Strategic Plan page") rather than by relative filesystem path, so the structure is independent of any one cluster's needs.

## Scope

**In scope:** the 21 units listed in `clusters.md`, grouped into 7 clusters (3 cloud + 4 cyber). Reuse of existing material in `original_materials/`, refactoring of existing material, and creation of new material where required.

**Out of scope (working assumption — confirm):** ICTPRG549 and ICTSAS518, which have source materials present but do not appear in the cluster list.

**No inherited learning/assessment material:** VU23226 (Enterprise Systems) and ICTCLD505 (Cloud Disaster Recovery) have no folders in `original_materials/`. ICTCLD505's UoC reference (`_Complete_R1.docx`) is present in `courseware/`, so we have a defined target to author against. **VU23226 has no UoC reference either** — that needs to be obtained upstream (training.gov.au / VETNet) before the Enterprise Systems mapping can include it. This is the one narrow exception to the read-only-originals principle: we don't chase source content upstream, but we do need the unit's UoC reference document, because without it there's no defined target to author against.

## Operating principles

- **Cluster is the unit of delivery and assessment.** Cross-cluster duplication is acceptable; intra-cluster duplication is what we are targeting for removal.
- **`original_materials/` is read-only reference.** We don't try to fix, complete, or update the originals in place. Whatever we decide to use gets **copied** into the workspace (per cluster) and the copies become the working artefacts. Gaps in the originals are gaps to author against, not gaps to chase upstream.
- **Reuse > refactor > rewrite.** Existing material is the default; only create new content where reuse is not viable.
- **Maintain mapping integrity.** Whatever we do, every Performance Criterion, Performance Evidence, Knowledge Evidence, Foundation Skill and Assessment Condition for every unit must still be assessed somewhere. The cluster's mapping document is the audit trail.
- **Document decisions, not just outcomes.** When two units overlap and we pick one assessment over another, the rationale needs to live somewhere we can find later — both for validation and for the inevitable future audit.

## Constraints and risks

| Item | Why it matters |
|---|---|
| **ICTCLD505 has no inherited learning/assessment source** (UoC reference available). | Cluster will author fresh content for this unit. Plan capacity accordingly. |
| **VU23226 has no inherited source *and* no UoC reference.** | The UoC reference must be obtained before the Enterprise Systems cluster mapping can include it. Narrow upstream ask, but real. |
| **Source materials are inconsistent in structure.** | Comparing units to find overlap is harder when documents are organised differently and named differently. A normalisation step (the per-unit summary, in our own workspace) is needed before meaningful audit work can start. |
| **Two units (ICTCLD503, ICTCLD504) have an updated set of materials in a separate folder.** | Risk of referencing stale content unless we explicitly nominate the updated set as the canonical reference and ignore the older copies. |
| **Cluster assignments are "suggested" but not yet final.** | Some unit placements may shift after content audit reveals actual overlap (e.g. ICTSAS526 DR/contingency vs ICTCLD501 Cloud DR). |
| **Tracked changes / comments may exist inside .docx files.** | Worth knowing before we treat any file as the "current" version. |
| **Tim is one person.** | Pace and prioritisation matter. Critical-path work (audit + cluster scope-of-work decisions) needs to come before material refactoring. |

## Success criteria

The project is "done" when each cluster has:

1. A delivery plan covering scope, sequencing, and assessment strategy.
2. A consolidated assessment pack (assessor + student versions) that demonstrably covers every required mapping element for every unit in the cluster.
3. A learner resource / teaching pack covering the cluster narrative.
4. A traceability artefact (unit mapping document) showing where each PC/PE/KE/FS/AC is taught and assessed within the cluster.
5. A record of which source items were reused as-is, which were refactored, and which were newly authored — so validators can see the lineage.

All cluster outputs are authored against the templates in `templates/` at the workspace root (delivery plan, assessment mapping tool, project + written assessment templates for both student and assessor versions). The institutional `_TEMPLATES/` folder inside `original_materials/` is a *reference only* — `templates/` is the format-of-record for new work.

## Method (working approach)

Roughly four phases, run mostly in sequence with some overlap:

1. **Inventory and normalise** — produce a per-unit single-page summary covering "what does this unit currently look like, what does it assess, and what is its delivery shape". This is the prerequisite for any meaningful overlap analysis.
2. **Cluster audit** — for each cluster, find overlapping content and overlapping assessment, decide what to merge, what to drop, and what to keep. Confirm cluster composition.
3. **Cluster build** — produce the cluster deliverables (delivery plan, consolidated assessment, learner resource, mapping).
4. **Validation pass** — internal review against pre-validation tool + training package mapping before submission.

Phases are detailed in `work_breakdown_structure.md`.
