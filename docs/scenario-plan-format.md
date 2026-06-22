# Scenario-plan format — standard

**Audience:** humans and LLM agents authoring a scenario's scenario plan. Paths are relative to the
`diploma-cloud-cyber-content/` repo root.

A scenario plan (`scenario-plans/<SEMESTER>.md`) is the **authored** bridge between the assessment
contract and the in-world world: it maps every `SR-*` in the scenario's **consolidated assessment plan**
(`assessment-plans/<SEMESTER>.md`) to the concrete **scenario element** that provides it. There is **one
scenario plan per scenario** (a scenario spans all the semester's clusters — the world is shared, never
duplicated per cluster; see [scenario-flow.md](scenario-flow.md)).

It is the counterpart of the consolidated assessment plan: that doc is **derived** (the cross-cluster
`SR-*` contract); this doc is **authored** (the world that satisfies it). The scenario *materials*
themselves are single-sourced on the website (see [website-architecture.md](website-architecture.md)); the
scenario plan does not duplicate them — it **names** each element and points at where it lives.

This standard fixes the plan's structure so one check can run against it:

- **`validate-scenario-plan` (linter + cross-check — deterministic):** the required sections/fields are
  present and well-formed (FORMAT), **and** every `SR-*` in the consolidated assessment plan is satisfied by
  at least one scenario element, with no element claiming a non-existent `SR-*` (CROSS-CHECK, bidirectional).

The **quality and coherence** of the world — whether it reads as a believable place with no leakage between
clusters — stays a human call (the Gate 6→7 human review). The cross-check only proves the contract is
mechanically covered.

## Conventions

- **Scenario-element IDs** are `SE-NN` — sequential within the one scenario plan (e.g. `SE-01`). Each is
  declared once in the elements section (§3) and may satisfy any number of `SR-*`.
- **Scenario-requirement references** use the canonical `SR-<CLUSTER>-NN` ids exactly as they appear in the
  consolidated assessment plan's register (e.g. `SR-CL2-03`). They must appear **unwrapped** (not inside
  backticks) on an element's `Satisfies:` line to count.
- **Element locations** reference scenario content the way the relevant audience consumes it — abstractly
  for student-facing material ("the YAT intranet's ICT Strategic Plan page"), and by the concrete asset
  (lab id, template name, lab-pack) where that is the element. Never leak course/assessment meta-language
  into element *descriptions* that quote in-world content (the in-world rule still applies to what the
  scenario says); the plan itself is an authoring doc and may name clusters/ATs in its structure.

## Required sections (in order)

The linter requires these headings and their key fields. Prose within each is free.

1. **Header banner** — title `# <SEMESTER> — Scenario Plan`; a `> **STATUS:** …` line; and a
   **Assessment binding** line naming the consolidated assessment plan this scenario satisfies and linking
   it (`assessment-plans/<SEMESTER>.md`).
2. **`## 1. World overview`** — the shared world this scenario instantiates (the organisation, the systems
   and their state progressions, the cluster framing). Narrative; references [scenario-flow.md](scenario-flow.md)
   rather than restating the durable model.
3. **`## 2. Scenario elements`** — the element table, then **per element** a `### SE-NN — <name>` block
   carrying, as labelled fields:
   - **Kind** — environmental/access · narrative/situational · artefact/template (free text);
   - **Location:** where the element is single-sourced (website page/collection, lab id, lab-pack path,
     template name) — the pointer, not a copy;
   - **Satisfies:** the `SR-*` ids this element provides *(authoritative — the cross-check reads these)*.
4. **`## 3. SR coverage`** — the human-readable proof that every contract requirement is met: the
   `SR-*` → element rollup and a one-line verification statement. *(A rollup view of §2's `Satisfies:`
   lines; may be generated. The cross-check's authoritative source is §2.)*
5. **`## 4. Open questions / TBDs`** — choices awaiting decision (mark `[TBD — …]`).
6. **`## Changelog`** — dated entries; current-state prose above, history here.

## What makes a good element

For each `SR-*` in the consolidated register, ask: *what real thing in the world provides this?* Capture it
as an `SE-NN` and bind it. Typical kinds:

- **Environmental / access** — a lab (AWS Academy lab id), a deployable lab-pack, the tooling an AT runs in.
  These usually satisfy the `SR-*` whose AC link names the unit's environment Assessment Conditions.
- **Narrative / situational** — a stakeholder role someone can play, a documented procedure on the intranet,
  a baseline system in a specific state, a constraint document. These satisfy the narrative `SR-*` (no AC).
- **Artefact / template** — a supplied template, an exemplar document chain, a provided code/IaC appendix.

One element may satisfy several `SR-*`, and one `SR-*` may be satisfied by several elements — the cross-check
only requires every `SR-*` to be covered by at least one. An element that satisfies **no** `SR-*` is allowed
(pure world-building) but flagged advisory, so a forgotten binding is visible.

## Skeleton

```markdown
# S1 — Scenario Plan
> **STATUS: DRAFT.** <one line>
> **Assessment binding:** satisfies the S1 consolidated assessment plan — see
> [assessment-plans/S1.md](../assessment-plans/S1.md). Every SR-* in its register is bound below.

## 1. World overview
<the organisation; the systems + state progressions; cluster framing — references scenario-flow.md>

## 2. Scenario elements
| SE | Element | Kind | Satisfies |
|----|---|---|---|
| SE-01 | AWS Academy lab environment | environmental | SR-CL1-01, SR-CL2-01, SR-CL3-01 |

### SE-01 — AWS Academy lab environment
- **Kind:** environmental / access
- **Location:** AWS Academy — Cloud Foundations [104469] + Cloud Architecting [172221]
- **Satisfies:** SR-CL1-01 · SR-CL2-01 · SR-CL3-01

## 3. SR coverage
SR-CL1-01 → SE-01; … Verification: every SR-* in assessment-plans/S1.md is satisfied by ≥1 element.

## 4. Open questions / TBDs
## Changelog
```

## See also

- [process-assessment.md](process-assessment.md) — the run-sheet; step 4 designs the scenario (and declares
  the `SR-*`), step 5 consolidates them into the contract, step 6 authors the scenario materials this plan
  maps; the scenario cross-check is Gate 6→7's machine condition.
- [assessment-plan-format.md](assessment-plan-format.md) — defines the `SR-*` register this plan satisfies.
- [scenario-flow.md](scenario-flow.md) — the durable cross-cluster world model the plan instantiates.
- [website-architecture.md](website-architecture.md) — where the scenario materials are single-sourced.
```
