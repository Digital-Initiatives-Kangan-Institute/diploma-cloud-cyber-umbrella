# Docs index

The single documentation surface for the **courseware-development umbrella** — the course-agnostic
process, conventions and format standards, plus the docs for the course it currently hosts (the Diploma
Cloud & Cyber). Covers the umbrella **and** the sub-repos (sub-repos hold no docs of their own). Every
document below has a one-line description; **read this index at the start of a session and load the
relevant doc before related work** (the same index-then-load-on-demand pattern as LLM memory). Add a
line here whenever you add a doc — an un-indexed document is invisible.

> **Paths inside these docs:** the deterministic tooling (skills + validators) lives in the umbrella's
> `.claude/skills/`. Docs describing assessment/delivery/scenario authoring use paths relative to the
> **content repo** root; website docs relative to the **website repo** root. Each doc notes which where
> it matters.

## Project orientation
- [project-overview.md](project-overview.md) — what the project is: context, scope, in/out of scope, operating principles, delivery context, success criteria.
- [clusters.md](clusters.md) — the cluster structure (which units group into which clusters).
- [source-materials.md](source-materials.md) — map of the `original_materials/` source set: the four material-state patterns, the courseware/templates layout, and what's missing.
- [reuse-permissions.md](reuse-permissions.md) — multi-TAFE origin of the source materials + Kangan's (still-being-confirmed) reuse rights, and the fallback if legal denies reuse.

## Authoring & delivery process
- [process-assessment.md](process-assessment.md) — the **assessment run-sheet**: the step→gate pipeline (transcribe → consolidate UoC → audit → cluster plan → **consolidate plans** → **scenario plan** → scenario materials/website → assessor/student instruments → mapping → cluster coverage → pre-validation), each gate a validator + human review (human removable as a step earns confidence). The scenario plan is developed *from* the consolidated contract (linear, not co-developed); the website is built *from* the scenario plan.
- [process-delivery.md](process-delivery.md) — the **delivery run-sheet**: the step→gate pipeline (cluster specification → topic breakdown → topic spec → topic decks → practice tasks → delivery plan), each gate a validator + human review, mirroring the assessment run-sheet. Consumes the assessment run-sheet's outputs (ATs, assessment plan, scenario, mappings); teach/practice/assess strategy; AT → Topic → component model.
- [cluster-specification-format.md](cluster-specification-format.md) — the standard format for a cluster's **delivery frame** (`<cluster>/cluster-specification.md`): nominal hours / weeks / sessions / session length, the elicited schedule conventions, and the derived topic budget. Step 1 of the delivery run-sheet — produced by the `setup-cluster-spec` elicitation, checked by `validate-cluster-spec` (format-driven linter: field presence + arithmetic + over-nominal authorisation).
- [slide-plan-format.md](slide-plan-format.md) — the standard format for a Topic's **slide plan** (`delivery/topic_NN/slide_plan.md`), the kept+validated source the deck is built from: per-component `Teaches:` (canonical UoC tags), each slide's type tag + mandatory `image:` source (`none`/`reuse`/`diagram`/`gen`/`placeholder`). The gate before deck build — checked by `validate-slide-plan` (format + backwards-coverage vs `coverage.md`, reusing the shared tag parser). Image model: `diagram` = an editable `.drawio` rendered to PNG in-pipeline by the `draw-diagram` skill (Pillow), `gen` = the `image-gen` skill; AWS-reuse a human paste.
- [delivery-plan-format.md](delivery-plan-format.md) — the standard format for a cluster's **delivery plan outline** (`<cluster>/delivery/delivery-plan.md`), Step 6 (terminal) of the delivery run-sheet. The plan is a **semester-instance** artefact (prerequisite-gated on the intake's session count / days / online-classroom split; produced in a human-AI juggling session; disposable-per-instance) — an instance-prerequisites header + a session grid (`# · Week · Day · Mode · Activity · Placed`). Checked by `validate-delivery-plan` (completeness-for-generation: contract + grid consistency + every Topic/AT placed + frame reconciliation); a validated outline is then filled into the institutional `…_Delivery_Plan.docx`.
- [cluster-authoring-conventions.md](cluster-authoring-conventions.md) — standing conventions for authoring assessment artefacts: UoC traceability, KE locations, template workflow, cross-AT shape, folder layout.
- [assessment-plan-format.md](assessment-plan-format.md) — the standard format for a cluster's assessment plan: per-AT UoC-coverage tags + a scenario-requirements (`SR-*`) register that the scenario plan is validated against; checked by `validate-assessment-plan`.
- [scenario-plan-format.md](scenario-plan-format.md) — the standard format for a scenario plan: **Part 1** the scenario narrative (story bible, human-led) + **Part 2** a forward build checklist (`SE-NN` items with keynotes/status/location binding every `SR-*`); developed from the consolidated contract and the basis the website is built from; cross-checked by `validate-scenario-plan` (run-sheet Gate 6).
- [document-template-system.md](document-template-system.md) — the branded YAT/MTS document system: how realistic the documents are and where realism yields to student experience; generator scripts + the umbrella's shared `docx`/`pptx` helpers; the consulting-chain document set; **one template per deliverable** (not one superset per type with parts marked N/A); the artefact roles (fillable template / assessor exemplar / student model); the violet course-side note + supplied-section conventions.
- [mapping-document-standard.md](mapping-document-standard.md) — the Assessment Mapping document as a derived artefact: the contract (machine-readable, UoC-tagged benchmarks), the generate → validate pipeline, the FS/AC closest-fit convention, and the shared template layout.
- [kangan-branding.md](kangan-branding.md) — the Kangan/BKI brand spec used for teaching decks.
- [lab-pack-standard.md](lab-pack-standard.md) — the course-wide lab-pack standard: runnable CloudFormation + local validation harness students deploy into ephemeral AWS Academy labs, and the Academy constraints (proven live).
- [region-substitution-standard.md](region-substitution-standard.md) — the notation bridging the multi-region **design** layer and the single-region (`us-east-1`) Learner Lab **deploy** layer: the `[scenario: … | deploy: …]` token, the canonical mapping, the design-stays-multi-region / deploy-is-single-region principle, and residency/DR handling.

