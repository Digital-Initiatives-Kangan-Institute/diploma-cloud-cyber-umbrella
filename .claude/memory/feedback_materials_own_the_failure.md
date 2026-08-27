---
name: feedback-materials-own-the-failure
description: "If someone with the run sheet and lab pack in front of them struggles mechanically, the cause is the pack or the instructions — never the person"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a40bd230-c889-45bf-97c8-0b1ee173f18b
  modified: 2026-08-27T19:09:00.091Z
---

If a person working through a task **with the run sheet in front of them and the lab pack
provided** gets stuck, the cause is one of exactly two things:

1. **A defect in the lab pack** — the environment does something the materials do not expect.
2. **Not enough detail in the instructions** — including detail that has gone stale, and
   warnings that were never there.

Never "the student should have known". The materials own the failure. Both causes can be true
at once: an ASG health-check grace period too short for a Windows boot was a pack defect *and*
the missing "Unhealthy for several minutes is normal, do not intervene" was missing detail.

**The boundary, and it matters — this applies to the MECHANICAL path only.** Deploying,
navigating a console, building to a spec, knowing how long to wait. It does **not** apply to
the assessed judgement. A student who cannot identify the single points of failure is not
short of detail; that is `[ICTCLD502 PC 2.2]` doing its job.

The line is the same one `Satisfactory when` draws — see
[[feedback-mark-uoc-intent-not-invented-settings]]. Anything not load-bearing for a UoC item
can be spelled out as far as it takes. Anything that IS load-bearing gets a leading question at
most, and only in the practice sheet, never the answer.

**How to apply:** the human walk-through is the test — every stumble is a defect to fix, not a
note about the person. Triage it into pack or detail, fix it in the generator, rebuild. Aim for
instructions detailed enough that nobody ever has to start over, because a restart is usually a
student "fixing" something that was working.
