---
name: one-course-agnostic-mechanism
description: "There must be exactly ONE course-agnostic mechanism per artefact type, shared across all clusters and reusable for future courses — one source of truth, one engine, one process; unify legacy/first-built paths onto it, never fork; a capability gap becomes a feature of the one engine."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5fe40dfd-42a4-49d7-8e7d-5da57c8df524
---

**Principle (Tim, 2026-07-09 — "the single most important factor"): every artefact type is produced by
exactly ONE mechanism, shared across all clusters and reusable for any future course — one source of
truth, one place to troubleshoot or add functionality, one process, as course-agnostic as possible.**

**Why:** the first-built cluster (CL1) kept ending up on an older, bespoke path while later clusters
(CL2/CL3) established the cleaner pattern — leaving *two ways to build the same thing* (assessment
instruments; teaching decks). Two paths = double the maintenance + troubleshooting surface, and they
drift. The factory must be reusable for *any* course, so the machinery has to be single + generic, not
per-cluster.

**How to apply:**
- When a first-cluster artefact sits on a different path from later clusters, **unify it onto the one
  canonical mechanism** (retrofit old → new) — don't keep both. Precedents: instruments (CL1 hand-authored
  → per-AT generator like CL2/CL3, see [[assessment-run-sheet]]); teaching decks (CL1 per-topic `.py`
  scripts → the generic `build_topic_deck.py` + content-complete `slide_plan.md`, see [[delivery-run-sheet]]).
- A capability the old path had that the canonical one lacks → **add it to the one engine, never fork.**
  The migration is the *completeness test* for the single mechanism (when the last CL1 deck reproduces from
  a `slide_plan.md`, the mechanism is proven complete).
- **Reproduce → validate → adopt:** prove the regenerated artefact reproduces the committed one (e.g.
  `validate-instrument-reproduction`; the deck analogue = compare generic-built vs committed slide text +
  image count) *before* retiring the old path.
- **One source of truth per artefact:** notes live *in* `slide_plan.md` (`notes:`), not a sidecar module;
  content lives in the validated source, not a bespoke script.
- Keep the **engine in the umbrella** (course-agnostic); a course supplies only its data + a thin
  **`brand.py`** seam. The visual/layout pack (`kangan_deck.py`) is the one remaining brand seam — swap it
  per institution, don't fork the engine ([[umbrella-engine-architecture]]).
- **Don't abstract speculatively** — generalise a seam only when a second course/brand actually needs it.

Related: [[umbrella-engine-architecture]], [[assessment-run-sheet]], [[delivery-run-sheet]],
[[memory-principles-not-state]].
