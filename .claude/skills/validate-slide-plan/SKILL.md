---
name: validate-slide-plan
version: 1.0.0
updated: 2026-06-24
model: claude-haiku-4-5-20251001
description: >-
  This skill should be used whenever a Topic's slide plan needs checking — e.g. "validate the slide
  plan", "does the slide plan cover the topic plan", "check the slide plan format", "is every slide's
  image source declared", or after authoring or editing a delivery/topic_NN/slide_plan.md. It runs a
  deterministic check (the bundled validate_slide_plan.py): a FORMAT check (header + ## Slides present;
  every component section carries a Teaches: line; every slide carries a recognised [TYPE] tag and a
  mandatory image: field) and a BACKWARDS-COVERAGE check against the sibling coverage.md (every
  component present; the slide plan's Teaches: tags cover every UoC item coverage.md teaches; no
  phantom tags). It is the gate before a Topic's deck is built. It checks structure + coverage, not
  whether a slide teaches its concept well (that is human review).
---

# Validate a Topic's slide plan

A Topic's `delivery/topic_NN/slide_plan.md` is the **kept, validated source the deck is built from** (no
longer disposable). It must (a) conform to the format and (b) cover what its sibling `coverage.md`
requires — so the deck built from it cannot silently drop a component or a UoC item. This skill proves
both mechanically, before the deck is built.

## When to use

- After authoring or editing a Topic's `slide_plan.md`.
- As the **gate before building the Topic deck** (delivery run-sheet).

It checks structure + coverage, not pedagogical quality (does a slide actually teach its concept) — that
stays human review.

## The validator

The engine is **`validate_slide_plan.py`**, bundled at `.claude/skills/scripts/`, stdlib-only. It reads
the **sibling `coverage.md`** as its contract and uses the **same tag machinery as the assessment
validators** (`valid_tag_set` / `resolve_tags`) plus the same taught-table reader as
`validate_delivery_coverage`, so a UoC tag counts here exactly as it does anywhere in the project. The
format it enforces is [slide-plan-format.md](../../../docs/slide-plan-format.md).

## How to run it

> **Python:** `python`, `python3`, or `py -3`.

```bash
python .claude/skills/scripts/validate_slide_plan.py \
  --plan <cluster>/delivery/topic_NN/slide_plan.md
# coverage.md is read from the same topic_NN/ folder; consolidated_uoc.md from the cluster root
```

Exit `0` on PASS, `1` otherwise.

## Interpreting the result

Goal: `RESULT: PASS — slide plan conforms and covers coverage.md`.

**Hard failures (must fix):**
- **slide with no `image:` field** — every slide must declare one (`none`/`reuse`/`diagram`/`gen`/
  `placeholder`); a missing field is ambiguous. Add it.
- **invalid `image:` keyword** — use one of the five.
- **component section with no `Teaches:` line** — add the canonical `[UNIT SEC num]` tags the component
  teaches.
- **slide with an unrecognised `[TYPE]`** — use `PRIMER/BESPOKE/AWS …/DEMO/EX/TABLE/TAKEAWAYS`.
- **component in `coverage.md` with no slide-plan section** — add the `### C<n>` section.
- **UoC item `coverage.md` teaches but the slide plan doesn't** (MISSING) — add it to the right
  component's `Teaches:` line (the slides genuinely teach it), or fix `coverage.md` if the claim is wrong.
- **phantom `Teaches` tag** — a tag that is not a real consolidated UoC item; correct it.

**Advisory:** a `Teaches` tag valid but **not** in `coverage.md`'s taught set (the slide plan claims to
teach something the topic spec doesn't) — reconcile the two.

## Portability

Self-contained and stdlib-only; the only external inputs are the sibling `coverage.md` and the cluster's
`consolidated_uoc.md`, plus the format doc it enforces. Lifts into any course repo carrying the umbrella
`docs/` tooling layer.
