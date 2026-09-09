# Slide-plan format — standard

**Audience:** humans and LLM agents authoring a Topic's **slide plan** — the gate before the deck is
built (delivery run-sheet, the deck step). Paths are relative to the **content repo**
root.

A Topic's **slide plan** (`delivery/topic_NN/slide_plan.md`) is the **kept, validated source** the deck
is built from — the teaching + exercise slides in deck order, each with its type, its **finished content**
(title + bullets, read verbatim by `build_topic_deck.py`), and its image source. It is authored from the
AT's **practice workbook**: each component is one block of workbook tasks, taught then exercised, so the
deck and the worksheet advance together. The Topic's `coverage.md` (its UoC contract) is **generated
from the plan** by `scripts/generate_topic_coverage.py` — the plan is the source of truth; coverage is
the derived mapping record.

Two checks run against it (deterministic; no agent — pedagogical quality stays human review):

- **`validate-slide-plan` (format linter):** the required structure is present — every component section
  carries a `Teaches:` line, every slide carries a type tag, every image slide names a source.
- **`validate-slide-plan` (backwards coverage):** the slide plan covers what `coverage.md` requires —
  every component is present, and the union of the slide plan's `Teaches:` tags covers every UoC item
  `coverage.md` teaches. Uses the **same tag machinery as the assessment validators**
  (`valid_tag_set`/`resolve_tags`), so a tag counts here exactly as it does anywhere in the project.

## Conventions

- **UoC tags** use the one project standard ([cluster-authoring-conventions.md §1](cluster-authoring-conventions.md)):
  full `[UNIT SECTION numbering]`, **unwrapped** (not in backticks), ranges/lists allowed. They live on
  the per-component **`Teaches:`** line — this is the authoritative slide-plan→UoC mapping the backwards
  check reads.
- **Component IDs** (`C1`, `C2`, …) match `coverage.md`'s components exactly — the slide plan has one
  `### C<n>` section per component, plus an `### Opener` and `### Close` (no `Teaches:` required on those
  two — they carry no UoC).
- **Slide type tags** mark each slide; they are presentation markers, not UoC tags (backtick/bold
  optional). One of: `[PRIMER]` (vendor-neutral fundamental), `[BESPOKE]` (authored from brief),
  `[AWS <Mx> <Sy>]` (reuse a named source slide), `[DEMO]` (recorded/live demo), `[EX]` (exercise),
  `[TABLE]`, `[TAKEAWAYS]`. Compound is allowed (`[EX] [BESPOKE]`).
- **Every `[EX]` slide names its workbook tasks** — its first bullet is `Workbook — tasks N to M.` (or a
  question rehearsal: `The assessment's questions Q1 to Q3, rehearsed from your practice build.`). This
  is the activity→worksheet alignment the whole delivery model rests on.
- **Render safety (machine-gated — the builder has no line-wrapping and no markdown):** every bullet
  goes on **one line**, however long — a wrapped continuation renders as its own broken bullet; and
  rendered text (titles, kickers, bullets) is **plain text only** — `**bold**`, `*italic*` and backticks
  come out literally on the slide. `notes:` blocks are exempt (speaker pane). Both fail
  `validate-slide-plan` before build.
- **Image source — every slide carries an `image:` field** (mandatory, no exceptions), so there is never
  ambiguity about whether a slide has an image. Value is exactly one of:
  - `image: none` — the slide has no image. **An explicit, required value, not an omission.**
  - `image: reuse <file>` — an externally-sourced asset (e.g. an AWS Academy slide) **committed into the
    topic's `images/` folder** as `<file>` (a filename, extension optional). The builder **places it** like
    any other image; if the file isn't present yet it falls back to a labelled placeholder. *(A free-text
    reference that names no committed file stays a placeholder — the pre-asset state.)*
  - `image: diagram <ref>` — a technical diagram authored as an editable **`.drawio`** and rendered to
    PNG **in-pipeline** by the **`draw-diagram` skill** (Pillow; no draw.io app). `<ref>` names the
    diagram. Editable by students; manual draw.io export is the fallback if a render isn't close enough.
  - `image: gen <prompt>` — a non-technical/decorative image from an image model; **generate-once,
    commit, human-check** (non-deterministic).
  - `image: placeholder <note>` — a human supplies it.
  - **Every route resolves from committed source in the topic folder** (`diagrams/<ref>` spec, `images/`
    gen cache, or `images/<file>` reuse asset), so a deck rebuild always repopulates every slide — no
    post-build hand-pasting to lose on regen. Only a not-yet-supplied `reuse`/`placeholder` needs a human.

