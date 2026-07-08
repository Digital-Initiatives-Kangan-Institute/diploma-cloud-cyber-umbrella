---
name: validate-mapping-doc
version: 1.0.0
updated: 2026-06-22
model: claude-haiku-4-5-20251001
description: >-
  This skill should be used to check that an Assessment Mapping document
  (<cluster>/mappings/<UNIT>_Assessment_Mapping.docx) is complete and accurate — e.g. "validate the
  mapping doc", "is the assessment mapping complete", "does the mapping document cover every UoC
  item", "check the mapping docx against the marking benchmark", "did the mapping doc drift from the
  ATs", or before treating a cluster's mapping documents as final. It runs a deterministic check (the
  bundled validate_mapping_doc.py) that confirms every assessable item in the unit's own UoC appears
  as a row and is mapped to at least one AT (completeness), and that each row's AT-column codes match
  the AT marking benchmarks (accuracy). Use it whenever a mapping document must be confirmed against
  its source of truth, even if the user does not name the script.
---

# Validate Assessment Mapping document

A unit's Assessment Mapping document is a **derived artefact**: each row is a UoC item (PC / PE / KE
/ FS / AC) and the AT columns carry the criterion code(s) that evidence it. Because it is
auto-generated from the source UoC and the AT marking benchmarks, the only ways it goes wrong are
that it **drifts from the UoC** (an item dropped or left unmapped) or **drifts from the benchmarks**
(a stale docx or a hand-edit). This skill checks both — the mechanical guard that the document an
auditor reads still faithfully reflects what the unit requires and what the ATs actually assess.

## When to use

- Before treating a cluster's `mappings/*_Assessment_Mapping.docx` as final.
- After (re)generating or hand-editing a mapping document, to confirm it is in sync.
- To find which UoC items a mapping document is missing, leaves unmapped, or maps inconsistently
  with the marking benchmark.

## The validator

The engine is **`validate_mapping_doc.py`**, bundled at `.claude/skills/scripts/`. It performs two
checks:

- **COMPLETENESS (primary, hard)** — source of truth is the **unit's own UoC** transcription
  (`units_of_competency/<UNIT>_Complete_*.md`), parsed here independently of the generator. Every PC
  / PE / KE / FS / AC item must appear as a row **and** be mapped to ≥1 AT. Reports `MISSING` (no
  row / row-count shortfall), `BLANK` (a row mapped to no AT), `PHANTOM` (a row that is not a UoC
  item).
- **ACCURACY (secondary)** — source of truth is the **AT marking benchmarks**, via the cluster's
  canonical `invert_benchmarks()` (or, for the older CL1-style generators, the hand-authored
  `DATA_*`). **PC/PE/KE are hard** (a mismatch fails); **FS/AC are advisory** — their codes are
  closest-fit judgement (the generator's `FS_MAP` / `AC_MAP`), not benchmark-derived, so a pure
  closest-fit cell is summarised, and only a *conflict* (the benchmark tags the item but the doc
  differs) is itemised for review.

The docx is read with the standard library only, so completeness has no third-party dependency. The
accuracy oracle imports the cluster's mapping build module (which uses python-docx); it loads
lazily, so completeness still runs where python-docx is absent.

## How to run it

> **Python interpreter:** run the command below with whatever Python 3 launcher your system has —
> `python3`, `python`, or `py -3` (on Windows, `python3` may be the Microsoft Store alias).

```bash
# one unit
python3 .claude/skills/scripts/validate_mapping_doc.py --mapping <UNIT>_Assessment_Mapping.docx
# every mapping doc in a cluster
python3 .claude/skills/scripts/validate_mapping_doc.py --cluster <S1-CLx dir>
```

- `--mapping <docx>` — a single mapping document. Its source UoC is auto-found in the sibling
  `units_of_competency/`; override with `--uoc <md>`.
- `--cluster <dir>` — validate every `mappings/*_Assessment_Mapping.docx` under the cluster.
- `--no-accuracy` — completeness only (skip the benchmark cross-check).
- `--require-accuracy` — treat a missing/unavailable accuracy oracle as a failure rather than a skip.

Exit `0` on PASS (complete; PC/PE/KE accurate where the oracle is available), `1` otherwise.

## Interpreting the result

- **COMPLETENESS: PASS** — every UoC item is present and mapped; the section counts are echoed.
- **MISSING / ROW COUNT** — a UoC item has no row (or a positional section's row count differs from
  the UoC). Close the gap in the mapping doc.
- **BLANK** — a row is present but mapped to no AT: an unassessed requirement walking past an
  auditor. Map it, or confirm it is genuinely out of scope.
- **PHANTOM** — a mapping row that is not a UoC item (extra or stale row). Remove it.
- **ACCURACY: FAIL (PC/PE/KE)** — a hard mismatch between the doc's codes and the benchmark
  inversion: the docx is stale or hand-edited. Regenerate, or fix the benchmark.
- **ACCURACY advisory (FS/AC)** — *closest-fit* cells are expected (a count, not an error);
  *conflicts* mean the benchmark does tag that FS/AC item and the doc differs — worth a human glance.

## Portability

Self-contained: the validator lives in `.claude/skills/scripts/` and reads the docx + source UoC
with stdlib only, so completeness works in any course repo from just the cluster directory. The
accuracy cross-check additionally needs the cluster's `scripts/s1_clN/build_s1_clN_mapping_docs.py`
(and python-docx) to derive the benchmark oracle; where that is unavailable it is skipped (or fails
under `--require-accuracy`), and completeness still runs.
