---
name: process-mapping-and-audit
description: The map-process skill turns a factory's step→gate run-sheet into a GENERATED Mermaid process map + a JSON audit model; the JSON is the seam for a decided-not-built downstream process-audit capability.
metadata:
  node_type: memory
  type: project
  originSessionId: 5fe40dfd-42a4-49d7-8e7d-5da57c8df524
---

**`map-process`** (course-agnostic skill, umbrella `.claude/skills/map-process/`, stdlib-only) parses a
factory's run-sheet (the umbrella step→gate convention) and emits, per run-sheet, a **GENERATED** map to
`docs/process-maps/<slug>.md` (Mermaid flowchart + a tooling-&-locus table + a cross-check/audit table)
plus `<slug>.json` (the structured model) and a `factory-overview.md` chaining ≥2 run-sheets. **Maps are
derived artefacts — regenerate, never hand-edit.** Registered in [docs/INDEX.md](../../docs/INDEX.md).

**Design decisions (2026-07-09, this build):**
- **Mermaid, not draw-diagram reuse** — a process map that evolves + feeds an audit wants text that diffs,
  renders free on GitHub/VS-Code, and an auditor LLM can read directly. (draw-diagram was the considered
  alternative; rejected for binary PNG + manual grid coords.)
- **Locus-tagged steps (light), not swim-lane subgraphs** — each step is tagged inline: 🏠 the umbrella
  tooling it runs (skill/agent/engine/MCP), 📦/🌐 the sub-repo/website data it draws on, 👤 if human-led.
  Surfaces the umbrella-tool-↔-sub-repo-data crossing without lane clutter.
- **Cross-check = the audit seam.** Every gate's named validator is resolved against the real inventory
  (skill dir / `skills/scripts/` engine / `agents/*.md` / umbrella `scripts/` engine / `mcp__*`); a
  named-but-missing validator or a doc status marker that contradicts reality is flagged red. This caught
  a real stale marker — delivery Gate 6 said "to build" though `validate-delivery-plan` was built
  2026-07-02 (fixed; both maps now 0-flag).

**First downstream use (2026-07-09):** the map's amber "candidate for tooling" flags (human-only gates)
were reviewed for automation potential; two candidates have been built: **delivery Gate 2→3** →
`validate-topic-breakdown` (every AT has ≥1 Topic; every Topic declares a valid AT; count fits the
frame — see [[delivery-run-sheet]]), and **assessment Gate 9→10** → `validate-student-instrument` (the
mechanical leak-lint: a `*-Student.docx` carries no assessor-only material — see [[assessment-run-sheet]]).
Remaining human-only candidate for tooling: **delivery Gate 5→6** (practice coverage + no-leakage);
**assessment Gate 12→done** (institutional pre-validation) stays human by nature.

**Decided-not-built (follow-on):** the **process-audit** capability itself — a separate skill/agent that
reads the `<slug>.json` model + flag set and reasons about deeper problems (orphan tools referenced by no
step, ordering/dependency issues, gates with no definition-of-done). `map-process` is its deterministic
input. Related: [[umbrella-engine-architecture]], [[delivery-run-sheet]], [[assessment-run-sheet]].
