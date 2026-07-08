# `.claude/skills/` — skills catalogue

Skills vendored into this repo (the authoritative sources live in
[ClaudePatternsAndSkills](https://github.com/timbaird/ClaudePatternsAndSkills); re-copy from there when
they improve). Two groups: the **vet-uoc-development pack** (deploy-together; shared engine) and the
**standalone** size-check skill.

## vet-uoc-development pack — deploy as a whole unit

A toolkit for developing and quality-assuring VET/TAFE assessment from official **units of competency
(UoCs)** — transcription, consolidation, and the traceability/coverage validators that prove
compliance. The six skills **share** the engine in `scripts/`, so they live together: the skill folders
are siblings here and `scripts/` sits at `.claude/skills/scripts/` (the path the engines expect). Don't
split them — a validator without its engine breaks.

| Skill | Version | Summary |
|---|---|---|
| [transcribe-uoc](transcribe-uoc/) | 1.0.0 | Convert an official UoC `.docx` → **verbatim** `.md` (lifts from Word XML), then validate fidelity. |
| [validate-uoc-transcription](validate-uoc-transcription/) | 1.0.0 | Word-level diff `.docx` vs `.md` to prove a transcription is verbatim (substantive vs cosmetic). |
| [consolidate-uocs](consolidate-uocs/) | 1.0.0 | Build a cluster's `consolidated_uoc.md`: extract every item verbatim (script) → group editorially (DRAFT) → validate completeness (script). |
| [validate-uoc-consolidation](validate-uoc-consolidation/) | 1.0.0 | Prove `consolidated_uoc.md` holds every source item exactly once (MISSING / UNEXPECTED / DUPLICATED). |
| [validate-at-traceability](validate-at-traceability/) | 1.0.0 | Prove one assessment task's marking criteria each carry a valid UoC tag and every tag resolves. |
| [validate-cluster-coverage](validate-cluster-coverage/) | 1.0.0 | Prove a cluster's ATs *together* evidence every consolidated item (gaps + phantoms). |
| [validate-mapping-doc](validate-mapping-doc/) | 1.0.0 | Prove a unit's Assessment Mapping docx is **complete** vs its UoC and **accurate** vs the marking benchmarks. |
| [validate-assessment-plan](validate-assessment-plan/) | 1.0.0 | Prove a cluster's `assessment_plan.md` conforms to the format standard (linter) and references every consolidated PC/PE/KE/FS item (UoC coverage). |
| [generate-consolidated-plan](generate-consolidated-plan/) | 1.0.0 | Deterministically derive a scenario's **consolidated assessment plan** (AT roster + whole-of-scenario coverage + unioned `SR-*` register) from its per-cluster plans. |
| [validate-consolidated-plan](validate-consolidated-plan/) | 1.0.0 | Prove a consolidated assessment plan is an exact, faithful union of its per-cluster source plans (catches stale aggregate / hand-edit / generator bug). |

**Shared engine — `scripts/`:** `inventory_uoc.py` · `transcribe_uoc.py` · `validate_uoc.py` ·
`validate_consolidated.py` · `validate_at_traceability.py` · `validate_cluster_coverage.py` ·
`validate_mapping_doc.py` · `validate_assessment_plan.py` · `generate_consolidated_plan.py` ·
`validate_consolidated_plan.py`.

> **`validate-mapping-doc` dependency note:** its **completeness** check is stdlib-only and portable
> like the rest of the pack. Its **accuracy** cross-check additionally imports the cluster's
> `scripts/s1_clN/build_s1_clN_mapping_docs.py` (which uses python-docx) to derive the benchmark oracle
> — so that half is coupled to this repo's generator layout, and is skipped (not failed) where the
> generator or python-docx is absent. Born here; not yet upstreamed to ClaudePatternsAndSkills.

## Standalone skills

| Skill | Version | Summary |
|---|---|---|
| [inspect-file-size](inspect-file-size/) | 1.0.0 | Check whether an Office/zip file is too big to commit and find what's inflating it. **Self-contained** — its `inspect_file_size.py` is bundled in the skill folder (no shared `scripts/`), so it's a drop-in. |

## Prerequisites
- A **Python 3 interpreter** on PATH (`python3`, or `python` / `py -3` on Windows) — standard library
  only (no venv, no `pip install`).
- For the UoC pack: a VET course repo layout — cluster directories with `units_of_competency/`,
  `assessments/`, and `consolidated_uoc.md`.
