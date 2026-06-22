---
name: mapping-pipeline
description: Assessment Mapping docs are a derived artefact — one engine generates all clusters, the validate-mapping-doc skill checks them. Built 2026-06-22. CL1 mappings conformant but its instruments still lack machine-readable benchmarks (Route A retrofit open).
metadata:
  type: project
---

The Assessment Mapping document pipeline is built and documented in
[mapping-document-standard.md](../../docs/mapping-document-standard.md) (the contract + generate→validate
pipeline). Durable points to keep in mind:

- **Derived artefact — never hand-edit a mapping docx.** Change the assessor benchmark (or the UoC) and
  regenerate. One engine — `scripts/mapping/generate_mapping_doc.py` — generates every cluster (per-cluster
  `build_s1_clN_mapping_docs.py` are now thin wrappers holding only data + the inversion the validator
  reads). Use the engine's `--check <cluster>` to prove a regen reproduces committed table content before
  `--build`; the `validate-mapping-doc` skill checks completeness (vs the unit's own UoC) + accuracy (vs the
  benchmark inversion — PC/PE/KE hard, FS/AC advisory closest-fit).

- **CL1 is conformant (2026-06-22).** Mappings engine-generated + validate clean; all three assessor
  instruments carry UoC-tagged benchmarks and pass `validate-at-traceability` (AT2/AT3 had tag-notation
  defects — section repeated inside compound tags `[… PE 1, PE 2]` / `[… FS a, FS b]`, and abbreviated
  `[KE n]` — now fixed). The engine drives CL1's mapping from its hand-authored `DATA_*` (faithful to those
  benchmarks); the only optional gap vs CL2/CL3 is a single Python `BENCHMARK` that both builds the docx
  and drives the mapping. **Separate pre-existing finding (not chased):** `validate-cluster-coverage`
  under-reads CL1's pilot-era docx (its `at_items` only scans the detected benchmark section, missing
  items that ARE present, e.g. ICTCLD502 PC 2.x) — a coverage-validator parsing quirk on CL1, not a real gap.

- **Why the engine exists:** building the validator surfaced that the three clusters' generators had
  diverged (CL1 hand-authored/in-place; CL2 flat-list + prefix split; CL3 per-AT split). The engine unified
  them; reproduction was proven by table-content diff before replacing the finished-cluster tooling — the
  [[feedback-verify-change-impact]] discipline applied to a refactor.
