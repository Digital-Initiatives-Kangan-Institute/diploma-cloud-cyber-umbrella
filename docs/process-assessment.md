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

Steps 5–7 are **per scenario** (once every cluster has reached step 4); steps 8–9 loop **per AT**; steps
10–11 are **cluster-level** (after all ATs exist). The **scenario plan is developed *from* the completed
consolidated assessment plan** (step 6, after step 5) — not in parallel with the cluster plans — and the
website is built *from* the scenario plan (step 7).

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
├── assessments/            # per-AT folders (AT1/, AT2/, …) — produced in steps 8–9
├── delivery/               # delivery materials (the delivery run-sheet's output)
├── mappings/               # per-UoC Assessment Mapping docs — produced in step 10
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
> step 4** — where the human decides what (if anything) to reuse while building the assessment plan (reusable
> scenario assets are carried forward to the scenario plan at step 6).

**4 · Assessment plan** *(per cluster)*
Author the **assessment plan** (one per cluster, to the format standard) — the AT structure with, **per AT**,
its **UoC coverage** (canonical `[UNIT SEC num]` tags) and its **scenario requirements** (`SR-*`, which
subsume the unit's AC items), plus provenance, the coverage-verification rollup, and the scenario-requirements
register. The scenario is **not** developed here — it is developed from the consolidated contract at step 6. →
[assessment-plan-format.md](assessment-plan-format.md) · detail [§4](#4--assessment-plan).
> **⟱ Gate 4→5:** *validator* `validate-assessment-plan` = **PASS** — the plan conforms to the format and
> every consolidated PC/PE/KE/FS item is covered by an AT; **+ human review** — the AT-structure design is
> sound and the scenario requirements (`SR-*`) are captured. *(Whether the scenario provides those `SR-*` is
> checked at the scenario plan's cross-check — step 6.)*

**5 · Consolidate the assessment plans** *(per scenario — after every cluster's step 4)*
Deterministically aggregate the scenario's per-cluster plans into one **consolidated assessment plan**
(`assessment-plans/<SEMESTER>.md`): the AT roster, the whole-of-scenario UoC coverage rollup, and the
**unioned `SR-*` register** (cluster-scoped ids → no collisions). This is the single cross-cluster contract
the scenario plan is developed from and validated against; it is **derived — never hand-edited** (the
per-cluster plans stay the source). Generated by `generate_consolidated_plan.py`. → detail [§5](#5--consolidate-the-assessment-plans).
> **⟱ Gate 5→6:** *validator* `validate-consolidated-plan` = **PASS** — the consolidated plan is an exact,
> faithful union of the per-cluster plans (no missing/extra AT, coverage entry, or `SR-*`). Regenerate if it
> reports drift.

**6 · Scenario plan** *(per scenario — developed from the completed contract)*
Develop the **scenario plan** (`scenario-plans/<SEMESTER>.md`, to the format standard) in two parts:
**Part 1** the **scenario narrative** (the story bible — organisation, people, systems, situation, constraints,
tone; human-led creative work) and **Part 2** the **forward build checklist** — every artefact to build (policy,
project doc, template, lab-pack, role), each with **keynotes**, a status, a target location, the `SR-*` it
satisfies and the AT(s)/practice that consume it. Developed *from* the consolidated contract (its `SR-*`
register is the input), **not** in parallel with the cluster plans. →
[scenario-plan-format.md](scenario-plan-format.md) · [scenario-flow.md](scenario-flow.md) · detail [§6](#6--scenario-plan).
> **⟱ Gate 6→7:** *validator* `validate-scenario-plan` = **PASS** — the plan conforms to the format and every
> `SR-*` in the consolidated assessment plan is satisfied by ≥1 checklist item, with no phantom `SR-*`; **+
> human review** — Part 1's world is **viable** (it can host every assessment) and coherent (no leakage between
> clusters; consistent system state).

**7 · Scenario materials** *(per scenario — built from the scenario plan; timing flexible)*
Build the in-world content **from the scenario plan's checklist (step 6)** — single-sourced on the website
(in-world only — no course/assessment meta-language), each checklist item realised at its target location to
its keynotes. Expect significant human↔AI looping. →
[scenario-flow.md](scenario-flow.md) · [website-architecture.md](website-architecture.md) · detail [§7](#7--scenario-materials).
> **⟱ Gate 7→8:** the **[`verify-scenario-realisation` agent](../.claude/agents/verify-scenario-realisation.md)**
> *(read-only)* = every Part-2 item is **realised** in the built website/repos (no NOT-FOUND) and its content
> **meets its keynotes** (no `partial`/`mismatch`); orphans + in-world/consistency breaches surfaced **+ human
> review**. The agent remaps plan↔website from scratch each run; re-run after each batch of fixes until clean.

**8 · Assessor instruments** *(loop per AT)*
Populate the institutional assessor template for each AT: Details, Teacher/Assessor instructions, and the
**Marking Guide with bidirectional UoC traceability** (every criterion carries `[UNIT SEC num]`; a reverse
map closes the loop). → [cluster-authoring-conventions.md](cluster-authoring-conventions.md) · [document-template-system.md](document-template-system.md) · detail [§8](#8--assessor-instruments).
> **⟱ Gate 8→9:** *validator* `validate-at-traceability` = **PASS** for the AT (no phantom tags, no
> free-floating criteria; pass the AT's allocation via `--expect` for reverse-coverage) **+ human review**.

**9 · Student instruments** *(loop per AT)*
Derive the student-facing instrument from the assessor version (shared Details/Task/Resources; strip the
Marking Guide, benchmark, and model answers). → detail [§9](#9--student-instruments).
> **⟱ Gate 9→10:** *human review* — student copy carries everything the student needs and nothing
> assessor-only. *(No script.)*

**10 · Mapping documents** *(cluster-level)*
Generate the per-unit Assessment Mapping docs from the engine (rows from the source UoC, AT-column codes
from the assessor benchmarks, FS/AC closest-fit). Never hand-edit a mapping docx — it is derived. →
[mapping-document-standard.md](mapping-document-standard.md) · detail [§10](#10--mapping-documents).
> **⟱ Gate 10→11:** *validator* `validate-mapping-doc` = **PASS** for every unit — complete vs the unit's
> own UoC (every item present + mapped) and accurate vs the benchmarks (PC/PE/KE hard; FS/AC advisory)
> **+ human review**.

**11 · Cluster coverage** *(capstone)*
Confirm the cluster's ATs, taken together, evidence **every** consolidated item. → [validate-cluster-coverage skill](../diploma-cloud-cyber-content/.claude/skills/validate-cluster-coverage/SKILL.md) · detail [§11](#11--cluster-coverage).
> **⟱ Gate 11→12:** *validator* `validate-cluster-coverage` = **100%** (no MISSING required item, no
> PHANTOM reference; AC environment-satisfied unless `--include-ac`) **+ human review**.

**12 · Institutional pre-validation**
Run the institutional Pre-Validation Tool over each AT and address findings. → detail [§12](#12--institutional-pre-validation).
> **⟱ Gate 12→done:** *human / institutional* sign-off. The cluster's assessment is complete.

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

## §4 — Assessment plan
*(per cluster, human-led.)* Author `assessments/assessment_plan.md` to the **format standard**
(`docs/assessment-plan-format.md`): the cluster AT structure with, **per AT**, its **UoC coverage**
(canonical `[UNIT SEC num]` tags — the authoritative item→AT mapping) and its **scenario requirements**
(`SR-*`, which subsume the unit's AC items), plus provenance, the coverage-verification rollup, and the
scenario-requirements register. Checked by **`validate-assessment-plan`** (format linter + every consolidated
PC/PE/KE/FS item covered by an AT). One plan per cluster; the cross-cluster view is derived by tooling reading
across them (step 5).

The **scenario is not designed here.** The per-AT `SR-*` capture *what the scenario must provide* for this
cluster; the scenario itself is developed once at step 6, from the **consolidated** contract (step 5) — the
cross-cluster view of what every assessment covers is exactly what makes a scenario viable, and that view is
the consolidated plan, not anything authored in parallel with the cluster plans.

**Step gotcha:**
- **Cluster ATs consolidate multiple per-unit ATs** — the marking guide must still evidence every item the
  source ATs did. KE coverage splits between a written appendix and post-presentation Q&A; the standalone
  per-unit "Knowledge Questions" format is not used at cluster level.

## §5 — Consolidate the assessment plans
*(Per scenario — once every cluster's step-4 plan exists.)* Run `generate_consolidated_plan.py --semester
<S>` to derive `assessment-plans/<S>.md` from the per-cluster `assessment_plan.md` files: the AT roster, the
whole-of-scenario UoC coverage rollup, and the **unioned `SR-*` register** (cluster-scoped ids, so the three
registers union without collision). The output is **derived — never hand-edited**; the per-cluster plans
remain the authored source. **`validate-consolidated-plan`** re-reads the sources and independently parses
the consolidated, asserting it is an exact faithful union (catching a stale aggregate, a hand-edit, or a
generator bug). The consolidated `SR-*` register is the single contract the scenario plan (§6) is validated
against.

## §6 — Scenario plan
*(per scenario — developed from the completed contract, not in parallel with the cluster plans.)* Author the
**scenario plan** (`scenario-plans/<SEMESTER>.md`) to the format standard
([scenario-plan-format.md](scenario-plan-format.md)) in **two parts of different nature**:

- **Part 1 — scenario narrative (the story bible).** The fiction: organisation, people, systems, situation +
  drivers, constraints, tone. **Human-led creative** work (AI assists; never auto-generated). Its only test is
  **viability** — can this world plausibly host every assessment? — a cross-cluster human judgement (the world
  is single-sourced and shared; see [scenario-flow.md](scenario-flow.md)).
- **Part 2 — the forward build checklist.** Every artefact to build — policy, project doc, template, lab-pack,
  stakeholder role — as a `SE-NN` item carrying **keynotes** (what it must contain), a **status** (`to-build` /
  `built` / `carry-over`), a target **location**, the **`SR-*`** it satisfies, and the AT(s)/practice that
  consume it. Items are grouped by target website content-collection so the step-7 build maps to them. The
  consolidated `SR-*` register (step 5) is the input — the checklist exists to satisfy it.

**`validate-scenario-plan`** lints the format (both parts present; each item carries `Satisfies:` + `Keynotes:`)
and cross-checks Part 2 bidirectionally against the consolidated register: every `SR-*` is satisfied by ≥1 item
(UNCOVERED otherwise), no item claims an `SR-*` outside the register (PHANTOM otherwise). The contract is
*derived*; the scenario plan is *authored*; the website (step 7) is *generated from* the scenario plan.

**Step gotchas:**
- **Part 1 is creative, Part 2 is contract-bound** — the linter only checks Part 1 is present; it never
  constrains the fiction. Keep the human↔AI creative loop on Part 1; let the rails (coverage + cross-check)
  catch dropped requirements in Part 2.
- **An item may satisfy several `SR-*`** (one role-brief → stakeholders + team) and world-building items may
  satisfy none (advisory) — group by what the artefact *is*, not one item per `SR-*`.

## §7 — Scenario materials
*(per scenario — built from the scenario plan; timing flexible.)* Realise each Part-2 checklist item into
in-world content at its target location, to its keynotes: author public-site + internal-intranet pages and
state-versioned per-AT documents (`-S<X>-CL<Y>-AT<Z>.md`), and the website spec. Content is **in-world only**.
Student-facing references are abstract ("the YAT intranet's … page"); author/assessor references use explicit
paths. Expect significant human↔AI looping; the scenario plan is what keeps it convergent.

The gate condition is the **`verify-scenario-realisation` agent** (read-only): it walks **every** Part-2
`SE-NN` item, locates its realisation in the built website/content repos (mapping plan↔website **live**, from
scratch — no stored manifest), and reports per item **FOUND / NOT-FOUND** plus a **keynote check**
(`meets`/`partial`/`mismatch`); it also surfaces **orphans** (built content traced to no item) and
**in-world/consistency** breaches. It *surfaces only* — the human fixes gaps, then re-runs it until the
realisation table is clean. Why an agent and not a deterministic script here: the other gates check
already-structured data (tags, table rows), but this gate bridges **prose items ↔ a file tree** — locating
which file realises an item, and judging whether its content meets the keynotes, is inherently semantic, and
the agent must read everything for the keynote check anyway. (Upstream, `validate-scenario-plan` already
deterministically guarantees plan ↔ contract — the rail is there, where the data is structured.) *(A
website-build-from-plan generator remains possible future tooling for authoring the materials; this step's
**gate** is the verification agent.)*

**Step gotcha:**
- **Scenario reference framing** — student-facing artefacts reference the scenario as students consume it
  (the mock website); author/assessor artefacts use explicit repo paths.

## §8 — Assessor instruments
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

## §9 — Student instruments
*(loops per AT.)* Copy the institutional Student template; derive content from the assessor companion (shared Details/Task/
Resources; strip Marking Guide, assessor instructions, benchmark, model KE answers).

## §10 — Mapping documents
*(cluster-level.)* The mapping doc is a **derived artefact** — one engine (`scripts/mapping/generate_mapping_doc.py`)
generates every cluster from a `CLUSTERS` entry; per-cluster `build_s1_clN_mapping_docs.py` are thin
wrappers. Run `--check <cluster>` (reproduces committed table content) then `--build`, then the
`validate-mapping-doc` gate. Full contract + FS/AC closest-fit convention: see the standard doc.

## §11 — Cluster coverage
*(capstone.)* `validate-cluster-coverage` builds the expected item set from `consolidated_uoc.md`, collects UoC
references from each AT's benchmark, and reports MISSING (gaps to close) + PHANTOM (bad refs). AC items are
not required by default (environment-satisfied; `--include-ac` to require them). This is the capstone to the
per-AT traceability checks of step 8.

## §12 — Institutional pre-validation
Run the institutional Pre-Validation Tool over each AT; address findings; obtain stakeholder sign-off. This
gate is human/institutional and cannot be progressed in a Claude session.

---

# Appendix — process-wide gotchas

- **`source-materials.md` is partially stale** — it describes a `semester_{1,2}/cl_<name>/` layout that
  doesn't match the filesystem. Trust the actual `SX-CLY-<Name>/` layout (cluster folders sit directly
  under the repo root).
