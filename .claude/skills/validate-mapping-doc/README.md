# validate-mapping-doc · v1.0.0 (updated 2026-06-22)

## Purpose
Prove an Assessment Mapping document (`<cluster>/mappings/<UNIT>_Assessment_Mapping.docx`) is
**complete** against the unit's own UoC (every PC/PE/KE/FS/AC item present and mapped to ≥1 AT) and
**accurate** against the AT marking benchmarks (each row's AT-column codes match the benchmark
inversion). The mapping doc is a derived artefact; this is the mechanical guard that it has not
drifted from either source of truth.

## Prerequisites
- A **Python 3 interpreter** on PATH (`python3`, or `python` / `py -3` on Windows). The completeness
  check is standard-library only.
- Shared script in `.claude/skills/scripts/`: **`validate_mapping_doc.py`**.
- A cluster directory with **`mappings/*_Assessment_Mapping.docx`** and the unit's source UoC in
  **`units_of_competency/<UNIT>_Complete_*.md`**.
- *Accuracy only:* the cluster's **`scripts/s1_clN/build_s1_clN_mapping_docs.py`** and **python-docx**
  (to derive the benchmark oracle). Missing → accuracy is skipped (completeness still runs).

## Inputs & outputs
- **In:** `--mapping <docx>` (one unit; UoC auto-found, or `--uoc <md>`) or `--cluster <dir>` (all
  units). Optional `--no-accuracy`, `--require-accuracy`.
- **Out, per unit:** `COMPLETENESS` PASS/FAIL with `MISSING` / `ROW COUNT` / `BLANK` / `PHANTOM`;
  `ACCURACY` PASS/FAIL on PC/PE/KE, plus FS/AC advisories (closest-fit count + itemised conflicts).
  **Exit 0** when complete and PC/PE/KE-accurate, else **1**.

## How it works
Reads the docx tables (stdlib `word/document.xml` walk) and independently parses the unit's source
UoC, then checks every item is present and mapped (completeness). For accuracy it reuses the
cluster's canonical `invert_benchmarks()` — or the CL1-style `DATA_*` — as the oracle, comparing
PC/PE/KE hard and FS/AC advisory (FS/AC codes are closest-fit, not benchmark-derived). Parsing the
source UoC here, independently of the generator, means a generator bug cannot hide from its own
check.

## Version history
- **v1.0.0 (2026-06-22)** — initial documented version. Validates CL1/CL2/CL3 mapping docs across all
  three generator shapes (CL3 per-AT-split inversion, CL2 flat-list + prefix split, CL1 hand-authored
  `DATA_*`).