## Scenario & website
- [scenario-flow.md](scenario-flow.md) — the cross-cluster scenario model: system↔cluster assessment/practice matrix, no-leakage invariant, system state progressions, CL3 framing, the single-source-on-the-website rule, and the in-world-only intranet rule.
- [website-architecture.md](website-architecture.md) — the YAT scenario website architecture (Astro, state-folder intranet URL model, content collections, projects model, state-versioned docs). Single source of truth for in-world scenario content.

## Meta
- [process-maps/](process-maps/) — **generated** (by the `map-process` skill, not hand-edited): a Mermaid flowchart of each run-sheet the factory implements + a `factory-overview.md` chaining them, each with a tooling-&-locus table (🏠 umbrella tools / 📦 sub-repo data / 👤 human-led per stage) and a cross-check/audit table (named-but-missing validators, stale doc-status markers). Regenerate whenever the run-sheets or skills inventory change. A visual summary of the current process + the input to a process audit.
- [doco-structure.md](doco-structure.md) — the four documentation surfaces (README / CLAUDE.md / MEMORY / docs) and the `CLAUDE.md`⇄`MEMORY` split; what belongs where and why.
- [skill-dependencies.md](skill-dependencies.md) — the convention for how a skill/tool declares + installs third-party dependencies: pure-stdlib preferred; otherwise a committed `requirements.txt` + a per-skill gitignored `.venv/` + an import guard + invoking with the venv's Python. Backed by the `ensure-python.mjs` SessionStart preflight. Reference implementation: the `upscale-image` skill.
