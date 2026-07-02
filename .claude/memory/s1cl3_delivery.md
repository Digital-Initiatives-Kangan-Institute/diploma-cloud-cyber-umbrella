---
name: s1cl3-delivery
description: S1-CL3 (Cloud Infrastructure Improvement) delivery workstream — 8-Topic spine agreed; Step 3 coverage PASS 64/64; next is Step 4 slide plans + decks.
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

## NEXT — Step 4 (slide plans + decks)
8 `slide_plan.md` (→ `validate-slide-plan`) then 8 decks via `build_topic_deck.py`. Then Step 5 (practice)
and Step 6 (delivery plan — deferred per-instance, see [[delivery-run-sheet]]).

## Flag (assessment-side, deferred)
`S1-CL3-.../consolidated_uoc.md` "Topic & assessment structure" narrative still describes the **OLD** AT
model (AT1 Team Setup / AT2 group analyse+design with a *business case* / AT3 implement). The **current**
model (AT1 Design / AT2 Team-Implementation / AT3 Implement, business-case retired) is what the validated
instruments + these coverage files use. Tag inventory is fine (nothing downstream breaks); only the prose
is stale. Fix belongs to the CL3 **assessment** workstream ([[s1cl3-assessment]]).
