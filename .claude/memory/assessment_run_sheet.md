---
name: assessment-run-sheet
description: "The assessment process is a formalised step→gate run-sheet (docs/process-assessment.md), validated END-TO-END on S1 — every deterministic gate (1–8, 9 leak-lint, 10, 11) PASSES; Gate 9 now has a mechanical leak-lint (validate-student-instrument, 2026-07-09), leaving only its residual quality/tone review + Gate 12 institutional pre-validation as human."
metadata: 
  node_type: memory
  type: project
  originSessionId: 5fe40dfd-42a4-49d7-8e7d-5da57c8df524
---

The cluster **assessment process is a formalised step→gate run-sheet** —
[process-assessment.md](../../docs/process-assessment.md), the **assessment run-sheet** (one of two; the
**delivery run-sheet** = process-delivery.md, to get the same treatment later). 12 steps; each **gate** =
a deterministic **validator** (where one exists) **+ human review**, with the human check removable per-gate
as a step earns confidence. The active workstream is **walking the gates against S1 (CL1/CL2/CL3)**: run the
validator where one exists; at a gateless gate, build a tool/agent for it.

**Gate-walk state (2026-06-22):**
- **Gate 1 transcribe / 2 consolidate-UoC** — existing validators, PASS on all 3 clusters.
- **Gate 3 audit** — reframed as **brownfield-only / optional** (skip if greenfield); built the read-only
  **`evaluate-legacy-materials` agent** (`.claude/agents/`) that surfaces reuse candidates, authors/decides
  nothing. Not a validation gate. Can't run on S1 (no `original_materials/` in repo).
- **Gate 4 plan** — built the **assessment-plan format standard** (docs/assessment-plan-format.md) +
  **`validate-assessment-plan`** (format linter + UoC-coverage). **All 3 S1 plans retrofitted** to the
  format (per-AT UoC coverage as canonical tags derived from the AT benchmarks; per-cluster **`SR-*`**
  scenario-requirements register; substance preserved). All PASS (CL1 106, CL2 105, CL3 72).
- **Gate 5 consolidate plans** *(per scenario)* — built **`generate-consolidated-plan`** (deterministic) +
  **`validate-consolidated-plan`** (independent faithful-union tester). Generated `assessment-plans/S1.md`
  (the cross-cluster AT roster + coverage rollup + **unioned SR-* register** = the single contract the
  scenario validates against). PASS.
- **Gate 6 scenario** — built the **scenario-plan format standard** (docs/scenario-plan-format.md) +
  **`validate-scenario-plan`** (format linter + bidirectional SR cross-check). The **scenario plan**
  (`scenario-plans/<S>.md`) is the *authored* counterpart of the *derived* consolidated plan: in-world
  **`SE-NN`** elements, each `Satisfies:` the `SR-*` it provides. Authored **`scenario-plans/S1.md`** (22
  elements binding all 24 `SR-*`); cross-check **PASS** (negative-tested: catches UNCOVERED + PHANTOM).
- **Gate 7 scenario materials / website** — built the read-only **`verify-scenario-realisation` agent**
  (`.claude/agents/`); proven on S1's built website. Its worklist is now **CLOSED** (see
  [[scenario-plan-reverse-mapping]]): 3 of 4 "gaps" were SR-wording mis-statements (SE-05/10/11), SE-16 a
  generator fix, and `website-improvement` (CL3 practice) was kept + refreshed.
- **⚠ Run-sheet was RELINEARISED — it is now 12 steps** (scenario **plan** = step 6, scenario
  **materials/website** = step 7, then **8 assessor / 9 student / 10 mapping / 11 cluster-coverage / 12
  pre-validation**). Older notes used the 11-step numbering — ignore those numbers.
- **Gate 8 assessor (`validate-at-traceability`)** — back-tested on current S1: **PASS 8/8** (CL1×3, CL2×2,
  CL3×3 — every criterion tagged, every reference a real UoC item; no phantoms/orphans). Run with `python`
  (not `python3`) on this machine.
