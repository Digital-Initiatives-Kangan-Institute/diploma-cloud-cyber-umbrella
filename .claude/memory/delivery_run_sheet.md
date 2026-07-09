---
name: delivery-run-sheet
description: "The delivery process is now a formalised step→gate run-sheet (docs/process-delivery.md) mirroring the assessment run-sheet; the 3-layer gate architecture; Steps 1 (cluster spec), 3 (coverage spine), and the slide-plan gate built + back-tested on S1; the decided Step-4 deck/image model and Step-5 practice model; what remains."
metadata: 
  node_type: memory
  type: project
  originSessionId: 5fe40dfd-42a4-49d7-8e7d-5da57c8df524
---

The cluster **delivery process is a formalised step→gate run-sheet** —
[process-delivery.md](../../docs/process-delivery.md), the **delivery run-sheet** (the second of two; the
**assessment run-sheet** = [[assessment-run-sheet]]). Restructured 2026-06-23 to mirror
process-assessment.md exactly (same "step separated by gates; machine condition + human review, human
removable as a step earns confidence" model). It **consumes** the assessment run-sheet's outputs (the
ATs, assessment plan, scenario/website, mappings) and sequences/teaches them.

**The 6 steps:** 1 cluster specification (delivery frame) · 2 topic breakdown (per AT) · 3 topic spec
(`coverage.md`) · 4 topic decks (Kangan) · 5 practice tasks · 6 delivery plan (institutional docx).

**3-LAYER GATE ARCHITECTURE (durable — Tim's design 2026-06-23; generalises to later delivery steps):**
the **format document is the single source of truth** — it both *informs the producing skill* and is an
*input to the validator*. Three layers per step:
1. **Producing skill** (e.g. `setup-cluster-spec`) — writes the artefact TO the format. For an artefact
   produced by **interactive human dialogue**, the **MAIN session** runs it, NOT a sub-agent — a
   sub-agent (Task tool) runs autonomously and can't ask the human questions turn-by-turn. (This is *why*
   the elicitation is a main-session skill, not an agent.)
2. **Deterministic Python linter** — checks **presence** of every field the format specifies (it **reads
   the format doc's `## Skeleton` block** for the field contract — no hardcoded field list; change the
   skeleton, the check follows) **+** the deterministic arithmetic. Must be **ASCII-safe / utf-8 stdout**
   or it crashes on a Windows cp1252 pipe (bitten + fixed here).
3. **Agent validator** — ONLY the residual **judgment** a deterministic check can't make. Built only
   where a step has real semantic judgment; for the cluster spec there is **none** (the judgment there —
   is the variance/topic-count acceptable — is the *human acceptance call*), so no agent at Step 1.

**Step 1 BUILT + back-tested on S1 (2026-06-23):**
- `docs/cluster-specification-format.md` (format standard + elicitation question-script + skeleton =
  machine-readable contract); `setup-cluster-spec` skill (main-session elicitation); `validate-cluster-spec`
  skill + `validate_cluster_spec.py` (format-driven linter; negative-tested across 5 failure modes).
- The spec (`<cluster>/cluster-specification.md`, cluster root) = the agreed **delivery frame**: nominal
  hours / weeks / sessions / session length, schedule conventions (onboarding, spare buffer, assessment
  placement), and the derived **topic budget**. Frame + budget **arithmetic must reconcile**.
- **Over-nominal rule:** linter **reports** variance always (never fails on variance alone); **fails an
  over-nominal frame ONLY when no authorisation is recorded** — the human may authorise going over.
- **Phase gate (leaving cluster-definition) = SEMESTER-LEVEL:** every cluster's spec passes
  `validate-cluster-spec` **+ human agreement to proceed**. **MET on S1** — CL1 (8h under), CL2 (+6h
  over, authorised), CL3 (+4h over, authorised) all PASS; Tim signed off the overages 2026-06-23.

