# `.claude/skills/` — skills catalogue

The course-agnostic **authoring engine's** skills. Two kinds:

- **Process skills — the run-sheet steps/gates** (below): they drive the assessment + delivery
  run-sheets and **share** the validator engine in `scripts/`, so they deploy as one unit (a validator
  without its engine breaks). The UoC/assessment core is vendored from
  [ClaudePatternsAndSkills](https://github.com/timbaird/ClaudePatternsAndSkills) (re-copy from there when
  it improves); the delivery + scenario skills were **born here** as part of the umbrella engine.
- **Self-contained tooling** (further down): drop-in skills that carry their own script + dependencies
  (their own `.venv` or stdlib-only), independent of `scripts/`.

Agents (not skills) live alongside in [`../agents/`](../agents/): `evaluate-legacy-materials` (assessment
Gate 3) and `verify-scenario-realisation` (assessment Gate 7→8).

---

## Process skills — deploy as a whole unit (shared `scripts/` engine)

The step→gate skills of the two run-sheets ([docs/process-assessment.md](../../docs/process-assessment.md),
[docs/process-delivery.md](../../docs/process-delivery.md)). All share the engine at
`.claude/skills/scripts/` (the path the engines expect) — keep the skill folders and `scripts/` together.

### Assessment run-sheet

| Skill | Version | Summary |
|---|---|---|
| [transcribe-uoc](transcribe-uoc/) | 1.0.0 | Convert an official UoC `.docx` → **verbatim** `.md` (lifts from Word XML), then validate fidelity. |
| [validate-uoc-transcription](validate-uoc-transcription/) | 1.0.0 | Word-level diff `.docx` vs `.md` to prove a transcription is verbatim (substantive vs cosmetic). |
| [consolidate-uocs](consolidate-uocs/) | 1.0.0 | Build a cluster's `consolidated_uoc.md`: extract every item verbatim (script) → group editorially (DRAFT) → validate completeness (script). |
| [validate-uoc-consolidation](validate-uoc-consolidation/) | 1.0.0 | Prove `consolidated_uoc.md` holds every source item exactly once (MISSING / UNEXPECTED / DUPLICATED). |
| [validate-assessment-plan](validate-assessment-plan/) | 1.0.0 | Prove a cluster's `assessment_plan.md` conforms to the format standard (linter) and references every consolidated PC/PE/KE/FS item (UoC coverage). |
| [generate-consolidated-plan](generate-consolidated-plan/) | 1.0.0 | Deterministically derive a scenario's **consolidated assessment plan** (AT roster + whole-of-scenario coverage + unioned `SR-*` register) from its per-cluster plans. |
| [validate-consolidated-plan](validate-consolidated-plan/) | 1.0.0 | Prove a consolidated assessment plan is an exact, faithful union of its per-cluster source plans (catches stale aggregate / hand-edit / generator bug). |
| [validate-scenario-plan](validate-scenario-plan/) | 1.1.0 | Prove a two-part scenario plan conforms and every `SR-*` in the consolidated plan is satisfied by a build-checklist `SE-NN` item (no UNCOVERED / PHANTOM). Gate 6→7. |
| [validate-at-traceability](validate-at-traceability/) | 1.0.0 | Prove one assessment task's marking criteria each carry a valid UoC tag and every tag resolves. |
| [validate-student-instrument](validate-student-instrument/) | 1.0.0 | Leak-lint a `*-Student.docx`: HARD-fail on assessor-only material leaking in (UoC mapping tags, Benchmark / Model Answer / Assessor Instructions / Marking Criteria); WARN on softer VET vocabulary. Mechanical half of Gate 9→10. |
| [validate-mapping-doc](validate-mapping-doc/) | 1.0.0 | Prove a unit's Assessment Mapping docx is **complete** vs its UoC and **accurate** vs the marking benchmarks. |
| [validate-cluster-coverage](validate-cluster-coverage/) | 1.0.0 | Prove a cluster's ATs *together* evidence every consolidated item (gaps + phantoms). |

### Delivery run-sheet

| Skill | Version | Summary |
|---|---|---|
| [setup-cluster-spec](setup-cluster-spec/) | 1.0.0 | Run the guided elicitation that produces a cluster's **delivery frame** (`cluster-specification.md`) — frame questions, arithmetic, over-nominal authorisation — then runs `validate-cluster-spec`. Interactive main-session; Step 1. |
| [validate-cluster-spec](validate-cluster-spec/) | 1.0.0 | Prove a `cluster-specification.md` conforms to the format skeleton and the frame + topic-budget arithmetic reconciles (over-nominal hours carry a recorded authorisation). Gate for Step 1. |
| [validate-topic-breakdown](validate-topic-breakdown/) | 1.0.0 | Prove the AT→Topic breakdown is structurally sound — every AT has ≥1 Topic, every Topic declares a valid AT (`**AT<n> content Topic**` marker), Topic count fits the frame. Gate for Step 2. |
| [validate-slide-plan](validate-slide-plan/) | 1.0.0 | Prove a Topic's `slide_plan.md` conforms (every component `Teaches:`; every slide a `[TYPE]` + `image:`) and backwards-covers its sibling `coverage.md`. Gate before deck build (Step 4). |
| [validate-delivery-plan](validate-delivery-plan/) | 1.0.0 | Prove a `delivery-plan.md` outline is complete-for-generation — conforms, grid internally consistent, every Topic + assessment placed, reconciles with the frame. Gate for Step 6. |

