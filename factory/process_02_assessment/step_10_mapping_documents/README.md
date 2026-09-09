# Step 10 — Mapping documents

*(cluster-level)* · Run-sheet: [process-assessment.md](../../../docs/process-assessment.md)

Generate each unit's Assessment Mapping document from the ATs' machine-readable benchmarks. A derived artefact — never hand-edited.

## Tooling

- engine `generate_mapping_doc.py` — `scripts/mapping/`
- registry seam `mapping_registry.py` — content repo `scripts/`
- validator `validate_mapping_doc.py` — `.claude/skills/scripts/`
- standard `mapping-document-standard.md` — `docs/`

## Gate

**Gate 10 → 11** · *validator* `validate-mapping-doc` = **PASS** for every unit — complete and accurate against the benchmarks.

## Status

**Not ported** — the tooling above still lives at its legacy location. Converting it is done on request,
test-first; see [factory/README.md](../../README.md).
