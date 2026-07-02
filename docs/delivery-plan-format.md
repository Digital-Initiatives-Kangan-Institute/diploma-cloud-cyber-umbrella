# Delivery-plan format — standard

**Audience:** humans and LLM agents producing a cluster's **delivery plan outline** — the last step of
the [delivery run-sheet](process-delivery.md). Paths are relative to the `diploma-cloud-cyber-content/`
repo root.

A cluster's **delivery plan** lays the Topics, practice and assessments onto a concrete session grid and
is issued as the institutional `…_Delivery_Plan.docx`. Unlike every earlier delivery artefact, the plan
is **semester-instance-specific, not a course artefact**: the course can be fully developed (assessment,
decks, practice) with no delivery plan at all, because the plan depends on facts that do not exist until
a specific intake is imminent — how many sessions that intake actually gets, on which days, and which
sessions are **online** vs **in the classroom** (typically known only ~2–4 weeks before the semester).
Re-run the step for a different intake and you get a different plan from the same course. **The plan is
disposable-per-instance; the course it is built from is not.**

Those instance facts are a **prerequisite**. Once they are known, the plan is produced in a
**collaborative human-AI juggling session** — try a layout, look at it, move things, refit — until the
sequence works (spacing, catch-up placement, on-campus practical/presentation vs online balance). That
sequencing is **human judgment and stays human**; this format does not try to reduce it to rules. What
the format *does* is capture the outcome of that session as a machine-readable **outline
(`<cluster>/delivery/delivery-plan.md`)** whose **completeness can be checked** — so the AI knows when
the juggling session has produced *enough* to generate the docx, and can keep prompting the human for any
decision still missing. When the outline validates, an automated step fills the docx from it.