**Shared engine — `scripts/`:** `inventory_uoc.py` · `transcribe_uoc.py` · `validate_uoc.py` ·
`validate_consolidated.py` · `validate_assessment_plan.py` · `generate_consolidated_plan.py` ·
`validate_consolidated_plan.py` · `validate_scenario_plan.py` · `validate_at_traceability.py` ·
`validate_student_instrument.py` ·
`validate_mapping_doc.py` · `validate_cluster_coverage.py` · `validate_cluster_spec.py` ·
`validate_topic_breakdown.py` · `validate_slide_plan.py` · `validate_delivery_coverage.py` ·
`validate_delivery_plan.py`.
*(`validate_delivery_coverage.py` is the delivery spine engine — invoked at delivery Gate 3→4; it has
no dedicated skill-folder wrapper yet.)*

> **`validate-mapping-doc` dependency note:** its **completeness** check is stdlib-only and portable
> like the rest of the pack. Its **accuracy** cross-check additionally imports the cluster's
> `scripts/s1_clN/build_s1_clN_mapping_docs.py` (which uses python-docx) to derive the benchmark oracle
> — so that half is coupled to this repo's generator layout, and is skipped (not failed) where the
> generator or python-docx is absent. Born here; not yet upstreamed to ClaudePatternsAndSkills.

---

## Self-contained tooling (own script + dependencies)

Drop-in skills independent of `scripts/`. Each carries its own engine; those needing third-party
packages follow [docs/skill-dependencies.md](../../docs/skill-dependencies.md) (committed
`requirements.txt` + a gitignored per-skill `.venv/`).

| Skill | Version | Deps | Summary |
|---|---|---|---|
| [draw-diagram](draw-diagram/) | 1.0.0 | Pillow (`.venv`) | Author an editable draw.io `.drawio` from a node/edge spec + render it to PNG with Pillow — deterministic, no app. Network / cloud-architecture / flowchart / simple ERD. The `image: diagram` half of the deck image pipeline. |
| [image-gen](image-gen/) | 1.0.0 | OpenRouter API key | Deterministic image-generation engine — a no-LLM wrapper that calls an OpenRouter image model with a resolved prompt + refs + model name and saves candidates for human curation. The `image: gen` half of the deck/website pipeline. |
| [upscale-image](upscale-image/) | 1.0.0 | Pillow (`.venv`) | Deterministic Pillow upscaler to an exact print-resolution size (Lanczos + cover-fit centre-crop + DPI stamp). No model, no network. |
| [review-slides](review-slides/) | 1.0.0 | PyMuPDF (`.venv`) + LibreOffice | Render a built `.pptx` to one PNG per slide (LibreOffice headless + PyMuPDF) and visually review — leftover placeholders, overflow/overlap, garbled images, off-brand slides. The deck QA gate; re-runnable. |
| [inspect-file-size](inspect-file-size/) | 1.0.0 | stdlib | Check whether an Office/zip file is too big to commit and find what's inflating it. Bundled `inspect_file_size.py`. |
| [map-process](map-process/) | 1.0.0 | stdlib | Turn a factory's step→gate run-sheet into a **Mermaid process map** + audit model (tooling & locus per stage; cross-check flags named-but-missing validators + stale doc status). Course-agnostic. |

---

## Prerequisites
- A **Python 3 interpreter** on PATH (`python3`, or `python` / `py -3` on Windows). The process-skill
  pack + `inspect-file-size` + `map-process` are **stdlib-only** (no venv, no `pip install`).
- **Self-contained tooling with deps:** create the skill's `.venv` and install its `requirements.txt`
  once per machine (see [docs/skill-dependencies.md](../../docs/skill-dependencies.md)); `review-slides`
  also needs **LibreOffice** (`brew install --cask libreoffice`), `image-gen` an **OpenRouter API key**.
- For the process-skill pack: a VET course repo layout — cluster directories with
  `units_of_competency/`, `assessments/`, `consolidated_uoc.md`, and (delivery) `cluster-specification.md`
  / `delivery/topic_NN/`.
