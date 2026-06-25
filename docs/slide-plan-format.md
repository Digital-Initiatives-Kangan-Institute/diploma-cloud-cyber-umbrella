# Slide-plan format — standard

**Audience:** humans and LLM agents authoring a Topic's **slide plan** — the gate before the deck is
built (delivery run-sheet, the deck step). Paths are relative to the `diploma-cloud-cyber-content/` repo
root.

A Topic's **slide plan** (`delivery/topic_NN/slide_plan.md`) is the **kept, validated source** the deck
is built from — the teaching + exercise slides in deck order, each with its type, its **finished content**
(title + bullets, read verbatim by `build_topic_deck.py`), and its image source. It is the **counterpart
of `coverage.md`**:
`coverage.md` says *what the Topic must cover* (components + UoC); the slide plan says *how each of those
is delivered, slide by slide*. The deck is built from it; it is **no longer disposable** (the older
convention deleted it — superseded).

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
- **Image source — every slide carries an `image:` field** (mandatory, no exceptions), so there is never
  ambiguity about whether a slide has an image. Value is exactly one of:
  - `image: none` — the slide has no image. **An explicit, required value, not an omission.**
  - `image: reuse <deck S#>` — an existing external asset (e.g. an AWS diagram); a **placeholder** with
    this reference is emitted and a **human pastes** it. *(The peculiar case — vendor-library courses.)*
  - `image: diagram <ref>` — a technical diagram authored as an editable **`.drawio`** and rendered to
    PNG **in-pipeline** by the **`draw-diagram` skill** (Pillow; no draw.io app). `<ref>` names the
    diagram. Editable by students; manual draw.io export is the fallback if a render isn't close enough.
  - `image: gen <prompt>` — a non-technical/decorative image from an image model; **generate-once,
    commit, human-check** (non-deterministic).
  - `image: placeholder <note>` — a human supplies it.
  - **Anything generated (`diagram`/`gen`) is placed straight into the deck; only `reuse` needs a human.**

## Required sections (in order)

This is the human-readable description; the [skeleton](#skeleton) is the authoritative contract the
linter parses.

1. **Header banner** — title `# Topic <NN> <Title> — Slide plan`; a `> **Covers:** …` line naming the
   Topic and (for humans) linking its `coverage.md`; a `> **STATUS:** …` line.
2. **`## Depth ceiling`** — the level the slides teach to (the AT level) and what is out of scope.
3. **`## Teaching source`** — bespoke / AWS-sourced / generated; which source modules where relevant.
4. **`## AWS pin table`** *(reuse courses)* — the exact source deck + slides to reuse, or `None`.
5. **`## Slides`** — `### Opener`, then `### C<n> — <title>` per component (each with a `Teaches:` line
   and its slides), then `### Close`. Each slide is a `- [<TYPE>] <title>` line with its content bullets
   beneath (markdown `- ` items, indent = level) and a mandatory `image:` field; optional `kicker:` /
   `timer:` (EX) / `source:` (DEMO) / `note:` (TABLE) fields, and `| … |` rows for a TABLE.
6. **`## Build notes`** — slide count, exercise summary, inputs.
7. **`## Changelog`** — dated entries.

## What the linter checks

`validate-slide-plan` is deterministic, stdlib-only, and reads `coverage.md` in the same `topic_NN/`
folder as its contract. It:

- **format:** confirms the header + `## Slides` are present; every `### C<n>` component section carries a
  non-empty `Teaches:` line; every slide line carries a recognised `[<TYPE>]` tag; **every slide carries
  an `image:` field** whose value is a valid keyword (`none`/`reuse`/`diagram`/`gen`/`placeholder`) — a
  slide with no `image:` field at all is a failure (ambiguous);
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
  Foundation done (Topic 6); now build the network the workload sits in.
  image: none

### C1 — Virtual network & subnets
- Teaches: [ICTCLD401 PC 2.2] · [ICTCLD401 KE 5]
- [PRIMER] Networking, the essentials
  What a network/subnet/IP/CIDR is.
  image: reuse ACF M05 S6
- [AWS M05 S11] The VPC — your private network in AWS
  A VPC is a logically isolated section of AWS you define.
  image: none
- [EX] Build the design's VPC + subnets
  Stand up the VPC + subnets in the lab.
  image: none

### C2 — Controlling traffic (security groups)
- Teaches: [ICTCLD401 KE 9]
- [BESPOKE] Security groups — stateful, least-privilege
  The sg-alb -> sg-app -> sg-db chain.
  image: diagram sg-chain

### Close
- [BESPOKE] What you built
  The network tier, to the design, evidenced.
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
