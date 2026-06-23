---
name: scenario-plan-reverse-mapping
description: The S1 scenario plan is reverse-engineered from the DELIVERED world (not paraphrased from the SR contract); the durable structural discoveries from that mapping, and the OPEN question on the right way to build scenario plans out in future (user paused here to explore deliberately).
metadata:
  type: project
---

`scenario-plans/S1.md` is now **reverse-engineered from the delivered S1 world** — each element grounded in a
real artefact with its concrete location — superseding the first cut, which was **circular** (it paraphrased
the consolidated `SR-*` register, so of course the cross-check passed). The point of reverse-engineering: make
the cross-check *mean something* (does the world that exists actually back the contract?) and surface where it
doesn't. See [[assessment-run-sheet]] (Gate 6) and [[mapping-pipeline]] (same derived-artefact discipline).

**Durable structural discoveries (the non-obvious WHY for next time):**
- **The delivered scenario spans two repos.** The **website** is the single source of truth for in-world
  content — intranet ICT docs, engagement packs under `src/content/projects/<slug>/`, `policies/`,
  `reference/`, downloadables in `public/templates` + `public/documents`. The **content repo** holds the
  lab-packs (`<AT>/lab-pack/`), the template **generators** (`scripts/templates/`; output is generated, not
  committed), and the AT instruments that reference it all. A scenario element's `Location:` therefore needs a
  `website:` / `content:` / `external:` prefix to be unambiguous.
- **Real artefacts satisfy MULTIPLE `SR-*`** — one engagement role-brief gives both stakeholders *and* team
  structure; one engagement pack gives requirements *and* the artefact thread. So a faithful scenario plan
  groups elements **by delivered artefact**, not one-element-per-SR (contrast the assessment plan, whose
  coverage is per-AT). The first draft's one-SE-per-SR shape was an artefact of paraphrasing, not the world.
- **Stakeholders are recurring roles**, not per-AT props: **Sam Walker (YAT ICT Manager)** is the persistent
  acceptance authority across every engagement, **Pat Lin** the MTS lead — so one stakeholder element
  satisfies the sign-off `SR-*` in all three clusters.
- **Practice-side content is real but unbound** — the CL2 LMS practice engagement, the AccentLoitte 2022
  exemplar, the governance policy suite, the reference library are all delivered world-building with no
  assessment `SR-*`. They belong in the plan as **advisory** elements; the validator's "satisfies no SR-*
  [info]" flag is the intended visibility for that, not an error.
- **The mapping found 5 delivery gaps** where the world is thinner than the contract (web-app payload vs
  infra-only; CL2 AT2 IaC/microservice/webhook artefacts referenced-but-not-single-sourced; no standalone DR
  risk register; no explicit AT3 assessor "combined" fallback template; IR-1..7 in the SR vs IR-1..5
  delivered). These are captured **in `scenario-plans/S1.md` §4** as TBDs — don't duplicate them here. The
  cross-check still PASSES (each SR is *mechanically* satisfied by ≥1 element); the gaps are for the Gate 6→7
  **human** review.

**RESOLVED → see [[scenario-plan-model]].** The structure question raised here is now decided: the scenario
plan is a two-part artefact (narrative story-bible + forward build checklist), developed **after** the
consolidated assessment plan, and the website is generated **from** it (forward), not reverse-mapped from an
existing website. This reverse-mapped S1 was the diagnostic that proved the model; S1's checklist items are
real/`built` and keep their concrete locations, but new scenarios author the checklist forward (`to-build`).

**Gate 7→8 proven on S1 (2026-06-22).** The `verify-scenario-realisation` agent (see [[scenario-plan-model]])
ran against S1's built website/repos: all 23 items realised. It retired one stale gap (SE-13) and
confirmed/refined the rest. **The whole worklist is now CLOSED (2026-06-22)** — durable lesson below.

**Worklist outcome — three of four "gaps" were SPEC mis-statements, not missing artefacts.** The
verification correctly surfaced mismatches; investigation each time drove the world+contract to a consistent
state (usually by fixing the *SR wording*, occasionally the build):
- **SE-05** (CL1 web-app payload) — *false positive*: the CL1 LMS app is **out of scope** (YAT in-house); the
  lab-pack placeholder is the deliberate deliverable. Reworded SR-CL1-05; added the **lab-pack acceptance
  criterion** to `docs/lab-pack-standard.md` + the verify agent (a lab-pack = a deployable, Academy-proven
  *pack*, never a live deployment; provided-to-work-from artefacts are not a lab-pack either).
- **SE-10** (CL2 AT2 appendices) — *spec mis-statement*: inline-by-design (no lab-pack) because **authoring the
  deploy YAML is the assessed skill** (ICTCLD505) and the data-store template is **deliberately faulty**.
  Reworded SR-CL2-04.
- **SE-11** (CL2 DR risk register) — *spec mis-statement*: AC 1 "data to assess risk events" = provided
  environment data; AC 3 "reporting standard" = the **DR Plan template**; the **risk register is
  student-authored**. Reworded SR-CL2-06.
- **SE-16** (CL3 AT3 fallback) — *part mapping-error, part one real fix*: the fallback artefact existed
  (lab-pack `improved.yaml`); the genuine fix was the **AT3 assessor generator** now naming the fallback path
  (edit the *generator*, not the docx, then regenerate).
- **`website-improvement`** (CL3 practice) — **kept + refreshed** (no-leakage requires a CL3 website practice
  vehicle): realigned to the current `ledgerline-improvement` framing (Solution Design, IR-1…7, Phase 1/2),
  website differentiation preserved, website `solution-design.md` authored; bound as advisory **SE-24**.
  Practice vehicles are maintained under the **delivery** run-sheet, not the assessment one.

**Open follow-up (minor):** the downloadable branded `YAT-Website-Improved-Solution-Design` asset isn't
generated (no `scripts/scenario/` builder yet) — the in-world page stands alone; a delivery-side parity task.
