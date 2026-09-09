---
name: feedback-checks-inform-not-decide
description: Never frame a check/test/tool call as deciding an open question — it yields a data point Tim weighs; the decision stays his
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 77416d00-5307-4727-9ed3-b2c031fdaafd
  modified: 2026-09-09T17:24:04.858Z
---

Never announce a check as the thing that will settle, decide, or be decisive about an open question
("let me check X — that decides it", "this is the deciding factor"). A check produces **a data point**.
That data point is then weighed, along with everything else, in working out how to implement something.
Report what the check found and what it bears on; leave the decision open.

**A finding never blocks the work.** No single check, constraint or failed test means the project — or
even the current approach — cannot proceed. At most it leans us toward one option or rules out one
particular way of doing a thing; the goal is still reachable, and there is room to be creative about
how. Never frame a result as a dead end. The framing is always: *we will check this, and it informs how
we proceed.*

**Why:** it overstates the evidential weight of one lookup and quietly annexes a decision that is Tim's
to make. He is the one who holds the whole picture — constraints, history, preference, cost — and a
single grep or import-graph reading is one input to that, not a verdict. Framing it as decisive also
pre-commits the conversation to whatever the check returns, which forecloses options he may still want.

**How to apply:** say what the check will *tell us*, not what it will settle — "let me check how the
tests import the scripts, that bears on whether filename numbering is viable" rather than "this decides
it". When reporting, give the finding and its implication, then stop; don't append "so it's X". Applies
to constraints too: a hard technical blocker still gets reported as a constraint he weighs, not as a
closed question. Related: [[feedback-scope-stays-where-asked]] (surface, let Tim decide) and
[[feedback-minimal-hedging-live-troubleshooting]] (the opposite failure — this rule is about not
*over*claiming, not about hedging more).
