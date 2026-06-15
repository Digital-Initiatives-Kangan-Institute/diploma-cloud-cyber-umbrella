# Cluster development process — for LLM agents

**Audience:** an LLM agent picking up the cluster refactor task. Not a human-facing document.

**Status:** Steps 1-7 below define the assessment-creation process, applied end-to-end on the S1-CL1 pilot. Follow them for a new cluster; see the cluster's working state (in LLM memory) for the worked end state.

**Prerequisites you must read before acting:**
- `CLAUDE.md` (repo root) — working rules. Rule 1: nothing recorded as decided without Tim's explicit approval. Rule 5: no unilateral git operations.
- [project-overview.md](project-overview.md) — project scope, in/out of scope, operating principles.
- `clusters.md` — cluster composition (units per cluster).
- [source-materials.md](source-materials.md) — workspace layout. Note: `source-materials.md` describes a nested `courseware/semester_{1,2}/cl_<name>/` layout, but cluster folders now sit directly under the repo root as `SX-CLY-<Cluster-Name>/`. Trust the filesystem over `source-materials.md`.

**Working rules for documents you produce:**
- Verbatim quoting only. No paraphrasing, no creative interpretation, no completion of partial source material.
- Every quoted item carries a source reference tag `[UNIT SECTION numbering]` (e.g. `[ICTCLD401 PC 1.2]`).
- Mark all produced documents as **DRAFT** at the top with a status banner. Groupings, comments, assessment ideas are proposals, not decisions.
- Do not modify anything under `original_materials/`. It is read-only reference.

---

## Skills — the deterministic spine of this process is now skill-driven

The faithful, unforgiving parts of this process — transcription, consolidation, and the various
completeness/traceability checks — are packaged as portable Claude Code skills under
`.claude/skills/` (they travel with the repo and lift into future courses unchanged). **Prefer the
skill**; the step text below documents what each does and the conventions it follows, and remains
the reference if you need to run the underlying script by hand.

| Step | Need | Skill | Bundled script | Model |
|---|---|---|---|---|
| 1 (prereq) | Transcribe a unit `.docx` → verbatim `.md` | `transcribe-uoc` | `transcribe_uoc.py` | Haiku |
| 1 | Check a transcription is verbatim against its `.docx` | `validate-uoc-transcription` | `validate_uoc.py` | Haiku |
| 2 | Build a cluster's `consolidated_uoc.md` | `consolidate-uocs` | `inventory_uoc.py` | Opus |
| 2.5 | Check a consolidation is complete | `validate-uoc-consolidation` | `validate_consolidated.py` | Haiku |
| 6 | Check one AT's UoC traceability (every criterion tagged, every reference real) | `validate-at-traceability` | `validate_at_traceability.py` | Haiku |
| 6–7 | Check the cluster's ATs together evidence every consolidated item | `validate-cluster-coverage` | `validate_cluster_coverage.py` | Haiku |
| delivery 3 | Gate a teaching deck's size before committing | `inspect-file-size` | `inspect-file-size/inspect_file_size.py` | Haiku |

The skills call deterministic, **stdlib-only** scripts in `.claude/skills/scripts/`, so the work is
faithful by construction and runs anywhere with `python3` (no virtualenv). Composition is by shared
script, not skill-to-skill chaining: `transcribe-uoc` runs the `validate_uoc.py` gate itself, and
`consolidate-uocs` runs the `validate_consolidated.py` gate itself, so every produced artefact is
auto-validated deterministically; the standalone `validate-*` skills re-check an existing artefact
without rebuilding it. Steps 3–7 remain **authoring** steps (judgement-led), but their key
correctness checks — marking-guide traceability (Step 6) and cluster coverage (Steps 6–7) — are now
skill-gated; only the authoring itself is manual.

---

## Cluster folder layout (input state)

The target cluster directory is `SX-CLY-<Cluster-Name>/`. Every cluster folder has one consistent shape — `units_of_competency/` and `mappings/` are **top-level siblings** of `assessments/`. Before you start, it must contain:

```
SX-CLY-<Cluster-Name>/
├── assessments/                          # per-AT folders (AT1/, AT2/, ...) — populated in Steps 6–7
│   ├── AT1/
│   ├── AT2/
│   └── ...
├── delivery/                             # teaching/delivery materials (topic_NN/ etc.)
├── mappings/                             # per-UoC Assessment Mapping docs (one per unit)
├── units_of_competency/
│   ├── <UNIT_A>_Complete_R1.md           # markdown transcription
│   ├── <UNIT_B>_Complete_R1.md
│   ├── ...
│   └── original/
│       ├── <UNIT_A>_Complete_R1.docx     # source UoC (read-only)
│       ├── <UNIT_B>_Complete_R1.docx
│       └── ...
└── consolidated_uoc.md                   # produced in Step 2 (at the cluster root)
```

The validators' `UOC_DIR` and Step 1's `cd` target are `<cluster>/units_of_competency/`.

If any `.md` is missing while its `.docx` exists, transcribe it with the **`transcribe-uoc`** skill (it lifts the unit content verbatim from the Word XML — never retyped — reconstructs the structure from the document styles, and auto-validates the result). Transcription used to be an out-of-band prerequisite; it is now a skill.

---

## Step 1 — Validate UoC transcription fidelity

**Purpose:** confirm each `.md` UoC is verbatim against its `.docx` source. No LLM hallucination, paraphrasing, or omission.

**Inputs:** every `.docx`/`.md` pair under `assessments/units_of_competency/` (paired by filename).

**Method:** Invoke the **`validate-uoc-transcription`** skill on the cluster's `<docx> <md>` pairs.
It runs the bundled validator (`.claude/skills/scripts/validate_uoc.py`) and interprets the result
per the exit criteria below. The same validator also lives at `<repo_root>/scripts/validate_uoc.py`
(Appendix A reproduces its source); to run it by hand:
   ```bash
   cd <cluster_dir>/units_of_competency
   python3 .claude/skills/scripts/validate_uoc.py \
     original/<UNIT_A>_Complete_R1.docx <UNIT_A>_Complete_R1.md \
     original/<UNIT_B>_Complete_R1.docx <UNIT_B>_Complete_R1.md \
     ...
   ```

