---
name: feedback-finalised-assessments-change-control
description: "Assessment instruments freeze per delivery cycle, not forever: institutional review PASS freezes them FOR that delivery; once delivered they REOPEN for a feedback-driven improvement pass (edit the generators in place); the next human review re-freezes them for the next intake."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5fe40dfd-42a4-49d7-8e7d-5da57c8df524
  modified: 2026-08-26T14:47:54.725Z
---

A cluster's assessment instruments are frozen **per delivery cycle**, not permanently. The freeze is
what institutional review buys: approval to deliver *that exact copy* to *that intake*. Delivering it
spends the approval.

**The cycle:**

1. **Authored** — instruments live; the generators are the edit locus ([[one-course-agnostic-mechanism]]).
2. **Institutional review / pre-validation PASS** — the terminal human gate of the assessment run-sheet
   ([[assessment-run-sheet]]). Instruments are **frozen for that delivery**: don't edit them in the
   run-up to or during the intake they were approved for.
3. **Delivered** — the approval has served its purpose. Student and staff feedback now exists.
4. **Improvement pass — instruments are OPEN.** Feedback drives an iterative-improvement review; changes
   are made **in place, in the generators**, and regenerated. No new versioned file, no fork.
5. **Human review again** before the next intake uses them → back to frozen for that delivery.

**How to tell which phase you're in:** the cluster's `[[s1cl1-assessment]]`-style entry. "Review PASSED,
not yet delivered" = frozen, warn before touching. "Delivered, improvement pass under way" = open, edit
the generators normally.

**Why in-place rather than a versioned fork:** the generator is the single source of truth for the
instrument, and forking generators forks the mechanism — the thing we most want to avoid
([[one-course-agnostic-mechanism]]). Git holds every superseded version, so the audit trail is intact
without parallel `…v1.2…` files.

**How to apply:** when a request would change a frozen (approved-but-not-yet-delivered) instrument, stop
and say so before doing anything — name the change and get explicit go-ahead. When the cluster is in an
improvement pass, that warning is noise; just do the work. Either way, never regenerate an instrument
silently as a side effect of other work ([[feedback-verify-change-impact]], [[feedback-suggest-commits]]).

**Current state:** S1-CL1 reviewed 2026-07-10, **delivered**, and now in a feedback-driven improvement
pass — **open**.
