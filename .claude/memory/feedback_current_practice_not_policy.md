---
name: feedback-current-practice-not-policy
description: "Never write things up as decided/locked/policy — everything here is the current practice, open to evolution; the sole exception is an external constraint we have no capability to change"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3282db21-77b8-4c8c-8477-2f354b43b279
  modified: 2026-09-09T17:23:56.924Z
---

**Everything recorded here is the current practice, not policy.** Processes, conventions, standards
and design choices are what we do *now* and stay open to change the moment a better path appears.
Write them that way.

The **sole exception** is a constraint we have **no capability to change** — the Learner Lab refusing
IAM creation, CloudFormation rejecting a non-ASCII description. State those firmly, because softening
a wall misleads. Externally imposed is not enough on its own: an outside constraint we could negotiate
or work around is still current practice.

**Why:** a thing written as settled stops getting questioned. Locking language turns a working
approach into something the next session defends instead of improves, and the work gets contorted to
protect a rule that was only ever a preference.

**The concrete harm — this is the failure mode that matters.** Tim brings ideas for improving how the
work is done. When a doc says "this is how we do it", a later session **quotes that documentation back
at him as grounds for not considering the idea** — effectively "it is written that we do it this way,
so we cannot do yours". That is the whole cost: locking language written today becomes a refusal to
think tomorrow, aimed at the person best placed to improve the process. Nothing here is ever grounds
for declining an idea. Documentation records how we currently understand the job and currently
approach it; new understanding, new methods and new tooling are always possible, and the docs must be
written so they invite that rather than block it.

**How to apply:**
- Don't write **DECIDED**, **LOCKED**, **canonical**, **policy**, **the rule**, **invariant**,
  **never**, **must** for anything we chose ourselves.
- Write "the current approach", "what we do now", "the ambition is…". Where something is worth
  protecting, state it as an **ambition** (we prefer X wherever it is free), not a prohibition.
- Record a change as the new current practice — not as a decision that superseded an old one. The
  old one is simply gone. See [[feedback-process-docs-current-only]].
- Never record anything as *decided / agreed / canonical* unless it was actively discussed **and**
  explicitly approved; flag what is open with `[TBD — needs discussion: <what is open>]`.
- A thing tried **once** is not a convention. Say it is being trialled, name where it has been tried,
  and do not propagate it — a shape copied to seventeen places before it has settled is expensive to
  change, which is itself a reason it stops changing.
- When Tim proposes a change to something already written down, treat the existing doc as **context,
  never as an objection**. Weigh the idea on its merits; if the doc bears on it, say what it says and
  why it was written that way, then keep considering.