**Behaviour of the validator (see Appendix A for source):**
- Extracts text from `.docx`/`word/document.xml` — paragraphs and table cells in document order, with `w:br` → newline, `w:tab` → tab.
- **Excludes headers and footers** (`word/header*.xml`, `word/footer*.xml`) — per Tim 2026-05-22.
- Strips markdown syntax from `.md`: headings (`#`/`##`/...), table pipes and `| --- |` separator rows, list bullets (`-`/`*`/`+`/`N.`), `<br>` → newline.
- Tokenises both to whitespace-separated words and compares sequences.
- Two-tier comparison: substantive (word add/remove/change) vs cosmetic (smart quotes, en/em dashes, NBSP, soft hyphen, BOM).

**Exit criteria:**
- Every pair returns `EXACT MATCH (byte-equivalent at word level)`.
- `VERBATIM after cosmetic normalisation` is acceptable but report the cosmetic diffs to Tim — he may want to fix the source.
- Any `SUBSTANTIVE DIFFERENCES FOUND` result blocks progress. Do not proceed to Step 2 until resolved.

**Result for S1-CL1 (2026-05-22):** all three pairs (ICTCLD401, ICTCLD502, ICTICT517) returned `EXACT MATCH`.

---

## Step 2 — Build consolidated UoC

**Purpose:** produce a single `consolidated_uoc.md` at the cluster root, containing every PC / FS / PE / KE / AC across all units in the cluster, verbatim, source-tagged, organised into groups where assessment overlap is plausible.

**Output:** `SX-CLY-<Cluster-Name>/consolidated_uoc.md`.

**Now skill-driven:** the **`consolidate-uocs`** skill performs this step — it extracts every item
verbatim and pre-tagged (`inventory_uoc.py`), groups them into topics (the editorial judgement,
always marked **DRAFT / TBD** per Rule 1), then validates completeness (the `validate-uoc-consolidation`
skill / `validate_consolidated.py`). The grouping is the only judgement layer; the extract and
validate layers are deterministic. The sub-steps below document the conventions the skill follows —
they are also in the skill's own `references/consolidation-guide.md`.

**Sections excluded from consolidation** (per Tim 2026-05-22): Application, Unit Sector, Modification History, Unit Mapping Information, Links. The consolidation covers only the **five assessable element types**: PC, FS, PE, KE, AC.

### 2.1 Itemise every PC/FS/PE/KE/AC from each source UoC

For each unit, extract every item across the five element types and assign a stable reference number:

| Section | Numbering scheme |
|---|---|
| PC | Use the source numbering (e.g. `1.2`, `3.4`). Source format inside the Elements table: `<num> <text>` separated by `<br>`. |
| FS | Use the skill name from the Foundation Skills table (e.g. `Reading`, `Oral Communication`, `Get the work done`). Skill names are not unique per unit but **are** unique per unit + skill. |
| PE | Number top-level bullets `1..N` in source order. **Special case:** if the only top-level bullet is a parent ending with `:` (e.g. ICTICT517's `- For one organisation:`), number the immediate sub-bullets `1..N` instead. |
| KE | Number top-level bullets `1..N` in source order. Nested sub-bullets are quoted as part of the parent item, not as separate items. |
| AC | Number access-list bullets `1..N` in source order. The trailing prose paragraph `Assessors of this unit must satisfy...` is numbered as the next item (e.g. AC 5 for ICTCLD401, AC 9 for ICTCLD502, AC 6 for ICTICT517). |

### 2.2 Quote each item verbatim

- Copy the text directly from the source `.md`. No paraphrasing.
- Preserve PC numbering prefix in the quoted text (e.g. `1.2 Identify impact of shared security responsibility models` — the `1.2 ` stays in the quote).
- For nested KE bullets, preserve the indentation structure. The whole parent + children is quoted as one item.

Example:
```
- [ICTCLD401 KE 3] principles and functions of cloud computing solutions and technologies, including:
  - Infrastructure as a Service (IaaS)
  - Platforms as a Service (PaaS)
  - Software as a Service (SaaS)
```

### 2.3 Tag each item with `[UNIT SECTION numbering]`

Format: `[<UNIT_CODE> <SECTION> <numbering>]`. Examples:
- `[ICTCLD401 PC 1.2]`
- `[ICTCLD502 FS Oral communication]`
- `[ICTICT517 PE 3]`
- `[ICTCLD401 KE 11]`
- `[ICTCLD502 AC 9]`

**Tags must appear unwrapped in the consolidated doc** (i.e. not inside backticks) for the validator in Step 2.5 to count them as real references. The preamble may use backtick-wrapped tags as examples — those are excluded from the count.

### 2.4 Group items where assessment overlap is plausible

- Group items where the underlying competency/topic is similar enough that one assessment artefact could plausibly evidence all members.
- Each group has:
  - A heading: `## Group N — <short name>`.
  - **Why grouped:** 1–2 sentences. Brief.
  - **Assessment idea (TBD):** 1–2 sentences. Brief. Mark as TBD per CLAUDE.md Rule 1.
  - The list of items, each verbatim with source tag.
- Items that don't fit any group go under `## Ungrouped items` with a one-line note on why they're ungrouped.
- **Do not record groupings as decisions.** They are Claude's proposals subject to Tim's review.

### 2.5 Validate the consolidated document

Invoke the **`validate-uoc-consolidation`** skill. It runs the bundled, general arg-driven validator
(`.claude/skills/scripts/validate_consolidated.py`) — no per-cluster code edits, the cluster and its
units are arguments:

```bash
python3 .claude/skills/scripts/validate_consolidated.py --cluster <cluster> \
  --unit <CODE>=units_of_competency/<CODE>_Complete_R<N>.md \
  --unit <CODE>=units_of_competency/<CODE>_Complete_R<N>.md \
  [--assessor-ac]
```

(`--assessor-ac` counts the trailing "Assessors of this unit must satisfy…" paragraph as one extra
AC item — on for CL1–CL3. Appendix B reproduces an older S1-CL2-hardcoded version for reference.)

The validator:
- Parses each source `.md` to build the expected reference inventory (PCs from the Elements table, FSs from the Foundation Skills table, PE/KE/AC by counting top-level bullets with the parent-bullet special case for ICTICT517-PE-style structures).
- Parses `consolidated_uoc.md`, **stripping single-backtick code spans first** so that example tags in the preamble are not counted.
- Extracts every `[<UNIT> <SECTION> <numbering>]` tag.
- Reports MISSING, UNEXPECTED, DUPLICATED items.

**Exit criteria:** validator prints `RESULT: PASS — every expected item appears exactly once, nothing extra.`

**Result for S1-CL1 (2026-05-22):** PASS — 126 items expected (52 PCs + 16 FSs + 14 PEs + 24 KEs + 20 ACs), 126 references found, all unique.

---

## Step 3 — Audit existing standalone assessments for reuse potential

**Purpose:** understand what assessment content already exists for each unit in `original_materials/`, so the cluster assessment plan in Step 4 prefers reuse over greenfield authoring.

**Inputs:** `original_materials/DipIT_20260313/SX-CLY-<Cluster-Name>/<UNIT>/` for each unit in the cluster.

**Method:**

1. **Identify each unit's material pattern.** From [source-materials.md](source-materials.md):
   - **Pattern A — flat:** assessment files at the top of the unit folder, named `<UNIT> AT1 …docx`, `<UNIT> AT2 …docx` (Student + Assessor variants).
   - **Pattern B — folder-structured:** assessments nested under `Assessment Tool/AT1/`, `Assessment Tool/AT2/`.
   - **Pattern C — validation-only:** real content buried inside `Original (pre external validation)/` or `Post external validation/` subfolders.
   - **Pattern D — non-standard:** handle case-by-case (e.g. ICTCYS407's Splunk-heavy structure with Moodle `.mbz` and VM artefacts).
2. **List the assessment artefacts** for each unit. Note both Student/Learner and Assessor versions. Note supporting templates (e.g. ICTICT517 has `Cost Benefit Analysis template.xlsx`, `Draft Plan template.docx`, `Feedback Record template.docx`). Brightspace/LMS exports (`.imscc`, `.zip`) are delivery bundles, not authored assessment artefacts — note them but don't treat as ATs.
3. **Extract text from each `.docx`** using the existing `docx_to_text` from `scripts/validate_uoc.py`. Dump to a scratch directory (e.g. `/tmp/<cluster>_assess/`) — these are throwaway working files, not versioned outputs.

   ```bash
   mkdir -p /tmp/<cluster>_assess
   cd <repo_root>/original_materials/DipIT_20260313/SX-CLY-<Cluster-Name>
   python3 -c "
   import sys
   sys.path.insert(0, '<repo_root>/scripts')
   from validate_uoc import docx_to_text
   from pathlib import Path
   files = {
       # Edit this dict for each cluster — map output filename → source .docx path
       '<unit>_AT1_student.txt':  '<UNIT>/.../AT1 Student.docx',
       '<unit>_AT1_assessor.txt': '<UNIT>/.../AT1 Assessor.docx',
       # ...
   }
   for out, src in files.items():
       Path('/tmp/<cluster>_assess', out).write_text(docx_to_text(Path(src)))
       print(f'{out}: extracted')
   "
   ```

4. **Read each Student/Learner version** to understand what each task assesses (the task instructions and questions). Dip into Assessor versions when you need:
   - the mapping table showing which question maps to which PC/PE/KE
   - the expected/benchmark answers (only if you need to understand expected scope)
5. **For each existing AT, capture (mentally or in a scratch note):**
   - One-line summary of what it does
   - Which UoC items (PC/PE/KE) it appears to address — by inspection, not by reading any pre-existing mapping doc
   - Format (Questioning / Portfolio / Observation / Report / Case-Study / mixed)
   - Notable scenario assets (case studies, strategic plans, network diagrams, organisational policies, supporting templates, code repositories referenced) — these are reusable raw material for Step 4
   - Any quality issues to be aware of (cover-sheet typos, placeholder bugs in question templates, drafts marked "for review", inconsistent versioning between Student and Assessor copies)

**Output:** an internal working inventory feeding Step 4. May be a scratch artefact (the extracted text files + your mental map) rather than a versioned document — the audit findings get crystallised into `assessment_plan.md` in Step 4.

**Exit criteria:** you can name, for each unit, every AT in source, what format it is, what UoC items it appears to cover, and what scenario assets it carries.

**Result for S1-CL1 (2026-05-22):**
- **ICTCLD401** (Pattern B): AT1 Questioning (KE-coverage, 13 questions, one placeholder bug at Q12); AT2 actually a 6–8h AWS practical despite the cover-sheet mislabelling it "Knowledge Questions" — 5 parts covering IAM, VPC, EC2, RDS, multi-layer + autoscaling. No standalone HA-style practical.
- **ICTCLD502** (Pattern A): AT1 Questioning (KE coverage); AT2 Portfolio-Observation-Report (HA practical against the "Llamazonia" e-commerce case study — boss-interview-driven HA-requirements activity, on-prem evaluation, cloud HA design, implementation, failure simulation).
- **ICTICT517** (Pattern A): five-AT structure — AT1 Knowledge Questions (open-response, 3 Qs against KE 1–4), AT2 Evaluate Strategic Plan (against the YAT College case study with full strategic plan, ICT environment description), AT3 Effects of Change (Part 1 CBA + Part 2 observation meeting with superior and colleague), AT4 Develop Action Plan and Obtain Approval, AT5 Knowledge Quiz (MCQ on broader IT/management concepts). YAT case study includes a documented change-management procedure usable as a closure-cycle scaffold.

---

## Step 4 — Synthesise cluster assessment plan

**Purpose:** produce a cluster-level assessment plan that draws on the existing standalone content from Step 3 where possible, identifies the gaps, and weaves everything into a single integrated scenario so the cluster delivery feels coherent rather than three units stapled together.

**Output:** `<cluster>/assessments/assessment_plan.md`.

**Method:**

1. **Pick a scenario spine.** Look at existing case studies across the unit assessments. Recommend the one that:
   - Has the most pre-authored scaffolding (strategic plan, environment description, stakeholder hierarchy, procedures, supporting templates).
   - Can absorb the technical work of the other units with rename-only changes (e.g. one web-workload migration narrative can carry a foundation build *and* an HA hardening exercise).
   - Maintains a professional tone appropriate for the qualification level.
   - **Mark the recommendation as TBD per CLAUDE.md Rule 1.** Never lock in a scenario without explicit approval. Present the alternatives with reasoning.
2. **Propose a cluster AT structure.** Typical shape: one running case-study project broken into phases (e.g. strategic context → foundation build → harden/extend → closure) + one consolidated written/questioning AT alongside that covers all units' KE.
3. **Map provenance per AT.** For each cluster AT, document:
   - Which source ATs / templates / parts it draws from (specific names and parts, not generic references)
   - What's used "as-is" vs "with modification"
   - The specific modifications required
4. **Build the group coverage map.** A table with one row per group + ungrouped item from `consolidated_uoc.md`. For each, state which cluster AT covers it and how. This is the audit trail proving every UoC item is addressed. **No row may be missing.** If you can't justify a row, the cluster AT structure has a hole and must be revised before the doc is shipped.
5. **List required modifications and additions.** Two sub-lists:
   - **Modifications** to existing content: rewrites, dedup between source ATs, scenario rebrands, bug fixes (e.g. broken question-answer placeholders).
   - **New authoring required:** closure brief, bridging instructions between phases, any sub-deliverables that fill gaps the source ATs don't cover (e.g. a Security Responsibilities Matrix to operationalise a shared-responsibility-model group).
6. **List things to drop / set aside** — source content that doesn't fit the cluster structure, would create assessment-strategy mismatch (e.g. mixing MCQ with open-response in one AT), or is vendor-specific in a way that limits reuse.
7. **List open questions** — choices the plan makes that warrant Tim's review before drafting begins. Be specific (e.g. "Scenario choice — YAT vs Llamazonia vs reskinned alternative — same-industry-as-Tim's-workplace risk for YAT").
8. **Mark everything TBD** per Rule 1. The plan is a proposal, not a decision.

**Exit criteria:**
- Group coverage map has explicit entries for **every** group + ungrouped item from `consolidated_uoc.md`. None missing.
- Modifications/additions list is concrete enough for the next stage to act on (each item names the specific source AT/part it touches and what changes).
- Open questions are framed as choices, not vague uncertainties.

**Result for S1-CL1 (2026-05-22):** plan produced at `S1-CL1-Cloud-Design-Build/assessments/assessment_plan.md`. Recommends **YAT College** as scenario spine (from 517's existing case study), four-phase project (Strategic context / Foundation build / HA hardening / Closure) + one consolidated questioning AT. 6 modifications and 6 new authoring items identified. 6 open questions flagged. All marked TBD.

---

## Step 5 — Author cluster scenario materials

**Purpose:** build the shared cluster scenario that AT-authoring depends on. Per the S1-CL1 pilot the scenario is single-sourced on the website (see the sibling doc [scenario-flow.md](scenario-flow.md)); reference scenario content abstractly, never by path.

**Output:** a populated `<repo_root>/scenario/` folder containing public-site content, internal-intranet content, state-versioned documents per AT, templates, and a `website.md` spec for the mock delivery vehicle.

**Method:**

1. **Build the scenario checklist** at `<repo_root>/scenario/checklist.md` listing every document/page the scenario must publish, mapped to the UoC AC items it satisfies (per `consolidated_uoc.md`).
2. **Author content files** organised as:
   - Public-site pages (`public-*.md`) — about/mission, strategic plan summary, org structure, locations, cluster project narrative front page
   - Internal-intranet pages (`internal-*.md`) — ICT environment overview, on-prem network diagram, LMS server status, hardware/software inventory, backup/recovery process, LMS app spec, policies (change management, user access, acceptable use, WHS, privacy, backup-retention, security/incident-response), references (industry standards, legislative requirements, reference architectures), project/engagement materials (role brief, migration requirements, consultation notes, CBA cost inputs, HA database requirements)
   - State-versioned files use suffix `-S<X>-CL<Y>-AT<Z>.md` (e.g. `internal-ict-environment-overview-S1-CL1-AT1.md`); stable files have no suffix
   - Each file carries `**Relevant to:**` header naming the AT(s) the version is valid for
3. **Author the `website.md` spec** for the mock delivery vehicle (intent, site structure, SSO gate, state-versioning behaviour, hosting/build TBDs).
4. **Validate content fidelity:** scenario content adapted from existing materials (e.g. YAT case study) preserves the source structure with adjustments noted per the legal-reuse rules in [reuse-permissions.md](reuse-permissions.md).

**Exit criteria:** every scenario file in the checklist is either authored, marked as carry-over from existing materials, or explicitly flagged TBD. Cross-references between scenario files use bare filenames (since they live in the same folder).

**Result for S1-CL1 (2026-05-23):** scenario complete — 27 content files (6 public + 21 internal) + `website.md` spec + checklist. YAT College RTO scenario at 175 Cremorne St, Cremorne VIC. ICT staff lack cloud experience; MTS engaged for the migration; Sam Walker = YAT ICT Manager, Pat Lin = MTS Senior Consultant (TBD placeholder names).

---

## Step 6 — Author per-AT assessor template content

**Purpose:** turn the cluster assessment plan and scenario into a populated institutional assessor template for each AT, ready for live delivery.

**Output:** per-AT assessor `.docx` (the institutional template) + companion `.md` (the source-of-truth content). For each AT this includes the Details header, the Teacher/Assessor Instructions (assessment overview, task description, resources, criteria), and the Marking Guide with full UoC traceability.

**Method:**

1. **Select the right institutional template** from `<repo_root>/templates/`:
   - **Project Assessment - Assessor.docx** fits multi-part assessments (e.g. written deliverable + observed presentation) because of its native Part A / Part B structure + per-Part marking guide tables + observation accommodation.
   - **Written Assessment - Assessor.docx** fits single-mode written assessments only.
2. **Copy the chosen institutional template** into the cluster AT folder with a descriptive name (e.g. `AT1 - Business Case - Assessor.docx`). Do not modify the .docx structure.
3. **Author a companion markdown file** with the same name (`AT1 - Business Case - Assessor.md`) that mirrors the template structure. This is the source-of-truth that's pasted into the .docx when locked in.
4. **Populate the Details header** — qualification, unit code(s) (list all units from which any UoC requirement is mapped to this AT — see Step 4's group coverage map), assessment task title, task number (X of Y), due date (leave blank — per delivery), assessor name (leave blank).
5. **Populate the Teacher/Assessor Instructions** — sections per the template:
   - Assessment overview (method, open/closed book, reasonable adjustment, support level, submission)
   - Task(s) to be assessed (with the Part A / Part B structure if multi-part; reference the scenario site by placeholder URL; reference the Document Archive for example past business cases / past presentations)
   - Time allowed (leave blank per Tim's standing direction)
   - Location (leave blank)
   - Resources required (teacher/assessor + student supplied — include scenario site access + lab access + role-play preparation)
   - Assessment criteria (Satisfactory rule)
   - Second attempt + Assessment retention (institutional boilerplate — preserve as-is)
6. **Author the Marking Guide** — the most substantial section. Apply the **bidirectional UoC traceability rule** (see [cluster-authoring-conventions.md](cluster-authoring-conventions.md) §1):
   - Each marking criterion has a UoC reference column with full `[UNIT SECTION numbering]` notation
   - Every UoC item the AT claims to evidence (from the cluster assessment plan's group coverage map) must appear in at least one criterion
   - Include a **UoC coverage verification (reverse map)** table at the end of the Marking Guide that lists every UoC item AT-X claims to evidence + the criterion(ia) that evidence it
   - Scope strictly to what AT-X is mapped to; explicitly note which UoC items are deferred to other ATs in the cluster
7. **Surface scenario-authoring dependencies discovered during drafting** — add them to the scenario checklist's backlog (e.g. example previous business cases in the Document Archive) so they don't get lost.
8. **Tim copy-pastes the markdown content into the .docx** when locked in. The .docx becomes the canonical institutional artefact.

**Exit criteria:**
- The Marking Guide's reverse-map table closes the loop (no UoC item claimed by the AT is left without a criterion; no criterion exists without UoC traceability).
- **Confirmed mechanically with the `validate-at-traceability` skill** — no free-floating criteria, no phantom/mistyped references; and, passing the AT's allocation from the Step 4 group coverage map via `--expect`, every item the AT is meant to evidence is present.
- All scenario-authoring dependencies surfaced during AT drafting are added to the scenario checklist's backlog.
- The .docx is populated with the markdown content (post-paste).

**Result for S1-CL1 AT1 (2026-05-24):** markdown content drafted at `S1-CL1-Cloud-Design-Build/assessments/AT1/AT1 - Business Case - Assessor.md`; .docx awaits paste. See the cluster's working state (in LLM memory) for the full state.

---

## Step 7 — Author per-AT student template content

**Purpose:** derive the student-facing version of each AT from the assessor version.

**Output:** per-AT student `.docx` (institutional Student template) + companion `.md`.

**Method:**

1. Copy the matching institutional Student template from `<repo_root>/templates/` into the cluster AT folder.
2. Derive the student content from the assessor companion markdown — most content (Details, Task description, Resources) is shared between Student and Assessor versions; strip the assessor-only sections (Marking Guide, assessor-specific instructions, marking guidance benchmark, model KE answers).
3. Tim copy-pastes into the .docx when locked in.

**Result for S1-CL1 AT1:** **Not yet started** — pending Tim's lock-in of the assessor docx content.

---

## Post-Step-7 work (S1-CL1 progress, for pattern reference)

Steps 6 + 7 are repeated **per AT** in the cluster, not once per cluster. S1-CL1 has applied the pattern to AT1, AT2, AT3:

- **AT1** (Business Case + presentation) — Project Assessment template; Part A written + Part B observed presentation. v1.0 committed.
- **AT2** (Cloud Foundation Build) — Project Assessment template **single-task** (no Part split — "implementation is a project even if the deliverable is written" per Tim 2026-05-25). v1.0 committed.
- **AT3** (HA Hardening) — Project Assessment template; Part A (HA Design — student-authored) + Part B (HA Deployment Report). v1.0 committed.

AT3-specific operational artefact authored during the process: a **CloudFormation template** (`scenario/assessor-resources/at2-baseline-cloudformation.{md → yaml}`) — assessor distributes to students at start of AT3 day to deploy a consistent AT2 baseline (since AWS Academy labs reset between sessions). The `scenario/assessor-resources/` folder convention was established for this; intended for assessor-only operational artefacts.

## What has NOT been defined yet

As of 2026-05-26, S1-CL1 has reached the end of Step 7 for all three ATs. Remaining work:

1. **Per-UoC mapping documents** — uses workspace `templates/Assessment Mapping Tool.docx`. One per UoC in the cluster (three for S1-CL1). Tim has started edits to the three mapping docx files; not yet locked in. Maps each PC/PE/KE/FS/AC of each UoC to where in the cluster's ATs it is evidenced.
2. **Operational delivery artefacts** — see the cluster's working state (in LLM memory) § Pending — operational / pre-delivery for the running list (CloudFormation YAML, Records Management Policy content, AT1 templates, exemplars batch).
3. **Cluster coverage check** — once a cluster's ATs are authored, run the **`validate-cluster-coverage`** skill to confirm the ATs together evidence every required (PC/FS/PE/KE) item in `consolidated_uoc.md`; close any gaps it reports. (AC items are environment-satisfied and not required in criteria.) This is the capstone to the per-AT `validate-at-traceability` checks from Step 6.
4. **Pre-validation pass** — run the institutional Pre-Validation Tool over each AT.
5. **Stakeholder review** of the full cluster.
6. **Apply the same Steps 1–7 pattern to remaining clusters** (S1-CL2, S1-CL3, S2-CL1 through S2-CL4).

If you are picking this up on a new cluster, follow Steps 1–7 in order against that cluster's UoCs. Read the cluster's working state (in LLM memory) as the worked example of the end state.

---

## Quirks and gotchas encountered (preserve in future runs)

1. **`source-materials.md` is partially stale.** Describes a `semester_{1,2}/cl_<name>/` layout that doesn't match the filesystem. Use the actual `SX-CLY-<Name>/` layout.
2. **`.docx` headers/footers contain content** (e.g. training-package attribution, unit code) that is **not** in the `.md`. Tim explicitly excluded these from the verbatim check (2026-05-22). Do not re-flag them as missing.
3. **Markdown list bullets** (`- `) at the start of a line are markdown syntax, not source content. The Step 1 validator must strip them, otherwise it produces false-positive "insert" findings for every bulleted item in PE/KE/AC sections.
4. **ICTICT517 PE structure is unusual:** a single top-level bullet `- For one organisation:` with 6 nested sub-bullets. The 6 sub-bullets are the assessable items. The Step 2 validator special-cases this — preserve the special case.
5. **Backtick-wrapped reference tags in the preamble** (used as documentation examples) will be falsely counted by the Step 2.5 validator unless code spans are stripped first. Preserve the `re.sub(r"\`[^\`]*\`", "", text)` step.
6. **Section numbering for FS uses the skill name verbatim** — including spaces (`FS Get the work done`) and case sensitivity (`Oral communication` in ICTCLD502 vs `Oral Communication` in ICTICT517 — different casing in source, preserve as-is).
7. **Don't trust cover-sheet titles in source ATs.** ICTCLD401 AT2's cover sheet says "Knowledge Questions" but the actual content is a 6–8 hour AWS practical with screenshot evidence. Read the body of each AT, not just the title or cover sheet. Source ATs also frequently contain template-residue ("Note to assessment designer:" orange-text instructions that should have been removed), placeholder typos (e.g. "QUESTIONINGASSSESMENT" doubled in 401 headers), and question-answer placeholders that reference the wrong topic (ICTCLD401 AT1 Q12 — the DNS question — has an Answer template that prompts for shared-security-responsibility content instead).
8. **Units of competency vary in the number of authored ATs.** ICTICT517 has five (AT1–AT5) while ICTCLD401/502 have two each (AT1 + AT2). Don't assume "one AT per unit, two units in cluster → six ATs to audit". Map the actual AT list per unit in Step 3.
9. **Source assessments may be drafts.** ICTCLD502's AT1+AT2 source files are explicitly marked "(draft) V4.0" / "(draft) V3.0" — note draft status in Step 3 and consider whether to chase a non-draft version before relying on the content.
10. **Brightspace / LMS exports (`.imscc`, `.zip` bundles) are delivery packages, not authored assessment artefacts.** Don't try to extract assessment content from them in Step 3 — the substantive assessments live in the `.docx` files. Note their presence (they may be useful for delivery later) but they are out of scope for the assessment audit.
11. **Cluster ATs may consolidate multiple per-unit ATs.** Per the 3-AT structure decision for S1-CL1, three units' content collapses into 3 cluster ATs (not 9+ per-unit ATs). The marking guide must continue to evidence every UoC item the consolidated source ATs originally evidenced. The KE coverage is split between a written KE Appendix (BC §-style) and the post-presentation Q&A — the standalone "Knowledge Questions" AT format from per-unit source is **not used** at cluster level.
12. **Marking criteria must trace to UoC, bidirectionally.** Every criterion has a UoC reference column (`[UNIT SECTION numbering]` notation, full unit refs); every UoC item the AT claims to evidence must appear in at least one criterion. A reverse-map table at the end of the Marking Guide confirms closure. See [cluster-authoring-conventions.md](cluster-authoring-conventions.md) for the full rule.
13. **Questions in context, not abstract recall.** Per QA-team preference established 2026-05-23: replace *"explain the difference between IaaS/PaaS/SaaS"* with *"for each component of your solution, identify whether it is IaaS/PaaS/SaaS and explain why"*. Applies to all KE questions in cluster ATs.
14. **Project Assessment template fits multi-part assessments better than Written Assessment.** AT1 of S1-CL1 has Part A (Business Case) + Part B (observed presentation); the Project template's native Part A/B/C structure + tabular per-Part marking guide + observation accommodation made it the right choice over the Written template. See [cluster-authoring-conventions.md](cluster-authoring-conventions.md) §3.
15. **Scenario references use abstract framing for student-facing artefacts, explicit paths for author/assessor-facing artefacts.** Student-facing: "the YAT intranet's ICT Strategic Plan page" (matches how students consume the scenario — via the mock website at `https://www.placeholder.com.au`). Author/assessor-facing: `<repo_root>/scenario/internal-X.md`.

---

## Appendix A — `validate_uoc.py` (Step 1 tool)

Canonically bundled with the skills at `.claude/skills/scripts/validate_uoc.py` (used by the
`validate-uoc-transcription` and `transcribe-uoc` skills); also at `<repo_root>/scripts/validate_uoc.py`.
Reproduce verbatim if missing. Invocation: `python3 <repo_root>/scripts/validate_uoc.py <docx1> <md1> [<docx2> <md2> ...]`. Exit code 0 on all-pass, 1 on any substantive diff.

```python
#!/usr/bin/env python3
"""Validate that a .md UoC transcription is verbatim against the source .docx.

For each pair, extract textual content in document order from the .docx
(paragraphs + table cells, preserving line breaks within cells), strip
markdown syntax from the .md, and diff the resulting word sequences.

Reports differences in two tiers:
  - Substantive: words added/removed/changed
  - Cosmetic: punctuation/quote/whitespace normalisation differences
"""

import difflib
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def docx_to_text(docx_path: Path) -> str:
    """Extract textual content from a .docx in document order.

    Paragraphs are separated by newlines. Table cell content is also
    paragraph-like; line breaks within a cell (w:br) become newlines, so
    they line up with the <br> markers used in the .md.
    """
    with zipfile.ZipFile(docx_path) as z:
        with z.open("word/document.xml") as f:
            tree = ET.parse(f)

    body = tree.getroot().find(f"{W_NS}body")
    if body is None:
        return ""

    out_lines = []

    def render_paragraph(p_elem) -> str:
        parts = []
        for node in p_elem.iter():
            tag = node.tag
            if tag == f"{W_NS}t":
                parts.append(node.text or "")
            elif tag == f"{W_NS}tab":
                parts.append("\t")
            elif tag == f"{W_NS}br":
                parts.append("\n")
        return "".join(parts)

    def walk(elem):
        for child in elem:
            tag = child.tag
            if tag == f"{W_NS}p":
                out_lines.append(render_paragraph(child))
            elif tag == f"{W_NS}tbl":
                for row in child.findall(f"{W_NS}tr"):
                    for cell in row.findall(f"{W_NS}tc"):
                        cell_parts = []
                        for cp in cell.findall(f"{W_NS}p"):
                            cell_parts.append(render_paragraph(cp))
                        # Use newline within cells so it lines up with <br> in md
                        out_lines.append("\n".join(cell_parts))
            elif tag == f"{W_NS}sdt":
                # Structured document tag — recurse into content
                content = child.find(f"{W_NS}sdtContent")
                if content is not None:
                    walk(content)
            else:
                walk(child)

    walk(body)
    return "\n".join(out_lines)


def md_to_text(md_path: Path) -> str:
    """Strip markdown syntax from a .md file, leaving the textual content.

    Removes heading markers, table pipes, table separator rows, and converts
    <br> tags to newlines. Leaves prose otherwise untouched.
    """
    raw = md_path.read_text(encoding="utf-8")
    out_lines = []
    for line in raw.splitlines():
        stripped = line.strip()
        # Skip empty lines (we'll re-add structure via newlines)
        if not stripped:
            out_lines.append("")
            continue
        # Table separator row: | --- | --- | ...
        if re.fullmatch(r"\|?\s*(:?-{3,}:?\s*\|\s*)+:?-{3,}:?\s*\|?", stripped):
            continue
        # Heading: # Foo, ## Foo, etc.
        m = re.match(r"^#{1,6}\s+(.*)$", stripped)
        if m:
            out_lines.append(m.group(1))
            continue
        # List item: - foo, * foo, + foo, or numbered "1. foo"
        m = re.match(r"^([-*+]|\d+\.)\s+(.*)$", stripped)
        if m:
            stripped = m.group(2)
        # Table row: | a | b | ... → split into cell contents (one per line)
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            cell_lines = []
            for c in cells:
                cell_lines.extend(re.split(r"<br\s*/?>", c, flags=re.IGNORECASE))
            out_lines.extend(cl.strip() for cl in cell_lines)
            continue
        # Regular line: convert any inline <br> to newlines
        parts = re.split(r"<br\s*/?>", stripped, flags=re.IGNORECASE)
        out_lines.extend(p.strip() for p in parts)
    return "\n".join(out_lines)


def normalise_cosmetic(text: str) -> str:
    """Apply cosmetic normalisations: smart quotes, dashes, NBSPs, NFC."""
    text = unicodedata.normalize("NFC", text)
    replacements = {
        "‘": "'", "’": "'", "‚": "'", "‛": "'",
        "“": '"', "”": '"', "„": '"', "‟": '"',
        "–": "-", "—": "-", "−": "-",
        " ": " ",
        "…": "...",
        "­": "",
        "﻿": "",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def to_words(text: str) -> list:
    return text.split()


def diff_report(label, docx_text, md_text):
    docx_words = to_words(docx_text)
    md_words = to_words(md_text)
    raw_match = docx_words == md_words

    docx_norm = normalise_cosmetic(docx_text)
    md_norm = normalise_cosmetic(md_text)
    docx_norm_words = to_words(docx_norm)
    md_norm_words = to_words(md_norm)
    cosmetic_match = docx_norm_words == md_norm_words

    findings = {
        "label": label,
        "docx_word_count": len(docx_words),
        "md_word_count": len(md_words),
        "exact_match": raw_match,
        "cosmetic_match": cosmetic_match,
        "substantive_diff": [],
        "cosmetic_diff": [],
    }

    if not cosmetic_match:
        sm = difflib.SequenceMatcher(a=docx_norm_words, b=md_norm_words, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            findings["substantive_diff"].append({
                "op": tag,
                "docx_range": (i1, i2),
                "md_range": (j1, j2),
                "docx_words": docx_norm_words[i1:i2],
                "md_words": md_norm_words[j1:j2],
            })

    if cosmetic_match and not raw_match:
        sm = difflib.SequenceMatcher(a=docx_words, b=md_words, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            findings["cosmetic_diff"].append({
                "op": tag,
                "docx_words": docx_words[i1:i2],
                "md_words": md_words[j1:j2],
            })

    return findings


def print_findings(f):
    print(f"\n{'=' * 70}")
    print(f"  {f['label']}")
    print(f"{'=' * 70}")
    print(f"  docx words: {f['docx_word_count']}    md words: {f['md_word_count']}")
    if f["exact_match"]:
        print("  RESULT: EXACT MATCH (byte-equivalent at word level)")
        return
    if f["cosmetic_match"]:
        print("  RESULT: VERBATIM after cosmetic normalisation (quotes/dashes/whitespace)")
        if f["cosmetic_diff"]:
            print(f"  Cosmetic-only diffs ({len(f['cosmetic_diff'])} blocks):")
            for d in f["cosmetic_diff"][:10]:
                print(f"    [{d['op']}]  docx: {d['docx_words']!r}")
                print(f"          md:   {d['md_words']!r}")
            if len(f["cosmetic_diff"]) > 10:
                print(f"    ... and {len(f['cosmetic_diff']) - 10} more")
        return
    print("  RESULT: SUBSTANTIVE DIFFERENCES FOUND")
    print(f"  Substantive diff blocks: {len(f['substantive_diff'])}")
    for d in f["substantive_diff"]:
        print(f"\n    [{d['op']}] docx[{d['docx_range'][0]}:{d['docx_range'][1]}]  md[{d['md_range'][0]}:{d['md_range'][1]}]")
        print(f"      docx: {' '.join(d['docx_words'])!r}")
        print(f"      md:   {' '.join(d['md_words'])!r}")


def main():
    pairs = sys.argv[1:]
    if not pairs or len(pairs) % 2 != 0:
        print("Usage: validate_uoc.py <docx1> <md1> [<docx2> <md2> ...]", file=sys.stderr)
        sys.exit(2)

    any_substantive = False
    for i in range(0, len(pairs), 2):
        docx_path = Path(pairs[i])
        md_path = Path(pairs[i + 1])
        label = f"{docx_path.name}  vs  {md_path.name}"
        docx_text = docx_to_text(docx_path)
        md_text = md_to_text(md_path)
        f = diff_report(label, docx_text, md_text)
        print_findings(f)
        if not f["cosmetic_match"]:
            any_substantive = True

    print()
    sys.exit(1 if any_substantive else 0)


if __name__ == "__main__":
    main()
```

---

## Appendix B — `validate_consolidated_uoc.py` (Step 2 tool)

**Superseded.** The current Step 2.5 validator is the general, arg-driven `validate_consolidated.py`,
bundled with the skills at `.claude/skills/scripts/validate_consolidated.py` and invoked via the
`validate-uoc-consolidation` skill (no per-cluster code edits). This appendix retains the original
S1-CL2-hardcoded version for reference. Lives at `<repo_root>/scripts/validate_consolidated_uoc.py`. Invocation: `python3 <repo_root>/scripts/validate_consolidated_uoc.py`. Exit code 0 on PASS, 1 on FAIL.

**Before running, edit the constants near the top for the target cluster:**
```python
CLUSTER_DIR = Path("<absolute path to <repo_root>/SX-CLY-<name>>")
UNITS = ["<UNIT_A>", "<UNIT_B>", ...]
```

Source:

```python
#!/usr/bin/env python3
"""Validate that consolidated_uoc.md references every PC/FS/PE/KE/AC from each
source UoC exactly once.

Builds the expected inventory by parsing each source .md file:
- PCs: numbered "X.Y" entries inside the Elements and Performance Criteria table
- FSs: skill-name keys in the Foundation Skills table
- PEs/KEs/ACs: top-level bullet items under each section heading
  (with parent-bullet special case for ICTICT517-PE-style structures)

Then parses consolidated_uoc.md for every reference tag of the form
[UNIT SECTION numbering] and reports any item that is missing, duplicated,
or unexpected. Strips single-backtick code spans before extracting tags so
that example tags in the preamble are not falsely counted.
"""

import re
import sys
from collections import Counter
from pathlib import Path

# ---- EDIT THESE FOR THE TARGET CLUSTER ----
CLUSTER_DIR = Path("/Users/timbaird/Documents/Kangan/diploma-cloud-cyber/S1-CL1-Cloud-Design-Build")
UNITS = ["ICTCLD401", "ICTCLD502", "ICTICT517"]
# -------------------------------------------

UOC_DIR = CLUSTER_DIR / "units_of_competency"
CONSOLIDATED = CLUSTER_DIR / "consolidated_uoc.md"


def parse_pcs(md_text: str) -> list:
    m = re.search(r"# Elements and Performance Criteria\n(.*?)(?=\n# )", md_text, re.DOTALL)
    if not m:
        return []
    return re.findall(r"\b(\d+\.\d+)\s+", m.group(1))


def parse_fs(md_text: str) -> list:
    m = re.search(r"# Foundation Skills\n(.*?)(?=\n# )", md_text, re.DOTALL)
    if not m:
        return []
    section = m.group(1)
    names = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        if re.match(r"\|\s*(SKILL|Skill)\s*\|", line):
            continue
        if re.match(r"\|\s*-+\s*\|", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 2 and cells[0] and not cells[0].lower().startswith("skill"):
            names.append(cells[0])
    return names


def parse_section_bullets(md_text: str, heading: str) -> int:
    """Count assessable bullets under a heading.

    Default: top-level bullets ('- ' with no leading whitespace).
    Special case: if the section has exactly one top-level bullet ending
    with ':' (parent like '- For one organisation:'), count immediate
    sub-bullets ('  - ') instead.
    """
    pattern = rf"# {re.escape(heading)}\n(.*?)(?=\n# )"
    m = re.search(pattern, md_text, re.DOTALL)
    if not m:
        sections = re.findall(rf"# {re.escape(heading)}\n(.*?)(?=\n# |\Z)", md_text, re.DOTALL)
        if not sections:
            return 0
        section = sections[-1]
    else:
        section = m.group(1)

    lines = section.splitlines()
    top_level = [line for line in lines if re.match(r"^- ", line)]

    if len(top_level) == 1 and top_level[0].rstrip().endswith(":"):
        sub = [line for line in lines if re.match(r"^  - ", line)]
        return len(sub)

    return len(top_level)


def build_inventory() -> set:
    expected = set()
    for unit in UNITS:
        md = (UOC_DIR / f"{unit}_Complete_R1.md").read_text(encoding="utf-8")
        for pc in parse_pcs(md):
            expected.add(f"{unit} PC {pc}")
        for fs in parse_fs(md):
            expected.add(f"{unit} FS {fs}")
        for n in range(1, parse_section_bullets(md, "Performance Evidence") + 1):
            expected.add(f"{unit} PE {n}")
        for n in range(1, parse_section_bullets(md, "Knowledge Evidence") + 1):
            expected.add(f"{unit} KE {n}")
        ac_count = parse_section_bullets(md, "Assessment Conditions")
        for n in range(1, ac_count + 1):
            expected.add(f"{unit} AC {n}")
        # Trailing "Assessors of this unit must..." paragraph counted as next AC
        expected.add(f"{unit} AC {ac_count + 1}")
    return expected


def extract_refs(text: str) -> list:
    """Pull every reference tag. Skip backtick-wrapped tags (preamble examples)."""
    cleaned = re.sub(r"`[^`]*`", "", text)
    return re.findall(r"\[(ICT\w+|BSB\w+|VU\d+) (PC|FS|PE|KE|AC) ([^\]]+)\]", cleaned)


def main():
    expected = build_inventory()
    consolidated = CONSOLIDATED.read_text(encoding="utf-8")
    raw_refs = extract_refs(consolidated)
    found = [f"{u} {s} {n}" for u, s, n in raw_refs]
    counts = Counter(found)

    found_set = set(found)
    missing = sorted(expected - found_set)
    unexpected = sorted(found_set - expected)
    duplicated = sorted([(ref, c) for ref, c in counts.items() if c > 1])

    print(f"Expected items:   {len(expected)}")
    print(f"Found references: {len(found)} ({len(found_set)} unique)")
    print()

    if missing:
        print(f"MISSING ({len(missing)}):")
        for ref in missing:
            print(f"  - {ref}")
        print()

    if unexpected:
        print(f"UNEXPECTED ({len(unexpected)}):")
        for ref in unexpected:
            print(f"  - {ref}  (count={counts[ref]})")
        print()

    if duplicated:
        print(f"DUPLICATED ({len(duplicated)}):")
        for ref, c in duplicated:
            print(f"  - {ref}  ({c} times)")
        print()

    if not missing and not unexpected and not duplicated:
        print("RESULT: PASS — every expected item appears exactly once, nothing extra.")
        sys.exit(0)
    else:
        print("RESULT: FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
```
