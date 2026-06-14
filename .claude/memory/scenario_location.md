---
name: scenario folder location and course-wide reuse intent
description: Scenario materials live at <repo_root>/scenario/, shared across all clusters in the diploma
type: project
originSessionId: df4c62a3-dd05-4ef4-a776-3c7ab7048cba
---
The cluster scenario materials (YAT College — strategic plan, current ICT environment, policies, project briefs, references, state-versioned documents) live at `<repo_root>/scenario/`, NOT inside any individual cluster's folder.

**Why:** Tim moved the scenario folder to repo root on 2026-05-23 because the same YAT scenario is used across all clusters in the diploma. State-versioned documents (e.g. `internal-ict-environment-overview-S1-CL1-AT1.md`, then a future `internal-ict-environment-overview-S1-CL2-AT1.md`) evolve as the course progresses, but the underlying organisation stays the same. Per-cluster duplication of the scenario would be wasteful and would risk divergence.

**How to apply:**
- When authoring cluster artefacts that reference scenario content, use **abstract references** ("the YAT intranet's ICT Strategic Plan page", "the LMS application specification", "the ICT manager consultation notes") rather than file paths. Students consume the scenario via the mock website (`scenario/website.md` describes the delivery vehicle), not via file paths.
- When authoring **author-facing or assessor-facing** artefacts that need to point at a specific scenario file (e.g. templates checklists, assessor benchmarks), use explicit repo-root paths: `<repo_root>/scenario/internal-X.md`.
- Don't create per-cluster scenario folders. If a cluster needs scenario state at a specific AT, add the AT-suffixed file to the shared `<repo_root>/scenario/` folder (the AT suffix on the filename is what distinguishes state versions).
- Captured in `documentaion/project_overview.md` § Delivery context.
