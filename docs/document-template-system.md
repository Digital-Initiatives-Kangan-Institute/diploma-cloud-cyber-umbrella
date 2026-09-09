# Document template system

A branded document-generation system produces the YAT/MTS documents a course's assessments are built
around — the Business Case, Solution Design, Deployment Report and DR Plan (plus the Business Case
Presentation deck). Python scripts (`python-docx`, `python-pptx`) generate `.docx`/`.pptx` from the
brand pack. This document records the build model, the shared helpers, the document set, the artefact
roles, and the conventions that keep templates, exemplars and models consistent.

Build scripts and assessor exemplars live in the **content repo**; served templates and student-model
PDFs live in the **website repo** (`public/`).

## How realistic, and when realism yields

These documents sit inside a scenario, and the current approach is to make them **as realistic as is
practicable — stopping wherever realism would cost the student**. The aim is not to mimic a real
organisation's document practices as closely as possible. Where a realistic convention makes a
deliverable harder to read, harder to complete, or harder to be certain about, the convention gives
way and the student experience wins.

The clearest worked case is template scoping, below: a real organisation would keep one document
template per type and expect the author to judge which parts apply. That is realistic, and it is what
this system used to do. In practice students read an inapplicable section as a required one, so the
templates are now scoped per deliverable instead.

## Build model

Build scripts live in `scripts/`. Do not hand-edit a generated `.docx`/`.pptx` — edit the script and
regenerate, or the change is lost on the next build and can't be reviewed in a diff. Dependencies:
`python-docx`, `python-pptx`, installed in the umbrella's `scripts/.venv`.

Workflow for served artefacts: an agent builds the `.docx`, Tim prints it to PDF, and the agent wires
it into the intranet.

## Shared helpers (reuse, don't duplicate)

The course-agnostic helpers live in the **umbrella** at `scripts/helpers/`, imported by every course's
build scripts:

| Module | Holds |
|---|---|
| `scenario_document.py` | `configure_styles`, `build_header_footer`, `wordmark` |
| `docx_styling.py` | `set_cell_borders`, `shade_cell`, `add_field`/TOC, `paragraph_bottom_rule` |
| `docx_body_text.py` | `add_body_paragraph`, `add_guidance_text`, `add_response_placeholder`, `add_bullet_list` |
| `docx_tables.py` | `add_template_table`, `add_data_table`, `set_cell_content`, and the Kangan instrument-table helpers |
| `docx_callouts.py` | `add_convention_box`, `add_applicability_note` |
| `docx_evidence.py` | described-evidence blocks for exemplars |
| `instrument_layout.py` | the assessment-instrument layout functions shared by assessor and student copies |
| `pptx_brand.py`, `kangan_deck.py`, `deck_images.py` | deck helpers |

Each course supplies its own `brand.py` in its content repo `scripts/`. Brand per
`scenario/branding/brand-pack.md` §4/§5.2/§5.3: teal `#1F5A5C` headings, terracotta `#C5613B` accent,
**ochre `#C99932` disclosure banner in the page header (docx) / master-slide footer (pptx) on every
page**, cream cover band, Source Sans 3, professional cover, and a Word TOC field.

## Document set — the consulting chain

Business Case (why) → Solution Design (what/how) → Deployment Report (what was built); plus the
Business Case Presentation deck, the DR Plan and the Team Plan.

## Template scoping — one template per deliverable

**A template holds exactly and only what the deliverable it serves requires.** Nothing in it should
need to be skipped, and nothing should carry an "applicability" caveat. A student opening it should be
able to treat every section as theirs to complete.

Where two assessments produce the same *kind* of document but ask for different things, they get
separate templates rather than one superset with parts marked inapplicable — and naming follows what
the template actually is, so a template serving one assessment says so in its filename rather than
presenting itself as a standing organisational document.

**The library is the set of templates an assessment asks for.** The intranet Templates page carries
those and nothing else: offering a template no criterion marks invites a student to write their
assessment into it. A survey of all eight S1 instruments found three — the Business Case and its
board-presentation deck (S1-CL1 AT1), and the Disaster Recovery Plan (S1-CL2 AT1). The Solution
Design, Deployment Report and Team Plan templates were retired when those assessments became
workbooks that capture the work themselves. The page lives at the website repo's
`src/pages/intranet/[state]/templates/index.astro`; add an entry when an assessment starts asking
for a deliverable document.

## When a deliverable template is needed at all

The current approach is that an assessment instrument is a **workbook** which captures the student's work
itself, so a separate fillable template is used only where a unit-of-competency requirement explicitly
demands one — and an **exemplar exists only where such a template does**, because the assessor copy of the
workbook already carries the model answers. Templates and exemplars with no student submittable under the
current design are retired.

