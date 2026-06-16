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
- [suggest commits, don't auto-commit](feedback_suggest_commits.md) — when a commit seems appropriate, suggest it's a good time and wait for confirmation; never auto-commit (memory is version-controlled + syncs across machines).
- [one step at a time](feedback_one_step_at_a_time.md) — for hands-on interactive walk-throughs (AWS console, lab setup), give ONE step then wait for what he sees; don't front-load 10 steps.
- [draft naming pragmatism](feedback_draft_naming_pragmatism.md) — during drafts, don't fuss over file naming; defer naming discipline to delivery-ready versions.
- [verify change impact](feedback_verify_change_impact.md) — before side-effecting changes (esp. running file-writing generators), verify where output lands + `git status` what got staged; a "helpful" regenerate once created a phantom nested sub-repo and committed it.

## Cluster workstreams (S1) — assessment + delivery per cluster (current working state)
- [S1-CL1 assessment](s1cl1_assessment.md) — **COMPLETE (2026-06-15)** — pilot cluster, assessment workstream: AT shape, settled cross-AT design decisions; all 9 instruments finalised, Multi-AZ resolved, Records Policy authored.
- [S1-CL1 delivery](s1cl1_delivery.md) — **COMPLETE (2026-06-15)** — CL1 delivery workstream: Topic/session structure, Accounting/Ledgerline practice scenario, AT3 practice model; 14 decks built, session-sizing adequate.
- [S1-CL2 assessment](s1cl2_assessment.md) — **COMPLETE (authoring + coverage 105/105, 2026-06-15)** — Cloud DR cluster (501/503/505): vehicle, AT structure, the DR≠design≠residency reframe, offshore-India spine, lab usage, template parity; only the institutional Pre-Validation meeting remains.
- [S1-CL2 delivery](s1cl2_delivery.md) — CL2 delivery workstream: week/session frame, 10-Topic spine (AT1 design / AT2 build), LMS practice vehicle, re-check vs the re-pointed assessments.
- [S1-CL3 assessment](s1cl3_assessment.md) — Cloud Infrastructure Improvement (504 + 401, lightest): **write-is-the-seam** model — 504 individual (AT1 design+present, AT3 deploy+operate whole system), 401 entirely AT2 via the **divided YAML write** (not 504-assessed); no business case; agreed "to be" design provided to AT2.
- [S1-CL3 delivery](s1cl3_delivery.md) — CL3 delivery workstream: not started yet (assessment authoring leads).
