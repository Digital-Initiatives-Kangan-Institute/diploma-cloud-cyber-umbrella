# Cluster delivery-planning process

**Audience:** humans and LLM agents picking up the cluster **delivery-planning** task. Sister document
to [process-assessment.md](process-assessment.md) (which covers the assessment-creation process).

> **Paths** in this document are relative to the `diploma-cloud-cyber-content/` repo root.

**Relationship to `process-assessment.md`:** `process-assessment.md` is the **assessment run-sheet** — how the cluster's **assessment artefacts** are created, as a step→gate pipeline (transcribe → consolidate UoC → audit → plan → consolidate plans → scenario → assessor/student instruments → mapping → cluster coverage → pre-validation). This document records how a cluster's **delivery plan** is produced — the trainer-facing schedule that sequences delivery and assessment across sessions. The two processes share inputs (the consolidated UoC, the assessment plan, the scenario) but produce different outputs.

**Prerequisites you must read before acting:**
- The umbrella `CLAUDE.md` — working discipline + git-safety rules.
- [project-overview.md](project-overview.md) — project scope, delivery context (AWS Academy lab environments, scenario architecture), success criteria (a delivery plan is success-criterion #1 per cluster).
- [process-assessment.md](process-assessment.md) — the assessment-creation process whose outputs this plan sequences.
- [cluster-authoring-conventions.md](cluster-authoring-conventions.md) and [scenario-flow.md](scenario-flow.md).
- The cluster's working state lives in LLM memory (the per-cluster delivery entry).

**Working rules for documents produced (same as `process-assessment.md`):**
- Nothing recorded as a decision unless actively discussed with Tim and explicitly approved. Proposals are marked **TBD**.
- Mark produced documents as **DRAFT** while in progress.
- Do not modify anything under `original_materials/`. It is read-only reference.
- The institutional delivery-plan format-of-record is `templates/Delivery_Plan_Template_v0.1.docx`.

---

## Input state (S1-CL1)

- Cluster folder: `S1-CL1-Cloud-Design-Build/`
- `delivery/` now holds **`topic_01/` … `topic_14/`** (one per content Topic; each with `coverage.md` + `slide_plan.md`) plus `planning/` (the retained spine, session scaffold, and deck catalogue). **Assessments are not Topics** — they're lettered non-Topic sessions in the spine, with no `topic_NN/` folder.
- Available inputs: the three populated AT `.docx` (source of truth), `consolidated_uoc.md`, `assessments/assessment_plan.md`, the shared `scenario/` + the YAT website, and the per-UoC mapping docs under `mappings/`.
- Institutional template: `templates/Delivery_Plan_Template_v0.1.docx`.

---

## Semester 1 structure (planning context)

Provided by Tim 2026-05-31 as the planning frame for S1 cluster delivery plans. Teaching hours are **goals** — a few hours may be shifted between clusters if a plan needs it.

**Semester 1 = 18 weeks = 2 terms.**

**Delivery sequencing:**
- **CL1** — delivered first, on its own, **weeks 1–8** (8 weeks).
- **CL2 + CL3** — delivered **in parallel** after CL1 completes, **weeks 9–18** (10 weeks).

**Per-cluster hours, session model, and variance:**

| Cluster | Goal hrs | Weeks | Session model | Sessions | Delivered hrs | Variance vs goal |
|---|---:|---|---|---:|---:|---:|
| CL1 | 104 | 1–8 (8 wks) | 4 × 3h sessions/wk = 12h/wk | 32 | 96 | **+8** (under / unused) |
| CL2 | 84 | 9–18 (10 wks) | 3 × 3h sessions/wk = 9h/wk | 30 | 90 | **−6** (over) |
| CL3 | 56 | 9–18 (10 wks) | 2 × 3h sessions/wk = 6h/wk | 20 | 60 | **−4** (over) |

Variance sign convention: **+** = delivers fewer than goal (unused budget); **−** = delivers more than goal.

**Net variance across the semester:** +8 − 6 − 4 = **−2 hours** (the session model delivers ~2h over the combined 244h goal). Close enough to target.

**Student weekly load:** weeks 1–8 = 4 sessions/wk (CL1, 12h); weeks 9–18 = 5 sessions/wk (CL2's 3 + CL3's 2, 15h).

> **Current focus:** CL1 (weeks 1–8, 32 sessions). The CL2/CL3 figures are recorded for reference and are not needed for the CL1 delivery plan.

---

## Delivery strategy — teach / practice / assess

The basic approach for the cluster (per Tim 2026-05-31). Each Topic / competency area moves through a three-phase cycle:

1. **Teach** — deliver the theory: slides, class discussion, activities, and practical demonstration. A demonstration may be a **recorded video** (where one is available) rather than a live in-class demo.

2. **Practice** — students practise what they have learned through in-class activities that reinforce the learning and prepare them for assessment. Because the authored assessment tasks already cover every required UoC item, the lowest-hanging practice design is a **practice task that mirrors the assessment but set in a different scenario / under different circumstances** — close enough to build the skill, different enough that it is not rote rehearsal of the real assessment. A practice task may be split into **several exercises that, taken together, cover all parts of the related assessment**.

3. **Assess** — assess the student using the **already-authored assessment tasks** (the ATs produced via `process-assessment.md`).

**Design implication:** practice tasks are derived from the ATs (so coverage is guaranteed) but re-scenarioed away from the real assessment context. The session plan interleaves these three phases across the teaching block (S2–S28 for CL1) ahead of each assessment point.

---

## The process

**Model:** `AT → Topic → component`. A **Topic** is the delivery unit (one `topic_NN/` folder — the level you build materials for and schedule into sessions; aligns with the Delivery Plan template's "Topic and description" field). A Topic's **components** (C1, C2, …) are the things it covers, defined *inside* its `coverage.md`, derived straight from the AT — there is no separate decomposition document.

**Framing already established** (above): Semester 1 structure; the teach / practice / assess strategy; the **practice scenario** (YAT Accounting System / Ledgerline — same org, different system, added to the AT1 intranet as a peer engagement to the LMS, indistinguishable until the task is handed out); and the session bookend scaffold.

**Per-Topic folder:**
```
topic_NN/
├── coverage.md          — UoC + AT alignment (the spec) — kept
├── slide_plan.md        — the build sheet: teach + exercise slides interleaved, in deck order
│                          ([BESPOKE] = author from brief · [AWS Mx Sy] = AWS slide to reuse · [EX] = exercise)
│                          — DISPOSABLE: a working aid; delete once the deck is built
└── Topic_NN_Slides.pptx — the generated Kangan-branded deck — THE ARTEFACT OF RECORD
```
The deck is **generated** from the plan by a per-Topic Kangan build script, then the human pastes the reused AWS images into the placeholders **directly from the main AWS deck folder** (`original-materials/…`). The plan isn't kept synced to the deck — it's disposable; the deck is the source of truth.

### Step 1 — Break the AT into Topics
**Purpose:** from the assessment itself, identify the conceptual **Topics** — coherent teaching units anchored to the AT's own structure (deliverable sections, appendix/KE questions, marking criteria; the natural movements of producing the deliverable).
**Inputs:** the AT **`.docx`** (Student + Assessor) — the source of truth (see quirks).
**Method:** read both; name the Topics (e.g. Business Case = *know the tech → diagnose → build evidence → decide & plan → make the case*); place them in the cluster Topic sequence (content + assessment Topics) against the fixed bookend sessions; create a `topic_NN/` folder each.
**Result (S1-CL1):** 14 content Topics across AT1 (1–5) / AT2 (6–10) / AT3 (11–14); assessments are separate lettered non-Topic sessions (a–i, in delivery order); + onboarding (S1) + catch-up (S31–32).

### Step 2 — Spec each Topic (`coverage.md`)
**Purpose:** state what the Topic must cover, in **UoC** and **AT** terms — the contract its materials satisfy. **The AT sets the depth ceiling** — don't teach deeper than the assessment requires (e.g. Topic 1 = exactly Appendix 2 Q1–Q5, *recognise/explain/classify*, not build).
**Method:** list the Topic's components C1..Cn (from the AT); per component, the UoC it **teaches** (full `[UNIT SECTION num]` tags) + the **AT alignment** (which criteria / deliverable sections / appendix questions it prepares for); distinguish *taught here* vs *applied (taught earlier)*; state what's out of scope (covered elsewhere); end with a coverage checklist. **Only UoC + AT cross-references** — nothing pointing at working drafts, so the file stands alone when those are deleted.
**Result (S1-CL1):** Topics 1 & 2 done as the pattern.

### Step 3 — Slide plan → deck (Kangan-branded, generated)
**Purpose:** turn the coverage into a slide plan, then **generate** the Kangan-branded Topic deck from it. The **deck is the canonical artefact**; the plan is a working aid, deleted when the deck is done.

**The slide-creation process (settled 2026-06-01):**
1. **`slide_plan.md`** — walk the Topic's components top-to-bottom; for each, **teach then its exercise**, in deck order. **For a hands-on AWS practical, insert a `[DEMO]` between them — the flow is `teach → demonstrate → practice`** (a demo of the exact task, immediately before the student activity). Non-AWS / analytical activities keep the plain `teach → practice`. Mark each slide `[PRIMER]` (vendor-neutral fundamentals — see primer-first below), `[BESPOKE]` (content brief inline), `[AWS Mx Sy]` (an AWS deck slide to reuse), `[DEMO]` (recorded demo), or `[EX]` (exercise). The plan **pins up front exactly which AWS slides the Topic needs** (deck + slide numbers, via `aws-deck-catalogue-draft.md`) — this pin table is what drives both the agent's reading and the human's image-paste.
2. **(agent) generate the deck** — a per-Topic build script (`scripts/build_kangan_topicNN_deck.py`) authors **every** slide — bespoke *and* AWS-sourced — fresh into the **Kangan brand layouts** (title / divider / content / activity / **demo** / takeaways / table; see `kangan-branding.md`). The agent reads the pinned AWS slides directly from `original-materials/…` and authors from them (reuse-first, below). Output `Topic_NN_Slides.pptx`.
3. **(human) paste the AWS images** — drop the reused diagrams/screenshots into the placeholder slots in PowerPoint, **straight from the main AWS deck folder**.

**Marking the AWS source on a slide** (so provenance is traceable now that there's no `source_slides/` folder):
- **Slide carries an image/diagram from AWS** → render it as a **labelled image placeholder** that names the diagram **and the exact source slide(s)** — e.g. *"AWS — VPC building blocks diagram (ACA M07 S16)"*, not just "(ACA M07)". The deck alone isn't enough: the human needs the **slide number** to know which image to grab. The placeholder *is* the source marker; the human pastes the real image over it.
- **Content/text-only AWS slide (no image to mark on)** → author the content reuse-first **and** add a visible on-slide note **"take from AWS [deck · slide ref]"**, so the source is traceable and the human can cross-check against the original.

**Why authored-with-placeholders, not re-skinned:** re-skinning the AWS deck in place mis-sizes text and can't carry vector diagrams; authoring fresh into the Kangan layouts gives a clean, consistent deck, and the placeholders/notes make the (few) images a quick manual paste from the main folder. (Raster images *can* be auto-extracted, but the clean authored layout is worth the manual image step.)

**Primer-first (no assumed baseline).** Students may not arrive with base IT knowledge, so every technical concept is taught **fundamentals-first**: a short vendor-neutral **`[PRIMER]`** (what the thing *is* — e.g. what a subnet/IP is, how DNS resolves a name, what a firewall does) **before** the AWS-context slide that shows how AWS implements it. Per-concept shape: **`[PRIMER] → [AWS] teach → [DEMO] → [EX]`**. Reuse-first still governs the primer — pin an AWS "basics" slide where one teaches the fundamental; author a bespoke primer only where AWS assumes the knowledge.

**Reuse-first (AWS content) — the governing principle for AWS-heavy topics.** Where an AWS deck covers a teach point, **author the slide FROM the AWS slide's actual content** — extract + read the relevant AWS module(s) from `original-materials/AWS-Instructor Presentations/…` **before** authoring (the AWS decks are the source, not your own knowledge). Bespoke is reserved for genuine gaps (VET evidence discipline, scenario-specific framing, the supplied-design specifics). *Authoring teach content from your own approximation when an AWS deck covers it is the mistake this rule exists to prevent.* The long-path trick for the ACA decks: `cp` to a short Windows-addressable temp dir, then open with python-pptx.

**Open thread — reuse vs rewrite.** Authoring AWS content *fresh into Kangan slides* edges toward
rewriting rather than reusing. The resolution so far is human **consolidation** of the drafted Kangan
slides with the actual AWS reference slides into the final deck. The pure-reuse-vs-rewrite model is
**not yet settled** — revisit.

**Demos — recorded first.** **Always use an AWS recorded demo where a suitable one exists** (catalogued in `planning/aws-recorded-demos-catalogue.md`); a **live instructor demo is the fallback only when none is available**. The `demo_slide` layout shows which (RECORDED DEMO vs DEMONSTRATION) via its `source` parameter.

**Brand:** teaching decks wear **Kangan/BKI** branding (gold `#EDAB0C` + charcoal, Roboto), **not** the in-world YAT case-study brand — see `kangan-branding.md`. All brand + layout code lives in **`scripts/kangan_deck.py`** (the shared base for every deck); per-Topic builders (`build_kangan_topicNN_deck.py`) are content-only and `import kangan_deck as k`.

**Slide-build rules (apply as you place each slide):**
- **The plan holds briefs, not finished copy.** A `[BESPOKE]` block is the *substance* of a slide; write the actual title + bullets at build time (drafted on demand as the deck is assembled).
- **Student-facing slides stay in-world** — same rule as the intranet. No course/assessment language *on the slide*: no "AT1 / Appendix 2 / Business Case §x", and nothing that tips **which system is the assessed one** (students practise on the Accounting System; the real engagement is handed out later). **Source-deck references MAY stay on the slide; UoC references MUST NOT (Tim, 2026-06-03).**
- **Keep (visible to students):** the *source-deck* provenance in a teach slide's kicker — the AWS module (e.g. "AWS · ACF M06 S10") **and** the bespoke ICTCLD502 HA decks — plus image-placeholder labels and the demo `source=` cue. These tell a teacher or curious student *where to read more*; they're attribution, not course meta. *(Label the 502 decks by title, e.g. "ICTCLD502 HA — Identify HA requirements", not "502 Topic N" — the deck author's "Topic 1–4" numbering collides with our delivery Topic numbers.)*
- **Drop (off student slides):** **UoC references** (PC / KE / AT / criterion codes). No student needs to look up the unit of competency, so they add nothing on a slide. The UoC mapping lives in **`coverage.md`** (and trainer notes if needed) — never on a student-facing slide.
- **No forward references in an exercise** — it may use only what's been taught *by that point in the deck*. If an exercise needs a service or concept from a later component, reorder, or re-cast it onto things already known (e.g. classify *described* services, not yet-unnamed AWS products).
- **Reused activities must respect the depth ceiling** — a large AWS activity often runs far deeper than the AT needs; drop it for this Topic (it belongs to a later, deeper one) rather than overshoot.

**Tempo bands** (for later session-sizing; a Topic may span >1 session): ~15–20 min teach / 40–45 activity = 3 small components per class · ~20–30 / 60–70 = 2 medium · ~30–40 / 140–150 = 1 big/practical-heavy.

**What's git-tracked.** The assembled, curated Topic decks (`topic_NN/Topic_NN_Slides.pptx`) **are
git-tracked** — the org-owned repo is the primary instructor-to-instructor channel for finished teaching
materials. Only the **raw AWS source decks** (`**/source_slides/`) and `/original-materials/` stay
**git-ignored** — the reason is **size + file count** (1 GB+), *not* licensing (the audience is
authorised instructors, covered by reuse rights). `.pptx` binary bloat is acceptable for now; Git LFS is
the fallback if history grows. **Don't auto-regenerate a consolidated deck** to fix trivia — the human
hand-consolidation (added source slides + images) would be lost.

**Before the deck is final — size check** (run it after the human has added the images back). Decks are git-tracked (the repo is the instructor-to-instructor channel), so keep them small enough for plain git. Use the **`inspect-file-size`** skill (it runs its bundled `.claude/skills/inspect-file-size/inspect_file_size.py`) — it reports the deck size and its largest internal objects, and fails over the 25 MB guideline. If it's large (guideline: warns over 25 MB), find what's driving it and optimise *before* committing: bloat usually rides in on pasted AWS slides (uncompressed images of *any* type, embedded video/audio, dragged-in masters). Fix with PowerPoint > Compress Pictures (whole deck, 150 ppi, delete cropped areas) or by dropping the offending object, then re-run the check. Don't assume the culprit — diagnose it; it won't be the same thing every time.

**Result (S1-CL1):** Topics 1–3 built this way — Topic 1 (mixed: bespoke + AWS images, authored with placeholders), Topic 2 (all bespoke), Topic 3 (mixed: the two AWS Pricing-Calculator slides). All Kangan-branded; each opener → components (*teach → exercise → takeaways*) → close; exercises run on the Accounting practice scenario.

### Still to do (S1-CL1)
Work the remaining Topics through Steps 2–3 · pin AWS deck slide-ranges · size Topics against the tempo bands and lay them onto S2–S28 (deferred until the materials reveal each Topic's real footprint).

---

## Quirks and gotchas encountered

1. **The `.docx` is the source of truth for each AT, not the `.md`.** The markdown companions were an intermediate step toward the institutional `.docx`; downstream edits may have landed only in the `.docx`. Extract from the `.docx`. (Per Tim 2026-05-31.)
2. **`docx_to_text` extraction on Windows.** The repo's `scripts/validate_uoc.py` has a reusable `docx_to_text(Path)`. Printing its output straight to the Windows console fails on non-cp1252 glyphs (e.g. `☐` ballot box); and native Python doesn't resolve bash's `/tmp`. Write the extracted text to a file under `tempfile.gettempdir()` with `encoding='utf-8'`, then read it.
3. **`.pptx` extraction + long paths.** No shared pptx helper exists; slide text lives in `ppt/slides/slideN.xml` as `<a:t>` elements (namespace `http://schemas.openxmlformats.org/drawingml/2006/main`) — iterate them per slide, ordered by N. **Two Windows traps:** (a) the AWS deck folder has deeply-nested duplicate directories that push paths past the 260-char `MAX_PATH` limit — `zipfile.ZipFile` then fails even though MSYS `find`/`cp` see the file (the `\\?\` long-path prefix did **not** reliably work); (b) native Python doesn't resolve MSYS `/tmp`. **Fix that worked:** `cp` the needed decks (via bash, which handles long paths) into a short **Windows-addressable** dir such as `/c/Users/<u>/AppData/Local/Temp/<x>`, then point Python at the `C:/Users/.../Temp/<x>` form.
