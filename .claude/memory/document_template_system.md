---
name: document-template-system
description: Branded YAT/MTS document system — python-docx/pptx scripts generate Business Case / Solution Design / Deployment Report templates, exemplars + models from the brand pack
metadata:
  type: project
---

A branded document-generation system produces the YAT/MTS institutional documents (built 2026-06-01). **Build scripts live in `scripts/`** (source repo) and generate `.docx`/`.pptx` from the brand pack — **do not hand-edit the generated files; edit the script and regenerate.** Deps: `python-docx`, `python-pptx` (installed).

**Shared helpers (reuse, don't duplicate):** `build_bc_template.py` holds the docx helpers (palette, `configure_styles`, `build_header_footer`, `wordmark`, `set_cell_borders`, `shade_cell`, `add_field`/TOC, `guidance`, `response`, `table`); `pptx_brand.py` the deck helpers; `build_bc_exemplar.py` the filled-table/prose helpers (`etable`, `para`, `bullets`, `uoc`). Brand per `scenario/branding/brand-pack.md` §4/§5.2/§5.3: teal `#1F5A5C` headings, terracotta `#C5613B` accent, **ochre `#C99932` disclosure banner in the page header (docx) / master-slide footer (pptx) on every page**, cream cover band, Source Sans 3, professional cover + Word TOC field.

**Document set = the consulting chain:** Business Case (why) → Solution Design (what/how) → Deployment Report (what was built); plus the Business Case Presentation deck. A real org keeps **ONE template per type, NOT per-AT.**

**Three artefact ROLES per document type:**
1. **Generic template** (fillable) — in-world, **NO** assessment scaffolding (no UoC tags, KE, reflections, Student ID). Lives in **website `public/templates/`**, wired on the intranet Templates page via the `templates` array in `src/pages/intranet/[state]/templates/index.astro`.
2. **Assessor exemplar** (worked model answer) — **retains** UoC `Evidences:` tags + KE + reflections; cover says "internal marking reference". Lives in **source repo `assessments/AT*/`** (BC→AT1; deployment reports→AT2/AT3).
3. **Student model** (finished in-world doc) — no assessment scaffolding; a past/peer project's real deliverable, downloadable **PDF** from website `public/documents/`, linked via a project `.md`. (The AccentLoitte `lms-replacement` project carries the full BC + Solution Design + Deployment Report chain.)

**Key conventions:**
- **Generic template ≠ assessment instrument** — strip UoC/KE/Student-ID from templates; add them only in the AT-specific exemplar.
- **ONE superset template per type** with a **"Not applicable — [reason]"** convention for sections a given deployment doesn't need (mark, don't delete — proves completeness). The Deployment Report superset folds AT2 foundation tests + AT3 HA simulations. The *model* teaches the convention by marking sections N/A: the AT2 baseline marks HA sections N/A; the on-prem AccentLoitte marks cloud sections N/A but §5 cutover applies.
- **Deployment-report evidence is described, not fabricated** — `[SCREENSHOT — should show …]` placeholders (no real AWS captures available; deliberately **no student deployment-report model** — it would leak the AT2/AT3 build).
- **Served artefacts → website `public/`; internal exemplars → source repo.** Workflow: agent builds `.docx` → **Tim prints to PDF** → agent wires into the intranet.
- **The supplied AT2 baseline design** is now the branded Solution Design **PDF** on the intranet (AT2+), replacing the old wiki `.md` page; it doubles as the model for AT3, where students author their own HA Solution Design.
- **Feedback is captured in-deliverable, not as a standalone Feedback Record** (the inherited `ICTICT517_Feedback Record template.docx` is not used). Each key deliverable carries a review/sign-off block where the role-played superior writes comments and signs off — the natural document → feedback → sign-off cycle. The **Solution Design template has a §9 Review and Approval** block (§9.1 reviewer-feedback-and-author-response table + §9.2 sign-off table with an *Approved / Approved with comments / Rejected* decision); on the AT3 HA design this submission-to-superior carries the Group 10 feedback PCs (seek/respond/confirm feedback + provide for approval — 401 4.2, 502 5.2, 517 2.4, 517 3.3), because the *action plan* / *evaluation* a 517 PC names rides with the design's "how", not the business case's "should we". The Business Case sign-off block serves the AT1 strategic feedback/approval.

See [[website-current-state]] (where served artefacts live), [[s1cl1-delivery-state]] (Topic teaching decks), [[feedback-draft-naming-pragmatism]].
