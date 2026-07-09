# Cluster delivery run-sheet

**Audience:** humans and LLM agents creating a cluster's **delivery materials** — the trainer-facing
schedule, the teaching decks, and the practice. This is one of the project's **two run sheets** — the
[assessment run-sheet](process-assessment.md) and the delivery run-sheet (here). The assessment
run-sheet **produces** the cluster's assessment artefacts; this run-sheet **sequences and teaches**
them, so it consumes the assessment run-sheet's outputs (the ATs, the assessment plan, the
scenario/website, the mapping docs).

> **Paths** in this document are relative to the **content repo** root.

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

All validators are **stdlib-only** and live in the umbrella's `.claude/skills/scripts/`; run them with
any Python 3 launcher (`python` / `python3` / `py -3`).

**Where the engine lives (course-agnostic).** The shared **deck/doc/mapping engine** —
`scripts/build_topic_deck.py`, `scripts/helpers/`, `scripts/mapping/` — lives in the **umbrella** (run
with the umbrella's `scripts/.venv`, which carries python-docx/pptx). It is brand- and registry-agnostic:
the **course** supplies its own `brand.py` (palette + org identity) and `mapping_registry.py` (clusters +
qualification + unit prefixes) in **its** `scripts/`, plus the semester-specific generators
(`scripts/s1_cl*/`, `scenario/`, `templates/`). The engine resolves the course's data automatically —
`build_topic_deck` walks up from the slide-plan path to the content repo's `brand.py` (or `--brand`);
`generate_mapping_doc.py` takes `--registry <content-repo>/scripts/`. So the same engine builds any
course's decks/mapping docs unchanged; only the sub-repo data differs.

> **Principle — one course-agnostic mechanism (no forks).** Every artefact type is produced by exactly
> **one** mechanism, shared across all clusters and reusable for any future course: for teaching decks that
> is the generic `build_topic_deck.py` reading a **content-complete `slide_plan.md`** (content *and*
> `notes:` in the one validated source) — not per-topic build scripts or sidecar notes modules. A
> first-built cluster on an older path is **retrofitted onto the canonical mechanism**, not kept as a
> second path; a capability the old path had becomes a **feature of the one engine**, proven by
> reproduction-validation before the old path is retired. The visual/layout pack (`kangan_deck.py`) is the
> one brand seam — swapped per institution, never forked.

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
> **⟱ Gate 2→3:** *validator* `validate-topic-breakdown` = every AT (`assessments/AT<n>/`) has **≥1
> Topic**; every Topic declares a valid AT via its `coverage.md` **`**AT<n> content Topic**`** marker (no
> phantom AT; any alignment heading agrees); the Topic count **fits the frame** (≤ sessions available —
> nominal-count divergence is reported, not failed) **+ human review** — the Topics are the *right* ones,
> sized sanely against the frame. **built** — *structure only; the UoC-coverage depth is Gate 3→4.*

**3 · Topic spec (`coverage.md`)** *(loop per Topic)*
State what each Topic must cover, in **UoC** and **AT** terms — components C1..Cn from the AT; per
component the UoC it **teaches** (canonical `[UNIT SEC num]` tags) and the **AT alignment**. **The AT
sets the depth ceiling** — don't teach deeper than the assessment requires. → detail [§3](#3--topic-spec).
> **⟱ Gate 3→4:** *validator* `validate-delivery-coverage` = the union of all Topics' `coverage.md` tags
> **covers every assessed UoC item** in `consolidated_uoc.md` (nothing assessed-but-untaught; no phantom
> tags) **+ human review.** **built** — *this is the delivery spine, the analogue of the assessment
> run-sheet's `validate-cluster-coverage`* (back-tested on CL1, 90/90).

**4 · Slide plan → Topic deck** *(loop per Topic)*
Five stages: **author** `slide_plan.md` (the kept, validated source) → **validate** (`validate-slide-plan`)
→ **assemble** the Topic's committed image assets (`diagrams/` specs + `images/` gen/reuse files) →
**build** the Kangan deck (images placed + body text auto-fit in-pipeline) → **QA** (`inspect-file-size`
+ `review-slides`). The **deck is a pure function of committed source**, so it rebuilds + re-reviews at
will. → [slide-plan-format.md](slide-plan-format.md) · [kangan-branding.md](kangan-branding.md) · detail
[§4](#4--topic-decks). **generic builder `build_topic_deck.py` + validate-slide-plan + inspect-file-size +
review-slides built.**
> **⟱ Gate 4→5:** *validator* `validate-slide-plan` = **PASS** (conforms + covers `coverage.md`) **before
> the deck is built**; then on the built deck `inspect-file-size` ≤ guideline (git-tracked — keep small)
> **+ `review-slides`** (render → per-slide PNGs): **0 placeholder boxes**, no overflow/overlap, no garbled
> gen images, acceptable whitespace **+ human review** — pedagogy sound; student slides **in-world**,
> **no UoC codes**, no tell of the assessed system; reuse-first respected; depth ceiling not overshot.

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
> **+ human review.** **built** (`validate-delivery-plan`, 2026-07-02). The cluster's delivery is complete.

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

**Each Topic names its AT** in its `coverage.md` intro, via the canonical marker
**`**AT<n> content Topic**`** (e.g. *"…· **AT1 content Topic** ·…"*) — the machine-readable source of the
Topic→AT assignment, corroborated by the `## N. AT<n> equivalence / alignment` section. The
**`validate-topic-breakdown`** gate reads that marker to prove every AT has ≥1 Topic, every Topic names a
real AT, and the Topic count fits the frame.

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

The step-3 gate is where the **delivery spine** lives: `validate-delivery-coverage` reads every Topic's
`coverage.md` tags and confirms their union covers every **assessed** UoC item in `consolidated_uoc.md` —
the teaching-side mirror of the assessment run-sheet's cluster-coverage check. Because the `coverage.md`
tags use the same canonical `[UNIT SEC num]` machinery (the shared `valid_tag_set`/`resolve_tags` parser),
the check is deterministic.

**Result (S1-CL1):** all 14 Topics specced; canonical tags in each `topic_NN/coverage.md` standardised
project-wide; `validate-delivery-coverage` **PASSES 90/90**.

## §4 — Slide plan → Topic deck
*(loops per Topic.)* A five-stage pipeline: **author** the Topic's `slide_plan.md` (to the
[slide-plan format standard](slide-plan-format.md)) → **validate** it (`validate-slide-plan` — conforms +
covers `coverage.md`) → **assemble** the Topic's committed image assets → **build** the Kangan-branded
deck → **visually review** it (`inspect-file-size` + `review-slides`).

**The governing invariant: a deck is a pure function of committed per-Topic source** — the `slide_plan.md`
+ the Topic's `diagrams/` specs + `images/` assets. So a rebuild always repopulates every slide, and the
deck can be re-generated + re-reviewed at will. Each slide's mandatory `image:` source resolves
**in-pipeline**: `diagram` (an editable `.drawio` → PNG via **draw-diagram**), `gen` (**image-gen**,
generate-once + committed), and **`reuse`** (an externally-sourced asset — e.g. an extracted AWS slide —
committed into the Topic's `images/`) are **all placed straight into the deck**; a `reuse`/`placeholder`
whose file isn't present yet renders as a labelled placeholder until the asset lands. The builder also
**auto-fits + vertical-centres body text** (a bounded tier set, {18–24}pt) so a light slide fills the page
and a dense one stays readable — no per-slide hand-tuning, and sizes stay consistent by rule.

Each teaching/activity/demo slide also carries **teacher speaker notes** (the notes pane — Presenter View,
never on the student slide), authored **with** the slide content (co-drafted, or a source-level
`draft-slide-notes` pass) so a teacher can run the deck cold. Type-aware: teaching = walk-the-points +
misconception + question + UoC tie; demo = what to demonstrate/emphasise **+ where to find the AWS
recorded demo** (from `planning/aws-recorded-demos-catalogue.md`); activity = a facilitation script. See
[slide-plan-format.md](slide-plan-format.md) — notes are committed source (a `notes:` block in the plan),
written to the deck on every build.

**The slide-creation process:**
1. **`slide_plan.md`** — walk the Topic's components top-to-bottom; for each, **teach then its exercise**,
   in deck order. **For a hands-on AWS practical, insert a `[DEMO]` between them — the flow is `teach →
   demonstrate → practice`.** Mark each slide `[PRIMER]` (vendor-neutral fundamentals), `[BESPOKE]`
   (content brief inline), `[AWS Mx Sy]` (an AWS deck slide to reuse), `[DEMO]` (recorded demo), or
   `[EX]` (exercise). The plan **pins up front exactly which AWS slides the Topic needs** (deck + slide
   numbers, via `planning/aws-deck-catalogue-draft.md`) — this pin table drives both the agent's reading
   and the human's image-paste.
2. **assemble the committed image assets** (before building, so the build has everything in place):
   author each `diagram` spec into `topic_NN/diagrams/<ref>.json`; run `image-gen` for each `gen` slide
   (generate-once → committed under `topic_NN/images/`); extract/export each `reuse` slide's asset into
   `topic_NN/images/<file>` (for AWS reuse: pull the pinned slide from the instructor decks). Commit them
   — they are the deck's source of truth.
3. **(builder) generate the deck** — the **generic `scripts/build_topic_deck.py`** reads the validated
   `slide_plan.md` and authors **every** slide into the **Kangan brand layouts** (title / divider /
   content / activity / demo / takeaways / table; see [kangan-branding.md](kangan-branding.md)),
   mapping each slide's `[TYPE]` to a layout, **resolving each `image:` in-pipeline** via
   `scripts/helpers/deck_images.py` — `diagram`→draw-diagram, `gen`→image-gen, `reuse`→the committed
   `images/<file>` (all **placed straight into the deck**; a not-yet-supplied `reuse`/`placeholder`→a
   labelled placeholder; `none`→none) — and **auto-fitting + vertical-centring body text**. Output
   `Topic_NN_Slides.pptx`. *(**One generic builder for every Topic in every cluster** — CL1 was migrated
   off its per-Topic scripts onto `slide_plan.md` + `build_topic_deck.py` on 2026-07-09; no per-topic build
   scripts remain. A Topic delivered as two decks for sizing — e.g. topic_08 → `slide_plan_08a.md` /
   `slide_plan_08b.md`, each declaring `> **Covers-components: …**` — builds each half the same way.)*
4. **QA the built deck** — `inspect-file-size` (≤25 MB) **and** `review-slides` (render → per-slide PNGs):
   confirm **0 leftover placeholder boxes**, no text overflow/clipping, no image↔text overlap, no garbled
   gen images, and acceptable whitespace/text-fill. Fix (reshape a wide-short diagram, re-extract an asset,
   supply a missing `reuse` file) and rebuild — the rebuild is idempotent, so re-QA is cheap.

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
lives in **`scripts/helpers/kangan_deck.py`** (the shared base); the generic `build_topic_deck.py`
imports it and is content-agnostic (it reads each Topic's `slide_plan.md`).

**Slide-build rules (apply as you place each slide):**
- **The plan holds the finished slide content** (title + bullets + image directive) — the builder reads
  it verbatim, so write the real copy in `slide_plan.md`, not a brief.
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

**Result (S1-CL1):** Topics 1–14 (mixes of bespoke + AWS-sourced); all Kangan-branded; each opener →
components (*teach → exercise → takeaways*) → close; exercises run on the Accounting practice scenario.

**Result (S1-CL2):** the generic `build_topic_deck.py` proven end-to-end on **topic_01** — `slide_plan.md`
(full content) → 20-slide deck with the web-scale architecture diagram (draw-diagram, in-pipeline) + two
decorative images (image-gen / Nano Banana) **placed automatically**; 1.86 MB. The remaining CL2 Topics
need their slide plans authored, then built the same way.

**Result (S1-CL3):** all 8 Topics built from their validated slide plans — 6 draw-diagram diagrams
(2 flowcharts + 4 architecture/allocation) + 8 image-gen heroes placed in-pipeline; 13–18 slides each,
**each deck size-gated with `inspect-file-size` (all 0.8–0.98 MB, well under guideline) before commit**.
*(Run the size gate on the built decks **before** committing — it is part of this step, not an
afterthought.)*

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

**Result (S1-CL2):** the LMS practice (`lms-global-expansion`) needed no provided baseline design — the
LMS is the learner's own CL1 build, so the practice extends it via the HA-hardened ICT records (unlike
Ledgerline/website, which the learner hasn't built and so get a `scripts/scenario/` design). Two
conventions settled here:
- **Provided build artefacts for practice go as separate in-world docs in the practice project folder**
  (e.g. a data-store template + microservice code), **not** inline like the assessment instrument. They
  stay **comparable-but-not-identical** to the assessment's (a *different* injected fault; *different*
  code/field names) — the no-leakage guard at the artefact level. In-world means design-region only; the
  lab/`us-east-1` substitution stays in the delivery decks, never on the intranet.
- **Adding a per-AT state** (CL2 lacked `s1-cl2-at2`): add the slug to `states.ts`, add it to **every**
  `appearsIn` that carries the prior AT's slug (the underlying state is unchanged across a cluster's ATs
  unless a doc says otherwise), scan for exceptions, then `astro sync` to validate.

## §6 — Delivery plan
*(cluster-level — terminal, and **per semester-instance**.)* The delivery plan lays the Topics (step
2–4) + the assessments onto a concrete session grid and is issued as the institutional
`…_Delivery_Plan.docx`. Unlike every earlier step, it is **not a course artefact**: the course can be
fully developed (assessment, decks, practice) with **no** delivery plan, because the plan depends on
facts that do not exist until a specific intake is imminent — how many sessions that intake gets, on
which days, and which sessions are **online** vs **classroom** (typically known only ~2–4 weeks out).
Re-run it for another intake and you get a different plan from the same course. **The plan is
disposable-per-instance; the course is not.** So this step is deferred by nature — reaching it does not
mean the cluster is unfinished; it means the cluster is *course-complete* and waiting on a real intake.

Those instance facts are a **prerequisite**. Once known, the plan is produced in a **collaborative
human-AI juggling session** — try a layout, look, move things, refit — until the sequence works
(spacing, catch-up placement, on-campus practical/presentation vs online balance). That sequencing is
**human judgment and stays human**. The session's *output* is a machine-readable **outline
(`<cluster>/delivery/delivery-plan.md`)** whose completeness can be checked; when it validates, an
automated step fills the docx from it (from `kangan-templates/Delivery_Plan_Template_v0.1.docx`).

**Pipeline:** prerequisites known → juggling session writes the outline → `validate-delivery-plan` →
(gaps reported → keep prompting the human) → PASS → generate the docx. The outline format is
[delivery-plan-format.md](delivery-plan-format.md).

The step-6 gate is **`validate-delivery-plan`** (BUILT 2026-07-02 — `validate_delivery_plan.py` +
skill): a **completeness-for-generation** check — the outline conforms to the format (header fields +
grid columns from the skeleton), the session grid is internally consistent (numbered `1…N`, every cell
decided, `Mode`/`Activity` in vocabulary), **every built Topic (`delivery/topic_NN/`) and every
assessment (`assessments/AT<n>/`) is placed**, and the grid reconciles with the frame (row count ==
declared total; reservations honoured). It **reports** intake-vs-nominal divergence + the mode split. A
PASS means "complete enough to generate the docx"; each FAIL is a decision still to be made. There is
**no agent validator** — the *quality* of the sequence is the human's call, made live in the session.
*(Still to build: the docx generator that fills the template from a validated outline — authored at
instance-time alongside the first real plan.)*

**Result (S1-CL1):** `delivery/S1_CL1_Delivery_Plan.docx` produced by hand (pre-gate) from the scaffold
`delivery/planning/cl1-delivery-sessions-draft.md`.
**Result (S1-CL2):** course-complete through Step 5; the Step-6 gate is built but the plan itself is
**deferred** — no intake to plan against yet.

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
