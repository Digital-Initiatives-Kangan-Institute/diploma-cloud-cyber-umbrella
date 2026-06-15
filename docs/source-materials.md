# Source materials

A map of the `diploma-cloud-cyber-content` source materials — what lives in the workspace and what
state each piece of source material is in. (Project docs — overview, clusters, the authoring/delivery
processes — are catalogued in the docs [INDEX.md](INDEX.md).)

> **Paths** are relative to the `diploma-cloud-cyber-content/` repo root.

## Source-material workspace folders

| Folder | Purpose |
|---|---|
| `original_materials/` | All source materials as supplied. **Read-only reference.** Files we decide to reuse get copied out into the workspace (per cluster) and edited there — the originals are never modified, never extended, never "completed". |
| `templates/` | Workspace-level templates we author cluster outputs against (Assessment Mapping Tool, Delivery Plan, Project Assessment student/assessor, Written Assessment student/assessor). Distinct from the institutional `_TEMPLATES/` folder nested inside `original_materials/`. |
| `courseware/` | Scaffolded working workspace where finished cluster artefacts live. Organised as `semester_{1,2}/cl_<cluster_name>/units_of_competency/`. Each `units_of_competency/` folder already contains the `<UNIT>_Complete_R1.docx` reference document for the units in that cluster (the training-package UoC definition). |

## `original_materials/DipIT_20260313/`

The primary source set. One folder per unit code, plus a `_TEMPLATES` folder with the institutional document templates.

### Material-state classification

Source materials fall into four shapes. This matters because the **first job** is to normalise our internal view of each unit before we can compare them.

**Pattern A — "Current-template flat":** Files at the top of the folder, named `<UNIT> AT1 Questioning…`, `<UNIT> AT2 Portfolio/Observation…`, plus Learning Guide, Student unit guide, Unit Assessment Mapping, Unit Content Mapping, Pre-Validation Tool. This is the target/normalised shape.

Units in Pattern A: BSBCRT512, BSBXTW401, ICTCLD501, ICTCLD502, ICTCYS610, ICTCYS613, ICTICT517, ICTNWK540, ICTSAS524, ICTSAS526, ICTSAS527.

**Pattern B — "Folder-structured":** Materials organised into subfolders such as `Assessment Tool/`, `Student Guide/` (or `Unit Guide/`), `Course Resources/`, `Unit Mapping/`. Newer or differently-authored units.

Units in Pattern B: ICTCLD401, ICTCLD503, ICTCLD504, ICTNWK553.

**Pattern C — "Validation-only / minimal":** Only a Pre-Validation Tool plus `Original (pre external validation)/` and `Post external validation/` (or equivalent version) folders. The actual deliverables are nested inside those version folders and need to be excavated.

Units in Pattern C: BSBXCS402, ICTICT532, ICTSAS518.

**Pattern D — "Special / non-standard":** Materials that don't fit the above.

- **ICTCYS407** — heavily Splunk-focused; includes lab data, an .mbz (Moodle course backup), VM artefacts, and micro-course content rather than the standard AT1/AT2 docx set.
- **ICTPRG549** — only an Assessor Guide. No student-facing material, no mapping, no pre-validation tool. Note: ICTPRG549 is **not** in the cluster list.

### Unit folders — summary

| Unit code | Pattern | Cluster | Notes |
|---|---|---|---|
| BSBCRT512 | A | Threat Hunting | Has Scoping / Solutions / Solution Feedback templates. |
| BSBXCS402 | C | Cyber Policy | Pre-validation + version folders only — content buried. |
| BSBXTW401 | A | Cloud Improve Infra as a Team | Includes team-project artefacts (MP Tech Solution Profile, Team Titans Animation Project doc). |
| ICTCLD401 | B | Cloud Design and Build | Includes a `Brightspace Export/` folder. |
| ICTCLD501 | A | Cloud Disaster Recovery | Has session-plan delivery schedule .xlsx and DR plan template. |
| ICTCLD502 | A | Cloud Design and Build | Has sample content delivery schedule .xlsx and `archived version/`. |
| ICTCLD503 | B | Cloud Disaster Recovery | **Updated materials also available** in `_ICTCLD503 504 update/`. |
| ICTCLD504 | B | Cloud Improve Infra as a Team | **Updated materials also available** in `_ICTCLD503 504 update/`. |
| ICTCYS407 | D | Threat Hunting | Splunk-heavy: presentations, lab data, VM, Moodle backup .mbz. |
| ICTCYS610 | A | Enterprise Systems | Multi-session `.pptx` set + Incident Response Plan and Guidance folder. |
| ICTCYS613 | A | Cyber Design | Has dedicated AT2 report template. |
| ICTICT517 | A | Cloud Design and Build | Includes Cost Benefit Analysis .xlsx + Draft Plan / Feedback Record templates. |
| ICTICT532 | C | Cyber Policy | Pre-validation + version folders only — content buried. |
| ICTNWK540 | A | Enterprise Systems | Many AT-numbered observations (AT1–AT7) and storage-calculation .xlsx files. Lab-setup doc. |
| ICTNWK553 | B | Enterprise Systems | Includes Proxmox ISO files, lab info, VM converters, and "Other Supported UoCs" folder. |
| ICTPRG549 | D | **not in cluster list** | Assessor Guide only. Confirm whether out of scope. |
| ICTSAS518 | C | **not in cluster list** | Pre-validation + version folders only. Confirm whether out of scope. |
| ICTSAS524 | A | Cyber Design | PAT + QAT for student and assessor. |
| ICTSAS526 | A | Cyber Design | PAT + QAT for student and assessor. |
| ICTSAS527 | A | Threat Hunting | Standard A-pattern files. |
| ICTCLD505 | UoC only | Cloud Disaster Recovery | No learning/assessment source, but `_Complete_R1.docx` is present in courseware — full UoC available to author against. |
| VU23226 | **no UoC, no source** | Enterprise Systems | No folder, no `_Complete` reference, no mention anywhere in supplied files. **UoC reference document must be obtained** before this unit can be included in any mapping. |

