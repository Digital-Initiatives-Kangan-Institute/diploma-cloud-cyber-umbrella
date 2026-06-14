---
name: memory-principles-not-state
description: Memory holds durable principles/decisions/rationale (the non-derivable WHY); NOT repo-derivable ephemeral state (file lists, paths, commit hashes, "what's built" snapshots) which goes stale the instant the repo moves
metadata:
  type: feedback
---

Record the **immutable** — principles, decisions, and the rationale behind them (the *why*; the things not recoverable from the repo). Do **not** record **ephemeral, repo-derivable state**: file inventories, folder paths, commit hashes, "AT-X is built with these files / validation green / committed at Y" snapshots. That state already lives authoritatively in the repo + git; copying it into memory creates a second source of truth that **goes stale almost as soon as it's written** — the next refactor silently invalidates it.

**Why:** Tim 2026-06-09 — diagnosed after a memory entry confidently claimed a lab-pack existed at a path when it had been deleted during the LMS→website reframe. The record was a stale snapshot, not a decision. Ephemeral records rot on creation; principles don't.

**How to apply:**
- Before writing a memory line, ask: *"is this recoverable from the repo / git / filesystem?"* If yes → don't record it. Record the **decision or principle** behind it, and if a reader needs the state, **point to where it actually lives** (a repo path, doc, or command) rather than pasting a snapshot.
- **Capture:** design decisions and reframes, rationale ("why X over Y"), conventions, constraints, scenario/vehicle choices, open questions only Tim can settle.
- **Don't capture:** what's built, where files sit, what's committed, validation results, "done" status — observations of a moving target.
- When a snapshot has served its purpose (e.g. proving a capability), record the **conclusion** and delete the artefact — don't keep it "just in case".
- Extends [[feedback-process-docs-current-only]]: that says record current-state-not-history; this says don't record *ephemeral/derivable* state at all — only durable decisions and pointers.
