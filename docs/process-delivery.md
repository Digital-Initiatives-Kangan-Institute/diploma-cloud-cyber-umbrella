# Cluster delivery run-sheet

**Audience:** humans and LLM agents creating a cluster's **delivery materials** — the trainer-facing
schedule, the teaching decks, and the practice. This is one of the project's **two run sheets** — the
[assessment run-sheet](process-assessment.md) and the delivery run-sheet (here). The assessment
run-sheet **produces** the cluster's assessment artefacts; this run-sheet **sequences and teaches**
them, so it consumes the assessment run-sheet's outputs (the ATs, the assessment plan, the
scenario/website, the mapping docs).

> **Paths** in this document are relative to the `diploma-cloud-cyber-content/` repo root.

## How this run-sheet works

Once a cluster's assessment artefacts exist, the pipeline below runs in order. Each **step** is one unit
of work (a brief description here; the deep detail is in the linked skill or section). Between every step
is a **gate** — the conditions that must hold before moving on:

- **Machine condition** — a deterministic validator that must pass (where one exists). This is the
  step's definition of done.
- **+ human review** — initially every gate also needs a human sign-off. **As a step earns confidence,
  the human check can be dropped from that gate** (leave the machine condition). Gates with no validator
  yet are **human-only** for now — those are the steps to grow tooling for.

Step 1 (the cluster specification) is authored **per cluster** but its gate is **semester-level**: the
cluster-definition phase ends only when *every* cluster's frame passes **and** the human agrees to
proceed. Steps 2–5 loop **per AT / per Topic**; step 6 is **cluster-level** (the capstone schedule).

All validators are **stdlib-only** and live in `.claude/skills/scripts/`; run them with any Python 3
launcher (`python` / `python3` / `py -3`). The deterministic skills travel with the repo and lift into
future courses unchanged (the format docs they read travel in the umbrella `docs/` tooling layer).

**Prerequisites to read before acting:**
- The umbrella `CLAUDE.md` — working discipline (nothing recorded as decided without explicit approval;
  mark proposals/produced docs **DRAFT/TBD**) + git-safety rules.
