---
name: intranet-in-world-only
description: All intranet content is in-world role-play — no course/assessment/cluster meta-language anywhere except the sanctioned UoC footer
metadata: 
  node_type: memory
  type: feedback
  originSessionId: cecc2119-3823-4017-82e0-21443e608ffd
---

Every page on the YAT mock intranet (`diploma-cloud-cyber-website/src/pages/intranet/**`) must read as a real artefact a YAT staff member or engaged contractor would plausibly find on their intranet. Course-meta language — "assessment task", "cluster", "AT1/AT2/AT3", "the student", "case study", "MTS consultant role" — is **not** in-world and must not appear in body content, descriptions, page lede, navigation summaries, or anywhere else user-visible.

**The sole sanctioned exception** is the small unobtrusive UoC-references footer on migrated scenario documents (rendered by `IntranetLayout` from a `uocReferences` frontmatter field). Tim 2026-05-26: "with the exception of the footer UoC references there should be no course meta, everything is in-world role play".

**Why:** preserves the case-study immersion. A leaked "this is an assessment task" line undermines the in-world principle (`scenario/website.md` §2.1). Tim called this out as a standing rule after spotting leaks during the policies + reference migration round.

**How to apply:**
- When migrating scenario-source content into intranet pages, scrub for: `cluster`, `AT1`/`AT2`/`AT3`, `assessment task`, `student` (when meaning the learner of the case study, not a YAT student-user), `MTS consultant role`, `case study`.
- False positives are common — `YAT students` (the learners enrolled at YAT), `Income Tax Assessment Act 1936`, `risk assessment`, `student assessment evidence`, `Privacy impact assessment`, `ergonomic assessment` are all in-world and stay.
- Replace meta-anchored guidance ("for AT2 cloud foundation builds...") with project-type-anchored guidance ("for foundation builds...").
- Code comments and Astro frontmatter (`uocReferences`, JSDoc annotations) are not user-visible — they may reference scenario / website spec freely.
- The UoC footer is the only place UoC codes ever appear in user-visible content.

**Related:** [[cluster authoring conventions]] §1 in-world-principle (already established); [[draft naming pragmatism]] (different scope).
