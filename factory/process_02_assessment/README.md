# Process 02 — Assessment

Turning the extracted units into a cluster's assessment: the plan, the scenario it is set in, the
assessor and student instruments, the mapping documents, and the coverage proof. This is where
judgement starts — extraction lifts, assessment decides.

Run-sheet: [docs/process-assessment.md](../../docs/process-assessment.md). Steps continue from
`process_01_extraction` (they are one run-sheet split across two folders).

## Steps

| Step | Name | Legacy location of its tooling |
|---|---|---|
| 04 | Assessment plan | `.claude/skills/scripts/validate_assessment_plan.py` |
| 05 | Consolidate the assessment plans | `.claude/skills/scripts/generate_consolidated_plan.py`, `validate_consolidated_plan.py` |
| 06 | Scenario plan | `.claude/skills/scripts/validate_scenario_plan.py` |
| 07 | Scenario materials | `.claude/agents/verify-scenario-realisation.md` (agent gate) |
| 08 | Assessor instruments | content repo `scripts/s1_cl*/build_*_assessor.py`; `validate_at_traceability.py` |
| 09 | Student instruments | content repo `scripts/s1_cl*/build_*_student.py`; `validate_student_instrument.py` |
| 10 | Mapping documents | `scripts/mapping/generate_mapping_doc.py`; `validate_mapping_doc.py` |
| 11 | Cluster coverage | `.claude/skills/scripts/validate_cluster_coverage.py` |
| 12 | Institutional pre-validation | human / institutional sign-off |

## Status

Structure only — **nothing ported**. Step folders are created as each step's work comes up.
