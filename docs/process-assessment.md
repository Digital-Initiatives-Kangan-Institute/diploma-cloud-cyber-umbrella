# Cluster assessment run-sheet

**Audience:** humans and LLM agents creating a cluster's **assessment artefacts**. This is one of the
project's **two run sheets** — the assessment run-sheet (here) and the
[delivery run-sheet](process-delivery.md). Both take the same dropped-in cluster inputs and run a fixed
pipeline of **steps separated by gates**.

> **Paths** in this document are relative to the `diploma-cloud-cyber-content/` repo root.

## How this run-sheet works

Drop a cluster's units of competency into `units_of_competency/` and the pipeline below runs in order.
Each **step** is one unit of work (a brief description here; the deep detail is in the linked skill or
section). Between every step is a **gate** — the conditions that must hold before moving on:

- **Machine condition** — a deterministic validator that must pass (where one exists). This is the
  step's definition of done: *transcribe* is finished when `validate-uoc-transcription` passes,
  *consolidate* when `validate-uoc-consolidation` passes, and so on.
- **+ human review** — initially every gate also needs a human sign-off. **As a step earns confidence,
  the human check can be dropped from that gate** (leave the machine condition). Gates with no validator
  yet are **human-only** for now — those are the steps to grow tooling for.

Steps 6–7 loop **per AT**; steps 8–9 are **cluster-level** (after all ATs exist).

**Prerequisites to read before acting:**
- The umbrella `CLAUDE.md` — working discipline (nothing recorded as decided without explicit approval;
  mark proposals/produced docs **DRAFT/TBD**) + git-safety rules.
- [project-overview.md](project-overview.md) — scope, in/out of scope, operating principles.
- [clusters.md](clusters.md) — which units group into which clusters.
- [cluster-authoring-conventions.md](cluster-authoring-conventions.md) — UoC traceability, KE locations,
  template workflow, cross-AT shape, folder layout.
- Do **not** modify anything under `original_materials/` (read-only reference).

## Cluster folder layout (input state)

`units_of_competency/` and `mappings/` are top-level siblings of `assessments/`:

```
SX-CLY-<Cluster-Name>/
├── assessments/            # per-AT folders (AT1/, AT2/, …) — produced in steps 6–7
├── delivery/               # delivery materials (the delivery run-sheet's output)
├── mappings/               # per-UoC Assessment Mapping docs — produced in step 8
├── units_of_competency/
│   ├── <UNIT>_Complete_R*.md       # verbatim transcription (step 1)
│   └── original/<UNIT>_Complete_R*.docx   # source UoC (read-only)
└── consolidated_uoc.md     # produced in step 2 (cluster root)
```

All validators are **stdlib-only** and live in `.claude/skills/scripts/`; run them with any Python 3
launcher (`python3` / `python` / `py -3`). The deterministic skills (transcription, consolidation, the
traceability/coverage/mapping validators) travel with the repo and lift into future courses unchanged.

---

# The pipeline (step → gate)