### `_TEMPLATES/` — institutional templates

Reference templates we should re-use when writing new materials so the look-and-feel stays consistent. Includes Direct Observation, OTCD, Product Assessment, Questioning Assessment, Student unit guide, Third-party observation (×4 variants), Unit Assessment Mapping, Unit Content Mapping, Work Placement Logbook, and the Network Courseware Pre-Validation Tool.

## `original_materials/_ICTCLD503 504 update/`

Updated teaching-and-learning material for two cloud units delivered separately to the main set.

| Subfolder | Contents |
|---|---|
| `ICTCLD503/ICTCLD503 T&L Final/` + `archive/` | Updated T&L final + archive. |
| `ICTCLD504/ICTCLD504 T&L - Final/` + `archive/` | Updated T&L final + archive. |

These updates should supersede the equivalent files in `DipIT_20260313/ICTCLD503/` and `ICTCLD504/` — to be verified during the audit phase.

## `courseware/` (workspace root)

The working destination for finished cluster artefacts. Already scaffolded with seven cluster folders under two semester folders, each containing a `units_of_competency/` subfolder pre-populated with the relevant unit-of-competency reference documents (`<UNIT>_Complete_R1.docx`). These reference docs contain the training-package definition for each unit: Application, Elements & Performance Criteria, Foundation Skills, Performance Evidence, Knowledge Evidence, Assessment Conditions, and Links.

```
courseware/
  semester_1/
    cl_cloud_design_build/units_of_competency/         (ICTCLD401, ICTCLD502, ICTICT517)
    cl_cloud_dissaster_recovery/units_of_competency/   (ICTCLD501, ICTCLD503, ICTCLD505)
    cl_cloud_improve_infrastructure/units_of_competency/  (BSBXTW401, ICTCLD504)
  semester_2/
    cl_cyber_design/units_of_competency/               (ICTCYS613, ICTSAS524, ICTSAS526)
    cl_cyber_enterprise_systems/units_of_competency/   (ICTCYS610, ICTNWK540, ICTNWK553) + VU23226 missing
    cl_cyber_policy/units_of_competency/               (BSBXCS402, ICTICT532)
    cl_threat_hunting/units_of_competency/             (BSBCRT512, ICTCYS407, ICTSAS527)
```

19 of 20 cluster-list units have a `_Complete_R1.docx`. **VU23226 does not** — and a search of the entire supplied source set found no reference to it anywhere.

## `templates/` (workspace root)

Cluster-output templates supplied for use in this project. These are the templates we author *to*, not the templates the source units were authored from.

| File | Purpose |
|---|---|
| `Assessment Mapping Tool.docx` | Cluster/unit mapping artefact. |
| `Delivery_Plan_Template_v0.1.docx` | Cluster delivery plan. |
| `Project Assessment - Assessor.docx` | Project-style AT, assessor version. |
| `Project Assessment - Student.docx` | Project-style AT, student version. |
| `Written Assessment - Assessor.docx` | Written/questioning AT, assessor version. |
| `Written Assessment - Student.docx` | Written/questioning AT, student version. |

## What's missing or unclear

1. **ICTCLD505** has no inherited learning/assessment material, but the UoC reference is available — we have what we need to author against. Plan capacity for an author-from-scratch effort within the Cloud Disaster Recovery cluster.
2. **VU23226** is missing entirely — including the UoC reference document. The UoC needs to be obtained (training.gov.au / VETNet, Victoria University accredited course) before the Enterprise Systems cluster mapping can include it. This is a small but real blocker on that cluster's mapping.
3. **ICTPRG549 and ICTSAS518 status.** Folders exist but units are not in the cluster list. Confirm out of scope so we don't spend time on them.
4. **Pattern-C units (BSBXCS402, ICTICT532, ICTSAS518).** Real content is buried inside "Original / Post external validation" subfolders. Need to look inside before we can compare them against other units.
5. **No existing inventory of overlaps.** The duplication problem is asserted but has not been evidenced unit-by-unit. The audit phase will produce that evidence.
