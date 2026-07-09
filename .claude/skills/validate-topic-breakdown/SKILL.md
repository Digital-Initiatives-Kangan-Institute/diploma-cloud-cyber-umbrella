---
name: validate-topic-breakdown
version: 1.0.0
updated: 2026-07-09
model: claude-haiku-4-5-20251001
description: >-
  This skill should be used whenever a cluster's AT -> Topic breakdown needs a structural check — e.g.
  "validate the topic breakdown", "does every AT have a topic", "did we break the ATs into topics
  properly", "check the topic-to-AT split", or after creating the delivery/topic_NN/ folders (delivery
  run-sheet Step 2). It runs a deterministic check (the bundled validate_topic_breakdown.py): every AT
  (assessments/AT<n>/) is covered by at least one Topic; every Topic (delivery/topic_NN/) declares its AT
  via the canonical coverage.md marker `**AT<n> content Topic**` and that AT is real (no phantom, and any
  alignment heading agrees with the intro marker); and the Topic count fits the frame (<= sessions
  available; divergence from the nominal topic count is reported, not failed). It is the gate for Step 2
  of the delivery run-sheet. It checks the breakdown's STRUCTURE, not whether the Topics are the right
  ones (that stays the human's acceptance call).
---

# Validate a cluster's Topic breakdown (delivery Gate 2→3)

Step 2 of the delivery run-sheet decomposes each **assessment task (AT)** into the conceptual **Topics**
that teach it, one `delivery/topic_NN/` folder each (see
[process-delivery.md §2](../../../docs/process-delivery.md)). This skill is the **Gate 2→3** structural
lint the run-sheet names: it proves the decomposition is sound before the Topic specs (`coverage.md`
depth) and decks are built on top of it.

## When to use

- After the `topic_NN/` folders are created (Step 2), before Topic specs / decks (Steps 3–4).
- Any time the AT → Topic split changes, as a cheap re-check.

It checks *structure*, not *quality* — whether these are the **right** Topics and whether the split is
pedagogically sound stays the human half of the gate. The UoC-coverage **depth** (does the union of
Topics teach every assessed item) is the separate Gate 3→4 check, `validate-delivery-coverage`.

## What it checks

- **A — every AT has ≥1 Topic.** The AT set is the `assessments/AT<n>/` folders; each must be claimed by
  at least one Topic.
- **B — every Topic declares a valid AT.** A Topic declares its AT with the canonical **`coverage.md`
  intro marker `**AT<n> content Topic**`**. The declared AT must be a real one (no phantom `AT9`), and
  where the Topic also carries an `## N. AT<n> equivalence / alignment` heading it must **agree** with
  the intro marker. A Topic folder with no `coverage.md`, or a `coverage.md` with no marker, fails —
  the Topic hasn't named its AT.
- **C — the Topic count fits the frame.** The Topic count must be **≤** the cluster-specification's
  `Teaching/practice sessions available` (each Topic needs at least one session) — a hard failure if
  not. Divergence from the `Nominal topic count` is **reported as a warning, never failed**: that count
  is a Step-1 *estimate*, confirmed here at Step 2.

## The convention it enforces

A Topic names its AT in its `coverage.md` **intro line**, e.g.
`**Topic 1 of 14** … · **AT1 content Topic** …`. This one marker is the machine-readable source of the
Topic→AT assignment; the `## N. AT<n> equivalence / alignment` section, where present, corroborates it.

## How to run it

> **Python:** use whatever Python 3 launcher you have — `python`, `python3`, or `py -3`.

```bash
python .claude/skills/scripts/validate_topic_breakdown.py --cluster <SX-CLY-dir>
```

Exit `0` on PASS, `1` on FAIL, `2` on a usage/error (missing cluster / no ATs / no Topics).

## Interpreting the result

Goal: `RESULT: PASS`. The per-AT lines report how many Topics each AT got; the `[warn]` lines are
information (a nominal-count divergence, or a missing spec), not failures.

**Hard failures (must fix):**
- **an AT with no Topic** — break that AT into at least one Topic.
- **a Topic that declares no AT / a phantom AT / a mismatched AT** — add or correct the
  `**AT<n> content Topic**` marker so it names one real AT, consistently with any alignment heading.
- **more Topics than sessions available** — the breakdown can't fit the frame; merge Topics or revisit
  the frame (Step 1).

Fix and re-run until PASS. Whether the Topics themselves are well-chosen is the human half of the gate.

## Portability

Self-contained and stdlib-only (`validate_topic_breakdown.py` in `.claude/skills/scripts/`). Reads only
the committed cluster layout (`assessments/`, `delivery/topic_*/coverage.md`, `cluster-specification.md`),
so it lifts into any course repo that follows the delivery run-sheet conventions.