**1 · `transcribe-uoc` — Transcribe the units of competency**
Lift each official UoC `.docx` into a **verbatim** `.md` (Word-XML extraction, never retyped; structure
rebuilt from document styles). → [transcribe-uoc skill](../diploma-cloud-cyber-content/.claude/skills/transcribe-uoc/SKILL.md) · detail [§1](#1--transcribe). **built**
> **⟱ Gate 1→2:** *validator* `validate-uoc-transcription` (`validate_uoc.py`) = **EXACT MATCH** for every
> `.docx`/`.md` pair (verbatim-after-cosmetic is acceptable but report the diffs) **+ human review**.

**2 · `consolidate-uocs` — Consolidate the cluster's UoCs**
Extract every PC/FS/PE/KE/AC verbatim and source-tagged `[UNIT SEC num]` into one `consolidated_uoc.md`,
grouped where assessment overlap is plausible (grouping is the only judgement layer — mark **DRAFT/TBD**).
→ [consolidate-uocs skill](../diploma-cloud-cyber-content/.claude/skills/consolidate-uocs/SKILL.md) · detail [§2](#2--consolidate). **built**
> **⟱ Gate 2→3:** *validator* `validate-uoc-consolidation` (`validate_consolidated.py`) = **PASS** — every
> item appears exactly once (no MISSING / UNEXPECTED / DUPLICATED) **+ human review**.

**3 · Audit source assessments** *(brownfield only — optional; skip if greenfield)*
A **legacy / brownfield** step: it applies only when standalone assessment materials **already exist** for
the cluster's units (in `original_materials/`) and might be reusable. **Judgement first:**
- **Greenfield** (no pre-existing materials) → nothing to audit; **skip**.
- **Brownfield** → run the **[`evaluate-legacy-materials` agent](../.claude/agents/evaluate-legacy-materials.md)**
  *(read-only)*: it scans `original_materials/` against `consolidated_uoc.md` and **surfaces** candidate
  reusable material — each source AT's format, the UoC items it appears to touch, and any scenario assets —
  **authoring nothing and deciding nothing**. It brings options to the surface for the human to weigh. →
  detail [§3](#3--audit-source-assessments).
> **⟱ Gate 3→4:** *not a correctness check.* **Greenfield:** proceed. **Brownfield:** the
> `evaluate-legacy-materials` agent has been run and its surfaced candidates are **in hand as an input to
> step 4** — where the human decides what (if anything) to reuse while building the plan + scenario.

**4 · Assessment plan and scenario design** *(co-developed)*
Two outputs, developed **together**: (a) the **assessment plan** (one per cluster, to the format standard) —
the AT structure with, **per AT**, its **UoC coverage** (canonical `[UNIT SEC num]` tags) and its
**scenario requirements** (`SR-*`); and (b) the **scenario design** — the narrative the assessments need to
be meaningful, captured in the scenario plan. Co-developed because a scenario is only viable judged against
a clear, **cross-cluster** view of what every assessment must cover (the scenario is a shared asset). →
[assessment-plan-format.md](assessment-plan-format.md) · [scenario-flow.md](scenario-flow.md) · detail [§4](#4--assessment-plan-and-scenario-design).
> **⟱ Gate 4→5:** (a) *validator* `validate-assessment-plan` = **PASS** — the plan conforms to the format
> and every consolidated PC/PE/KE/FS item is covered by an AT; **+** (b) *human review* — the AT-structure
> design is sound and the scenario requirements (`SR-*`) are captured. *(Whether the scenario actually
> provides those `SR-*` is checked at Gate 5's scenario cross-check.)*

**5 · Scenario materials**
Author the shared cluster scenario **from the agreed design (step 4)** — the in-world content the ATs
depend on, single-sourced on the website (in-world only — no course/assessment meta-language). →
[scenario-flow.md](scenario-flow.md) · [website-architecture.md](website-architecture.md) · detail [§5](#5--scenario-materials).
> **⟱ Gate 5→6:** *human review* — every scenario file in the checklist is authored, marked carry-over,
> or flagged **TBD**; AC items the scenario must satisfy are covered. *(No script.)*

**6 · Assessor instruments** *(loop per AT)*
Populate the institutional assessor template for each AT: Details, Teacher/Assessor instructions, and the
**Marking Guide with bidirectional UoC traceability** (every criterion carries `[UNIT SEC num]`; a reverse
map closes the loop). → [cluster-authoring-conventions.md](cluster-authoring-conventions.md) · [document-template-system.md](document-template-system.md) · detail [§6](#6--assessor-instruments).
> **⟱ Gate 6→7:** *validator* `validate-at-traceability` = **PASS** for the AT (no phantom tags, no
> free-floating criteria; pass the AT's allocation via `--expect` for reverse-coverage) **+ human review**.

**7 · Student instruments** *(loop per AT)*
Derive the student-facing instrument from the assessor version (shared Details/Task/Resources; strip the
Marking Guide, benchmark, and model answers). → detail [§7](#7--student-instruments).
> **⟱ Gate 7→8:** *human review* — student copy carries everything the student needs and nothing
> assessor-only. *(No script.)*

**8 · Mapping documents** *(cluster-level)*
Generate the per-unit Assessment Mapping docs from the engine (rows from the source UoC, AT-column codes
from the assessor benchmarks, FS/AC closest-fit). Never hand-edit a mapping docx — it is derived. →
[mapping-document-standard.md](mapping-document-standard.md) · detail [§8](#8--mapping-documents).
> **⟱ Gate 8→9:** *validator* `validate-mapping-doc` = **PASS** for every unit — complete vs the unit's
> own UoC (every item present + mapped) and accurate vs the benchmarks (PC/PE/KE hard; FS/AC advisory)
> **+ human review**.

**9 · Cluster coverage** *(capstone)*
Confirm the cluster's ATs, taken together, evidence **every** consolidated item. → [validate-cluster-coverage skill](../diploma-cloud-cyber-content/.claude/skills/validate-cluster-coverage/SKILL.md) · detail [§9](#9--cluster-coverage).
> **⟱ Gate 9→10:** *validator* `validate-cluster-coverage` = **100%** (no MISSING required item, no
> PHANTOM reference; AC environment-satisfied unless `--include-ac`) **+ human review**.

**10 · Institutional pre-validation**
Run the institutional Pre-Validation Tool over each AT and address findings. → detail [§10](#10--institutional-pre-validation).
> **⟱ Gate 10→done:** *human / institutional* sign-off. The cluster's assessment is complete.

---

# Step detail

## §1 — Transcribe
Invoke `transcribe-uoc` on each `<docx>` (it lifts content verbatim from the Word XML, rebuilds structure
from styles, and auto-runs the `validate_uoc.py` gate). Validate any existing `.md` with
`validate-uoc-transcription`. The validator extracts `.docx` text in document order (paragraphs + table
cells; `w:br`→newline, `w:tab`→tab), strips markdown from the `.md`, and diffs word sequences in two tiers
(substantive vs cosmetic).

**Step gotchas:**
- **`.docx` headers/footers carry content** (training-package attribution, unit code) that is **not** in
  the `.md` — excluded from the verbatim check by design; don't re-flag as missing.
- **Markdown list bullets (`- `) are syntax, not content** — the validator strips them; otherwise every
  PE/KE/AC bullet is a false-positive insert.
- **FS uses the skill name verbatim**, including spaces and case (`Oral communication` in ICTCLD502 vs
  `Oral Communication` in ICTICT517 — preserve as-is).

## §2 — Consolidate
`consolidate-uocs` extracts every item pre-tagged (`inventory_uoc.py`), groups into topics (DRAFT/TBD),
then runs `validate_consolidated.py`. Excludes non-assessable sections (Application, Unit Sector,
Modification History, Unit Mapping, Links). Numbering: PC keeps source numbering; FS = skill name; PE/KE/AC
numbered `1..N` in source order; the trailing "Assessors of this unit must satisfy…" paragraph is the next
AC. Tags must appear **unwrapped** (not in backticks) to be counted.

**Step gotchas:**
- **ICTICT517 PE is a parent bullet** — a single `- For one organisation:` with 6 sub-bullets; the **6
  sub-bullets are the assessable items**. The consolidation parser and the mapping engine both special-case
  this (single top-level bullet ending `:` → its sub-bullets are the items). Preserve it.
- **Backtick-wrapped example tags in the preamble** are excluded by stripping code spans first — preserve
  the `re.sub(r"`[^`]*`", "", text)` step.
- **KE nested sub-bullets are folded into the parent** (one item under the parent's tag), unlike the
  PE parent-bullet case.

## §3 — Audit source assessments
*(Brownfield only — optional.)* This is the **legacy-materials** step: when a cluster's units already have
standalone assessment materials (the per-unit ATs in `original_materials/`), surface what's there so step 4
can **prefer reuse over greenfield authoring**. A **greenfield** cluster (no such materials) skips it
entirely — there is nothing to audit.

**The `evaluate-legacy-materials` agent — read-only; surfaces, never authors or decides.** Given `consolidated_uoc.md`
and `original_materials/<cluster>/`, it:
- identifies each unit's material pattern (flat / folder-structured / validation-only / non-standard) and
  lists Student + Assessor variants and supporting templates (excluding LMS bundles);
- reads each and surfaces, per source AT: a one-line summary, its **format**, the **UoC items it appears to
  touch** (by inspection, against the consolidated UoC), reusable **scenario assets**, and quality issues;
- **writes no deliverables and makes no reuse decision** — it presents the candidate set to the human.

The human carries those candidates into **step 4**, where the actual reuse decisions are made (and recorded
in the assessment plan). So there is **no separate validation gate** here: the only condition to proceed is
*greenfield → skip*, or *brownfield → the agent has run and its candidates are surfaced as an input to
step 4*. The agent is built — [`.claude/agents/evaluate-legacy-materials.md`](../.claude/agents/evaluate-legacy-materials.md);
run it when a brownfield cluster with accessible `original_materials/` arrives (it can't be exercised on S1
here — that source set isn't in this repo, and S1's audit is long done).

**Step gotchas (these inform the agent's reading):**
- **Don't trust cover-sheet titles** — e.g. ICTCLD401 AT2's sheet says "Knowledge Questions" but it's a
  6–8h AWS practical. Read the body. Source ATs also carry template residue, placeholder typos, and
  wrong-topic answer placeholders.
- **AT count varies per unit** — ICTICT517 has 5 ATs, ICTCLD401/502 have 2 each. Don't assume one-per-unit.
- **Source assessments may be drafts** (e.g. ICTCLD502 "(draft) V4.0") — note status; consider chasing a
  non-draft.
- **LMS exports (`.imscc`, `.zip`) are delivery bundles, not authored ATs** — note them, don't mine them.

## §4 — Assessment plan and scenario design
*(co-developed, human-led.)* Two captured outputs: `assessments/assessment_plan.md` **and** a scenario
design brief. The assessment plan and the scenario narrative shape each other, so develop them in
conjunction — not plan-then-scenario.

- **Assessment plan** — author `assessments/assessment_plan.md` to the **format standard**
  (`docs/assessment-plan-format.md`): the cluster AT structure with, **per AT**, its **UoC coverage**
  (canonical `[UNIT SEC num]` tags — the authoritative item→AT mapping) and its **scenario requirements**
  (`SR-*`, which subsume the unit's AC items), plus provenance, the coverage-verification rollup, and the
  scenario-requirements register. Checked by **`validate-assessment-plan`** (format linter + every
  consolidated PC/PE/KE/FS item covered by an AT). One plan per cluster; the cross-cluster view is derived
  by tooling reading across them.
- **Scenario design (the narrative)** — discuss and arrive at the story, organisation, stakeholders,
  situation and constraints that give the assessments their meaningful shape, and **capture** the agreed
  shape in a scenario design brief. Largely a human conversation; it is the upstream creative decision the
  step-5 materials are authored from and the instruments reference.
- **Why co-developed (and cross-cluster):** a scenario is only viable if it can supply the conditions every
  assessment needs. So design it against a **clear, explicit view of what each assessment must cover** —
  derived from the consolidated UoC and the AT structure. Because the scenario is a **shared cross-cluster
  asset** (single-sourced; see [scenario-flow.md](scenario-flow.md)), test that view **across clusters**,
  not just this one: the world must coherently host every cluster's assessments — providing each the
  conditions it needs, with no contradiction and no leakage between what different clusters reveal.

**Step gotcha:**
- **Cluster ATs consolidate multiple per-unit ATs** — the marking guide must still evidence every item the
  source ATs did. KE coverage splits between a written appendix and post-presentation Q&A; the standalone
  per-unit "Knowledge Questions" format is not used at cluster level.

## §5 — Scenario materials
Realise the agreed scenario design (§4) into in-world content. Build the scenario checklist (each file → the
AC items it satisfies), author public-site + internal-intranet
pages and state-versioned per-AT documents (`-S<X>-CL<Y>-AT<Z>.md`), and the website spec. Content is
**in-world only**. Student-facing references are abstract ("the YAT intranet's … page"); author/assessor
references use explicit paths.

**Step gotcha:**
- **Scenario reference framing** — student-facing artefacts reference the scenario as students consume it
  (the mock website); author/assessor artefacts use explicit repo paths.

## §6 — Assessor instruments
*(loops per AT.)* Select the institutional template (**Project Assessment** for multi-part written + observed; **Written
Assessment** for single-mode), populate the Details header (list every unit any mapped item comes from),
the Teacher/Assessor instructions, and the Marking Guide.

**Step gotchas (the traceability rule this gate enforces):**
- **Marking criteria trace to UoC, bidirectionally** — every criterion carries a full `[UNIT SEC num]`
  reference; every item the AT claims appears in ≥1 criterion; a reverse-map table closes the loop.
- **Multi-part ATs have multiple benchmark sub-sections** (Part-A + Part-B). The traceability/coverage
  validators read from the **first** benchmark heading onward, so all sub-sections are captured.
- **Compound tags must not repeat the section inside** — use `[… PE 1, 2]`, not `[… PE 1, PE 2]`
  (the latter resolves to a phantom `PE PE 2`).
- **Questions in context, not abstract recall** — "for each component, identify whether it is IaaS/PaaS/SaaS
  and why", not "explain the difference".
- **Project template fits multi-part** better than Written (native Part A/B + observation accommodation).

## §7 — Student instruments
*(loops per AT.)* Copy the institutional Student template; derive content from the assessor companion (shared Details/Task/
Resources; strip Marking Guide, assessor instructions, benchmark, model KE answers).

## §8 — Mapping documents
*(cluster-level.)* The mapping doc is a **derived artefact** — one engine (`scripts/mapping/generate_mapping_doc.py`)
generates every cluster from a `CLUSTERS` entry; per-cluster `build_s1_clN_mapping_docs.py` are thin
wrappers. Run `--check <cluster>` (reproduces committed table content) then `--build`, then the
`validate-mapping-doc` gate. Full contract + FS/AC closest-fit convention: see the standard doc.

## §9 — Cluster coverage
*(capstone.)* `validate-cluster-coverage` builds the expected item set from `consolidated_uoc.md`, collects UoC
references from each AT's benchmark, and reports MISSING (gaps to close) + PHANTOM (bad refs). AC items are
not required by default (environment-satisfied; `--include-ac` to require them). This is the capstone to the
per-AT traceability checks of step 6.

## §10 — Institutional pre-validation
Run the institutional Pre-Validation Tool over each AT; address findings; obtain stakeholder sign-off. This
gate is human/institutional and cannot be progressed in a Claude session.

---

# Appendix — process-wide gotchas

- **`source-materials.md` is partially stale** — it describes a `semester_{1,2}/cl_<name>/` layout that
  doesn't match the filesystem. Trust the actual `SX-CLY-<Name>/` layout (cluster folders sit directly
  under the repo root).