- **Gate 10 mapping (`validate-mapping-doc --cluster <C>`)** — **PASS** all 3 clusters / 8 docs
  (completeness + accuracy). Advisories left for the human pre-validation eye: FS/AC closest-fit cells, and a
  CL2 AC discrepancy (**AC#5 ICTCLD501 / AC#4 ICTCLD505 doc=`C1` vs benchmark=`D1`**) — passes because AC is
  satisfied by assessment *setup*, but flag it at Gate 12.
- **Gate 11 cluster-coverage (`validate-cluster-coverage --cluster <C>`)** — **PASS 3/3**: every consolidated
  UoC item evidenced by ≥1 AT in every cluster.
- **Gate 9 student instruments** — all **8 present** (1:1 with assessors). **Mechanical leak-lint now built
  (2026-07-09): `validate-student-instrument`** — HARD-fails a `*-Student.docx` that leaks assessor-only
  material (UoC mapping tags `[UNIT SEC num]`; Benchmark / Model Answer / Assessor Instructions / Marking
  Criteria labels), WARNs on softer VET vocabulary; the UoC footer, "Knowledge Evidence" deliverable names
  + criterion codes are legitimate and pass. **PASS all approved S1 student copies** (CL3-AT2 one advisory
  warn); assessor copies FAIL hard (calibration proof). *Completeness / in-world tone* stays the human part.
  **Gate 12 institutional pre-validation** — human; the **only fully-human gate now outstanding** for S1.

**Instruments unified to ONE generator process (2026-07-09).** CL1's AT1/AT2/AT3 assessor+student
instruments were **hand-authored Word docs** (docx metadata: App=Word, creator="Academic Governance &
Quality"); CL2/CL3 were already script-generated. Retro-fitted CL1 to the same process — per-AT
`scripts/s1_cl1/build_s1_cl1_atM_{assessor,student}.py` fill the Kangan template via the shared umbrella
`helpers.docx_tables` engine (student single-sources shared content from the assessor). Proven faithful by
the new **`validate-instrument-reproduction`** skill (umbrella `.claude/skills/scripts/`): body text +
order equivalence vs the committed doc, a deliberate change absorbed via `--sub` (applied post-normalise so
a plain-space rule matches an NBSP). Each regenerated instrument was verified **content+order identical to
the git-HEAD original except the deliberate change**, all 6 PASS, students still leak-clean. Made
**EVERGREEN**: the embedded intranet URL (`https://www.placeholder.com.au`) was DROPPED (name the site, not
the URL — students told the live URL out-of-band), so docs never go stale on a URL change. The **6 committed
.docx were regenerated in place = canonical**. Net: **no second authoring path — every cluster's instruments
are edit-the-builder-and-regenerate.** (`brand.WEBSITE_URL` was tried then reverted — evergreen needs no URL
constant.) **Website base URL set to the deployed domain (2026-07-09):** `astro.config.mjs` `site:` +
`robots.txt` sitemap + the sign-in/contact/README pages + `scenario/website.md` now use
`https://yat.timbaird.com` (the real canonical URL — infra config for sitemap/canonical/OG, *not* an
evergreen-doc concern; instruments stay URL-free). The website **auto-deploys on push to `main`**, so the
change goes live on commit (no manual redeploy).

**Architecture (decided):** per-cluster `assessment_plan.md` = **authored source of truth**; the
**consolidated plan = derived** (generated, never hand-edited); the **scenario plan** (next) validates
against the consolidated **SR-*** register. `SR-*` ids are **cluster-scoped** (`SR-CL3-01`) so registers
union without collision. AC items are discharged via the SR register's **AC-link** column.

**STATUS — assessment run-sheet PROVEN END-TO-END on S1 (2026-06-23).** All deterministic gates (1–8, **9
leak-lint**, 10, 11) PASS; the run-sheet takes S1 to **"everything placed, only human pre-validation
remaining."** Gate 9's mechanical half is now automated (`validate-student-instrument`, 2026-07-09); its
residual *quality/completeness/tone* review + **Gate 12** (institutional pre-validation) are the only
human-owned checks. Gate 12 is the single fully-human gate.

**The delivery run-sheet is now underway** — see [[delivery-run-sheet]] (process-delivery.md restructured
to step→gate; Step 1 built + back-tested on S1). **Deferred follow-up (non-blocking):** generate the
branded `YAT-Website-Improved-Solution-Design` download asset (delivery-side parity). Related:
[[mapping-pipeline]], [[scenario-plan-model]], [[scenario-plan-reverse-mapping]].
