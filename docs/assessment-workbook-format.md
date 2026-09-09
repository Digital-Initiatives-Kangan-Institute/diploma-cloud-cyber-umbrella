# Assessment workbook format

The current approach to authoring an assessment instrument: a **workbook** the student works through
one framed task at a time, rather than a brief plus a blank template they fill in on their own.

The instrument is one document. The student reads a task, does the thing, and writes the answer in the
box under it. The assessor reads the same document with the answers filled in, each element tagged with
what it evidences and what has to be true for that to be met.

This document is the format standard for that instrument, the rules for when a separate template
survives alongside it, and the process for converting or authoring one. It is course-agnostic: the
engine lives in the umbrella, and a course supplies content.

## Why this shape

A large blank template asks a student to hold the whole shape of an unfamiliar document in their head
before they can write the first sentence. Most of what goes wrong at that point is structural, not
technical — they do not know what the section wants, so they write around it.

The workbook removes that. It supplies the order, the framing and the capture surface; the student
supplies the thinking. The evidence then lands next to the task that produced it rather than in an
appendix, which is also where an assessor wants to find it.

**The trade this makes:** the student never produces the professional document. Where a unit requires
one, the workbook does the thinking and a closing task assembles it — see *When a template survives*.

## One definition, rendered two ways

A workbook is authored once and rendered per mode:

| Mode | What it is |
|---|---|
| `student` | the blank sheet — the job, empty capture tables, empty screenshot boxes, empty response boxes. No UoC tags, no marking language |
| `assessor` | the same document worked — model answers in teal, screenshot boxes replaced by a description of what should be in them, each element carrying `Evidences:` and `Satisfactory when` |

A third rendering, the **practice** sheet, passes its own content lists through the same renderer — same
shapes, different scenario — so practice and assessment cannot drift structurally even though every
value in them differs. Practice adds what the assessment withholds: click-by-click steps, leading
questions, a worked exemplar row, and a personal-notes box.

Nothing about a task exists twice. A student copy and an assessor copy that disagree is a class of bug
this format removes rather than manages.

## The element schema

A content module is a list of dicts. `helpers/run_sheet.py:element()` renders one:

| Key | What it does |
|---|---|
| `n` | task number — what later tasks reference when they copy an answer forward |
| `title` | the heading |
| `prompt` | what the student is asked |
| `resources` | `[(label, url)]` — the scenario documents this element needs, each label saying *why* it matters here |
| `table` | `(columns, model_rows)` — a capture table the student fills |
| `given` | how many leading columns of `table` are pre-filled for the student |
| `blank_rows` | how much room an un-given table offers |
| `exemplar` | how many leading rows render worked — **practice only** |
| `points` | key points a written response should touch on |
| `diagram` | caption for a drawing slot |
| `uoc` | the UoC items this element evidences — **assessor copy only** |
| `standard` | what must be true for them to be met — **assessor copy only** |
| `clicks` | click-by-click steps — **practice only** |
| `consider` | leading questions — **practice only** |

An element with no `uoc` and no `standard` renders as scaffolding: it is not a marking criterion, and
its prompt should say so in words the student can see ("Preparation — not assessed").

## The scaffolding dials

`given` and `exemplar` are the two places where an author decides how much to hand over. Both are worth
setting deliberately rather than by habit.

- **`given`** pre-fills leading columns. Pre-fill a column when knowing it is not the evidence — a
  student does not demonstrate a recovery-objective criterion by knowing that a database has one. Leave
  it blank when the column *is* the finding the item asks for.
- **`blank_rows`** sets how much room an un-given table offers. Three blank rows on a "list every single
  point of failure" table reads as *there are three*.
- **`exemplar`** shows the shape of an answer by working the first row. Practice only, and it must never
  be one of the answers the task is actually asking for — where a task has one real answer, draw the
  exemplar from the current environment instead. Form without finding.

## The marking model

Every settings table in a workbook contains values invented so the student has a concrete task; the
unit's wording is usually vaguer than the task. So each element carries two assessor-only lines:

- **`Evidences:`** — which UoC items this element carries.
- **`Satisfactory when`** — what has to be true for them to be met.

**An assessor marks the second, never the table.** A student whose values differ but who meets the
stated standard is Satisfactory; one who matches the model answer exactly but misses the standard is
not. Writing the `standard` is the real authoring work — see
[cluster-authoring-conventions.md](cluster-authoring-conventions.md) §1 on traceability.

## When a template survives — and therefore when an exemplar does

The preferred position is that **everything the student produces is captured in the workbook**. A
separate fillable template is used only where a unit-of-competency requirement explicitly and definitely
calls for one.

Before keeping or building a template, find the item that requires a separate document and quote it.
The worked contrast, from S1:

| | What the unit's assessment conditions say |
|---|---|
| **ICTCLD501** | `AC 3` — *"reporting standards for documenting and communicating disaster recovery plan"*. A template survives: the DR Plan |
| **ICTCLD503 / 504 / 505 / BSBXTW401** | every AC is an environment or input condition — a vendor, a managed database, an IDE, a browser, data sources, a safe working environment. None names a document format. No template |

Note what this means for a PC like `[ICTCLD503 PC 2.4]` *"Document and justify architecture design"*: the
whole text of the item is those five words. **Document** is satisfied by the workbook being a written
record; **justify** needs genuine written reasoning, which is a task with a response box, not a filled
table cell. One justification task per unit element, placed where that element's final PC sits.

