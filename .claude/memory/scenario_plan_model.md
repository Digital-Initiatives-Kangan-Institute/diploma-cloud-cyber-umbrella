---
name: scenario-plan-model
description: The decided architecture for the scenario plan — a two-part artefact (narrative story-bible + forward build checklist) developed AFTER the consolidated assessment plan (not co-developed), and the seam the website is later generated from. Supersedes the earlier "scenario co-developed with the assessment plan" sequencing.
metadata:
  type: project
---

The **scenario plan** has a decided shape and a decided place in the pipeline (agreed 2026-06-22, in
conversation). It is the **seam** between the assessment world and the delivered world: the SR contract flows
*in*, the website flows *out*. Builds on the reverse-mapping discoveries in [[scenario-plan-reverse-mapping]];
the gate tooling is in [[assessment-run-sheet]] (Gate 6).

**Two parts, of different nature:**
- **Part 1 — scenario narrative (story bible):** the fiction — organisation name/type/sector/size/locations,
  the people as characters, the systems, the situation + driver, constraints, tone. **Human-led creative**
  work (AI assists, never auto-generates). Not validated item-by-item against the contract; its only test is
  **viability** — can this world plausibly host every assessment? (a human cross-cluster judgement). It is the
  creative seed Part 2 is written in.
- **Part 2 — forward build checklist:** every artefact to *build* — policy, project doc, template, lab-pack,
  stakeholder role — each with **keynotes** (what it must contain), a **status** (to-build | built |
  carry-over), a target **location**, the **`SR-*`** it satisfies, and the **AT(s)/practice** that consume it.
  **Contract-bound + machine-validated** (every `SR-*` → ≥1 item; `validate-scenario-plan`). Fleshed out using
  Part 1's fiction.
- **Why the split matters for tooling:** the two halves want opposite treatment — Part 1 stays a free creative
  loop (tooling *captures*, never generates); Part 2 has deterministic rails (coverage + contract validation).
  The rails make the human↔AI creative loop faster and stop it silently dropping a requirement.

**Sequencing — now LINEAR, not parallel (this supersedes the old "co-develop scenario with the assessment
plan" rule):** cluster assessment plans → **consolidated** assessment plan (completed) → **scenario plan**
(Part 1 then Part 2, developed *from* the finished contract) → **website build** (a downstream step,
generated from the scenario plan; its timing is flexible — immediate or deferred). The original reason for
parallelism was viability (needing a clear cross-cluster view of what every assessment covers) — **the
consolidated plan now IS that view**, so the scenario is developed from it rather than alongside it. The
run-sheet (process-assessment.md) is updated to match: step 4 = cluster plan only (no co-developed scenario);
a scenario-plan step after consolidation; website build the following step.

**Build-checklist conventions (adopted; revisit if needed):** group items by **target website content-collection**
(policies / reference / ict / projects/`<slug>` / templates / environments / roles) so plan→website generation
is near-mechanical; one format serves built *and* greenfield worlds via the **status** field. `[TBD — confirm:
whether Part 2 should be SEEDED by a stub-per-SR scaffold generated from the consolidated register (coverage
guaranteed by construction) vs hand-authored against it — leaning scaffold.]`

**Gate 7→8 (website realises the scenario plan) — DECIDED 2026-06-22: a read-only AGENT, not a deterministic
script + manifest.** Built the **`verify-scenario-realisation` agent** (`.claude/agents/`): given the scenario
plan's Part 2 + the built website/content repos, it walks **every `SE-NN`** (anchored on the plan, so *missing*
is catchable), maps each item to its real path **live/from-scratch each run** (no stored manifest/`Targets`
field), reports FOUND / NOT-FOUND + a **keynote check** (meets/partial/mismatch), plus orphans + in-world/
consistency breaches. Surfaces only; human fixes; re-run until clean. **Why agent, not a rail:** the other
gates check already-structured data (tags, rows) — pure string ops — but this gate bridges **prose items ↔ a
file tree**; locating which file realises an item and judging keynote-conformance is irreducibly semantic, and
the agent must read everything for keynotes anyway, so a deterministic existence rail would only duplicate the
item→file matching (as a hand-maintained `Targets` list). Rejected alternatives, with reasons: a persistent
**manifest/site-map** (would be redundant machinery the agent has to re-verify anyway; Astro's `@astrojs/sitemap`
also *excludes* `/intranet/`, where the scenario lives); a **`Targets` field + deterministic validator** (the
duplication above). The deterministic rail stays **upstream** where the data is structured —
`validate-scenario-plan` already guarantees plan ↔ contract.
