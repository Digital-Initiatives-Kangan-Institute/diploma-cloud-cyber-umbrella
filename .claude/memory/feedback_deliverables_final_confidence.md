---
name: feedback-deliverables-final-confidence
description: Write deliverable docs at final confidence as if open dependencies were already done; track the dependency in MEMORY, never as an in-text "draft pending X" hedge.
metadata:
  type: feedback
---

**Write deliverables at their intended final confidence — as if their open dependencies were already
done.** Track the outstanding dependency in **MEMORY** (or a worklist `.md`), never as a hedge baked into
the document body (e.g. "draft pending the proving run", "provisional until X"). The only legitimate
readiness marker is a single **document-status field** in doc-control (Draft/Final), and only when the
doc may be consumed by others before a gate — one flag to flip, never prose scattered through the body.

**Why:** an in-text hedge *guarantees* rework — you must revisit the doc just to strip the caveat.
Writing confident means: if the dependency confirms, the doc is already correct (**zero rework**); if it
forces a change, you revisit the *specific* thing anyway, guided by the memory note — the generic hedge
bought nothing and polluted the deliverable in between. (Tim, on the AT3 instruments carrying a "draft
pending the proving run" caveat: don't hedge our bets in the document text and then redo the document to
un-hedge it.)

**How to apply:**
- Author the deliverable as if the dependent jobs are complete; put "verify/finalise after X" in MEMORY.
- Don't confuse with the `[TBD — …]` convention: that is for genuinely *open/unagreed* questions in
  working notes, not for hedging a finished deliverable's readiness.
- This is the forward-looking twin of [[feedback-process-docs-current-only]] (which bans *backward*
  archaeology): a doc carries neither past dead-ends nor future hedges — just the intended state.

Recorded 2026-06-21. See [[memory-principles-not-state]] (track state/deps in memory, keep them out of the artefact).
