---
name: feedback-finalised-assessments-change-control
description: "Once a cluster's assessments pass institutional review they are FINALISED/frozen — never edit the approved file again; any change goes to a NEW file with the new version (v1.2/v2.0) in its name, version shown in the document footer. Warn the user first."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5fe40dfd-42a4-49d7-8e7d-5da57c8df524
---

Once a cluster's assessments have **passed the institutional review / pre-validation** step (the
terminal human gate of the assessment run-sheet — see [[assessment-run-sheet]]), those instruments are
**FINALISED and frozen**. They have been formally approved for delivery; the approved file is the
baseline of record and must not be altered.

**The change-control model (as set by the user):**
- **The version number lives in the document footer.** The approved baseline is its current version
  (e.g. v1.0).
- **The current/approved file is never changed again.** Do not edit it in place.
- **Any change is made on a SEPARATE, NEW file** whose **filename carries the new version** — `…v1.2…`
  for a minor change, `…v2.0…` for a major one — and whose **footer version is bumped to match**. The
  old approved file stays exactly as it was, so the approved baseline and every superseding revision are
  all distinguishable and retained.
- **Warn the user first.** Before creating a revision, stop and tell them the artefact is
  finalised/approved, name the change and why, and get explicit go-ahead. Never revise as a matter of
  course — not even a "quick fix".

**Why:** institutional review is the last gate; passing it means "approved, deliver this exact copy."
Superseding via a new versioned file (rather than editing in place) keeps the approved baseline intact
and makes every revision auditable at a glance.

**How to apply:** treat a cluster's `[[s1cl1-assessment]]`-style entry as the source of truth for
whether it's finalised. If it is, any request that would touch its instruments triggers the warn →
new-versioned-file → footer-bump flow above. First instance: **S1-CL1 (finalised 2026-07-10)**.

Related: [[one-course-agnostic-mechanism]] (generators are the intended edit locus for LIVE artefacts —
but a finalised, approved copy is frozen; a superseding revision is a new file, and its generator/source
relationship is a deliberate decision, never a silent regenerate over an approved copy),
[[feedback-suggest-commits]].
