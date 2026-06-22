# Scenario-plan format — standard

**Audience:** humans and LLM agents authoring a scenario's scenario plan. Paths are relative to the
`diploma-cloud-cyber-content/` repo root.

A scenario plan (`scenario-plans/<SEMESTER>.md`) is the **seam between the assessment world and the delivered
world**: the assessment contract flows *in*, the website (and lab-packs, templates) is generated *out*. It is
developed **after** the consolidated assessment plan is complete (not in parallel with it) — the consolidated
plan is the cross-cluster view of what every assessment must cover, which is exactly what makes a scenario
*viable*, so the scenario is developed **from** it. There is **one scenario plan per scenario** (the world is
shared across the semester's clusters, never duplicated; see [scenario-flow.md](scenario-flow.md)).

It has **two parts of different nature:**

- **Part 1 — scenario narrative (the story bible).** The fiction: the organisation, the people, the systems,
  the situation and drivers, the constraints, the tone. **Human-led creative** work (AI assists; never
  auto-generated). It is *not* validated item-by-item against the contract — its only test is **viability**:
  can this world plausibly host every assessment? (a human cross-cluster judgement). It is the creative seed
  Part 2 is written in.
- **Part 2 — the forward build checklist.** Every artefact to **build** — policy, project document, template,
  lab-pack, stakeholder role — each with **keynotes** (what it must contain), a **status**, a target
  **location**, the **`SR-*`** it satisfies, and the **assessments/practice tasks** that consume it.
  **Contract-bound and machine-validated.** Fleshed out using Part 1's fiction; it is the basis the website is
  later built from.

The split governs the tooling: Part 1 stays a free creative loop (the format **captures** it, nothing lints
its content beyond presence); Part 2 has deterministic rails — `validate-scenario-plan` confirms the format
and that **every `SR-*` in the consolidated assessment plan is satisfied by ≥1 checklist item**, with no item
claiming a non-existent `SR-*`. The rails make the human↔AI creative loop faster and stop it silently dropping
a requirement. The **quality and coherence** of the world stays the Gate 6→7 human review.

## Conventions

- **Checklist-item IDs** are `SE-NN` — sequential within the one scenario plan. Each is declared once (Part 2)
  and may satisfy any number of `SR-*`.
- **`SR-*` references** use the canonical `SR-<CLUSTER>-NN` ids exactly as they appear in the consolidated
  assessment plan's register; they must appear **unwrapped** (not in backticks) on an item's `Satisfies:` line
  to count.
- **Grouping** — order Part 2's items by **target website content-collection** (`policies` / `reference` /
  `ict` / `projects/<slug>` / `templates` / `environments` / `roles`), so each item maps to a website entry and
  plan→website generation is near-mechanical. Group with `### <collection>` headings; the items themselves are
  `#### SE-NN` blocks.
- **Status** — every item carries `to-build` | `built` | `carry-over`, so one format serves a greenfield
  scenario (items start `to-build`) and a delivered one (items are `built` with real paths).
- **Locations** are prefixed `website:` (the `diploma-cloud-cyber-website` repo — SSOT for in-world content),
  `content:` (this repo: lab-packs, template generators), or `external:` (e.g. AWS Academy). For a `to-build`
  item the location is the **target**; for a `built` item it is the actual path.

## Required sections (in order)

The linter requires these headings and (in Part 2) these per-item fields. Prose within each is free.

1. **Header banner** — title `# <SEMESTER> — Scenario Plan`; a `> **STATUS:** …` line; and an
   **Assessment binding** line naming + linking the consolidated assessment plan
   (`assessment-plans/<SEMESTER>.md`) this scenario satisfies.
2. **`## Part 1 — Scenario narrative`** — the story bible (organisation, people, systems, situation/drivers,
   constraints, tone). Free-form (sub-headings encouraged); **linted for presence only** — this is the
   human-led creative part.
