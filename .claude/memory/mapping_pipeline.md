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

- **CL1 is only partly conformant — open follow-on ("Route A").** CL1's mappings are now engine-generated
  and validate clean, but they are driven from a direct inversion *synthesised from the hand-authored
  `DATA_*` dicts*; CL1's three assessor instruments still have **no machine-readable, UoC-tagged
  benchmark**, so `validate-at-traceability` can't check them. Full conformance = authoring real `BENCHMARK`
  structures for CL1's 3 assessors (like CL2/CL3). Separately scoped; not yet done.

- **Why the engine exists:** building the validator surfaced that the three clusters' generators had
  diverged (CL1 hand-authored/in-place; CL2 flat-list + prefix split; CL3 per-AT split). The engine unified
  them; reproduction was proven by table-content diff before replacing the finished-cluster tooling — the
  [[feedback-verify-change-impact]] discipline applied to a refactor.
