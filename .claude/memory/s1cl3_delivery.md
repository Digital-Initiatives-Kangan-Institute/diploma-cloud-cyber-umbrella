---
name: s1cl3-delivery
description: S1-CL3 (Cloud Infrastructure Improvement) delivery workstream — COURSE-COMPLETE through Step 5 (8-Topic spine; coverage 64/64; 8 slide plans + decks; practice = website EX tasks + a cfn-lint-clean website practice baseline modelled on the Ledgerline AT3 baseline, open improvement). Only Step 6 (delivery plan, deferred per-instance) remains.
metadata: 
  node_type: memory
  type: project
  originSessionId: 5fe40dfd-42a4-49d7-8e7d-5da57c8df524
---

S1-CL3 **delivery-planning** workstream (separate from assessment authoring — see [[s1cl3-assessment]]).
General method: docs/process-delivery.md. CL3 is the **lightest cluster** (56h nominal / 60 delivered,
weeks 9–18, 2×3h/wk, parallel with CL2). Frame: 20 sessions, **15 teaching/practice**, nominal 8 topics.

## Topic spine (8 content Topics) — soft-accepted 2026-07-02
Follows the **write-is-the-seam** AT model ([[s1cl3-assessment]]): AT1 individual Design (504 el 1–2) ·
AT2 group Team-Implementation (401 — team writes the IaC divided by the four components, NOT 504-assessed) ·
AT3 individual Implement (504 el 3–4, apply-as-update change-set).
- **AT1 → T1–T4 (design depth):** T1 analyse the baseline · T2 design for reliability (app-tier Multi-AZ +
  DB backup/restore + cross-Region DR; the **Multi-AZ-database cost-benefit rejection** is the centrepiece) ·
  T3 design for scalability + the four components (network/compute/database/storage; elastic-on-demand) ·
  T4 document + present the Solution Design → sign-off.
- **AT2 → T5–T6 (leadership depth):** T5 lead & plan the team build (401 el 1–2; allocate one component per
  member) · T6 write the IaC by component: lead/support/monitor the team (401 el 3–4).
- **AT3 → T7–T8 (build depth):** T7 deploy baseline + apply the improvement as a change-set (DB untouched —
  lab denies `rds:ModifyDBInstance`) · T8 test/refine/document the whole system + final sign-off.
Vehicle = **Ledgerline** (assessed); **website = practice vehicle**.

## Status (2026-07-02)
- **Step 1 (cluster spec):** PASS (phase gate met 2026-06-23).
- **Step 2 (topic breakdown):** 8-Topic spine soft-accepted (above).
- **Step 3 (coverage):** **`validate-delivery-coverage` PASS 64/64** — 8 `delivery/topic_NN/coverage.md`
  authored (T1 11 · T2 6 · T3 2 · T4 2 · T5 15 · T6 16 · T7 8 · T8 4); every 504+401 PC/PE/KE taught by
  ≥1 Topic. The two empty leftover scaffold dirs (topic_09/10) removed. Committed + pushed.

## Step 4 (slide plans + decks) — COMPLETE 2026-07-02
- **4a:** 8 `slide_plan.md` authored (per-topic sub-agents from each `coverage.md`), **`validate-slide-plan`
  PASS 8/8** (backwards-coverage vs coverage.md). 96 slides; image plan = 6 draw-diagram diagrams + 8 gen
  heroes. Committed `4dbe660`.
- **4b:** all 8 decks built via `build_topic_deck.py … --allow-gen` (the deck engine is now the **umbrella**
  `scripts/build_topic_deck.py`, run with the **umbrella** `scripts/.venv` which has python-pptx — NOT
  system python3; see [[umbrella-engine-architecture]]). 6
  diagrams rendered (editable `.drawio` + PNG; the 2 flowcharts + 4 arch/allocation eyeballed clean) + 8
  Nano-Banana heroes (~$0.32, generate-once cached). **Size-gated: `inspect-file-size` all 0.8–0.98 MB**
  (well under 25 MB). Committed `7ed2288` (push 408'd once on the ~7 MB binary payload over a flaky link;
  retry succeeded).
- **Process note:** run `inspect-file-size` on the built decks **before** committing (the process
  prescribes it at Step 4 — don't skip it).

## Step 5 (practice tasks) — COMPLETE 2026-07-02
Practice vehicle = the **website** (Ledgerline is assessed). Confirmed:
- **Practice engagement `website-improvement`** exists with full parity to the `ledgerline-improvement`
  assessment engagement (role-brief/consultation-notes/improvement-requirements/indian-reg/MSA/
  solution-design), tagged `s1-cl3-at1/at2/at3`. The **EX slides across all 8 topics ARE the practice
  tasks** (AT decomposed 1:1 onto the website).
- **Website practice baseline authored** — `delivery/practice-lab-pack/baseline.yaml` (+ README, .cfnlintrc),
  **modelled on the proven Ledgerline AT3 baseline**, adapted: internet-facing ALB (public site) · Linux +
  **MySQL** (not Windows/SQL Server) · single-AZ · same subnet/NAT/`!GetAZs`/region-substitution patterns.
  **cfn-lint clean**; NOT lab-proven (practice artefact — troubleshooting in class is fine). **No `improved.yaml`**
  — the assessor reference is an assessment-only thing; in practice the student applies **their own** improvement.
- **The improvement is OPEN.** The Ledgerline "no Multi-AZ DB" rule is a *legacy-SQL-Server* constraint that
  does NOT apply to the website (MySQL). Reworded the two EX slides that had imported it (topic_02 reliability,
  topic_07 deploy) so the website practice reaches its **own** data-tier call — using the Ledgerline contrast as
  a teaching device (same cost-benefit reasoning, potentially opposite answer). Decks 02 + 07 rebuilt, size-gated.
- **No-leakage:** website practice (reliability/infra improvement, MySQL, open Multi-AZ, +CDN, single-AZ start)
  is comparable-not-identical to the Ledgerline assessment (4 components, no Multi-AZ DB) — answers don't transpose;
  and it stays clear of CL2's website-ASSESSED scope (web-scale global-expansion design).

## NEXT — Step 6 (delivery plan) — deferred per-instance
The only remaining CL3 step; deferred by design (semester-instance artefact, see [[delivery-run-sheet]]).
**CL3 delivery is now course-complete through Step 5.**

## Resolved
`consolidated_uoc.md` AT-model narrative **corrected 2026-07-02** to the current model (AT1 Design 504
el 1–2 / AT2 Team-Implementation 401 el 1–4 / AT3 Implement 504 el 3–4) — the STATUS line, the
structure-section table + AT deliverables + approval moments, and the Topic 1–2 headers + Group-1
annotation. Topics 3–4 headers were already correct. Tag inventory untouched (delivery coverage 64/64 +
cluster coverage still PASS).
