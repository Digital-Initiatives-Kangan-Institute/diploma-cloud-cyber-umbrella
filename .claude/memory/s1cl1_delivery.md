---
name: s1cl1-delivery
description: "S1-CL1 (Cloud Design and Build) delivery workstream — COMPLETE (2026-06-15): Topic/session structure, the Accounting/Ledgerline practice scenario, the AT3 practice model."
metadata: 
  node_type: memory
  type: project
  originSessionId: 5fe40dfd-42a4-49d7-8e7d-5da57c8df524
---

> **STATUS: COMPLETE (2026-06-15).** CL1 delivery is done for the pilot — 14 topic decks built,
> session-sizing adequate. See **Status** at the foot. (Assessment workstream also complete —
> [[s1cl1-assessment]].)

The **delivery-planning** workstream for S1-CL1 (sessions + teaching materials; separate from
assessment authoring — see [[s1cl1-assessment]]). General method is in
docs/process-delivery.md; the canonical process doc is `docs/process-delivery.md`.

## Topic + session structure (CL1)
- **14 content Topics**, mapped to ATs: **AT1 = Topics 1–5, AT2 = 6–10, AT3 = 11–14**. Topic 8 is split
  into **8a** (compute & elasticity) + **8b** (database & storage) but is one Topic in the spine.
- **Assessments are lettered non-Topic sessions** (a–i). Onboarding = S1; catch-up = S31–32. Full
  Topic/session/tempo structure in `process-delivery.md`; spine + scaffolds in `delivery/planning/`.

## Practice scenario (settled)
Practice runs on the **YAT Accounting & Office Administration system (Ledgerline)** — same org,
**different system** than the assessed LMS — added to the intranet as a peer engagement
(indistinguishable on the site until a practice task is handed out). Deliberately a different profile so
analysis can't rhyme: internal/business-hours, 99.5% target (not 99.9%), SQL Server + commercial
licensing. **Students practise on Accounting, are assessed on the LMS.** Each AT gets a
parallel-but-different supplied artefact (e.g. AT2's Accounting Baseline Solution Design — RDS for SQL
Server, internal ALB over campus VPN, 99.5%; AT3 needs a parallel HA design). Website docs:
`projects/accounting-cloud-migration/` + `ict/accounting-*.md` (see docs/website-architecture.md).

## AT3 practice model (settled)
**Students produce their own HA design; we supply inputs** (the Accounting baseline +
`ha-database-requirements.md`), **not** a finished design — AWS/502 materials cover the exemplar
pattern, so a bespoke finished Accounting HA design would be redundant.

## Status — COMPLETE (2026-06-15); decks image- + notes-complete (2026-07-09)
- **14 topic decks** (`delivery/topic_*/Topic_*_Slides.pptx`). **MIGRATED to the generic builder 2026-07-09**
  — CL1 now builds from a **content-complete `slide_plan.md`** via `build_topic_deck.py`, exactly like
  CL2/CL3; the per-topic `build_s1_cl1_topic*_deck.py` + sidecar `topicNN_notes.py` are **retired/deleted**
  (no second path — see [[one-course-agnostic-mechanism]]). Proven faithful by the new
  **`validate-deck-reproduction`** gate (regenerated == committed: body + notes + image count) — every topic
  reproduced except two accepted *standardisations*: topic_01 gained its missing section-1 divider, and
  topic_08b's dividers renumbered 01/02→03/04. **topic_08 is a split topic** (1 `coverage.md` ↔ 2 decks) →
  two half-plans `slide_plan_08a.md` (`Covers-components: C1,C2`) / `slide_plan_08b.md` (`C3,C4`).
- **Images filled 31/31 (2026-07-09):** every flagged image gap placed — 10 draw-diagram diagrams
  (`topic_NN/diagrams/`), 7 gen images + 14 AWS-reuse extracts (`topic_NN/images/`), placed via an `_img()`
  helper → committed files (survey: `delivery/planning/image-gap-survey.md`; AWS source = the local
  gitignored instructor decks). Text auto-fits/centres; visual-reviewed via **`review-slides`**.
- **Teacher speaker notes across all 14 topics — 232 notes (2026-07-09):** now committed as **`notes:`
  blocks in each `slide_plan.md`** (migrated off the old `topicNN_notes.py` sidecar); teaching / demo (with
  WHERE TO FIND the recorded demo) / activity. See [[delivery-run-sheet]] for the notes layer.
- **Session sizing** (`S1_CL1_Delivery_Plan.docx`) — **adequate for now** (per Tim); refine from live
  delivery experience if needed. **Parked confirms** satisfied by the finalised assessor instruments
  ([[s1cl1-assessment]]).

CL1 delivery is complete for the pilot — decks now teachable cold (images + notes); tune from feedback.
