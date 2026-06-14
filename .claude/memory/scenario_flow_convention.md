---
name: scenario-flow-convention
description: Cross-cluster scenario model — system↔cluster assessment/practice matrix, no-leakage invariant, the per-cluster scenario docs, the LMS/Website/Ledgerline state progressions, and what's built vs outstanding.
metadata:
  type: project
---

**Source of truth: `scenario/scenario-flow.md`** (repo). Each S1 cluster has one **assessment** + one **practice** vehicle; a small system set (LMS, Website, Ledgerline) rotates through both roles.

| | Assessment | Practice |
|---|---|---|
| CL1 | LMS | Ledgerline |
| CL2 | Website | LMS |
| CL3 | Ledgerline | Website |

**No-leakage invariant:** every system is *assessed* in ≤1 cluster; cross-cluster reuse is always on the *practice* side. Practice-system ≠ assessment-system in every cluster.

**Per-cluster scenario docs:** `scenario/cluster-N-scenario-{assessment,practice}.md` (six lean deltas; replaced `cluster-2-scenario.md`). Human-facing docs are current-state only ([[feedback-process-docs-current-only]]).

## System state progressions (each tracks the LMS)

- **LMS:** on-prem (cl1-at1/at2) → single-AZ cloud (cl1-at3) → Multi-AZ HA (cl2/cl3). ICT state docs: `environment-overview{,-post-cutover,-ha-hardened,-cl3}` etc.
- **Website:** on-prem → single-AZ pilot (2023; CL1 + **CL3 practice** start state) → **HA-hardened (CL2 assessment baseline, PROVIDED)**. The website **diverges**: cl2 = HA, cl3 = single-AZ. So the `-ha-hardened` ICT docs were **split**: `-ha-hardened` = cl2 (website HA), `-cl3` = cl3 (website single-AZ); `website-server-status` (single-AZ, cl1+cl3) + `website-server-status-ha` (cl2). The HA website = output of CL3 website-improvement practice, provided directly so CL2 doesn't depend on it. See [[website-current-state]].
- **Ledgerline (DECIDED — mirrors LMS):** on-prem (cl1-at1/at2) → **single-AZ cloud (cl1-at3, cl2, cl3)** → **never HA in the canonical state**; **CL3 improves it from single-AZ**. (Teaching-vs-assessment slip accepted: they may harden it in CL1 teaching, but canonical stays single-AZ through CL3.) The single-AZ Ledgerline architecture already exists: the **Accounting Baseline Solution Design** + `for-documents-not-website/network-accounting-baseline-singleaz.drawio` = the CL3 starting-state doc.

## CL3 framing
Student-facing text says **"improvement"** (open-ended; may or may not be HA — the unit doesn't require HA), NOT "HA hardening." Slugs (`website-ha-hardening`, `ledgerline-ha-hardening`) are fine; displayNames are "…Cloud Infrastructure Improvement". **Main CL3 focus = planning + team leadership (BSBXTW401); the 504 technical side is light ("ticks in boxes").** 3 ATs individual→group→individual; owned-dimension model.

## Built & committed
- **CL2 assessment fully supported:** `website-global-expansion` project (5 docs — MSA/role-brief/requirements/consultation/data-residency; **starts HA-hardened**, adds global/DR/IaC/microservice) + HA website ICT state + **Website HA Solution Design** (`build_website_ha_solution_design.py` → docx/PDF + Multi-AZ diagram). `lms-global-expansion` is the CL2 **practice** exemplar (LMS).
- **CL3 practice (website):** single-AZ baseline + ICT cl3 state + Baseline Solution Design + `website-ha-hardening` project (the canonical improvement → HA = CL2's baseline).
- Diagrams: Solution-Design figures live in `public/diagrams/for-documents-not-website/`; intranet network diagrams stay in `public/diagrams/`.
- Commits: website `5960e29` (HA state + ICT split), main `5efa823` (HA generator). Earlier: website `72fb4a3`, main `c9a5c0f` (scenario docs).

## Resolved TBDs
CL2 baseline (= provided HA website); Ledgerline cloud timeline (= mirrors LMS, single-AZ by cl1-at3); CL2 practice↔assessment contrast (= LMS is the worked exemplar/practice, website is the assessment — system-transfer).

## OUTSTANDING (next session)
1. **Ledgerline state mirror — DONE** (commits `008bfdc` narrative+infra-spec, `f501926` network+inventory, `186e82b` cloud app-spec+costing). Ledgerline = single-AZ cloud at cl1-at3/cl2/cl3 with full LMS doc parity: `accounting-server-status-cloud` + `accounting-application-spec-cloud` + `accounting-operational-costing-cloud` (all cl1-at3/cl2/cl3); on-prem `accounting-server-status`/`-application-spec`/`-operational-costing` narrowed to cl1-at1/at2; env-overview/network/inventory accounting → single-AZ AWS across the 3 states.
2. **CL3 assessment build-out (Ledgerline):** the team-improvement engagement docs (planning/teamwork-heavy, BSBXTW401) + light 504.
3. **Re-point cascade — PLANS DONE (2026-06-08, uncommitted in `diploma-cloud-cyber`).** Re-pointed: CL2 `assessment_plan.md` (LMS→website assess, Accounting→LMS practice); CL3 `assessment_plan.md` + `consolidated_uoc.md` (website→Ledgerline, + 2-AT→3-AT realign + KE-6 contextual-Q resolution); CL2 scenario contrast (`cluster-2-scenario-{practice,assessment}.md`: authenticated cohort vs anonymous public). CL2 `consolidated_uoc` needed no change (vehicle-neutral, already three-part-AT1). **Remaining:** the CL2 AT1/AT2 `.docx` instruments + their ~11 generator scripts are still **LMS-framed** — regeneration **deferred** until the plan is signed off; CL2 delivery Topic docs partly **deleted** (redo after assessments final — [[s1cl2-delivery-state]]). See [[s1-cl2-cluster-state]], [[s1cl3-state]].
4. **Network diagrams — DONE** (commits `dc1ed0b` sources, `4779ab7` SVGs exported by Tim): accounting shown decommissioned→AWS in all three topology diagrams; shared end-state diagram FORKED — `network-at3-end-ha-hardened` (cl2, website HA) vs new `network-at3-end-cl3` (cl3, website single-AZ); `network-diagram-cl3.md` repointed; all SVGs regenerated.
5. **CL3 projects page — DONE** (commit `1076967`): added `lms-cloud-infrastructure`, `lms-replacement`, `accounting-cloud-migration` to the cl3 listing (completed). The two CL2 global-expansions were intentionally left OUT of cl3 (concurrent CL2 work, not history relative to CL3) — revisit if CL2/CL3 timing says otherwise. General rule recorded: a completed project should persist (as Completed) into later states.

## UNCOMMITTED right now
`diploma-cloud-cyber` repo (the re-point cascade, Rule-5 awaiting Tim's go): CL2 `assessment_plan.md`; CL3 `assessment_plan.md` + `consolidated_uoc.md`; `scenario/cluster-2-scenario-{practice,assessment}.md`; **deletions** of `S1-CL2-.../delivery/planning/cl2-teaching-topics-draft.md` + `delivery/topic_{01,02,03,05}/coverage.md`. (Website repo is clean/pushed at `4779ab7`.)
