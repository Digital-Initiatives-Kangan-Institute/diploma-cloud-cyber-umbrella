# Scenario flow & conventions

The ICT50220 cloud clusters (CL1–CL3) all play out inside **one shared YAT College world**. A small set of systems — the LMS, the public Website, and the Ledgerline accounting system — rotates through the clusters, each system serving as the *assessment* vehicle in at most one cluster and as a *practice* vehicle elsewhere. This document is the durable reference for that flow: the cross-cluster assessment/practice matrix and its no-leakage invariant, the per-cluster scenario-delta convention, the canonical state progression of each system, the CL3 framing, where the scenario actually lives (single-sourced on the website, never duplicated), and the standing rule that all in-world content stays in-world. It is written for both human authors and LLM agents working across the [content](cluster-authoring-conventions.md) and website repos.

## Cross-cluster system ↔ cluster matrix

Each Semester-1 cloud cluster has exactly **one assessment vehicle** and **one practice vehicle**. Three systems rotate through both roles:

| Cluster | Assessment | Practice |
|---|---|---|
| CL1 | LMS | Ledgerline |
| CL2 | Website | LMS |
| CL3 | Ledgerline | Website |

**No-leakage invariant:** every system is *assessed* in at most one cluster; all cross-cluster reuse happens on the *practice* side. In every cluster the practice system is different from the assessment system. This is what lets a learner meet a system as a worked exemplar in one cluster and then be assessed on a *different* system in another, without the assessment vehicle ever having been pre-walked as practice. CL2's contrast, for example, is a system-transfer: the LMS is the worked exemplar (practice) while the website is the assessment.

## Per-cluster scenario docs

Each cluster carries lean **scenario deltas** rather than a full restatement of the world — one for its assessment side and one for its practice side (`cluster-N-scenario-assessment.md` / `cluster-N-scenario-practice.md`). A delta describes only what is specific to that cluster's framing of the shared world (e.g. CL2's authenticated-cohort practice contrasted against an anonymous-public assessment). These human-facing docs are **current-state only**: what a thing *is*, never what it *was* or when it changed — historical state lives in git, not in prose (see [process-assessment.md](process-assessment.md)).

## System state progressions — the durable architecture

Each system advances through a fixed sequence of architectural states across the clusters. The LMS is the spine; the others are described relative to it.

### LMS

On-prem → single-AZ cloud → Multi-AZ HA.

- On-prem is the CL1 starting state.
- The cutover to single-AZ cloud happens within CL1.
- The LMS reaches Multi-AZ HA by CL2 and stays HA through CL3.

ICT state documents track these phases (environment overview, post-cutover, HA-hardened, and a CL3 variant).

### Website

On-prem → single-AZ pilot → **HA-hardened**, and then the website **diverges by cluster**.

- The single-AZ pilot is both the CL1 state and the **CL3 practice start state**.
- The **HA-hardened website is CL2's assessment baseline, and it is provided directly** — CL2 does not have to build it and does not depend on CL3 to produce it.
- Because of the divergence, **CL2 sees the HA website while CL3 sees the single-AZ website**. The ICT state docs are split to match: the HA-hardened set is CL2's, a separate CL3 set is the single-AZ website, and the website server-status doc exists in a single-AZ form (CL1 + CL3) alongside an HA form (CL2).
- Conceptually the HA website is the *output* of CL3's website-improvement practice — but it is handed to CL2 as a finished baseline so CL2 carries no dependency on CL3.

See [website-architecture.md](website-architecture.md).

### Ledgerline

Ledgerline **mirrors the LMS, but stops one step short of HA**: on-prem → single-AZ cloud → (improved, but not canonically HA).

- On-prem is the CL1 starting state; the cutover to single-AZ cloud lands within CL1 and Ledgerline is single-AZ cloud through CL1, CL2, and CL3.
- Ledgerline is **never HA in the canonical state**. CL3 improves it *from* single-AZ.
- A teaching-vs-assessment slip is accepted: Ledgerline may be hardened during CL1 teaching, but the canonical assessable state stays single-AZ through CL3.
- The single-AZ Ledgerline architecture is the CL3 starting-state reference (an Accounting Baseline Solution Design plus its single-AZ network drawing). Ledgerline carries full document parity with the LMS — server-status, application-spec, and operational-costing docs in both an on-prem form (CL1 early) and a single-AZ cloud form (CL1 cutover onward), with environment/network/inventory showing accounting on single-AZ AWS.

A general rule applies across all three progressions: **a completed project persists (marked Completed) into later states** rather than disappearing from the world once its cluster is past.

## CL3 framing

CL3 is framed as **improvement, not HA-hardening**. Student-facing text says "improvement" — open-ended, and explicitly *not* required to land on HA, because the unit does not mandate HA. Internal slugs may still read `website-ha-hardening` / `ledgerline-ha-hardening`, but display names are phrased as "…Cloud Infrastructure Improvement".

The **main CL3 focus is planning and team leadership** (BSBXTW401); the ICTCLD504 technical side is deliberately light. The cluster runs three assessment tasks in an **individual → group → individual** shape, on an owned-dimension model.

## Where the scenario lives

The YAT College scenario is **one shared world used across all clusters** — never duplicated per cluster (duplication wastes effort and invites divergence). All in-world scenario content (ICT environment, policies, project briefs, references, state-versioned documents) is **single-sourced on the website** as Astro content collections, **state-versioned by each document's `appearsIn` states** rather than by per-cluster folders. The website is the single source of truth; there is no authoritative repo-root scenario folder.

**How to apply:**

- Reference scenario content **abstractly** — "the YAT intranet's ICT Strategic Plan page", "the LMS application specification", "the ICT manager consultation notes" — and **never by file path**. Students consume the scenario through the website.
- Distinguish state versions by `appearsIn` (e.g. on-prem early states vs the post-cutover state), not by per-cluster directories.

(Website content lives in the `diploma-cloud-cyber-website/` repo's content collections; cluster authoring artefacts live in the `diploma-cloud-cyber-content/` repo. See [website-architecture.md](website-architecture.md) and [document-template-system.md](document-template-system.md).)

## In-world-only rule

Every page on the YAT mock intranet must read as a **real artefact** a YAT staff member or engaged contractor would plausibly find on their intranet. Course-meta language is **not** in-world and must not appear in body content, page descriptions, ledes, navigation summaries, or anywhere else user-visible. This preserves the case-study immersion: a single leaked "this is an assessment task" line breaks the in-world principle.

**The sole sanctioned exception** is the small, unobtrusive **UoC-references footer** on migrated scenario documents (rendered by the intranet layout from a `uocReferences` frontmatter field). That footer is the only place UoC codes ever appear in user-visible content.

**Scrub list** — when migrating scenario-source content into intranet pages, scrub for these meta terms: `cluster`, `AT1` / `AT2` / `AT3`, `assessment task`, `student` (when it means the *learner of the case study*, not a YAT student-user), `MTS consultant role`, `case study`. Replace meta-anchored guidance ("for AT2 cloud foundation builds…") with project-type-anchored guidance ("for foundation builds…").

**False positives** — these are genuinely in-world and must **stay**: `YAT students` (the learners enrolled at YAT), `Income Tax Assessment Act 1936`, `risk assessment`, `student assessment evidence`, `Privacy impact assessment`, `ergonomic assessment`.

Code comments and Astro frontmatter (`uocReferences`, JSDoc annotations) are not user-visible and may reference the scenario or website spec freely. See [cluster-authoring-conventions.md](cluster-authoring-conventions.md) for the established in-world principle, and [process-delivery.md](process-delivery.md) for how migration rounds run.
