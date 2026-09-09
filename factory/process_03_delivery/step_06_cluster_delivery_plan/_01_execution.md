# Step 06 — Execution

The step performed, in order. Before starting, confirm every item in
[`_00_prerequisites.md`](_00_prerequisites.md) holds.

## The sequence

1. **Read the frame.** Take total sessions, session length, and the reservations budgeted — onboarding,
   spare, dedicated assessment — from the cluster's `cluster-specification.md`.
2. **Build the calendar.** From P1 and P2, enumerate every real session with its date, week and slot,
   across the teaching weeks. → [A](#a--building-the-calendar)
3. **Scan public holidays.** Check the class days against the jurisdiction's holidays and rule out any
   that collide. → [B](#b--the-public-holiday-scan)
4. **Enumerate what must be placed.** List every built Topic (`delivery/topic_NN/`) and every assessment
   (`assessments/AT<n>/`). The validator fails if any is missing from the grid.
5. **Derive the sequencing constraints.** Read each Topic's `coverage.md` for the AT it teaches, and the
   assessment plan for any approval gate that fixes order. → [C](#c--sequencing-constraints)
6. **Set the teaching rate.** Start at **one Topic per session** and confirm it with the operator; adapt
   on request rather than fitting hours to sessions.
7. **Take the assessment allocation.** Ask the operator how many sessions each AT gets (P6).
   → [D](#d--assessment-time-is-the-operators-call)
8. **Do the arithmetic.** Sessions available minus teaching minus assessment equals in-term contingency.
   Report the delta rather than filling the space. → [E](#e--the-arithmetic)
9. **Reconcile against the frame.** Where the intake contradicts what the frame budgets, amend
   `cluster-specification.md` and re-validate it — do not bend the plan to a stale frame.
   → [F](#f--amending-the-frame)
10. **Sequence the grid with the operator.** Place the blocks, honouring the constraints from item 5.
    This is human judgement made live and is not reduced to rules.
11. **Write the outline** to `delivery/delivery-plan.md`, conforming to
    **[`_02_delivery-plan-format.md`](_02_delivery-plan-format.md)**.
12. **Validate.** Run **[`scripts/validate_cluster_delivery_plan.py`](scripts/validate_cluster_delivery_plan.py)**.
    Every failure is a decision still to be made. → [H](#h--running-the-validator)
13. **Generate the docx** from the validated outline with **`scripts/build_delivery_plan.py`**
    *(not yet built)*. → [G](#g--what-the-docx-needs-that-the-outline-does-not-carry)

Then the step's exit condition: [`_03_gate.md`](_03_gate.md).

---

## Detail

### A — Building the calendar

Sessions are real dates, not slot counts. From the start date and the completion date, enumerate the
teaching weeks, then place each weekly slot on its actual date. Carry the date into the grid: the
institutional template has a Session date field per session, and a plan that only counts sessions cannot
fill it.

### B — The public-holiday scan

Check the jurisdiction's public holidays against the days this cluster actually teaches, and rule out
collisions before the arithmetic — a lost session changes the delta.

Two traps worth knowing. A holiday can fall on a teaching day without affecting the cluster if the
cluster does not own that day (Melbourne Cup, Tue 3 Nov 2026, misses a Thu/Fri cluster entirely). And
some holidays **move year to year** — Victoria's AFL Grand Final Friday is set by the season fixture, so
it must be looked up for the specific year rather than assumed.

### C — Sequencing constraints

Rate and order are separate decisions. Item 6 sets how fast Topics are taught; this sets what may follow
what.

Each Topic's `coverage.md` declares the AT it teaches via its `**AT<n> content Topic**` marker, which
partitions the Topics by assessment. The assessment plan then supplies the ordering: where an AT is an
**approval gate** — a design signed off before it is built — every Topic teaching the dependent AT must
follow that AT's completion. Getting this wrong produces a grid that validates and is pedagogically
wrong, because the validator does not check order.

### D — Assessment time is the operator's call

How long an assessment needs is not derivable from the workbook's task count: it depends on how much is
supervised in class versus done in the student's own time, and on cohort size for anything presented or
observed. Ask; do not infer. A useful frame is whole weeks — "two weeks of classes per assessment" is
easier to judge than a session count.

### E — The arithmetic

The purpose is to expose the delta, not to consume it. Map what is available, subtract what is needed,
and report what is left as contingency — then let the operator decide where it sits.

```
sessions available  (teaching weeks × slots per week, less holidays)
  − teaching        (one per Topic, unless the rate was adapted)
  − assessment      (the operator's allocation per AT)
  = contingency     (in-term slack)
```

Post-term weeks (P3) are held **separate** from this and are not planned into. Naming them distinctly —
in-term contingency versus a reserve that is not expected to be used — keeps the plan honest about
where it intends to finish.

### F — Amending the frame

The frame is checked, not merely read: the validator fails if the frame budgets an onboarding or spare
session and the grid has none. When the intake genuinely differs — a mid-semester cluster inheriting an
already-onboarded cohort does not need an onboarding session — the correct move is to amend
`cluster-specification.md`, record why in its changelog, and re-run `validate-cluster-spec`. The frame is
a current working decision, not a fixed constraint.

### G — What the docx needs that the outline does not carry

Three gaps between a validated outline and a fillable institutional document:

- **Per-session UoC mapping** — the template's PC / LO / Know / Skill / Cond column. Derivable from each
  placed Topic's `coverage.md` tags; hand-filled for CL1.
- **Assessment type** per assessment session — Written / Project / Obs / 3rdP.
- **Mode translation** — the outline says `online` / `classroom`; the template's dropdown is FTF / O / WP.

### H — Running the validator

The validator is **driven by the format standard**: it parses the `## Skeleton` block of
[`_02_delivery-plan-format.md`](_02_delivery-plan-format.md) to learn the required headings, header
fields and grid columns. Change the skeleton and the presence checks follow — no code edit.

The format standard lives in this step folder, and the validator finds it there automatically — its
lookup understands the number-prefixed naming, so `--format` is only needed to point at a different
document:

```bash
python3 factory/process_03_delivery/step_06_cluster_delivery_plan/scripts/validate_cluster_delivery_plan.py \
  --plan <cluster>/delivery/delivery-plan.md
# or, the same file by another path:
#   --cluster-dir <cluster>
```

Scope is **one cluster**. `--plan` and `--cluster-dir` name the same file; the whole-of-semester plan is
step 07's separate validator.

Two things the skeleton **cannot** drive on its own: per-cell checks (non-empty, vocabulary membership)
run off a hardcoded six-role map, so a new column is required to *exist* but its cells go unchecked; and
ordering is not checked at all — see the `[TBD]` in [`_03_gate.md`](_03_gate.md).
