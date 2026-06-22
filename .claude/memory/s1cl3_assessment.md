---
name: s1cl3-assessment
description: "S1-CL3 (Cloud Infrastructure Improvement, ICTCLD504 + BSBXTW401) assessment workstream — the write-is-the-seam AT model (504 individual on design+deploy, 401 on the divided YAML write); instruments authored + validated 72/72."
metadata: 
  node_type: memory
  type: project
  originSessionId: 2dc8de09-19d6-46e4-8f5c-7f0c6cb6cb5e
---

CL3 = **Cloud Infrastructure Improvement**: **ICTCLD504** (improve cloud infrastructure) + **BSBXTW401**
(lead and facilitate a team) — assessment workstream. The **lightest** cluster (~56h, weeks 9–18, in
parallel with CL2). Built artefacts live in `S1-CL3-Cloud-Infrastructure-Improvement/`. Delivery:
[[s1cl3-delivery]]. Authoring rules: docs/cluster-authoring-conventions.md.

## The seam (why the ATs are shaped this way)
504 is a *technical* unit, so its evidence is **individual**; 401 is a *leadership* unit, so it needs a
**real team with divided, individually-accountable work**. The seam between them is the **CloudFormation
write**: of the three jobs — design / write the IaC / deploy — **design (504 el 1–2) and deploy (504 el 3)
are individual**, while **writing the IaC is not assessed by 504** (that is ICTCLD505, done in CL2). So
the write is the one job free to divide, and **dividing it by component is 401's team-work vehicle** — it
touches no individual 504 evidence. Don't re-tangle the two units onto one deliverable.

## AT model
- **AT1 (individual) — Design** (`504 el 1–2`): **Part A** Solution Design — analyse the baseline + design
  the whole improvement across all four concerns (CL2 Solution Design type; its *Review of the Existing
  Architecture* section is the analysis). **Part B** present for review + obtain sign-off-to-proceed
  (`PC 2.4/2.5`, FS Oral — an observed individual oral).
- **AT2 (group) — Team Implementation** (`401 el 1–4`): **Part A** project/team plan + allocate one IaC
  **component** to each member. **Part B** the team writes the CloudFormation for the agreed design,
  divided by component + integrated, across individually-led meetings; coordinate / support / monitor each
  against the plan / manage conflict; team sign-off gate. The write is the team-work vehicle, **not**
  504-assessed.
- **AT3 (individual) — Implement** (`504 el 3–4`): **apply-as-update** — deploy the baseline, then apply the
  approved improvement as a CloudFormation **change-set**; demonstrate / test / refine / document the
  **whole** system (all four concerns) + final sign-off. 401's division lives in the AT2 write, so AT3 is
  maximal individual 504.

## Design calls
- **Four components** = network / compute / database / storage (the AT2 write-allocation units; one per
  member, teams of four).
- **Encryption is baseline; data is out of scope.** The accounting system and its data are imaginary story;
  the lab database deploys **empty and encrypted at rest**. CL3 is an *infrastructure*-improvement exercise
  — encryption is not an improvement and there is no data migration, so every AT3 change is an
  **in-place/additive change-set** (no replacement, no IR-4 data-loss exposure).
- **Reliability = application-tier Multi-AZ + database backup/restore + cross-Region DR (Melbourne, data stays
  in Australia); the database is NOT Multi-AZ.** Ledgerline is a legacy app, vendor-certified single-instance
  only — a **Multi-AZ database limitation** surfaced as a discovered finding from the cloud migration (TF-03)
  and seeded through the current-state ICT records as a **breadcrumb trail**. The only route to DB failover
  (replace the accounting product — licence + data migration + change management + risk) is rejected as
  disproportionate (IR-2/IR-6); that cost-benefit call is the **AT1 analysis centrepiece**, with an **ASSESSOR
  FOCUS** pushback note on the AT1 Part B presentation checklist for candidates who reflexively propose a
  Multi-AZ database. Parameterised CloudFormation; a **light India residency slice** (CERT-In logs +
  Companies-Act books-of-account only — main system in Sydney, DPDP permits).
