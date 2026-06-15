---
name: feedback-process-docs-current-only
description: Record things as they ARE, not how they used to be — current state only, in EVERYTHING I persist (process docs, memory entries, status notes); no superseded/deleted/refactored-away archaeology; git holds it
metadata:
  type: feedback
---

**Record things as they ARE, not how they used to be.** This governs **everything I persist** — operational/process docs (e.g. `process-assessment.md`, `process-delivery.md`) **and memory entries, status notes, state snapshots**. Each must contain **only the current state/method** plus genuinely forward-useful guidance. **Do not** carry what was tried and abandoned, what got deleted or refactored away, terminology that was renamed, or evolution changelogs. A clean current-state record reads as if the dead ends never happened. **This applies hardest to anything a human reads** (specs, scenario docs, READMEs): 'as is' only. If deprecated history must be kept at all, it goes to **git** (or LLM-only memory) — never into a doc a person reads, and never as a changelog section inside one.

**Why:** these docs are required reading loaded into context every session, so every line costs tokens on every load. A reader following the working process gains nothing from the autopsy of the abandoned one. Tim's analogy: McDonald's gives staff the burger recipe — not the recipe plus decades of every process they tried and dropped.

**How to apply:**
- State the method. Full stop. No "this is how we do it, and here's a whole extra paragraph on how we used to."
- A superseded approach is **deleted**, not demoted to a "superseded notes" section.
- Convert a real lesson into **one line of forward guidance** only if it changes how the next person approaches the work (and even then, a clear positive instruction usually makes the "don't do X" warning unnecessary).
- **git history is the changelog/archaeology** — every prior version is recoverable, so the live doc doesn't carry it. Drop changelog sections from handover docs.

Recorded 2026-05-31 after Tim flagged deprecated-process commentary in `process-delivery.md` as token burn. See [[feedback-draft-naming-pragmatism]] (same spirit: don't over-invest in things that don't serve the working artefact).
