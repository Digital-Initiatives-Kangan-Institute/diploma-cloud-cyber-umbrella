# The factory

The courseware-development machinery, organised the way it actually runs: **factory → process → step →
gate**. A *process* is one run-sheet (a chunk of work with its own steps); a *step* is one unit of work
within it, holding everything that step needs — its instructions, the tools and scripts it runs, and the
gate that must pass before the next step starts.

This replaces the flat `scripts/` + `.claude/skills/scripts/` layout, where a file's name told you what
it did but never *where in the process it ran*.

## Naming

- `process_NN_<name>/` — one run-sheet. The number fixes display order.
- `step_NN_<name>/` — one step, a **folder** even when it holds a single file, so a step's shape is
  predictable and a step that grows needs no restructuring.
- Directory names may start with a digit; **filenames may not** — a filename becomes a Python module
  name, so it must be a valid identifier (`step_04_build_plan.py`, never `04_build_plan.py`).

## The shape of a step — being trialled, not settled

`[TBD — needs discussion: step shape]` — a **first attempt**, tried in exactly one place so far
(delivery step 06). It is not a convention and is not being rolled out. The intent is to work it until
that one step is genuinely useful, try it in a second step to see what has to change, and only consider
applying it more widely once it has firmed up through use.

The shape under trial has four parts, in this order. The distinction it is mainly testing is that
**prerequisites and gate are opposite ends of the step** — one is how you get in, the other is how you
get out — rather than two names for the same thing.

| Part | What it is |
|---|---|
| **Prerequisites** | The **entry** condition: (1) the previous step's gate has passed — which transitively guarantees every artefact the earlier steps produced; plus (2) anything else needed to start that no gate produces (typically facts about a specific intake, elicited from the operator). |
| **Step execution map** | The step performed, as a numbered sequence — each item **one or two sentences**, in the order it is done. Anything needing more explanation goes in *Detail* and is linked from the item. |
| **Gate** | The **exit** condition: the declared conditions that must hold before the next step starts. A condition may be a validator, a human review, an agent, or a combination. |
| **Detail** | At the foot of the document, lettered sections holding the explanation the numbered items link down to. Keeps the execution map scannable. |

The other step stubs are deliberately left alone — a shape that has been tried once is not worth
propagating to seventeen places, and retrofitting them now would make it expensive to change.

## Step numbering

Existing step numbers are preserved, so the docs, MEMORY entries and generated process maps do not have
to be renumbered:

| Process | Steps | Run-sheet |
|---|---|---|
| `process_01_extraction` | 01–03 | `docs/process-assessment.md` (its first three steps) |
| `process_02_assessment` | 04–12 | `docs/process-assessment.md` |
| `process_03_delivery` | 01–07 | `docs/process-delivery.md` (step 07 is new — not yet in the run-sheet) |

Extraction and assessment are one run-sheet split across two folders, so assessment continues at 04.
Delivery is a separate run-sheet and numbers itself from 01.

## Unit of development

`factory/` is **one unit** — one `venvs/test/`, one `requirements.txt`, one test plan
([`docs/test-plan.md`](docs/test-plan.md)), one suite. Processes and steps are organisation within it,
not units of their own: dependency profiles cut across process boundaries, `common/helpers/` is shared
between processes, and a step imports helpers so cannot be tested standalone.

`tests/` mirrors the implementation tree, so a test's location is derivable from the code's. Case IDs
are prefixed by the **surface** they cover (`CDP-01` for the cluster delivery plan, `HMDT-…` for the
markdown-table helper), so porting a step appends a section to the one plan rather than creating a new
unit. See the plan's own prefix legend.

## When a format standard changes

A step's format standard is the contract its validator reads, so changing it is a **behaviour change**
and takes the same route as any other — never a straight edit to the code. The order:

1. **Review the existing cases** against the change. Some describe behaviour that has moved: widen or
   reword them. Some may no longer be valid at all: retire them rather than leave a case asserting
   something the artefact no longer does.
2. **Then ask what is genuinely new** — and only add cases the reviewed ones do not already cover.
3. **Update the tests**, including any fixture the change invalidates.
4. **Then the code**, until the suite is green again.

Reviewing first is what stops the plan drifting into a pile of narrow, overlapping cases. Extending the
delivery-plan grid with `Date` and `Time` is the worked example: one existing case (an empty cell is
undecided) was written per-column and needed **widening**, not duplicating, and only two genuinely new
behaviours — a date that is not ISO, and dates running backwards — earned new cases.

## Migration — incremental, not big bang

The structure is installed; **nothing is ported yet**. Both layouts are live.

When work touches something still under the legacy layout, **ask the operator whether to convert it
now** — never convert unprompted, and never treat a task in the old layout as licence to reorganise it.
If the answer is yes, it moves to its `factory/process_NN_<name>/step_NN_<name>/` home **test-first**
(plan cases → tests → code, per [docs/test-first-process.md](../docs/test-first-process.md)) and leaves
nothing behind. If no, the work proceeds where it is and the conversion waits for another day.

`factory/` is authoritative for anything that has moved; the legacy locations remain authoritative for
everything else.

**Why this is worth doing** — in the flat layout a filename says what a script does but never where in
the process it runs, so a human has to already know the answer to find it. The structure is primarily
for human navigability; the secondary gain is consistent quality, since a predictable shape per step is
what stops the work being uneven between steps.

## Open

- `[TBD — needs discussion: helper migration]` — a helper cannot move alone: 90 scripts resolve imports
  by `sys.path.insert()` against the legacy path. Whether helpers move per-module as steps port, or in
  one pass, is open — see [common/README.md](common/README.md).
- `[TBD — needs discussion: gate declaration]` — whether gates are declared per step, in a per-process
  document, or both.