Where a template does survive, the workbook still does the generative work and its closing task copies
the answers across, with a map of task → template section. **Both are submitted.** The document is the
artefact marked for the documenting item; the workbook is the evidence the thinking is the student's own.

**Exemplars follow templates.** The assessor workbook already carries the model answers, so an exemplar
exists only where a student-fillable template does. Exemplars with no student submittable under the
current design are removed.

**Legacy content is not authoritative.** Trace it to a UoC item or drop it. The two failure modes worth
watching for are assessing what no item requires, and setting a bar well above what a vague item asks.

## Two conventions the tooling depends on

Both of these were learned by breaking them.

**Task numbering is continuous across the whole instrument.** Not restarted per part. Renumbering a
task is a **breaking change twice over**: the marking criteria's task ranges shift, and every delivery
deck's activity slides point at these numbers ("Workbook — tasks 5 to 9") — re-run the delivery
realignment loop for the affected topics. The traceability
validator resolves a criterion's `(tasks 12–14)` scope to workbook elements by number, so per-part
numbering makes any criterion beyond Part A unverifiable. It also reads better: a student following a
43-task workbook has one sequence, not three.

**Criterion codes are unique across the cluster.** The mapping engine inverts criterion tags into
`{UoC item: [criteria]}` with no AT attribution, so two ATs that both use `A1` cannot be told apart and
items land in the wrong AT column. Give each AT its own letter — S1-CL3 uses `D` for Design, `T` for
Team, `I` for Implement.

## Where the pieces live

Per [umbrella-engine-architecture](../.claude/memory/umbrella_engine_architecture.md), the engine is
course-agnostic and lives in the umbrella; a course supplies content.

| | |
|---|---|
| `scripts/helpers/run_sheet.py` | the workbook engine — the rendering primitives and `element()` |
| `scripts/helpers/workbook_instrument.py` | derives the marking guide, the reverse map and the mapping engine's `BENCHMARK` from the workbook's tags; and `assemble()`, which fills the institutional template |
| `scripts/tests/test_run_sheet.py` | holds the student/assessor split and the scaffolding dials |
| `<content-repo>/scripts/<cluster>/s?_cl?_at<N>_run_sheet.py` | the content — task lists plus a `render()` laying out that AT's document spine (CL1 uses the bare `atN_` form; a large AT may split across part files, e.g. CL2 AT1's `_part_{a,b,c}_`) |
| `<content-repo>/scripts/<cluster>/*_practice_run_sheet.py` + `build_*_practice.py` | the practice twin — same structure through the assessment's own renderer, different specifics, guidance added, marking apparatus stripped |
| `<content-repo>/scripts/<cluster>/build_..._assessor.py` | the instrument: institutional front matter, the criteria map, and the build |
| `<content-repo>/scripts/<cluster>/build_..._student.py` | a thin entry point calling the assessor module in `student` mode |

## The marking apparatus is derived, not written

An instrument says the same thing in three shapes: the workbook's per-element tags, the marking guide's
traceability lines, and the reverse-map table. Hand-maintaining the second and third is how they drift.

The author declares only which tasks each criterion groups:

```python
CRITERIA_MAP = [
    dict(code="A1", tasks=["1-3"], text="Scaling needs and current-state review …"),
    dict(code="A2", tasks=["4"],   text="Services identified …"),
]
```

Everything else is computed — the UoC line on each criterion, the reverse map (with verbatim UoC wording
read from `consolidated_uoc.md`), and `BENCHMARK` for the mapping engine. A tag added to a task reaches
all three without anyone remembering. Two failures are raised at build time rather than shipped:

- a criterion grouping tasks that carry no tags — it would be a free-floating criterion
- a tag that does not resolve in `consolidated_uoc.md` — a phantom

## Authoring or converting one

1. **Read the units, not the old instrument.** Pull the verbatim items the assessment plan assigns to
   this AT. Every task exists to evidence one of them.
2. **Decide what a template is doing, if anything.** Quote the AC that requires it, or drop it.
3. **Order the tasks the way the work happens.** Where a template survives, order them to its section
   order so the closing copy-out is transcription rather than translation.
4. **Write each element**: the framing sentence, the capture surface, the `uoc` tags, and the `standard`.
   The standard is the part that takes the time.
5. **Group the criteria** — declare `CRITERIA_MAP` and let the rest derive.
6. **Build both copies and check**: the coverage against the plan, no phantom tags, and
   `validate-student-instrument` on the student copy.
7. **Run the gates** — Gate 8 traceability, Gate 9 leak lint, Gate 10 mapping, Gate 11 cluster coverage
   (see [process-assessment.md](process-assessment.md)).

## Related documentation

- [process-assessment.md](process-assessment.md) — the run-sheet this instrument is step 8–9 of.
- [cluster-authoring-conventions.md](cluster-authoring-conventions.md) — UoC traceability and the
  standing conventions for any assessment artefact.
- [document-template-system.md](document-template-system.md) — the branded YAT document system, for the
  templates that do survive.
- [mapping-document-standard.md](mapping-document-standard.md) — the Assessment Mapping documents this
  instrument's `BENCHMARK` feeds.