**Step 2 — the TOPIC-BREAKDOWN gate (`validate-topic-breakdown`) — BUILT 2026-07-09.** The last
human-only *delivery* gate to get tooling (flagged as the top candidate by the process map —
[[process-mapping-and-audit]]). Deterministic, stdlib, `validate_topic_breakdown.py` + skill: every AT
(`assessments/AT<n>/`) has **≥1 Topic**; every Topic declares a valid AT via its `coverage.md` intro
marker **`**AT<n> content Topic**`** (no phantom AT; any `## N. AT<n> equivalence/alignment` heading must
agree); Topic count **≤ `Teaching/practice sessions available`** (nominal-topic-count divergence is
*reported, not failed* — it's a Step-1 estimate). **Structure only** — the UoC-coverage depth is the
Step-3 spine below. Negative-tested (missing-AT, phantom-AT, intro/section mismatch, over-capacity);
**PASS across CL1 (14 Topics) / CL2 (10) / CL3 (8)**. Convention now documented in process-delivery.md §2.

**Step 3 — the coverage SPINE (`validate-delivery-coverage`) — BUILT + back-tested on CL1 (2026-06-24):
90/90 PASS.** Imports the SAME tag machinery the assessment validators use, scans each Topic's
"taught/developed" table, unions, diffs against the consolidated assessed set (PC/PE/KE) — teaching-side
analogue of `validate-cluster-coverage`. **Project-wide tag standardisation done with it:** all delivery
`coverage.md` tags retrofitted to the one canonical standard (unwrapped `[UNIT SEC num]`; 110 unwrapped +
17 numbered). The 10 gaps it surfaced were all under-tagging (teaching existed, tags didn't), now closed.
*(Still pending to fully formalise: a `coverage.md` format standard + skill wrapper, and merging steps 2+3
into one iterative "Topic plan" step.)*

**Step 4 — the SLIDE-PLAN gate — BUILT + back-tested on CL1 (2026-06-24): 14/14 PASS.** The slide plan
(`delivery/topic_NN/slide_plan.md`) is now a **kept, validated artefact** (role change — it was disposable;
superseded) — the source the deck is built from. `docs/slide-plan-format.md` (skeleton = contract) +
`validate-slide-plan` (deterministic: format + **backwards coverage** vs the sibling `coverage.md`, reusing
the shared tag parser — every component present, Teaches union covers every taught tag; no agent —
pedagogical quality is human review). All 14 CL1 slide plans were **reverse-engineered from the built
decks** via a one-off `ast` generator (structure + image sources + per-component Teaches from coverage;
briefs not recoverable) for full back-test parity.

**DECIDED design (not yet built):**
- **Steps 2+3 merge** into one iterative "Topic plan" step: draft breakdown → soft human-accept shape →
  spec `coverage.md` → run `validate-delivery-coverage` → loop until PASS.
- **Step-5 practice-task model:** a practice task = the assessment **decomposed into its nominal steps, 1:1**
  (assessment step N → practice task N), on the **practice scenario** (comparable, not identical — the
  no-leakage guard), **interleaved** with teaching (teach→practice→…→sit the assessment; repeat per
  assessment across the cluster). Checkable: every assessment step has a practice task. Human judgment =
  decomposition + re-scenario.

**Deck-image pipeline BUILT (2026-06-24).** The **`draw-diagram` skill** (umbrella `.claude/skills/`)
authors an editable `.drawio` (stdlib) and renders it to PNG via **Pillow** — Pillow-only dependency, the
first skill to use the **skill-dependencies convention** (docs/skill-dependencies.md: committed
`requirements.txt` + per-skill **gitignored `.venv/`** + import guard + invoke with the venv's python;
pure-stdlib preferred). The **`ensure-python.mjs` SessionStart hook** is now wired (settings.json, alongside
the memory hook) — Node preflight that a usable Python 3 is on PATH. draw-diagram covers the shapes it
authors — boxes, ellipse/stadium terminators, decision diamonds, ER entity boxes, labelled orthogonal
arrows, crow's-foot (ER) edge endings — so one spec expresses a network, a flowchart, or a simple ERD
(NOT vendor icon stencils, and no obstacle-avoidance routing). Its renderer **honours fixed exit/entry ports + waypoints** from the .drawio
(hand-edited diagrams re-render true to source) and **authors explicit ports** so its own diagrams render
identically in draw.io and Pillow (proven 2026-06-25 against draw.io on network/flowchart/ERD). **Validation +
fallback (always offer):** show the render; if not close enough, the human opens the `.drawio` in draw.io and
either (a) exports by hand — *render-only problem, diagram is correct* — or (b) the spec is fixed +
regenerated — *underlying diagram error*. The imported **`image-gen` skill** is the decorative half.
Mapping: slide-plan `image: diagram` → draw-diagram, `image: gen` → image-gen (both placed in-pipeline);
only `image: reuse` needs a human paste.

**Step-4 deck BUILDER built (2026-06-25; relocated to the umbrella 2026-07-08 — see
[[umbrella-engine-architecture]]).** The generic **umbrella** `scripts/build_topic_deck.py` generates a
Kangan deck **FROM** a Topic's `slide_plan.md` (parser → `[TYPE]`→layout map → each slide's `image:` resolved
**in-pipeline** by the umbrella `scripts/helpers/deck_images.py`: diagram→draw-diagram, gen→image-gen/**Nano Banana**
`google/gemini-2.5-flash-image` ~US$0.04/img, **generate-once cached + cost-gated default-off**,
reuse/placeholder→placeholder, none→skip). `kangan_deck.place_image()` added — backward-compatible with
the 14 CL1 per-topic scripts. **One generic builder replaces the per-topic scripts; the slide plan now
holds FINISHED content (read verbatim), not briefs.** Proven end-to-end on CL2 topic_01:
validate-slide-plan PASS → 20-slide deck with the web-scale diagram + 2 gen images placed automatically
(1.86 MB).

**Step 4 formalised as a 5-stage pipeline (2026-07-08):** author `slide_plan.md` → `validate-slide-plan`
→ **assemble committed image assets** → **build** → **QA** (`inspect-file-size` + **`review-slides`**).
Governing **invariant: a deck is a pure function of committed per-topic source** — `slide_plan.md` +
`topic_NN/diagrams/` (specs) + `topic_NN/images/` (gen + reuse files); a rebuild always repopulates, so
decks are re-generatable + re-reviewable. Two engine behaviours now make that hold, automatically on every
build: **`reuse <file>` PLACES a committed asset** from `images/` (was a post-build human paste — the
"regen loses pasted images" fix), and **body text auto-fits + vertical-centres** to a bounded tier set
({18,20,22,24}pt — light slides scale up, dense settle at the 18 floor; consistent-by-rule). Also:
`[TABLE]`-with-no-columns degrades to a content slide (no crash). New **`review-slides` skill** (umbrella
`.claude/skills/`, LibreOffice→PDF + PyMuPDF→per-slide PNG, own venv) is the visual gate: 0 placeholder
boxes, no overflow/overlap, no garbled gen, whitespace/text-fill OK, images not under-sized. **S1 rolled
out across all decks** (CL1/2/3). **CL1 legacy:** its decks still build from per-topic scripts
(`scripts/s1_cl1/build_*.py`, images placed via an `_img()` helper → committed files), NOT the generic
builder — the scripts are CL1's content-complete source (its `slide_plan.md` are reconstructed skeletons);
full migration to the generic builder is deferred. See [[umbrella-engine-architecture]].

**Teacher speaker-notes layer (2026-07-09).** Every teaching/activity/demo slide carries **teacher notes
in the PowerPoint notes pane** (Presenter View — never on the student slide), making decks **teachable
cold**. Teacher-facing → **meta-language allowed** (UoC codes, AT ties, AWS source). **Type-aware:**
teaching = walk-points + misconception + question + UoC tie; **demo = what to demonstrate/emphasise + WHERE
TO FIND the AWS recorded demo** (deck·module·slide from `planning/aws-recorded-demos-catalogue.md`);
activity = a facilitation script (tell-students words, steps, must-produce, timing, share-back,
no-leakage). **Engine:** `kangan_deck.register_notes({title: notes})` + `notes=` on the 4 layouts write
`slide.notes_slide`. **Source-level, never post-build** (a rebuild must repopulate) — CL1 scripts use a
sibling `topicNN_notes.py` + `register_notes()`; CL2/CL3 use a `notes:` block in `slide_plan.md`. Drafted
by the **`draft-slide-notes`** agent pass (slide content + `coverage.md` UoC context), human-reviewed.
**Proven on CL1 Topic 01 (34 slides) + Topic 06 IAM trio.** Format: docs/slide-plan-format.md.

**Step 6 — the DELIVERY-PLAN gate — BUILT 2026-07-02.** The delivery plan is a **semester-INSTANCE
artefact, not a course artefact** (Tim's reframe): the course is fully developable (assessment, decks,
practice) with **no** delivery plan, because the plan needs facts that don't exist until an intake is
imminent — session count, days, and which sessions are **online vs classroom** (~2–4 weeks out). It is
**prerequisite-gated + disposable-per-instance**: those instance facts → a **collaborative human-AI
juggling session** (sequencing = human judgment, stays human) → a machine-readable **outline
`<cluster>/delivery/delivery-plan.md`** → `validate-delivery-plan` → (gaps reported, keep prompting) →
PASS → an automated step fills the docx. So reaching Step 6 = the cluster is **course-complete**, not
unfinished. `docs/delivery-plan-format.md` (skeleton = contract: instance-prereq header + session grid
`# · Week · Day · Mode · Activity · Placed`) + `validate_delivery_plan.py` + `validate-delivery-plan`
skill. The gate is **completeness-for-generation** (each FAIL = a decision still to make): contract
present, grid internally consistent (1..N, every cell decided, Mode/Activity in vocab), **every built
Topic (`topic_NN/`) + every assessment (`AT<n>/`) placed** (enumerated from dirs), frame reconciliation
(row count == declared total; reservations honoured); reports intake-vs-nominal + mode split. **No agent
validator** (sequence quality is human). Negative-tested 9 failure modes + a clean PASS. **Still to
build:** the docx generator (fills `kangan-templates/Delivery_Plan_Template_v0.1.docx` from a validated
outline) — authored at instance-time with the first real plan.

**CL2 delivery state (2026-07-02):** Gates 1–4 PASS. Gate 4 = **all 10 `slide_plan.md` authored +
`validate-slide-plan` PASS 10/10** and **all 10 decks built** (155 slides; 5 draw-diagram diagrams + 9
`gen` heroes via `--allow-gen`). **Step 5 (practice) COMPLETE** — the 28 `[EX]`s are the practice tasks;
LMS engagement `lms-global-expansion` verified state-correct; the AT2 **practice build artefacts** authored
as separate in-world intranet docs (comparable-not-identical: different fault + code); the missing
**`s1-cl2-at2` state added** (cloned from at1 across 61 docs); no-leakage PASS. Detail in [[s1cl2-delivery]].
**CL2 is course-complete (Steps 1–5 + Step-6 gate); Step 6 execution deferred — no intake yet.** AT1
coverage specs still **DRAFT — human review pending**.

**Run-sheet status: all 6 step-gates now BUILT.** **NEXT forward work = apply the run-sheet to CL3
delivery** (not started — cluster-spec exists from the Step-1 phase gate; next CL3 step is topic
breakdown → coverage → slide plans → decks → practice; see [[s1cl3-delivery]]). **STILL decided-not-built
(project-wide refinements):** steps 2+3 merge into one "Topic plan" step; `coverage.md` format standard +
skill; the Step-6 docx generator (instance-time). Related: [[assessment-run-sheet]], [[scenario-plan-model]].
