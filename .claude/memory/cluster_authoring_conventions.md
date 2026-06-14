---
name: cluster authoring conventions
description: Standing conventions for authoring cluster assessment artefacts — UoC traceability, KE evidencing locations, template workflow, scenario references
type: feedback
originSessionId: df4c62a3-dd05-4ef4-a776-3c7ab7048cba
---
These conventions govern how cluster assessment artefacts (briefs, templates, rubrics, benchmarks) are authored across the project. They have emerged from Tim's iterative direction during S1-CL1 work and apply to all cluster authoring going forward.

## 1. UoC traceability — bidirectional

**Why:** assessment validity. The project assesses UoC requirements, not Claude's opinion of what good work looks like.

**How to apply:**
- Every marking criterion must trace to one or more specific UoC items using **full reference notation** `[UNIT SECTION numbering]` (e.g. `[ICTICT517 PC 1.4]`, never `[PC 1.4]`).
- **No free-floating criteria** — items like "completes within agreed time" or "good eye contact" don't belong unless they trace to a UoC item.
- **Consolidation is OK** where multiple UoC items are naturally co-evidenced by the same student work product (e.g. a single criterion can cover both PC 1.4 and FS Writing if the artefact evidences both).
- **Bidirectional check:** every UoC item AT claims to evidence must appear in at least one criterion. Include a "UoC coverage verification (reverse map)" table in every assessor doc to close the loop.
- **AT-scope discipline:** each AT only evidences UoC items mapped to it; the rest go to other ATs in the cluster. Don't claim AT1 evidences AT2/AT3 items.
- **Free-floating criteria self-audit (mandatory final pass):** after drafting any marking guide, scan the UoC reference column on every criterion. **Any criterion with a blank UoC column, or with placeholder text like "(scoping context; supports the rest)" or "(institutional)" in place of a real `[UNIT SECTION numbering]` tag, is a free-floating criterion and must be either dropped or properly mapped.** Reason: caught late on AT2 v1 — two criteria (engagement context + scope of deployment) were drafted as scoping items with no UoC trace, slipped through the first draft, and had to be removed in a second pass. The rule itself was already in this convention; the gap was no enforcement habit. The fix is the self-audit pass before reporting any marking guide as drafted. Required template sections that *don't* trace to UoC (e.g. an Executive Summary, Engagement Context, Scope) can stay in the template — they aren't assessed criteria, they're scaffolding for a coherent deliverable. The Document Quality criterion implicitly catches weakness in those sections.

## 2. Knowledge Evidence — two locations

**Why:** consistent KE coverage across students (written) + assessor flexibility for depth (oral).

**How to apply:**
- **Location 1:** Knowledge Evidence Appendix in the Business Case / portfolio. Two question patterns:
  - **Selection-style:** *"Which of these [X items] did your solution use? Explain why."* — for enumerable KE items.
  - **Demonstration-style:** *"How does your plan demonstrate [principle]? Identify where it appears in your work."* — for principles/methodologies.
- **Location 2:** Post-presentation Q&A. Assessor selects from a tagged question bank, may probe deeper than the written appendix.
- **Questions in context, not abstract recall.** Bad: *"Explain the difference between IaaS, PaaS, SaaS."* Good: *"For each component of your AWS solution, identify whether it is IaaS, PaaS or SaaS, and explain your choice."*

## 3. Institutional template workflow

**Why:** institutional templates are the format-of-record for live delivery. Markdown is a one-time scaffold for drafting; the `.docx` becomes canonical after paste.

**How to apply:**
- The workspace `templates/` folder contains the institutional Word/Excel templates (Project Assessment - Assessor.docx, Project Assessment - Student.docx, Written Assessment - Assessor.docx, Written Assessment - Student.docx, Assessment Mapping Tool.docx, Delivery_Plan_Template_v0.1.docx).
- For each cluster AT, copy the relevant template into the cluster AT folder with a descriptive name (e.g. `AT1-BusinessCase-Assessor.docx`).
- Author the content in a **companion markdown file** alongside (e.g. `AT1-BusinessCase-Assessor.md`) that mirrors the template's section structure. Tim copy-pastes the content into the .docx when ready.
- **Once pasted, the .docx is canonical.** Subsequent edits (reviews, simplifications, fixes) happen in the .docx, not the .md. Don't try to keep the .md in sync — fighting Word's formatting through markdown round-trips is wasted effort.
- **Delete the companion .md after paste-in is complete.** It's a scaffold, not a long-lived artefact. Reason: stale .md files invite confusion about which is the source of truth. (Established 2026-05-24 after AT1 went through several rounds of in-docx editing and the .md companions drifted.)
- Same applies to other "working .md" authoring scaffolds (benchmarks, rubrics drafted as separate .md files): once their content lands in the canonical .docx, delete the scaffold.
- **Project Assessment template fits multi-part assessments** (e.g. written deliverable + observed presentation) because it has native Part A / Part B structure + per-Part marking guide tables + observation accommodation.
- **Written Assessment template fits single-mode written assessments** (questioning, report).

