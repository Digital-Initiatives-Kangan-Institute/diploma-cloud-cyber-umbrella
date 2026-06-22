# Assessment Mapping document — standard

**Audience:** humans and LLM agents authoring or checking a cluster's per-unit Assessment Mapping
documents. Paths are relative to the `diploma-cloud-cyber-content/` repo root.

The **Assessment Mapping document** (`<cluster>/mappings/<UNIT>_Assessment_Mapping.docx`, built on the
institutional `kangan-templates/Assessment Mapping Tool.docx`) is the RTO-facing evidence that every
component of a unit of competency is assessed: one row per UoC item (PC / PE / KE / FS / AC), with the
Assessment Task columns (AT1…AT5) carrying the marking-criterion code(s) that evidence that item. One
document **per unit** in the cluster.

This standard defines what the document is, the contract that makes producing it tool-driven, and the
generate → validate pipeline. It generalises beyond this diploma: any course whose assessment
instruments meet the contract can produce and check mapping documents the same way.

## The core principle — a derived artefact, never hand-authored

The mapping document is a **pure function of two sources of truth already in the repo**, plus one small
judgement layer:

1. **The unit's UoC** — the verbatim transcription at `units_of_competency/<UNIT>_Complete_*.md`
   (produced + verbatim-checked by the `transcribe-uoc` / `validate-uoc-transcription` skills). This
   fixes the **rows**: every PC/PE/KE/FS/AC item, in source order.
2. **The assessor instrument's marking benchmark** — which, for each marking criterion, lists the UoC
   item(s) it evidences. Inverted (criterion→item becomes item→criterion), this fills the **AT columns**.
3. **The FS/AC closest-fit layer** — the only human judgement (see below).

Because it is derived, the mapping document is **never hand-edited**. A hand edit, or a stale docx left
behind when a benchmark changes, is drift — and drift is exactly what the validator exists to catch. To
change a mapping, change the benchmark (or the UoC) and regenerate.

## The contract — what an assessment instrument must expose to be mappable

Producing the mapping mechanically depends on one discipline in the **assessor instrument**:

- **A machine-readable marking benchmark.** The benchmark is a structured list of
  `(criterion_id, uoc_reference_string)` rows — in this repo, a Python `BENCHMARK` constant in the
  unit's `scripts/s1_clN/build_s1_clN_atM_assessor.py` generator. A benchmark that exists only as prose
  inside a finished `.docx` cannot be inverted without first being re-expressed in this form.
- **Every criterion carries at least one UoC tag**, in the canonical `[<UNIT> <SECTION> <numbering>]`
  notation (e.g. `[ICTCLD504 PC 1.2]`, `[ICTCLD504 KE 4]`, `[ICTCLD504 FS Reading]`). This is the same
  bidirectional-traceability rule the **`validate-at-traceability`** skill already enforces at authoring
  time — so the contract is, in practice, "pass traceability validation."
- **A criterion-ID scheme that identifies the AT.** Each criterion code maps to exactly one Assessment
  Task. Two conventions are in use and both are acceptable; pick one per cluster and be consistent:
  - **Per-AT prefix** (CL2): one flat criterion list per item; a prefix rule buckets codes into columns
    (e.g. `A`/`B`/`C` → AT1, `D` → AT2). The split lives in the generator's `_split_codes()`.
  - **Per-AT benchmark** (CL3): each AT's benchmark is inverted under its own column directly, so the AT
    is known without a prefix rule. Criterion codes still carry an AT-distinct prefix for readability
    (CL3: AT1 `D#`, AT2 `I#`, AT3 `E#`).

Meet this contract and the mapping document is fully determined by the UoC and the benchmarks.

## The FS/AC closest-fit layer — the one judgement, kept advisory

Two row types are **not** reliably benchmark-derived:

- **Foundation Skills (FS)** that no criterion happens to tag, and
- **Assessment Conditions (AC)**, which describe the *environment* (lab / tool / access) and so map to
  the instrument's **Conditions** (`C#`), not to marking criteria.

These are filled by judgement — the generator's `FS_MAP` / `AC_MAP` closest-fit tables — and are
therefore treated as **advisory** in validation: a closest-fit cell is expected and is only summarised,
while a *conflict* (a benchmark genuinely tags that FS/AC item yet the document differs) is surfaced for
review. PC/PE/KE remain hard-checked. (One AC always maps to a `✓` on the relevant ATs: the
"assessors must satisfy…" assessor-requirement row.)