3. **`## Part 2 — Build checklist`** — the artefacts to build, grouped by content-collection (`###` headings),
   each a `#### SE-NN — <name>` block carrying, as labelled fields:
   - **Status:** `to-build` | `built` | `carry-over`;
   - **Location:** the `website:`/`content:`/`external:` target (or actual) path;
   - **Satisfies:** the `SR-*` ids this item provides *(authoritative — the cross-check reads these)*;
   - **Consumed by:** the AT(s) and/or practice tasks that use it;
   - **Keynotes:** what this artefact must contain (the spec the website-build works to).
4. **`## SR coverage`** — the `SR-*` → item rollup + a one-line verification statement. *(A rollup of Part 2's
   `Satisfies:` lines; may be generated. The cross-check's authoritative source is Part 2.)*
5. **`## Open questions / TBDs`** — choices awaiting decision, and delivery gaps where an item is thinner than
   its `SR-*` implies (mark `[TBD — …]`).
6. **`## Changelog`** — dated entries; current-state prose above, history here.

## What makes a good checklist item

For each `SR-*` in the consolidated register, ask: *what artefact in the world provides this, and what must it
contain?* Capture it as an `SE-NN` with **keynotes** that are specific enough to build from. Typical kinds:

- **Environmental / access** — a lab (AWS Academy lab id), a deployable lab-pack, the tooling an AT runs in.
- **Narrative / situational** — a stakeholder role someone can play, a documented procedure, a baseline system
  in a specific state, a constraint document.
- **Artefact / template** — a supplied template, an exemplar document chain, a provided code/IaC appendix.

One item may satisfy several `SR-*`, and one `SR-*` may be satisfied by several items — the cross-check only
requires every `SR-*` to be covered by at least one. An item that satisfies **no** `SR-*` is allowed (pure
world-building — policies for realism, practice-side content) but flagged advisory, so a forgotten binding is
visible.

## Skeleton

```markdown
# S2 — Scenario Plan
> **STATUS: DRAFT.** <one line>
> **Assessment binding:** satisfies the S2 consolidated assessment plan — see
> [assessment-plans/S2.md](../assessment-plans/S2.md). Every SR-* in its register is bound in Part 2.

## Part 1 — Scenario narrative
### Organisation
<name, type, sector, size, locations>
### People
<characters / stakeholder roles>
### Systems
<the systems + their states>
### Situation & drivers
### Constraints
### Tone & conventions

## Part 2 — Build checklist

### Policies
#### SE-01 — <policy name>
- **Status:** to-build
- **Location:** website: src/content/policies/<slug>.md
- **Satisfies:** SR-CLn-NN
- **Consumed by:** CLn ATx (assessment)
- **Keynotes:** <what this document must contain to satisfy the SR + be believable>

### Projects — <engagement slug>
#### SE-02 — <document name>
- **Status:** to-build
- **Location:** website: src/content/projects/<slug>/<doc>.md
- **Satisfies:** SR-CLn-NN
- **Consumed by:** CLn ATx (assessment); CLm practice
- **Keynotes:** …

## SR coverage
SR-CLn-NN → SE-01; … Verification: every SR-* in assessment-plans/S2.md is satisfied by ≥1 item.

## Open questions / TBDs
## Changelog
```

## See also

- [process-assessment.md](process-assessment.md) — the run-sheet; the cluster plans (step 4) consolidate into
  the contract (step 5); the **scenario plan** is developed from that contract (step 6); the **website** is
  built from the scenario plan (step 7). The scenario cross-check is the scenario-plan step's machine condition.
- [assessment-plan-format.md](assessment-plan-format.md) — defines the `SR-*` register this plan satisfies.
- [scenario-flow.md](scenario-flow.md) — the durable cross-cluster world model Part 1 instantiates.
- [website-architecture.md](website-architecture.md) — the content model Part 2's items are grouped by and the
  website-build targets.