The test is to quote the assessment condition that requires a document. `[ICTCLD501 AC 3]` — "reporting
standards for documenting and communicating disaster recovery plan" — requires one. `[ICTCLD503]`,
`[ICTCLD504]` and `[ICTCLD505]` name only environment and input conditions, so their "document and justify"
criteria are met by the workbook. See
[assessment-workbook-format.md](assessment-workbook-format.md).

The roles below apply to the templates that do survive.

## Artefact roles per document type

1. **Fillable template** — the document the student completes, served from the website repo
   `public/templates/` and wired to the intranet Templates page. Scoped to its deliverable (above). It
   carries no UoC tags and no marking language, but it *does* carry every section the deliverable
   needs — including knowledge-evidence questions and reflection prompts where the deliverable
   contains them.
2. **Assessor exemplar** (worked model answer) — **retains** UoC `Evidences:` tags plus the knowledge
   evidence and reflections; cover says "internal marking reference". Lives in the content repo
   `assessments/AT*/`.
3. **Student model** (finished in-world document) — no assessment scaffolding; a past project's real
   deliverable, downloadable as a **PDF** from the website repo `public/documents/`, linked via a
   project `.md`. The `lms-replacement` project carries the full Business Case + Solution Design +
   Deployment Report chain.

## Key conventions

- **A template carries no UoC tags and no marking language.** Those belong in the assessor exemplar
  and the instrument. This is about *marking* apparatus, not about content shape — a deliverable that
  genuinely contains knowledge-evidence questions has them in its template.
- **Course-side notes are violet** — `6A3EA1` at 9pt, distinguishing anything addressed to the student
  from the report content addressed to its in-world reader. Every violet note tells the student to
  delete it before submitting. Two kinds are in use:
  - *Guidance notes* — a "Getting started" prompt and any links into the scenario site, placed where
    the section's own grey guidance doesn't already make the source obvious.
  - *Supplied-section markers* — a single line above a pre-written section, saying the text below is
    part of the report, is not theirs to write, and should be left as it is.
- **Evidence goes where it is evidence of something — not in an appendix.** Where a screenshot or
  capture is required, the template puts the drop-zone in the section that section evidences, right
  under the step that produces it. Appendices of collected screenshots are what the deliverable used
  to do; they cost the student a filing decision for every capture, invite the same image being filed
  twice, and separate the evidence from the claim it supports.
- **Instrumented steps.** Where a template asks for a test or a capture, it also gives the steps to
  produce it — numbered, specific, followable without prior knowledge — and states what the capture
  must show. This is a deliberate trade of realism for clarity: a real deployment report would never
  tell its reader how to open a console. The report is also an assessment instrument, and where those
  two purposes conflict, the student not having to guess wins.
- **Supplied sections.** Where a section's content is the same for every student — fixed engagement
  context, a scope dictated by an approved design — it is pre-written into the template behind a
  supplied-section marker, in normal body styling so it reads as report content. It is not marked, and
  the assessment instrument says so. This removes writing that evidences nothing while keeping the
  deliverable a complete, coherent document.
- **Exemplar evidence is committed beside the generators** (`assessments/AT*/exemplar-evidence/`
  screenshots) so the assessor copy regenerates worked rather than blank. Student-facing models of the
  assessed builds stay off the site where they would leak an answer; the served in-world documents
  (e.g. the LMS deployment report) belong to already-completed scenario history, not the assessed work.
- **Served artefacts → website repo `public/`; internal exemplars → content repo.**
- The supplied AT2 baseline design is the branded Solution Design **PDF** on the intranet; it doubles
  as the model for AT3, where students author their own HA Solution Design.
- **Feedback is captured in-deliverable, not as a standalone Feedback Record.** Each key deliverable
  carries a review/sign-off block where the role-played superior writes comments and signs off — the
  natural document → feedback → sign-off cycle. In the surviving templates that block is the
  reviewer-feedback table plus a sign-off table with an *Approved / Approved with comments / Rejected*
  decision; in the workbook instruments the same cycle runs as walkthrough → feedback → sign-off
  tasks.
- **A block a deliverable's assessment doesn't look at doesn't belong in its template.** A review or
  sign-off block belongs where a criterion marks it; where no criterion does, it is furniture the
  student fills in for nobody.

## Related documentation

- [website-architecture.md](website-architecture.md) — where served artefacts live.
- [scenario-flow.md](scenario-flow.md) — the in-world scenario the documents sit within.
- [process-delivery.md](process-delivery.md) — how teaching and assessment are sequenced.
- [cluster-authoring-conventions.md](cluster-authoring-conventions.md) — cluster-level authoring rules.

For LLM agents: per-cluster delivery state and draft-naming pragmatics are held in memory rather than
in this document.
