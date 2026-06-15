---
name: s1cl1-delivery
description: S1-CL1 (Cloud Design and Build) delivery workstream — cluster-specific Topic/session structure, the Accounting/Ledgerline practice scenario, the AT3 practice model, and remaining session-sizing work.
metadata:
  type: project
---

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

## Open — remaining build-side work
- **Session sizing** — lay the 14 content Topics + lettered assessment sessions (a–i) onto S2–S28
  against the tempo bands (WIP `S1_CL1_Delivery_Plan.docx`).
- **Parked confirms** — verify the AT2 marking-criterion letters (A3/A4) and the AT2/AT3 contextual-KE
  question lists against the assessor docs.
