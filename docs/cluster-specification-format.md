# Cluster-specification format — standard

**Audience:** humans and LLM agents producing a cluster's **delivery frame** — the first step of the
[delivery run-sheet](process-delivery.md). Paths are relative to the `diploma-cloud-cyber-content/`
repo root.

A cluster's **specification** (`<cluster>/cluster-specification.md`) is the agreed **delivery frame**:
how many hours the cluster is funded for, over how many weeks and sessions, the session length that
falls out of that, the schedule conventions (onboarding, spare buffer, assessment placement), and the
**topic budget** that starting point implies. It is the box every later delivery step has to fit the
teaching into. It is **one per cluster**, sits at the cluster root (sibling of `consolidated_uoc.md`),
and is the input to Step 2 (topic breakdown).

**This document is the single source of truth — for what the spec contains *and* for what the validator
checks.** It informs the producing skill and is an **input to validation**: the linter reads its
[skeleton](#skeleton) (below) to learn the required headings and fields rather than hard-coding them, so
changing the skeleton changes the contract everywhere at once. Three layers run on the spec, in order:

- **`setup-cluster-spec` (elicitation — main session):** the guided conversation that *produces* the
  file — the main session asks the human the frame questions (with defaults), does the arithmetic, and
  writes the spec **to this format**. It is **not** a sub-agent: producing the spec is an interactive
  human dialogue, which only the main session can do.
- **`validate-cluster-spec` (linter — deterministic):** the structural gate — every heading and field
  **named in the skeleton** is present and non-empty, the **arithmetic reconciles** (sessions, hours,
  variance, topic budget), and any over-nominal hours carry a recorded authorisation. Driven by this
  doc; no field list of its own.
- **(agent validator — judgment, where warranted):** anything *beyond* "the field exists and the numbers
  add up" — coherence and soundness calls a deterministic check can't make. For this step the residual
  judgment is the human's acceptance call (is the variance acceptable, is the topic count sensible), so
  there is **no agent validator yet**; the layer is named here because later delivery steps (topic
  breakdown, coverage, decks) carry real semantic judgment and will use it.

**Phase gate (leaving cluster-definition).** Step 1's gate is **semester-level**, not per-cluster: the
definition phase is complete — and the delivery run-sheet may proceed to Step 2 (topic breakdown) — only
when **every** cluster being developed has a `cluster-specification.md` that **passes**
`validate-cluster-spec`, **and** the **human has agreed to proceed**.

## The elicitation (how the spec is produced)

The frame is **agreed with the human, not assumed.** When setting a cluster up, the main session works
through the questions below, **offering the default** each time and recording the human's answer. Ask
them roughly in this order (later answers depend on earlier ones):

1. **Nominal hours** — how many funded/nominal delivery hours is this cluster? *(no default — institutional)*
2. **Weeks** — over how many weeks is it delivered, and where in the semester (solo, or in parallel with
   another cluster)? *(no default — institutional)*
3. **Sessions per week** — how many class sessions per week? *(no default — institutional)*
4. **Session length** — *derived* as `nominal ÷ (weeks × sessions/week)`, then **rounded to a practical
   block** (whole or half hours). Offer the rounded length; the rounding is what creates variance.
5. **Onboarding session** — *"Do you want the first session to be orientation/setup (systems, access,
   scenario intro) with no teaching?"* **Default: yes.**
6. **Spare buffer** — *"Do you want the last session, or the last day, kept spare so students who are
   behind can catch up or resit?"* **Default: yes — the final day.**
7. **Final-assessment placement** — *"Should the final assessment complete immediately before the spare
   buffer (so the buffer is genuinely free)?"* **Default: yes.**
8. **Session pairing / rhythm** — how do sessions sit in the week (e.g. AM/PM pairs, N teaching
   days/week)? *(no default — per cluster)*
9. **Budget tolerance** — *"The rounded session length rarely hits nominal exactly. Do you want to run
   **under** nominal, or are you willing to **authorise** going a few hours **over** if it makes the
   weeks fit cleanly? If over, how many hours, and on whose authority?"* **Default: run at or under
   nominal.** A recorded over-nominal authorisation is what lets the linter pass an over-budget frame.

Once the answers are in, compute the frame and the topic budget (below), write the file, and run
`validate-cluster-spec`. The questions' *answers* are a human call; the linter only checks they are
present and the numbers reconcile.

