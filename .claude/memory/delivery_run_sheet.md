---
name: delivery-run-sheet
description: The delivery process is now a formalised step→gate run-sheet (docs/process-delivery.md) mirroring the assessment run-sheet; the 3-layer gate architecture decided here, Step 1 (cluster spec) built + back-tested on all S1 clusters, and what remains (the deterministic spine).
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

**The delivery SPINE is Step 3** — `validate-delivery-coverage` (to build): the union of all Topics'
`coverage.md` UoC tags must cover **every assessed UoC item** in `consolidated_uoc.md` — the teaching-side
analogue of the assessment run-sheet's `validate-cluster-coverage`. Deterministic (same canonical
`[UNIT SEC num]` tags).

**NEXT:** build the deterministic spine, value order: **Step 3 `validate-delivery-coverage`** (the spine),
then **Step 6 `validate-delivery-plan`** (placement + frame reconciliation + template). **Steps 2/4/5 stay
human** (Step 4 already has `inspect-file-size` for deck size; Step 2 a candidate light structural lint;
Step 5 the no-leakage human check). Back-test each against **CL1's built delivery** (14 topic decks +
`coverage.md` files) — the same back-test-on-S1 discipline that proved every assessment gate. Related:
[[assessment-run-sheet]], [[scenario-plan-model]].