**This document is the single source of truth — for what the outline contains *and* for what the
validator checks.** It informs the producing session and is an **input to validation**: the linter reads
its [skeleton](#skeleton) (below) to learn the required headings, header fields and grid columns rather
than hard-coding them. Three layers run on the plan, in order:

- **The juggling session (production — main session):** the guided human-AI conversation that *produces*
  the outline for a specific intake — the main session takes the prerequisite facts, works the layout
  with the human turn by turn, and writes the outline **to this format**. It is **not** a sub-agent:
  producing the plan is interactive human dialogue, which only the main session can do. *(Runs at
  instance-time; there is no standing skill for it yet — the format + gate are what exist now.)*
- **`validate-delivery-plan` (linter — deterministic):** the **completeness-for-generation** gate —
  every heading, header field and grid column **named in the skeleton** is present, the session grid is
  internally consistent (numbered `1…N` with no gaps, every cell decided), **every Topic and every
  assessment is placed**, and the grid **reconciles with the frame** (`cluster-specification.md`). Any
  gap is reported so the human can be prompted. Driven by this doc; no field list of its own.
- **(agent validator — judgment):** there is **none**, by design. Whether the *sequence* is good — the
  spacing, the catch-up cadence, the online/classroom mix — is the human's call made live in the
  juggling session, not something a validator should second-guess.

**Step gate (Step 6).** The plan's gate is **per-instance**: an outline for a given intake is ready to
generate the docx when it **passes** `validate-delivery-plan`. There is no semester-level phase gate
after it — Step 6 is the terminal step, run once per intake.

## Prerequisites (what must be known before the juggling session)

The plan cannot start until the intake's concrete shape is known. These are recorded in the outline's
`## 1. Instance prerequisites` block so the plan is self-describing and the reconciliation has something
to check against:

1. **Intake** — which semester/intake this plan is for (it is not reusable across intakes).
2. **Total sessions available** — how many class sessions this intake actually gets (may differ from the
   frame's nominal total; the validator reports any divergence).
3. **Teaching days per week** and **which days** — e.g. 2/week, Tuesday + Thursday.
4. **Online/classroom split** — how this intake's sessions are allocated across delivery modes (the
   thing that is not knowable until close to delivery, and that drives what practical/presentation work
   can go where).

## Required sections (in order)

This is the human-readable description; the **[skeleton](#skeleton) is the authoritative machine-readable
contract** the linter parses.

1. **Header banner** — title `# <cluster> — Delivery Plan (<intake>)`; a `> **INSTANCE:** …` line naming
   the intake and pointing at the frame + the docx to be generated.
2. **`## 1. Instance prerequisites`** — the prerequisite facts, as labelled `- Field: value` lines:
   `Intake:` · `Total sessions available:` · `Teaching days per week:` · `Teaching days:` ·
   `Online/classroom split:`.
3. **`## 2. Session grid`** — a markdown table, **one row per session**, columns:
   `#` *(session number, contiguous `1…N`)* · `Week` · `Day` · `Mode` *(`online` or `classroom`)* ·
   `Activity` *(one of `onboarding` / `teach` / `practice` / `practical` / `presentation` /
   `assessment` / `spare`)* · `Placed` *(what runs — Topic(s) as `T<n>`, practice as `[EX]`, an
   assessment as `AT<n>`, or `—` for a reserved/empty session)*.
4. **`## 3. Notes / decisions`** — free prose the human wants on the record: sequencing rationale,
   where catch-up lands, why a Topic spans the sessions it does. Not judged by the linter.
5. **`## Changelog`** — dated entries.

## What the linter checks

`validate-delivery-plan` is deterministic and stdlib-only. **It reads this document's
[skeleton](#skeleton) to learn the contract** (the `## …` headings, the `- Label:` header fields, and
the `## 2. Session grid` **column names**), then against a plan it:

- confirms every heading, header field and grid column **named in the skeleton** is **present** (header
  fields also non-empty);
- checks the **session grid is internally consistent**: session numbers run **contiguously `1…N`** (no
  gaps, no duplicates); **every cell is decided** — `Week`, `Day`, `Mode`, `Activity` non-empty and
  `Placed` present (an intentionally-empty session is written `—`, not left blank);
- checks **every value is in vocabulary**: `Mode ∈ {online, classroom}`, `Activity ∈ {onboarding, teach,
  practice, practical, presentation, assessment, spare}`;
- checks **coverage of placement** — enumerates the cluster's built Topics (`delivery/topic_NN/`) and its
  assessments (`assessments/AT<n>/`) and confirms **each is placed** somewhere in the grid (`T<n>` /
  `AT<n>` in a `Placed` cell). A Topic or AT with no session is a **gap** (fail) — the plan dropped it;
- **reconciles with the frame** (`cluster-specification.md`): the grid's row count equals the outline's
  declared `Total sessions available`; it **reports** how that compares to the frame's nominal `Total
  sessions` (a divergence is information — the intake's real allocation, not a failure); and it confirms
  the reservations the frame budgets for are honoured (**fails** if the frame budgets an onboarding or
  spare session but the grid has none of that activity);
- **reports** the mode split (online vs classroom) and the assessment-session count vs the frame's
  dedicated-assessment budget.

It does **not** judge whether the *sequence* is good — that is the human call made in the juggling
session. Exit `0` on PASS, `1` otherwise. A PASS means the outline is **complete enough to generate the
docx**; every failure is a decision still to be made.

## Skeleton

```markdown
# S1-CLn <Cluster Name> — Delivery Plan (<intake>)
> **INSTANCE: <intake>.** Frame: cluster-specification.md · Generates: S1_CLn_Delivery_Plan.docx

## 1. Instance prerequisites
- Intake: 2026-S1
- Total sessions available: 30
- Teaching days per week: 2
- Teaching days: Tuesday, Thursday
- Online/classroom split: classroom for practical + presentation sessions; online for lecture/teach

## 2. Session grid
| #  | Week | Day | Mode      | Activity     | Placed        |
|----|------|-----|-----------|--------------|---------------|
| 1  | 9    | Tue | classroom | onboarding   | —             |
| 2  | 9    | Thu | online    | teach        | T1            |
| 3  | 10   | Tue | classroom | practice     | T1 [EX]       |
| .. | ..   | ..  | ..        | ..           | ..            |
| 28 | 17   | Thu | classroom | assessment   | AT2           |
| 29 | 18   | Tue | classroom | spare        | —             |
| 30 | 18   | Thu | classroom | spare        | —             |

## 3. Notes / decisions
- <sequencing rationale, catch-up placement, mode choices worth recording>

## Changelog
- <date> — initial plan for <intake>.
```

## See also

- [process-delivery.md](process-delivery.md) — the delivery run-sheet; this plan is **Step 6**, the
  terminal per-instance step.
- [cluster-specification-format.md](cluster-specification-format.md) — the frame (Step 1) this plan is
  reconciled against; the sister format that this one mirrors.