## The pipeline

**Generate.** One engine — `scripts/mapping/generate_mapping_doc.py` — generates every cluster's mapping
docs: it parses the source UoC for the rows, inverts the assessor benchmarks **per AT** for the column
codes, applies the FS/AC closest-fit tables, and fills the institutional template. Each cluster is one
entry in the engine's `CLUSTERS` registry — data (benchmarks, `FS_MAP`/`AC_MAP`, titles) sourced from the
cluster's modules; policy is just two flags (`n_ats`, and whether FS/AC take benchmark codes before the
closest-fit map). Run `--check <cluster>` to confirm it reproduces the committed docs, then
`--build <cluster>`. The per-cluster `scripts/s1_clN/build_s1_clN_mapping_docs.py` files are now **thin
wrappers** that delegate to the engine (kept only for their data + the inversion the validator reads); to
add a new cluster, add a `CLUSTERS` entry — don't copy a per-cluster script. Output:
`<cluster>/mappings/<UNIT>_Assessment_Mapping.docx`.

**Validate.** The **`validate-mapping-doc`** skill (`.claude/skills/scripts/validate_mapping_doc.py`)
re-derives the expectation independently and checks the produced docx two ways:

- **Completeness (primary, hard)** — against the unit's *own* UoC: every item is present as a row **and**
  mapped to ≥1 AT. Flags `MISSING`, `BLANK` (present but unmapped — an unassessed requirement),
  `PHANTOM` (a row that is not a UoC item). The source UoC is parsed *independently of the generator*, so
  a generator bug cannot hide from its own check.
- **Accuracy (secondary)** — against the benchmark inversion: PC/PE/KE hard, FS/AC advisory (above). This
  is a drift check — is the on-disk document still in sync with the benchmarks it was built from.

Run it after every (re)generation, and before treating a cluster's mappings as final:

```bash
python3 .claude/skills/scripts/validate_mapping_doc.py --cluster <S1-CLx dir>
```

## The template layout (shared across clusters)

All clusters use the one `Assessment Mapping Tool.docx`, so the table layout is fixed; a 2-AT cluster
simply leaves the AT3 column blank. Tables are addressed in document order:

| Table | Section | Item column | AT1 / AT2 / AT3 columns |
|---|---|---|---|
| 3 | Assessment Conditions (AC) | 0 | 1 / 2 / 3 |
| 4 | Performance Criteria (PC) | 1 (col 0 = element) | 2 / 3 / 4 |
| 5 | Performance Evidence (PE) | 0 | 1 / 2 / 3 |
| 6 | Knowledge Evidence (KE) | 0 | 1 / 2 / 3 |
| 7 | Foundation Skills (FS) | 0 (col 2 = description) | 3 / 4 / 5 |

Each table has two header rows; data rows follow. PC and FS rows are matched by identity (PC number; FS
skill name); PE/KE/AC are positional, so their row counts must equal the UoC's item counts.

## Conformance status

- **CL2, CL3** — fully contract-conformant: machine-readable per-criterion benchmarks → generated
  mappings → validate clean (completeness + PC/PE/KE accuracy).
- **CL1** — conformant. Its mappings are engine-generated and validate clean, and its **three assessor
  instruments carry UoC-tagged benchmarks that all pass `validate-at-traceability`** (AT2/AT3 had
  tag-notation defects — the section repeated inside compound tags, e.g. `[… PE 1, PE 2]` / `[… FS a, FS b]`,
  and abbreviated `[KE n]` lacking the unit — fixed 2026-06-22). Regenerating the mappings also fixed the
  structural artefacts (the 401 AC block-row, the 517 PE split) and several verbatim defects (a PC typo, a
  truncation, a bloated FS table). The engine drives CL1's mapping from its hand-authored `DATA_*` (the
  `source: "data"` path in `CLUSTERS`), which is faithful to those benchmarks. The only structural
  difference from CL2/CL3 is that CL1 has no single Python `BENCHMARK` constant that *both* builds the
  assessor docx and drives the mapping (CL1's docx were authored directly) — unifying that is optional, not
  a conformance requirement.

## See also

- [process-assessment.md](process-assessment.md) — the cluster assessment-creation process (the mapping
  document is the artefact produced after Step 7).
- [cluster-authoring-conventions.md](cluster-authoring-conventions.md) — the bidirectional UoC
  traceability rule the contract depends on.
- `.claude/skills/validate-mapping-doc/` — the validator skill.
