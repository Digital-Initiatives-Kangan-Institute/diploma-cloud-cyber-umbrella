---
name: delivery-run-sheet
description: The delivery process is now a formalised step→gate run-sheet (docs/process-delivery.md) mirroring the assessment run-sheet; the 3-layer gate architecture; Steps 1 (cluster spec), 3 (coverage spine), and the slide-plan gate built + back-tested on S1; the decided Step-4 deck/image model and Step-5 practice model; what remains.
metadata:
  type: project
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

**Step-4 deck BUILDER built (2026-06-25).** The generic `scripts/build_topic_deck.py` generates a Kangan
deck **FROM** a Topic's `slide_plan.md` (parser → `[TYPE]`→layout map → each slide's `image:` resolved
**in-pipeline** by `scripts/helpers/deck_images.py`: diagram→draw-diagram, gen→image-gen/**Nano Banana**
`google/gemini-2.5-flash-image` ~US$0.04/img, **generate-once cached + cost-gated default-off**,
reuse/placeholder→placeholder, none→skip). `kangan_deck.place_image()` added — backward-compatible with
the 14 CL1 per-topic scripts. **One generic builder replaces the per-topic scripts; the slide plan now
holds FINISHED content (read verbatim), not briefs.** Proven end-to-end on CL2 topic_01:
validate-slide-plan PASS → 20-slide deck with the web-scale diagram + 2 gen images placed automatically
(1.86 MB).

**CL2 delivery state (2026-06-25):** Gates 1 (spec PASS), 2 (10-topic spine — AT1 = Topics 1–5 / AT2 =
6–10, each anchored to its AT), 3 (coverage **91/91 PASS**, after the tag retrofit + authoring the AT1
specs). AT1 coverage specs (topics 1,2,3,5) authored **DRAFT — human review of allocation/depth-ceilings
pending**. topic_01 deck built. Remaining: author the other 9 CL2 slide plans + build; CL2 Steps 5–6.

**NEXT:** finalise the spine (coverage.md format standard + skill; merge steps 2+3); build **Step 6
`validate-delivery-plan`**; author the remaining CL2 slide plans → decks. Related:
[[assessment-run-sheet]], [[scenario-plan-model]].
