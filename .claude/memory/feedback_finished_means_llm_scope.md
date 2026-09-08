---
name: feedback-finished-means-llm-scope
description: "\"Are you finished?\" means finished with what CAN be done in the LLM part — answer yes/no on that scope, then name the outside-the-LLM work separately."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4b2014d2-b066-43a7-bccf-fb8f1c68cafb
  modified: 2026-09-08T20:40:26.969Z
---

When Tim asks **"are you finished?"** he is asking whether the work that **can** be done in the
LLM part is done — not whether the whole thing is signed off. If the machine-checkable work is
complete, the answer is **"Yes, finished"**, then a short list of what remains outside the LLM
part (his review, a lab run, an institutional gate).

**Why:** answering "no, because a human hasn't reviewed it" reads as the work being incomplete
when it is not, and it buries the actual status under hedging. He asked twice in one session
before naming the rule. Human review and live-console verification were never mine to do, so
they were never reasons to withhold "finished".

**How to apply:** answer the scope asked. "Yes — finished. Outside the LLM part: X, Y." Do not
lead with the caveat, do not pad. The one thing that DOES make the answer "no" is an
LLM-doable check not yet run — so run it before answering rather than listing it as
outstanding (see [[feedback-verify-change-impact]]). Distinguish honestly between "I could do
this and haven't" (not finished) and "this needs a human or a live system" (finished).

Related: [[feedback-minimal-hedging-live-troubleshooting]] — same instinct, different setting.
