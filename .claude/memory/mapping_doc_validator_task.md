---
name: mapping-doc-validator-task
description: NEXT TASK (agreed 2026-06-22) — build a skill/tool that validates an Assessment Mapping docx is accurate against the AT marking-benchmark mappings. No such validator exists yet.
metadata:
  type: project
---

**Next task — pick up here.** Create a skill/tool (a `validate-mapping-doc` skill, alongside the other
validators) that checks an **Assessment Mapping document** (`<cluster>/mappings/*_Assessment_Mapping.docx`)
is accurate against the **mapping in the assessment tasks' marking benchmarks**.

**Refinement (Tim, 2026-06-22) — settle this BEFORE designing the validator:** the more valuable check may be
that the mapping document is **COMPLETE**, not merely internally consistent with the marking benchmark. So the
first question to resolve is **what the most appropriate source-of-truth document is to validate completeness
against** — the `consolidated_uoc.md`? the AT benchmarks? something else? Have that conversation at the start
of the task; it shapes the validator's design. The benchmark cross-check described below is *one* option, not
necessarily the chosen one.

**Why it's needed (the gap):** the four existing validators check the AT instruments + `consolidated_uoc.md`,
but **none reads the mapping docx**. Today the mapping docs are trusted only because they are *auto-inverted*
from the benchmarks by the build script — a hand-edit or a stale docx could silently drift from the
benchmarks with no mechanical check. (Confirmed 2026-06-22: no mapping-docx validator skill or script exists;
`validate-at-traceability` + `validate-cluster-coverage` validate the *benchmarks*, not the docx.)

**What it should do:** parse each UoC item's AT-column criterion codes from the `*_Assessment_Mapping.docx`
tables (PC/PE/KE/FS/AC), independently invert the AT assessor benchmarks (criterion → UoC), and assert the
docx matches the inversion — flag any item mapped in the docx to a criterion that doesn't evidence it, and any
item the benchmarks evidence that the docx leaves blank. Treat **FS/AC as advisory** (they're judgement /
closest-fit mapped, not benchmark-derived), PC/PE/KE as hard checks.

**Reusable building blocks** (all stdlib, in `diploma-cloud-cyber-content/.claude/skills/scripts/`):
- `docx_to_text` — the .docx text extractor the validators use.
- `validate_at_traceability.py` / `validate_cluster_coverage.py` — reuse their tag parsing + range/compound
  expansion + the unit-inheritance logic.
- `scripts/s1_cl3/build_s1_cl3_mapping_docs.py` `invert_benchmarks()` — the exact inversion the docx was
  built from; the validator reproduces it independently and compares to the docx's parsed cells.
- Targets: CL1, CL2, CL3 each have `mappings/*_Assessment_Mapping.docx`. Make it portable + stdlib-only like
  the others. This is general tooling, not CL3-specific.

Context: CL3 assessment reached Claude-complete on 2026-06-22 ([[s1cl3-assessment]]); this validator was the
agreed follow-on, deferred to a fresh (post-compaction) session.