## 4. Scenario references in cluster artefacts

**Why:** scenario lives at repo root and is shared across the course (see `scenario_location.md` memory entry).

**How to apply:**
- **Student-facing artefacts** reference scenario content **abstractly** — "the YAT intranet", "the LMS application spec page", "the ICT manager consultation notes" — not by file path.
- **Author / assessor-facing artefacts** that need to point at a specific scenario file use explicit repo-root paths: `<repo_root>/scenario/internal-X.md`.
- The intranet has a placeholder URL `https://www.placeholder.com.au` used throughout — assessments refer students to this URL.

## 5. Documentation cross-reference convention

**Why:** keep audit trail traceable.

**How to apply:**
- New scenario authoring dependencies surfaced during AT authoring — add them to the scenario checklist's "still to author" backlog (or note in the AT doc's "Authoring notes" section if it's a one-off).
- New template dependencies — add to `<cluster>/assessments/templates/checklist.md`.
- Status banners (`STATUS: DRAFT`) on every authored artefact per CLAUDE.md Rule 1; mark Claude-invented specifics with `TBD` per Rule 2.

## 6. Cross-AT shape comparability

**Why:** when an AT's deliverable shape recurs in a later AT (e.g. AT2 Deployment Report → AT3 HA Deployment Report), students benefit from the **same section structure in the same places**, so the second deliverable is recognisable from the first.

**How to apply:**
- Use the same major section headings in the same order across comparable deliverables (e.g. §1 Exec Summary, §2 Engagement Context, §3 Scope, §4 Build Narrative, §5 Configuration Decisions, §6 Testing, §7 Handover, §8 Knowledge Evidence, Appendices A–D)
- Within each section the *prompts* can differ — different KE questions, different screenshot list, different simulation prompts — but the heading and position stay constant
- Tim 2026-05-25 on AT3 Deployment Report vs AT2 Deployment Report: *"Use the same shape, the same major sections, so it is comparable, but prompt for the different required details as needed within that structure."*
- Same principle on AT3 HA Design vs AT2 supplied design: mirror the structure so the student recognises the parallel between "design supplied to you in AT2" and "design you author in AT3".

## 7. Project Assessment template covers single-task AND multi-part assessments

**Why:** previously the convention (§3) read as if Written Assessment template fit single-mode written work and Project Assessment fit multi-part. AT2 broke that mapping — it's a single-task written deliverable that's still better as a Project Assessment because *implementing infrastructure is a project even if the deliverable is written*.

**How to apply:**
- Default to **Project Assessment template** for any cluster AT that involves implementation, observation, OR a deliverable beyond a pure questioning instrument
- Single-task Project Assessments use the template without a Part A/Part B split (just one criteria table)
- Multi-part Project Assessments use Part A + Part B genuinely (AT1: written BC + observed presentation; AT3: HA Design + HA Deployment Report)
- **Written Assessment** template is reserved for pure single-mode questioning instruments
- Established 2026-05-25 (Tim during AT2 design)

## 9. Standard cluster folder shape

**Why:** as of 2026-06-06 Tim reshaped every cluster folder into one consistent layout — "slightly different from how CL1 started, but it makes more sense this way." Applies to all clusters (CL1 was migrated to match).

**How to apply:** each `SX-CLY-<Name>/` contains these top-level siblings:
- `assessments/` — per-AT folders (`AT1/`, `AT2/`, …); the per-AT assessor/student `.docx` + companion `.md` live here.
- `delivery/` — teaching/delivery materials (`topic_NN/`, `planning/`).
- `mappings/` — the per-UoC Assessment Mapping docs (one per unit).
- `units_of_competency/` (+ `original/`) — the UoC `.md` transcriptions and their source `.docx`. **No longer nested under `assessments/`** (that was CL1's original shape).
- `consolidated_uoc.md` — produced in Step 2, at the **cluster root**.

Implications: the validators' `UOC_DIR` is now `CLUSTER_DIR / "units_of_competency"` (not `assessments/units_of_competency`); Step 1's `cd` target is `<cluster>/units_of_competency`. `documentaion/process.md` was updated to match (its old diagram showed the nested shape). See [[s1-cl1-cluster-current-state]] for the worked end state.

## 8. Reframing principle for cluster ATs

**Why:** consolidating per-unit ATs into cluster ATs requires careful re-mapping.

**How to apply:**
- Where the original per-unit AT structure has multiple ATs (e.g. 517 has 5), the cluster AT may consolidate them. The marking guide must continue to evidence every UoC item the consolidated ATs originally evidenced.
- KE evidence in the cluster ATs is split: written-form (BC appendix) + verbal-form (Q&A). The original per-unit "Knowledge Questions" AT format is not used; the standalone questioning AT was dropped in the v2 assessment plan for S1-CL1.
- **Test the reframe against UoC:** before locking in any cluster AT structural choice, check whether the choice is UoC-mandated, UoC-aligned, or pure design choice. Document which (e.g. "the CBA is a delivery choice, not UoC-mandated; the UoC requires financial-implications evidence which the CBA provides").
