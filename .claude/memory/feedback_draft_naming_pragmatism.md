---
name: feedback-draft-naming-pragmatism
description: "During draft phase, don't fuss over file/artefact naming — defer to delivery-ready versions; and when you do name internal identifiers (slugs/folders), optimise for maintainer/LLM findability since students never see them"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: cecc2119-3823-4017-82e0-21443e608ffd
---

Don't spend time worrying about the name of draft files. Naming concerns get applied to delivery-ready versions, not to in-flight working artefacts.

**Why:** Tim 2026-05-26 — opportunity cost. Time spent debating draft filenames or pausing to resolve naming mismatches is time not spent building the actual artefacts students will see. Naming gets cleaned up when something reaches a delivery state.

**How to apply:**
- When a file's content evolves beyond what its filename suggests, don't pause to propose a rename — keep working on the content.
- Don't flag filename / location mismatches as decision points during drafting.
- Save naming-discipline questions for when an artefact is being prepared for delivery (live student delivery, exemplar packs, etc.).
- Applies broadly: scenario files, website artefacts, brand pack files, assessment drafts — anywhere content state is "still being shaped".
- **When you DO name internal identifiers (project slugs, content folders, file names): optimise for maintainer/LLM findability, nothing else.** Students never see these — they see the `displayName` / on-page label. Slugs are pure plumbing (`projects.ts` `slug:` → `content/projects/<slug>/` folder → URL path → cross-references in plans/scenario docs). So the *only* criterion is "how easily / intuitively can a teacher or LLM find the file to change when details shift" — pick the name that matches "where would I look for this." Don't optimise for student-facing aesthetics (there's no such thing for a slug). (Tim 2026-06-09.)
- Does NOT override docs/cluster-authoring-conventions.md §3 — institutional template + companion-`.md` workflow conventions still apply once content reaches the canonical `.docx` stage.
