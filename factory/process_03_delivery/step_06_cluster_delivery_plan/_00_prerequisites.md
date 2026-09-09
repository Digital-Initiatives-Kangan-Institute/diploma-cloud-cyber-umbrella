# Step 06 — Prerequisites

**Entry condition.** What must hold before the step starts. The step's *exit* condition is a different
thing entirely — see [`_03_gate.md`](_03_gate.md).

## 1. The previous gate has passed

**Gate 05 → 06** · *human review* — the practice covers the AT's parts, is re-scenarioed, and leaks
nothing.

That transitively guarantees the repo-side inputs this step reads, each being some earlier gate's output:

| Input | Produced by | Guaranteed by |
|---|---|---|
| `cluster-specification.md` — the delivery frame | step 01 | Gate 01 → 02 |
| `delivery/topic_NN/` — built Topics with `coverage.md` | steps 02–04 | Gate 04 → 05 |
| `assessments/AT<n>/` — completed assessments | process 02 | Gate 12 → done |

## 2. The instance facts are known

**No gate produces these.** They are facts about one specific intake, held only by the operator, and the
step cannot start without them.

| # | Required | Example |
|---|---|---|
| P1 | Semester start date, and the date all work must be completed by | starts w/c 5 Oct 2026; complete by 27 Nov |
| P2 | Class times — the days and slots this cluster owns | Thu 9–12, Thu 1–4, Fri 9–12 |
| P3 | Post-term scope — any weeks available beyond the completion date if students have not finished | two weeks, w/c 30 Nov and 7 Dec |
| P4 | Cohort size | presentation and observation assessments scale with headcount |
| P5 | Online / classroom split | typically known only 2–4 weeks out |
| P6 | Assessment time — sessions allowed per AT | see [`_01_execution.md` § D](_01_execution.md#d--assessment-time-is-the-operators-call) |
| P7 | Assessment type per AT — the institution's `Written` / `Project` / `Obs` / `3rdP` | a classification, not something to infer from the instrument — a technical build is `Project` even where it includes written responses |
| P8 | Cohort description — who this intake is | the only document-header field that **cannot** be derived from the repo; see below |

Ask for anything missing before starting. A step run on assumed instance facts produces a plan for an
intake that does not exist.

### The document-header fields, and where they come from

The institutional docx has five header fields. Four are derivable; one is not, which is why only that
one is a prerequisite:

| Field | Source |
|---|---|
| Qualification code and title | the course |
| Unit code and title | the cluster's `units_of_competency/` |
| Materials and resources | the cluster's own lab-packs, workbooks, decks and scenario site |
| LLN requirements | **derivable** — the units' Foundation Skills. CL2's `consolidated_uoc.md` already carries 23 `FS` items (Reading, Writing, Oral communication, Numeracy, Planning and organising) tagged per unit. `[TBD — needs discussion: LLN generation]` — no tool synthesises them into LLN prose yet, and this arguably belongs at extraction or assessment rather than here, since it is a property of the units, not the intake. |
| Cohort description | **P8 — operator input.** Group size, location, prior qualifications and delivery implications are facts about the people enrolled; nothing in the repo knows them. |

**Session dates and times are NOT prerequisites** — they are computed from P1 and P2 (start date,
teaching days, class slots), minus any public holiday. Asking for them would be asking twice.

→ Next: [`_01_execution.md`](_01_execution.md)
