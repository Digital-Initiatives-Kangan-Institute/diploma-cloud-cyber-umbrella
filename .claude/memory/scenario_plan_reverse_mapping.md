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