- [project-overview.md](project-overview.md) — scope, delivery context (AWS Academy labs, scenario
  architecture), success criteria (a delivery plan is success-criterion #1 per cluster).
- [process-assessment.md](process-assessment.md) — the assessment-creation process whose outputs this
  plan sequences.
- [cluster-authoring-conventions.md](cluster-authoring-conventions.md), [scenario-flow.md](scenario-flow.md),
  [kangan-branding.md](kangan-branding.md), [lab-pack-standard.md](lab-pack-standard.md).
- The cluster's working state lives in LLM memory (the per-cluster delivery entry).

**Working rules for documents produced (same as the assessment run-sheet):**
- Nothing recorded as a decision unless actively discussed and explicitly approved. Proposals are **TBD**.
- Mark produced documents **DRAFT** while in progress.
- Do not modify anything under `original_materials/` — read-only reference.
- The institutional delivery-plan format-of-record is `templates/Delivery_Plan_Template_v0.1.docx`.

## Cluster folder layout (delivery state)

The delivery materials sit under `delivery/`, alongside the assessment outputs and the cluster frame:

```
SX-CLY-<Cluster-Name>/
├── cluster-specification.md   # the delivery frame (step 1)
├── assessments/               # the ATs (from the assessment run-sheet) — the source of truth
├── consolidated_uoc.md        # the UoC contract (from the assessment run-sheet)
├── mappings/                  # per-UoC Assessment Mapping docs (from the assessment run-sheet)
└── delivery/
    ├── planning/              # working drafts: topic spine, session scaffold, AWS deck catalogue, demo catalogue
    ├── topic_NN/              # one per content Topic (steps 2–4)
    │   ├── coverage.md        #   UoC + AT alignment (the spec) — kept
    │   ├── slide_plan.md      #   the kept, validated source the deck is built from (slide-plan-format.md)
    │   └── Topic_NN_Slides.pptx  # the generated Kangan deck — THE ARTEFACT OF RECORD
    └── SX_CLY_Delivery_Plan.docx  # the institutional schedule (step 6)
```

The per-cluster delivery **frame** (hours / weeks / sessions / conventions) is **not** restated here — it
lives in each cluster's [cluster-specification.md](cluster-specification-format.md) (step 1). At the
semester level, the agreed S1 sequencing is: **CL1 solo, weeks 1–8; CL2 + CL3 in parallel, weeks 9–18.**

## Delivery strategy — teach / practice / assess

The basic approach per cluster. Each Topic / competency area moves through a three-phase cycle:

1. **Teach** — deliver the theory: slides, discussion, activities, practical demonstration. A demo may
   be a **recorded video** (where one exists) rather than a live in-class demo.
2. **Practice** — students practise what they learned through in-class activities that prepare them for
   assessment. The lowest-friction design is a **practice task that mirrors the assessment but set in a
   different scenario** — close enough to build the skill, different enough that it isn't rote rehearsal
   of the real assessment. A practice task may split into **several exercises that together cover all
   parts of the related assessment**.
3. **Assess** — assess using the **already-authored assessment tasks** (the ATs from the assessment
   run-sheet).

**Design implication:** practice tasks are derived from the ATs (so coverage is guaranteed) but
re-scenarioed away from the real assessment context — and that re-scenarioing is also a **no-leakage**
guard (see [scenario-flow.md](scenario-flow.md)). In-deck practice exercises are part of the Topic deck
(step 4); the AT-mirroring practice **task** is the distinct artefact of step 5.

---

# The pipeline (step → gate)

**1 · `setup-cluster-spec` — Cluster specification (delivery frame)** *(per cluster; gate is semester-level)*
Agree the delivery frame — nominal hours, weeks, sessions, the session length that falls out of them, the
schedule conventions (onboarding, spare buffer, assessment placement), and the topic budget that starting
point implies. Produced by the **main-session elicitation** (an interactive human dialogue, not a
sub-agent). → [cluster-specification-format.md](cluster-specification-format.md) · detail [§1](#1--cluster-specification). **built**
> **⟱ Gate 1→2 (definition phase):** *validator* `validate-cluster-spec` = **PASS for EVERY cluster**
> (fields present per the format skeleton; frame + topic-budget arithmetic reconcile; over-nominal hours
> carry a recorded authorisation) **+ human agreement to proceed.** Do not start step 2 until all
> clusters' frames are locked and signed off.

**2 · Topic breakdown** *(loop per AT)*
From each AT, identify the conceptual **Topics** — coherent teaching units anchored to the AT's own
structure (deliverable sections, appendix/KE questions, marking criteria), placed into the cluster's
session sequence against the frame's bookends; create a `topic_NN/` folder each. → detail [§2](#2--topic-breakdown).
> **⟱ Gate 2→3:** *human review* — every AT is broken into Topics that cover it, sized sanely against the
> frame's available sessions. *(No script yet; a light structural lint — every AT → ≥1 Topic, every Topic
> names its AT — is candidate tooling.)*

**3 · Topic spec (`coverage.md`)** *(loop per Topic)*
State what each Topic must cover, in **UoC** and **AT** terms — components C1..Cn from the AT; per
component the UoC it **teaches** (canonical `[UNIT SEC num]` tags) and the **AT alignment**. **The AT
sets the depth ceiling** — don't teach deeper than the assessment requires. → detail [§3](#3--topic-spec).
> **⟱ Gate 3→4:** *validator* `validate-delivery-coverage` = the union of all Topics' `coverage.md` tags
> **covers every assessed UoC item** in `consolidated_uoc.md` (nothing assessed-but-untaught; no phantom
> tags) **+ human review.** **to build** — *this is the delivery spine, the analogue of the assessment
> run-sheet's `validate-cluster-coverage`.*

**4 · Slide plan → Topic deck** *(loop per Topic)*
Author each Topic's `slide_plan.md` — the **kept, validated source** (per-component `Teaches:`, each
slide's type tag + mandatory `image:` source) — to the format standard, then **generate** the
Kangan-branded deck from it (primer-first, reuse-first; **generated diagrams placed in-pipeline**,
AWS-reuse images pasted by a human). The **deck is the artefact of record**; the slide plan is kept and
validated (**not** disposable). → [slide-plan-format.md](slide-plan-format.md) · [kangan-branding.md](kangan-branding.md) · detail [§4](#4--topic-decks). **validate-slide-plan + inspect-file-size built**
> **⟱ Gate 4→5:** *validator* `validate-slide-plan` = **PASS** (conforms + covers `coverage.md`) **before
> the deck is built**; then `inspect-file-size` ≤ guideline on the built deck (git-tracked — keep small)
> **+ human review** — pedagogy sound; student slides **in-world**, **no UoC codes**, no tell of the
> assessed system; reuse-first respected; depth ceiling not overshot.

**5 · Practice tasks** *(loop per AT)*
Derive the AT-mirroring **practice task** for each AT — re-scenarioed away from the real assessment, split
into exercises that together cover all parts of the AT. → detail [§5](#5--practice-tasks).
> **⟱ Gate 5→6:** *human review* — the practice covers the AT's parts and is re-scenarioed with **no
> cross-cluster leakage** (the scenario-flow no-leakage invariant). *(No script.)*

**6 · Delivery plan** *(cluster-level — capstone)*
Lay the Topics + assessment sessions onto the session grid from the frame, and generate the institutional
**Delivery Plan** docx (`templates/Delivery_Plan_Template_v0.1.docx`). → detail [§6](#6--delivery-plan).
> **⟱ Gate 6→done:** *validator* `validate-delivery-plan` = every Topic + every assessment is placed in a
> session; the sessions reconcile with the cluster-specification frame; the docx conforms to the template
> **+ human review.** **to build.** The cluster's delivery is complete.

---

# Step detail

## §1 — Cluster specification
*(per cluster; the gate is semester-level.)* Run the **`setup-cluster-spec`** skill — the main session
works through the format doc's elicitation questions with the human (nominal hours, weeks, sessions,
session length, the onboarding / spare-buffer / assessment-placement conventions, and budget tolerance),
does the arithmetic, records any over-nominal authorisation, writes `<cluster>/cluster-specification.md`
to the format, and runs `validate-cluster-spec`. It is **not** a sub-agent: producing the spec is an
interactive human dialogue, which only the main session can do.

The frame is the box every later step fits into: the topic budget (step 2's starting point) and the
session grid (step 6) both derive from it. The gate is the **definition-phase** gate — every cluster's
frame passes the linter and the human signs off — because the clusters share a semester and their hours
net against each other.

**Step gotcha:**
- **Over-nominal needs a recorded authorisation.** Rounding the session length to a practical block
  rarely hits nominal exactly. Running *under* is fine; running *over* is fine too **if** the human
  authorises it — and the linter fails an over-nominal frame whose `Over-nominal authorisation` is `n/a`.
  Record who authorised it and why.

## §2 — Topic breakdown
*(loops per AT.)* From the assessment itself, identify the conceptual **Topics** — coherent teaching
units anchored to the AT's own structure (the natural movements of producing the deliverable; e.g. a
Business Case = *know the tech → diagnose → build evidence → decide & plan → make the case*). Read **both**
the Student and Assessor `.docx` (the source of truth — see the appendix). Name the Topics, place them in
the cluster Topic sequence against the frame's fixed bookends (onboarding, spare buffer, assessment
sessions), and create a `topic_NN/` folder each.

**Model:** `AT → Topic → component`. A **Topic** is the delivery unit (one `topic_NN/` folder — the level
you build materials for and schedule into sessions; aligns with the Delivery Plan template's "Topic and
description" field). A Topic's **components** (C1, C2, …) are defined *inside* its `coverage.md` (step 3),
derived straight from the AT — there is no separate decomposition document. Assessments are **not Topics**
— they are lettered non-Topic sessions in the spine, with no `topic_NN/` folder.

**Result (S1-CL1):** 14 content Topics across AT1 (1–5) / AT2 (6–10) / AT3 (11–14); assessments are
separate lettered non-Topic sessions; + onboarding (S1) + spare/catch-up (S31–32).

## §3 — Topic spec
*(loops per Topic.)* State what the Topic must cover, in **UoC** and **AT** terms — the contract its
materials satisfy. **The AT sets the depth ceiling** — don't teach deeper than the assessment requires
(e.g. Topic 1 = exactly Appendix 2 Q1–Q5, *recognise/explain/classify*, not build). List the Topic's
components C1..Cn (from the AT); per component, the UoC it **teaches** (full `[UNIT SECTION num]` tags) +
the **AT alignment** (which criteria / deliverable sections / appendix questions it prepares for);
distinguish *taught here* vs *applied (taught earlier)*; state what is out of scope; end with a coverage
checklist. **Only UoC + AT cross-references** — nothing pointing at working drafts, so the file stands
alone when those are deleted.

The step-3 gate is where the **delivery spine** lives: `validate-delivery-coverage` (to build) will read
every Topic's `coverage.md` tags and confirm their union covers every **assessed** UoC item in
`consolidated_uoc.md` — the teaching-side mirror of the assessment run-sheet's cluster-coverage check.
Because the `coverage.md` tags use the same canonical `[UNIT SEC num]` machinery, the check is
deterministic.

**Result (S1-CL1):** all 14 Topics specced; the canonical tags are in each `topic_NN/coverage.md`.

## §4 — Slide plan → Topic deck
*(loops per Topic.)* Author the Topic's `slide_plan.md` to the [slide-plan format standard](slide-plan-format.md),
**validate it** (`validate-slide-plan` — conforms + covers `coverage.md`), then **generate** the
Kangan-branded deck from it. The **deck is the artefact of record**; the slide plan is the **kept,
validated source** it is built from (no longer disposable). Each slide carries a mandatory `image:`
source: **generated** images (`diagram` = Graphviz/Mermaid rendered to PNG, `gen` = image-model) go
**straight into the deck in-pipeline**; only **`reuse`** of an existing external asset (e.g. an AWS
diagram) is emitted as a labelled placeholder for a **human to paste**. (S1 leans on AWS reuse — the
exception; most courses generate their diagrams. The draw.io render path + image-gen are delivery-side
tooling.)

**The slide-creation process:**
1. **`slide_plan.md`** — walk the Topic's components top-to-bottom; for each, **teach then its exercise**,
   in deck order. **For a hands-on AWS practical, insert a `[DEMO]` between them — the flow is `teach →
   demonstrate → practice`.** Mark each slide `[PRIMER]` (vendor-neutral fundamentals), `[BESPOKE]`
   (content brief inline), `[AWS Mx Sy]` (an AWS deck slide to reuse), `[DEMO]` (recorded demo), or
   `[EX]` (exercise). The plan **pins up front exactly which AWS slides the Topic needs** (deck + slide
   numbers, via `planning/aws-deck-catalogue-draft.md`) — this pin table drives both the agent's reading
   and the human's image-paste.
2. **(agent) generate the deck** — a per-Topic build script (`scripts/<cluster>/build_*_topicNN_deck.py`,
   importing the shared `scripts/helpers/kangan_deck.py`) authors **every** slide — bespoke *and*
   AWS-sourced — fresh into the **Kangan brand layouts** (title / divider / content / activity / demo /
   takeaways / table; see [kangan-branding.md](kangan-branding.md)). Output `Topic_NN_Slides.pptx`.
3. **(human) paste the AWS images** — drop the reused diagrams/screenshots into the placeholder slots in
   PowerPoint, straight from the main AWS deck folder.

**Marking the AWS source on a slide** (provenance, since there is no `source_slides/` folder):
- **Slide carries an AWS image/diagram** → render a **labelled image placeholder** naming the diagram
  **and the exact source slide(s)** — e.g. *"AWS — VPC building blocks diagram (ACA M07 S16)"*. The
  placeholder *is* the source marker; the human pastes the real image over it.
- **Content/text-only AWS slide** → author the content reuse-first **and** add a visible note **"take
  from AWS [deck · slide ref]"**.

**Primer-first (no assumed baseline).** Students may not arrive with base IT knowledge, so every
technical concept is taught **fundamentals-first**: a short vendor-neutral **`[PRIMER]`** before the
AWS-context slide. Per-concept shape: **`[PRIMER] → [AWS] teach → [DEMO] → [EX]`**. Reuse-first still
governs the primer — pin an AWS "basics" slide where one teaches the fundamental.

**Reuse-first (AWS content) — the governing principle for AWS-heavy topics.** Where an AWS deck covers a
teach point, **author the slide FROM the AWS slide's actual content** — extract + read the relevant AWS
module(s) from `original-materials/AWS-Instructor Presentations/…` **before** authoring. Bespoke is
reserved for genuine gaps (VET evidence discipline, scenario-specific framing, supplied-design
specifics). The long-path trick for the ACA decks: `cp` to a short Windows-addressable temp dir, then
open with python-pptx.

**Open thread — reuse vs rewrite.** Authoring AWS content *fresh into Kangan slides* edges toward
rewriting rather than reusing. The resolution so far is human **consolidation** of the drafted Kangan
slides with the actual AWS reference slides into the final deck. The pure model is **not yet settled** —
revisit.

**Demos — recorded first.** **Always use an AWS recorded demo where a suitable one exists** (catalogued
in `planning/aws-recorded-demos-catalogue.md`); a **live instructor demo is the fallback only when none
is available**. The `demo_slide` layout shows which (RECORDED DEMO vs DEMONSTRATION) via its `source`
parameter.

**Brand:** teaching decks wear **Kangan/BKI** branding (gold `#EDAB0C` + charcoal, Roboto), **not** the
in-world YAT case-study brand — see [kangan-branding.md](kangan-branding.md). All brand + layout code
lives in **`scripts/helpers/kangan_deck.py`** (the shared base); per-Topic builders are content-only and
`import kangan_deck as k`.

**Slide-build rules (apply as you place each slide):**
- **The plan holds briefs, not finished copy.** Write the actual title + bullets at build time.
- **Student-facing slides stay in-world** — same rule as the intranet. No course/assessment language *on
  the slide*: no "AT1 / Appendix 2 / Business Case §x", and nothing that tips **which system is the
  assessed one**. **Source-deck references MAY stay on the slide; UoC references MUST NOT.**
- **Keep (visible to students):** the *source-deck* provenance in a teach slide's kicker (the AWS module,
  plus the bespoke ICTCLD502 HA decks by title), image-placeholder labels, and the demo `source=` cue.
- **Drop (off student slides):** **UoC references** (PC / KE / AT / criterion codes). The UoC mapping
  lives in `coverage.md`, never on a student-facing slide.
- **No forward references in an exercise** — it may use only what's been taught by that point in the deck.
- **Reused activities must respect the depth ceiling** — drop an activity that runs deeper than the AT
  needs (it belongs to a later Topic) rather than overshoot.

**Tempo bands** (for session-sizing; a Topic may span >1 session): ~15–20 min teach / 40–45 activity = 3
small components per class · ~20–30 / 60–70 = 2 medium · ~30–40 / 140–150 = 1 big/practical-heavy.

**What's git-tracked.** The assembled Topic decks (`topic_NN/Topic_NN_Slides.pptx`) **are git-tracked** —
the org-owned repo is the instructor-to-instructor channel for finished teaching materials. Only the raw
AWS source decks (`**/source_slides/`) and `/original-materials/` stay **git-ignored** (size + file
count, not licensing). **Don't auto-regenerate a consolidated deck** to fix trivia — the human
hand-consolidation (added source slides + images) would be lost.

**Size check (the gate's machine condition).** After the human has added images back, run the
**`inspect-file-size`** skill — it reports the deck size + its largest internal objects and fails over the
25 MB guideline. Bloat usually rides in on pasted AWS slides (uncompressed images, embedded media). Fix
with PowerPoint > Compress Pictures (whole deck, 150 ppi, delete cropped areas) or by dropping the
object, then re-run. Don't assume the culprit — diagnose it.

**Result (S1-CL1):** Topics 1–14 built this way (mixes of bespoke + AWS-sourced, authored with
placeholders); all Kangan-branded; each opener → components (*teach → exercise → takeaways*) → close;
exercises run on the Accounting practice scenario.

## §5 — Practice tasks
*(loops per AT.)* Derive the AT-mirroring **practice task** — re-scenarioed away from the real assessment
context, split into exercises that together cover all parts of the related AT (coverage is guaranteed
because it is derived from the AT). The re-scenarioing is also the **no-leakage** guard: a practice
vehicle for a system assessed in another cluster must stay clear of that cluster's assessed scope (see
[scenario-flow.md](scenario-flow.md)). Practice vehicles are maintained under this run-sheet, not the
assessment one.

**Result (S1-CL1):** the YAT Accounting System (Ledgerline) practice scenario — same org, different
system, added to the AT1 intranet as a peer engagement to the LMS, indistinguishable until the task is
handed out. A practice-scenario deck is built via `scripts/scenario/`.

## §6 — Delivery plan
*(cluster-level — capstone.)* Lay the Topics (step 2–4) + the assessment sessions onto the session grid
defined by the cluster-specification frame (step 1), then generate the institutional **Delivery Plan**
docx from `templates/Delivery_Plan_Template_v0.1.docx`. Size each Topic against the tempo bands (§4) and
fit it to the available teaching sessions; place the assessment sessions per the frame's
final-assessment-before-the-spare-buffer convention.

The step-6 gate condition is `validate-delivery-plan` (to build): every Topic and every assessment is
placed in a session, the session totals reconcile with the frame's `Total sessions` / delivered hours,
and the docx conforms to the template. The *quality* of the sequence stays a human call.

**Result (S1-CL1):** `delivery/S1_CL1_Delivery_Plan.docx` produced; the session scaffold is in
`delivery/planning/cl1-delivery-sessions-draft.md`.

---

# Appendix — process-wide gotchas

1. **The `.docx` is the source of truth for each AT, not the `.md`.** The markdown companions were an
   intermediate step toward the institutional `.docx`; downstream edits may have landed only in the
   `.docx`. Extract from the `.docx`.
2. **`docx_to_text` extraction on Windows.** The repo's `scripts/validate_uoc.py` has a reusable
   `docx_to_text(Path)`. Printing its output straight to the Windows console fails on non-cp1252 glyphs
   (e.g. `☐`); and native Python doesn't resolve bash's `/tmp`. Write the extracted text to a file under
   `tempfile.gettempdir()` with `encoding='utf-8'`, then read it. **(The same cp1252 trap bites any
   validator that prints non-ASCII to a pipe — keep gate output ASCII-safe / reconfigure stdout to
   utf-8.)**
3. **`.pptx` extraction + long paths.** Slide text lives in `ppt/slides/slideN.xml` as `<a:t>` elements
   (namespace `http://schemas.openxmlformats.org/drawingml/2006/main`). **Two Windows traps:** (a) the
   AWS deck folder's deeply-nested duplicate directories push paths past the 260-char `MAX_PATH` limit —
   `zipfile.ZipFile` then fails even though MSYS `find`/`cp` see the file; (b) native Python doesn't
   resolve MSYS `/tmp`. **Fix:** `cp` the needed decks (via bash) into a short Windows-addressable dir
   such as `/c/Users/<u>/AppData/Local/Temp/<x>`, then point Python at the `C:/Users/.../Temp/<x>` form.
4. **`source-materials.md` is partially stale** — trust the actual `SX-CLY-<Name>/` layout (cluster
   folders sit directly under the repo root).
