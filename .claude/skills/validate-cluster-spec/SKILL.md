---
name: validate-cluster-spec
version: 1.0.0
updated: 2026-06-23
model: claude-haiku-4-5-20251001
description: >-
  This skill should be used whenever a cluster's delivery frame needs checking — e.g. "validate the
  cluster specification", "check the delivery frame", "do the hours/sessions add up", "is the cluster
  spec complete", or after authoring or editing a cluster-specification.md. It runs a deterministic
  check (the bundled validate_cluster_spec.py) over a cluster's cluster-specification.md: that every
  heading and field named in the format standard's skeleton is present, that the frame arithmetic
  reconciles (total sessions, delivered hours, variance), that the topic-budget sessions reconcile, and
  that any over-nominal hours carry a recorded authorisation. It is the gate for Step 1 of the delivery
  run-sheet. It checks structure and arithmetic, not whether the frame is pedagogically sound (that is
  the human's acceptance call).
---

# Validate a cluster specification (delivery frame)

A cluster's `cluster-specification.md` is the agreed delivery frame — nominal hours, weeks, sessions,
session length, schedule conventions, and the topic budget that falls out of them (see
[cluster-specification-format.md](../../../docs/cluster-specification-format.md)). This skill proves it
is **complete and internally consistent** before the rest of the delivery run-sheet builds on it.

## When to use

- After `setup-cluster-spec` produces a spec, or after any edit to one.
- As the **Step-1 gate** of the delivery run-sheet, before topic breakdown (Step 2) begins.

It checks the *structure and the numbers*, not the judgement (is the variance acceptable, is the topic
count right) — that stays the human's call, and at later delivery steps an agent validator.

## The validator

The engine is **`validate_cluster_spec.py`**, bundled at `.claude/skills/scripts/`, stdlib-only. It is
**driven by the format document**: it reads the `## Skeleton` block of
`docs/cluster-specification-format.md` to learn the required headings and field labels, so the format
doc is the single source of truth (change the skeleton, the check follows). On top of that structural
check it verifies the deterministic arithmetic and the over-nominal-authorisation rule.

## How to run it

> **Python:** use whatever Python 3 launcher you have — `python`, `python3`, or `py -3`.

```bash
python .claude/skills/scripts/validate_cluster_spec.py --cluster <SX-CLY-dir>
# or
python .claude/skills/scripts/validate_cluster_spec.py --spec <SX-CLY-dir>/cluster-specification.md
# the format doc is auto-located in the umbrella docs/; override with --format <path> if needed
```

Exit `0` on PASS, `1` otherwise.

## Interpreting the result

Goal: `RESULT: PASS`. The `[frame]` line always **reports** the variance (over/under nominal) — that is
information, not a failure.

**Hard failures (must fix):**
- **missing / empty field or heading** — a field the format skeleton requires is absent. Add it.
- **arithmetic doesn't reconcile** — `total sessions ≠ weeks × sessions/week`, `delivered hours ≠ total
  × length`, or the stated `variance ≠ nominal − delivered`. Correct the numbers.
- **topic-budget doesn't reconcile** — `onboarding + spare + assessment + available ≠ total sessions`.
- **over nominal without authorisation** — delivered hours exceed nominal and `Over-nominal
  authorisation` is `n/a`/empty. Either bring it under nominal or record who authorised the overage.

Fix and re-run until PASS. Whether the frame is a *good* plan is the human half of the gate.

## Portability

Self-contained and stdlib-only; the only external input is the format doc (auto-located, or `--format`).
Lifts into any course repo that carries the umbrella `docs/` tooling layer.
