# Memory index

**LLM-only** durable memory for the **Diploma Cloud & Cyber** project — how Claude should behave here,
and the current standing of each cluster workstream ("principles, not state" — see
[[memory-principles-not-state]]). One line per memory; topic files hold the detail, loaded on demand.

> **Both-audience knowledge** (project, processes, conventions, scenario, website, lab-packs) is **not**
> here — it lives in **`docs/`**, catalogued in [docs/INDEX.md](../../docs/INDEX.md). Read that index
> every session and load the relevant doc before related work (see the umbrella `CLAUDE.md`).

## Working principles (how Claude operates here)
- [memory = principles not state](memory_principles_not_state.md) — record durable decisions/rationale (the non-derivable WHY); never repo-derivable ephemeral state (paths, commits, "what's built") — it goes stale on creation.
- [record current-state only](feedback_process_docs_current_only.md) — record things as they ARE, not how they used to be, in everything (docs, memory, status notes): current method only, no abandoned-path archaeology; git holds it.
- [write deliverables at final confidence](feedback_deliverables_final_confidence.md) — author docs as if open dependencies were done; track the dependency in MEMORY, never as an in-text "draft pending X" hedge (avoids redoing the doc just to strip caveats).
- [suggest commits, don't auto-commit](feedback_suggest_commits.md) — when a commit seems appropriate, suggest it's a good time and wait for confirmation; never auto-commit (memory is version-controlled + syncs across machines).
- [one step at a time](feedback_one_step_at_a_time.md) — for hands-on interactive walk-throughs (AWS console, lab setup), give ONE step then wait for what he sees; don't front-load 10 steps.
- [draft naming pragmatism](feedback_draft_naming_pragmatism.md) — during drafts, don't fuss over file naming; defer naming discipline to delivery-ready versions.
- [verify change impact](feedback_verify_change_impact.md) — before side-effecting changes (esp. running file-writing generators), verify where output lands + `git status` what got staged; a "helpful" regenerate once created a phantom nested sub-repo and committed it.

## Cluster workstreams (S1) — assessment + delivery per cluster (current working state)
- [S1-CL1 assessment](s1cl1_assessment.md) — **COMPLETE (2026-06-15)** — pilot cluster, assessment workstream: AT shape, settled cross-AT design decisions; all 9 instruments finalised, Multi-AZ resolved, Records Policy authored.
- [S1-CL1 delivery](s1cl1_delivery.md) — **COMPLETE (2026-06-15)** — CL1 delivery workstream: Topic/session structure, Accounting/Ledgerline practice scenario, AT3 practice model; 14 decks built, session-sizing adequate.
- [S1-CL2 assessment](s1cl2_assessment.md) — **COMPLETE (authoring + coverage 105/105, 2026-06-15)** — Cloud DR cluster (501/503/505): vehicle, AT structure, the DR≠design≠residency reframe, offshore-India spine, lab usage, template parity; only the institutional Pre-Validation meeting remains.
- [S1-CL2 delivery](s1cl2_delivery.md) — CL2 delivery workstream: week/session frame, 10-Topic spine (AT1 design / AT2 build), LMS practice vehicle, topic-coverage re-check vs the finalised website assessments.
- [S1-CL3 assessment](s1cl3_assessment.md) — Cloud Infrastructure Improvement (504 + 401, lightest): **Claude-complete 2026-06-22** — instruments validated 72/72, AT3 lab-pack proven live, mappings + AT2 team-plan exemplar built, "Improvement Business Case" retired (→ Solution Design). Write-is-the-seam model (504 individual design+deploy; 401 the divided YAML write in AT2); encryption baseline + data out of scope. Only the institutional **Pre-Validation** gate (human) remains.
- [S1-CL3 delivery](s1cl3_delivery.md) — CL3 delivery workstream: not started yet (instruments authored; delivery decks are the next CL3 workstream).

## Process formalisation (run-sheets + tooling)
- [assessment run-sheet](assessment_run_sheet.md) — **IN FLIGHT 2026-06-22:** the assessment process is now a step→gate run-sheet (docs/process-assessment.md); validating it gate-by-gate vs S1 + building a validator/agent per gateless gate. Built gates 3 (evaluate-legacy-materials agent), 4 (assessment-plan format + validate-assessment-plan; all 3 plans retrofitted), 5 (generate/validate-consolidated-plan; assessment-plans/S1.md). **NEXT: Gate 6 scenario tooling.**
- [mapping pipeline](mapping_pipeline.md) — **BUILT 2026-06-22:** Assessment Mapping docs are a derived artefact; one engine (`scripts/mapping/generate_mapping_doc.py`) generates all clusters + the `validate-mapping-doc` skill checks completeness/accuracy (see docs/mapping-document-standard.md). Never hand-edit a mapping docx. **Open follow-on:** CL1 instruments lack machine-readable benchmarks (Route A retrofit).