## Required sections (in order)

This is the human-readable description; the **[skeleton](#skeleton) is the authoritative machine-readable
contract** the linter parses. The headings and their labelled `- Field: value` lines are required (prose
may surround them).

1. **Header banner** — title `# <cluster> — Cluster Specification`; a `> **STATUS:** …` line naming the
   semester and the cluster's units.
2. **`## 1. Delivery frame`** — the numbers, as labelled fields:
   - `Nominal hours:` · `Weeks:` · `Sessions per week:` · `Session length (hours):`
   - `Total sessions:` *(= weeks × sessions/week)*
   - `Delivered hours:` *(= total sessions × session length)*
   - `Variance (nominal − delivered):` *(signed; `+` = under-delivers / unused budget)*
   - `Over-nominal authorisation:` *(`n/a` when at/under nominal; otherwise `<who>, <date>, +<N>h —
     <reason>`)*
   - `Sequencing:` *(which weeks; solo or parallel-with)*
3. **`## 2. Schedule conventions`** — the elicited answers, as labelled fields (presence checked, truth
   is the human's): `Onboarding session:` · `Spare/catch-up buffer:` · `Final-assessment placement:` ·
   `Session rhythm:`.
4. **`## 3. Topic budget`** — the derived starting point, as labelled fields:
   - `Onboarding sessions:` · `Spare sessions:` · `Dedicated assessment sessions:`
   - `Teaching/practice sessions available:` *(= total − the three reserved counts)*
   - `Nominal topic count:` *(the human's starting estimate of how many Topics to break the ATs into)*
5. **`## 4. Open questions / TBDs`** — anything unresolved (`[TBD — …]`).
6. **`## Changelog`** — dated entries; current-state prose above, history here.

## What the linter checks

`validate-cluster-spec` is deterministic and stdlib-only. **It reads this document's
[skeleton](#skeleton) to learn the contract** (the `## …` headings and the `- Label:` field names),
then against a spec it:

- confirms every heading and field **named in the skeleton** is **present and non-empty**;
- reconciles the **frame arithmetic**: `total sessions = weeks × sessions/week`;
  `delivered hours = total sessions × session length`; `variance = nominal − delivered`;
- reconciles the **topic budget**: `onboarding + spare + dedicated-assessment + teaching/practice
  available = total sessions`;
- applies the **over-nominal rule**: if `delivered > nominal` and `Over-nominal authorisation` is `n/a`
  / empty, it **fails** (over budget without sign-off); with an authorisation recorded, it **passes**
  and reports the overage;
- **reports** the variance (and any overage) either way — variance itself is never a failure, it is a
  human acceptance call.

It does **not** judge whether the conventions or the topic count are *right* — that is the human half of
the gate. Exit `0` on PASS, `1` otherwise.

## Skeleton

```markdown
# S1-CLn <Cluster Name> — Cluster Specification
> **STATUS: AGREED <date>.** Semester S1 · Units: <UNIT>, <UNIT>, <UNIT>

## 1. Delivery frame
- Nominal hours: 104
- Weeks: 8
- Sessions per week: 4
- Session length (hours): 3
- Total sessions: 32
- Delivered hours: 96
- Variance (nominal − delivered): +8
- Over-nominal authorisation: n/a
- Sequencing: weeks 1–8; delivered solo (before CL2 + CL3)

## 2. Schedule conventions
- Onboarding session: yes — S1 (orientation, systems/access setup, scenario intro; no teaching)
- Spare/catch-up buffer: yes — the final day (last 2 sessions): resits + overflow
- Final-assessment placement: completes immediately before the spare buffer
- Session rhythm: AM/PM pairs, 2 teaching days/week

## 3. Topic budget
- Onboarding sessions: 1
- Spare sessions: 2
- Dedicated assessment sessions: 2
- Teaching/practice sessions available: 27
- Nominal topic count: 14

## 4. Open questions / TBDs

## Changelog
- <date> — initial frame agreed.
```

## See also

- [process-delivery.md](process-delivery.md) — the delivery run-sheet; this spec is **Step 1**, the
  frame every later step fits into.
- [process-assessment.md](process-assessment.md) — the sister run-sheet; this spec consumes its outputs
  (the ATs / assessment plan tell you the assessment points the budget must reserve sessions for).
