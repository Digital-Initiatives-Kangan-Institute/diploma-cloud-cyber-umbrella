---
name: setup-cluster-spec
version: 1.0.0
updated: 2026-06-23
model: claude-opus-4-8
description: >-
  This skill should be used to PRODUCE a cluster's delivery frame — e.g. "set up the cluster
  specification", "let's define the delivery frame for CL2", "start the delivery planning for this
  cluster", or at the start of the delivery run-sheet for any cluster. It runs the guided conversation
  that fills in cluster-specification.md: the main session asks the human the frame questions (nominal
  hours, weeks, sessions, session length, schedule conventions, budget tolerance) with sensible
  defaults, does the arithmetic, records any over-nominal authorisation, writes the spec to the format
  standard, and runs validate-cluster-spec. It is Step 1 of the delivery run-sheet. Run it once per
  cluster. It is NOT a sub-agent — producing the spec is an interactive human dialogue, so the MAIN
  session runs it (a sub-agent cannot ask the human questions turn by turn).
---

# Set up a cluster specification (delivery frame)

The cluster specification (`<cluster>/cluster-specification.md`) is the agreed delivery frame — the box
the teaching is fitted into — and the first step of the delivery run-sheet. This skill is the **guided
conversation that produces it**: the frame is *agreed with the human, not assumed*.

The authoritative content + field contract is
[cluster-specification-format.md](../../../docs/cluster-specification-format.md). This skill is the
*how* (the conversation); that doc is the *what* (the fields).

## This runs in the MAIN session

Producing the spec is an **interactive dialogue** — you ask the human a question, they answer, the next
question depends on the answer. A sub-agent can't do that (it runs autonomously and returns a result).
So the **main session** runs this skill, using `AskUserQuestion` to put the choices to the human.

## The conversation (ask in order; offer the default each time)

Work through the format doc's elicitation questions, recording each answer. In order:

1. **Nominal hours** — the funded/nominal delivery hours for this cluster. *(institutional; no default)*
2. **Weeks + placement** — over how many weeks, and where in the semester (solo, or parallel with
   another cluster). *(no default)*
3. **Sessions per week.** *(no default)*
4. **Session length** — compute `nominal ÷ (weeks × sessions/week)`, then propose a **practical rounded
   block** (whole/half hours). The rounding is what creates the variance; surface the resulting variance
   as you propose it.
5. **Onboarding session?** — first session = orientation/setup, no teaching. *Default: yes.*
6. **Spare/catch-up buffer?** — keep the final session/day spare for catch-up + resits. *Default: yes,
   the final day.*
7. **Final-assessment placement?** — final assessment completes immediately before the spare buffer.
   *Default: yes.*
8. **Session rhythm** — how sessions sit in the week (e.g. AM/PM pairs, N teaching days/week).
   *(per cluster; no default)*
9. **Budget tolerance** — run **at/under** nominal, or **authorise going over**? If over: how many
   hours, and on whose authority (this is the authorisation the linter requires for an over-nominal
   frame). *Default: at/under nominal.*

## Then

1. **Compute the frame + topic budget:** total sessions = weeks × sessions/week; delivered hours =
   total × length; variance = nominal − delivered. Reserve onboarding/spare/dedicated-assessment
   sessions; teaching/practice available = total − those. Propose a starting **nominal topic count**.
2. **Write** `<cluster>/cluster-specification.md` to the format standard (use its skeleton).
3. **Validate:** run `validate-cluster-spec --cluster <cluster>` and fix any reconciliation error.

## The phase gate (leaving cluster-definition)

Step 1's gate is **semester-level**, not per-cluster: the cluster-definition phase is complete — and the
delivery run-sheet may move to Step 2 (topic breakdown) — only when

1. **every** cluster being developed has a `cluster-specification.md` that **passes**
   `validate-cluster-spec`, **and**
2. the **human has agreed to proceed**.

Run this skill once per cluster; do not leave the definition phase until all clusters' frames are locked
and signed off.
