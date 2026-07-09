---
name: gate-walk-invocations
description: The correct, non-obvious ways to invoke the S1 validation gates (the ones that cost troubleshooting) — so a future gate-walk goes straight to the working command.
metadata:
  node_type: memory
  type: reference
  originSessionId: 5fe40dfd-42a4-49d7-8e7d-5da57c8df524
---

Running the **full S1 gate-walk** (every deterministic gate, both run-sheets, all 3 clusters — all PASS
2026-07-09). Validators live in the umbrella `.claude/skills/scripts/`. The invocations that are
**non-obvious and cost troubleshooting** — go straight to these:

- **G2 consolidation (`validate_consolidated.py`)** — pass **ALL of a cluster's units in ONE call**
  (`--unit CODE=units_of_competency/<file>.md` for each, paths **relative to the cluster dir**) **and use
  `--assessor-ac`**. Each cluster's consolidated doc carries **3 AC items** (one per unit) that only
  reconcile in assessor-AC mode; without `--assessor-ac` they show as false `UNEXPECTED`, and passing a
  single `--unit` makes the *other* units' items look UNEXPECTED. Correct → `126/128`-style exact PASS.
- **G10 mapping-doc (`validate_mapping_doc.py`)** — run with the **umbrella `scripts/.venv/bin/python`**
  (it imports python-docx); system `python3` → `ModuleNotFoundError: No module named 'docx'`.
- **G1 transcription (`validate_uoc.py`)** — positional **pairs**: `validate_uoc.py <src.docx> <t.md>
  [<docx> <md> …]`. Exit **0 = verbatim**, 1 = substantive diff (no `RESULT:` grep — use the exit code).
  Sources are under `units_of_competency/original/`, transcriptions under `units_of_competency/`.
- **Scenario-level G5/G6 (`validate_consolidated_plan.py` / `validate_scenario_plan.py`)** — these are
  **per-semester, not per-cluster**: `--semester S1 --repo <content-repo>` (they default the plan +
  consolidated paths from that).
- **G8 at-traceability (`validate_at_traceability.py`)** — `--at <AT-Assessor.docx> --consolidated
  <cluster>/consolidated_uoc.md`, once per AT. (Base check = tags resolve + no free-floating criteria;
  add `--expect` for per-AT reverse-coverage — the *collective* reverse-coverage is G11.)
- **Everything else takes `--cluster <dir>`** (`validate_assessment_plan`, `validate_student_instrument`,
  `validate_cluster_coverage`, `validate_cluster_spec`, `validate_topic_breakdown`,
  `validate_delivery_coverage`); `validate_slide_plan` is per-topic (`--plan <topic_NN>/slide_plan.md`).

**Shell gotcha (this machine is zsh):** zsh does **not** word-split an unquoted `${var}` / `${assoc[k]}`
like bash — a space-separated unit list becomes ONE arg (→ bogus paths / false FAILs). Use `${=var}` or a
real array. This bit the first sweep; the gates themselves were fine.

**Not machine-gated (by design):** assessment G3 (audit — brownfield-only), G7 (scenario realisation —
the `verify-scenario-realisation` *agent*, read-only, run on request), G12 (institutional pre-validation
— human); delivery D5 (practice — human), D6 (delivery-plan — deferred per-instance, no `delivery-plan.md`
until an intake). Related: [[assessment-run-sheet]], [[delivery-run-sheet]].