## Per-topic asset folders (the deck's committed source)
A deck is a **pure function of committed per-topic source** — the `slide_plan.md` + two sibling folders,
both committed, that the builder reads:
- **`topic_NN/diagrams/`** — one draw-diagram spec per `diagram <ref>` (`<ref>.json`) plus its rendered
  `.drawio` + `.png`. The editable `.drawio` is the student-facing source; the `.png` is placed.
- **`topic_NN/images/`** — the raster assets: `gen` outputs (generate-once, cached by prompt) **and**
  `reuse` files (`<file>` named to match the slide's `image: reuse <file>`, e.g. an extracted AWS slide).

Assemble these **before** building (run-sheet §4 stage 2). Because the build is idempotent, a regenerated
deck always repopulates from these — nothing is lost on rebuild, and `review-slides` can re-check freely.

## Auto-layout (the builder does this — not authored in the plan)
The builder **auto-fits + vertical-centres body text**: it picks the largest size from a **bounded tier
set ({18, 20, 22, 24}pt)** at which the bullets still fit the content box, then centres the block. A
**light** slide scales up (fills the page, no top-dumped whitespace); a **dense** slide settles at the
18pt floor (never smaller than before). Discrete tiers keep type sizes consistent-by-rule across slides,
so variation reads as intentional. Don't hand-size in the plan; a caller may pass an explicit size only to
opt out. (Owned by `kangan_deck.py`; checked visually by `review-slides`.)

## Teacher speaker notes (per slide)
Every teaching/activity/demo slide carries **teacher speaker notes** — written into the PowerPoint **notes
pane** (Presenter View / printable notes pages), **never** on the projected slide. Because they are
**teacher-facing**, they are the one place **meta-language is allowed** — UoC codes, the assessment tie,
AWS source refs — none of which may appear on a student slide. They make a deck **teachable cold**.

**Keep them brief: 3–6 bullets per slide** — the intent (what this slide is for), one point to press,
one misconception or facilitation hint. Not an essay; a teacher running the deck cold needs hints.
Type flavour:
- **Teaching** (`[PRIMER]`/`[BESPOKE]`/`[AWS]`) — the intent, a press point, a misconception or a
  question to pose.
- **Demo** (`[DEMO]`) — what to demonstrate and emphasise, prep + rough timing; name the recorded demo
  source where one exists.
- **Activity** (`[EX]`) — which workbook tasks it runs, where students get stuck, what to press.
- **Skip** title / divider / takeaways / table — self-explanatory.

**How notes are attached (source-level — never post-build; a rebuild must repopulate them):** a
per-slide **`notes:`** block in `slide_plan.md` (multi-line, indented under the slide, placed last),
co-authored with the slide content. `build_topic_deck.py` reads them and writes the notes pane on
every build — one mechanism for every cluster.

Engine: `register_notes()` + `notes=` on the content/visual/activity/demo layouts write `slide.notes_slide`
(owned by `kangan_deck.py`). Notes are committed source, regenerated into the deck on every build.

## Required sections (in order)

This is the human-readable description; the [skeleton](#skeleton) is the authoritative contract the
linter parses.

1. **Header banner** — title `# Topic <NN> <Title> — Slide plan`; a `> **Covers:** …` line naming the
   Topic and (for humans) linking its `coverage.md`; a `> **STATUS:** …` line. **Split topic** (one Topic
   delivered as two decks for sizing, e.g. `slide_plan_08a.md` / `slide_plan_08b.md`): each half-plan adds a
   `> **Covers-components: C1, C2**` line naming the `coverage.md` components it owns — the linter then
   checks that half against just those components (the halves partition the Topic's components).
2. **`## Depth ceiling`** — the level the slides teach to (the AT level) and what is out of scope.
3. **`## Teaching source`** — bespoke / AWS-sourced / generated; which source modules where relevant.
4. **`## AWS pin table`** *(reuse courses)* — the exact source deck + slides to reuse, or `None`.
5. **`## Slides`** — `### Opener`, then `### C<n> — <title>` per component (each with a `Teaches:` line
   and its slides), then `### Close`. Each slide is a `- [<TYPE>] <title>` line with its content bullets
   beneath (markdown `- ` items, indent = level) and a mandatory `image:` field; optional `kicker:` /
   `timer:` (EX) / `source:` (DEMO) / `note:` (TABLE) / `notes:` (multi-line teacher speaker notes, placed
   last) fields, and `| … |` rows for a TABLE.
6. **`## Build notes`** — slide count, exercise summary, inputs.
7. **`## Changelog`** — dated entries.

## What the linter checks

`validate-slide-plan` is deterministic, stdlib-only, and reads `coverage.md` in the same `topic_NN/`
folder as its contract. It:

- **format:** confirms the header + `## Slides` are present; every `### C<n>` component section carries a
  non-empty `Teaches:` line; every slide line carries a recognised `[<TYPE>]` tag; **every slide carries
  an `image:` field** whose value is a valid keyword (`none`/`reuse`/`diagram`/`gen`/`placeholder`) — a
  slide with no `image:` field at all is a failure (ambiguous);
- **render safety** (mirrors the builder's line grammar): no stray line inside a slide block (a line
  that isn't a bullet, a field, a table row or notes-block content would render as its own level-0
  bullet — the wrapped-bullet defect), and no markdown in rendered text (titles, kickers, bullets);
- **backwards coverage** (vs the sibling `coverage.md`): every component `coverage.md` declares has a
  `### C<n>` section; the **union of the slide plan's `Teaches:` tags covers every UoC item `coverage.md`
  teaches** (MISSING = a taught item no slide plans to teach); no `Teaches:` tag is a phantom (PHANTOM =
  not a real consolidated UoC item); a `Teaches:` tag the topic spec doesn't claim is reported as EXTRA
  (advisory).

It does **not** judge whether a slide's content actually teaches its concept well — that is the human
review half of the gate. Exit `0` on PASS, `1` otherwise.

## Skeleton

```markdown
# Topic 07 Network & security base — Slide plan
> **Covers:** Topic 07 — see coverage.md
> **STATUS: DRAFT.**

## Depth ceiling
Stand up the network tier to a supplied design — single-AZ baseline; no HA (that is AT3).

## Teaching source
Mostly AWS-sourced (ACF M05, ACA M07); bespoke for the design topology + test discipline.

## AWS pin table
ACF M05 S5–S9, S11–S13; ACA M07 S10–S20, S30, S45.

## Slides

### Opener
- [BESPOKE] Continuing the build
  - Foundation done last Topic; now build the network the workload sits in.
  image: none

### C1 — Virtual network & subnets
- Teaches: [ICTCLD401 PC 2.2] · [ICTCLD401 KE 5]
- [PRIMER] Networking, the essentials
  - What a network, subnet, IP address and CIDR block are.
  image: reuse ACF M05 S6
- [AWS M05 S11] The VPC — your private network in AWS
  - A VPC is a logically isolated section of AWS you define.
  image: none
- [EX] Build the design's VPC and subnets
  - Workbook — tasks 4 and 5.
  - Stand up the VPC and subnets in the lab.
  timer: ~25 min
  image: none

### C2 — Controlling traffic (security groups)
- Teaches: [ICTCLD401 KE 9]
- [BESPOKE] Security groups — stateful, least-privilege
  - The chain: load balancer group, then app group, then database group.
  image: diagram sg-chain

### Close
- [BESPOKE] What you built
  - The network tier, to the design, evidenced.
  image: none

## Build notes
~N slides. Exercise = stand up the network tier of the practice engagement.

## Changelog
- <date> — authored.
```

## See also

- [process-delivery.md](process-delivery.md) — the delivery run-sheet; the slide plan is the gate before
  the deck is built.
- [cluster-authoring-conventions.md](cluster-authoring-conventions.md) §1 — the one UoC-tag standard the
  `Teaches:` lines use.
- The Topic's `coverage.md` — the spec the slide plan is validated against (components + taught UoC).
