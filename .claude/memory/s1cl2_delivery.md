---
name: s1cl2-delivery
description: "S1-CL2 (Cloud Disaster Recovery) delivery workstream — COURSE-COMPLETE through Step 5 (Gates 1–4 PASS, 10/10 slide plans + decks; Step 5 practice: AT1+AT2 practice run sheets mirroring the assessments, LMS engagement, AT2 practice build artefacts, s1-cl2-at2 state, no-leakage verified). Step-6 gate built; the delivery plan itself is a semester-instance artefact, deferred until a real intake exists."
metadata: 
  node_type: memory
  type: project
  originSessionId: 5fe40dfd-42a4-49d7-8e7d-5da57c8df524
  modified: 2026-09-08T21:21:02.430Z
---

S1-CL2 **delivery-planning** workstream (separate from assessment authoring — see [[s1cl2-assessment]]).
General method: docs/process-delivery.md; process doc `docs/process-delivery.md`.

## Frame
CL2 = **weeks 9–18, 30 × 3h sessions (3/wk), 84h**, delivered **in parallel with CL3**. AT1's `.docx`
allocates Part A ≈ 2 wks / Part B ≈ 3 wks → **AT1 phase ≈ first 5 wks, AT2 phase ≈ last 5 wks**.

## Topic spine (10 content Topics)
- **AT1 → T1–T5** at **design/plan depth:** web-scale design · microservice design · DR
  requirements/impact · DR strategy/plan · documenting + presenting.
- **AT2 → T6–T10** at **build depth:** IaC + operate provided templates · author own template · build
  the microservice · monitoring · documenting/sign-off.
- Collectively the two ATs' coverage tags every PC and PE they assess.

## Practice vehicle (settled)
The **LMS** (`lms-global-expansion`) is the CL2 practice vehicle — web-scale-credible, so it carries the
web-scale teaching needs. (Assessed on the website, practised on the LMS — see
docs/scenario-flow.md.)

## Status (2026-07-02)
- **Gates 1–4 PASS.** Cluster spec PASS; coverage `validate-delivery-coverage` **91/91**; **all 10
  `slide_plan.md` authored + `validate-slide-plan` PASS 10/10** (the 9 missing — 02–05 design, 06–10
  build — authored to full content this session; build topics carry the region-substitution token on
  deploy DEMO/EX slides + a `[DEMO]` before each practice). The AT1 coverage specs remain **DRAFT —
  human review of allocation/depth-ceilings pending.**
- **All 10 decks built** via `build_topic_deck.py` (155 slides): 5 draw-diagram diagrams (editable
  `.drawio` + PNG) + 9 decorative `gen` heroes (via `--allow-gen`, generate-once cached; ~$0.36; the
  key needs `OPENROUTER_API_KEY` in the umbrella-root `.env`, gitignored). Heroes vetted — the model
  ignores "no text" ~1-in-9, so **human-check gen images** (topic_02 needed a regen for a typo).
- **Step 5 (practice tasks) COMPLETE** — see below. Committed to both repos.

## Step 5 — practice tasks (COMPLETE 2026-07-02; run sheets added 2026-09-08)
- **Practice run sheets built (2026-09-08):** `AT1-Practice-Design-DR-Plan-Run-Sheet.docx` (43 tasks) +
  `AT2-Practice-Microservice-IaC-Run-Sheet.docx` (22 tasks) in `delivery/practice/`, mirroring both
  assessments task-for-task through the assessments' own renderers (per docs/process-delivery.md §5 /
  docs/assessment-workbook-format.md). AT2 practice carries a *different kind* of planted fault
  (ProvisionedThroughput∧PAY_PER_REQUEST mutual exclusion vs the assessment's KeySchema mismatch).
  Machine-verified (repro ×4, leak lint, live URL sweep); human read + lab walk pending.
- **Model (docs/process-delivery.md §5):** re-scenarioing IS the no-leakage guard. The 28 `[EX]` slides
  across T1–10 are the in-class exercises (coverage guaranteed — derived from the components).
- **LMS practice engagement exists + state-correct:** `projects/lms-global-expansion/` (website repo) —
  full parity with the assessment engagement `website-global-expansion/` (MSA/role-brief/requirements/
  data-residency/consultation-notes). Practice inputs are YAT operational docs **referenced at the
  HA-hardened state**, not reproduced.
- **AT2 practice build artefacts authored** (the one real gap) — as **separate in-world docs in the
  practice project folder** (not inline like the assessment): `provided-data-store-template.md` +
  `provided-microservice-code.md`. **Comparable-but-not-identical:** different fault (ProvisionedThroughput
  vs PAY_PER_REQUEST — assessment's was a KeySchema/AttributeDefinitions name mismatch) + different code
  (LMS fields `activity_id/action/module_ref` vs `event_id/event_type/source_ip`). In-world clean (design
  region `ap-south-1`; **no lab/us-east/token meta** — that stays in the decks).
- **State-model fix:** CL2 had **no `s1-cl2-at2` state** (every other cluster has per-AT states). Added it
  and **cloned `s1-cl2-at1` → `s1-cl2-at2`** across all 61 tagged docs (underlying state unchanged for the
  build; scan found zero exceptions). Pattern for adding a per-AT state: add to `states.ts`, add the slug
  to every appearsIn that has the prior AT's slug, **add it to `src/config/projects.ts` too — the project
  records carry their own `appearsIn` (+ `stateOverrides`)**, scan for exceptions, `astro sync`.
  **That `projects.ts` step was missed in the original clone and shipped a live defect** (found 2026-09-08):
  the project-document route gates on the state being in BOTH the document's `appearsIn` and the project's,
  so every `/intranet/s1-cl2-at2/projects/…` URL 404'd — breaking the committed AT2 instrument's own links
  and the provided build artefacts, which exist only at that state. Fixed + deployed. **Verify a new state
  by sweeping the live URLs, not by trusting the frontmatter** — the repo looked correct throughout.
- **No-leakage PASS:** the website assessment *requires* the anonymous-public axis (CDN/WAF/SEO — "exposure
  an internal authenticated system does not carry"); the LMS practice is clean of it → the LMS answer can't
  be transposed to the website. LMS = CL1 assessment / CL2 practice (assessed once; practice≠assessment).
- **No "practice baseline design" gap:** unlike Ledgerline/website (student hasn't built them → a provided
  design is authored via `scripts/scenario/`), the **LMS is the learner's own CL1 build** → CL2 practice
  extends it via the HA-hardened ICT records; no dedicated provided design needed.

## Status of Step 6 — deferred by design
CL2 is **course-complete through Step 5**. The Step-6 gate `validate_cluster_delivery_plan.py` (factory step folder) is **BUILT**
(see [[delivery-run-sheet]]), but the CL2 **delivery plan itself is deferred**: the plan is a
**semester-instance** artefact whose prerequisites (a real intake's session count / days / online-vs-
classroom split) don't exist yet. It is produced later in a human-AI juggling session, validated, then
filled into `S1_CL2_Delivery_Plan.docx`. Reaching this point = CL2 is finished at the course level, not
outstanding work.

## Open
- AT1 coverage specs still **DRAFT** — human review of allocation/depth-ceilings pending.