- **Scalability = elastic-capacity-on-demand, demonstrable by test** (not a forecast of load growth) — lets
  each component carry a real scalability story on an internal low-load finance system without breaching
  IR-2 (over-provisioning would be the gold-plating IR-2 forbids).
- **No business case** — neither UoC requires one; the 504 approval gate is the AT1 presentation; cost-benefit
  rides inside the Solution Design.
- The agreed "to be" design is **provided** to AT2 (the AT1 Solution Design exemplar doubles as it; published
  in-world at `s1-cl3-at2` onward). An assessor **reference combined template** is the AT3 fallback.

## Build state — instruments authored + validated
The full assessment is authored: **AT1 Design, AT2 Team Implementation, AT3 Implement — assessor + student
each — plus the AT1 Solution Design exemplar.** Kangan Project-Assessment instruments, single-sourced
(student derives from assessor); generators in `scripts/s1_cl3/`. **Validation PASS:** cluster coverage
72/72 + AT1/AT2/AT3 bidirectional traceability. Reuse: CL1 AT3 lab-pack pattern; CL2 Solution Design (AT1) +
Deployment Report (AT3) templates/generators + scenario world; students' CL2 (505) IaC skill (the AT2 write
reuses it).

## Remaining (engineering / process, not instrument authoring)
- **AT3 lab-pack — PROVEN live 2026-06-21** (Cloud Architecting Sandbox): Express baseline deploys (`us-east-1`
  + Sydney `ap-southeast-2`); apply-as-update yields app-tier Multi-AZ with the **DB untouched**; India slice
  deploys in Mumbai (`ap-south-1`). **Key constraint found: the `voclabs` lab role denies `rds:ModifyDBInstance`**
  — RDS is **create-only** in the lab, so the change-set must not modify the DB (the `BackupRetentionPeriod` bump
  was removed from `improved.yaml`; DB-tier DR is design-level, not lab-executable). Failover / scale-out / PITR
  demos not run (config valid; standard behaviour). Findings in `docs/lab-pack-standard.md` + the lab-pack
  `claude-notes.md`. The AT3 instruments were authored at final confidence (no caveat, no stale lab
  specifics); the only "draft pending proving run" hedge was a stale line in assessment_plan item 8, now
  de-hedged. See assessment_plan §6.8.
- **DB edition — DECIDED 2026-06-21 (do not re-litigate):** the in-world scenario **stays on SQL Server
  Standard**; the **lab deploys SQL Server Express** (`sqlserver-ex`) as a documented stand-in (README discloses
  it; the lab DB is empty so Express's 10 GB/RAM/core limits never bite — same pattern as region simulation).
  Driver: SE (`sqlserver-se`, license-included) is rejected on the sandbox's permitted classes (`db.t3.medium`,
  proven live), so both lab templates default to Express. **Why not change the engine** (e.g. PostgreSQL,
  which deploys cleanly): it spans ~30+ files across active CL3 **and completed CL1/CL2**, and it would **delete
  the commercial-licensing cost-benefit element** (~$27k/yr Ledgerline+SQL-Server licensing; license-included
  vs BYOL) that is the *assessed* differentiator from the open-source LMS — too costly, and it guts pedagogy.
  Residual tidy only: the soft `~13.5 vs ~22 GB` SQL-data figure (low priority).
- **`mappings/` Assessment Mapping docs (504, 401) — DONE 2026-06-22** (`build_s1_cl3_mapping_docs.py`:
  auto-inverts the AT1/AT2/AT3 benchmarks into the institutional template; 0 unmapped; FS auto-tagged from
  the benchmarks, ACs closest-fit to the instrument Conditions — AC5 legislative auto-maps to D5).
- Remaining: an **AT2 team-plan exemplar** (a model team plan; base on `build_s1_cl3_at1_team_plan_exemplar.py`).
- Downstream: scenario `IR-6` wording (re-point "Improvement Business Case" → the Solution Design's
  cost-benefit justification); the institutional **Pre-Validation** gate.
