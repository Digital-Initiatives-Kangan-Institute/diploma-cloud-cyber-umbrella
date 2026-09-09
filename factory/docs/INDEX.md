# Factory docs index

Documentation for the **factory** — the courseware-development machinery (`factory/`), organised
factory → process → step → gate. Every document below has a one-line description; **read this index
before working in `factory/` and load the relevant doc before related work.**

Add a line here whenever you add a doc — an un-indexed document is invisible.

> **Scope.** This index covers the factory's *own* machinery docs. The course-and-process documentation
> surface for the umbrella and its sub-repos remains [docs/INDEX.md](../../docs/INDEX.md), which stays
> required reading. Where a run-sheet or format standard is named here, it lives there until its step is
> ported — see the `[TBD]` in [factory/README.md](../README.md) on where format standards belong.

## Development

- [test-plan.md](test-plan.md) — the factory's **single test plan**: every case the unit commits to
  covering and the test function that covers it. `factory/` is one unit of development, so one plan
  serves all three processes plus `common/`; case IDs are prefixed by step (`H`, `E01–E03`, `A04–A12`,
  `D01–D06`). Built test-first per
  [docs/test-first-process.md](../../docs/test-first-process.md); checked by the
  `test-plan-linter-python` skill.

## Structure

- [../README.md](../README.md) — what the factory is: the naming convention, step numbering, the unit of
  development, and the incremental migration rule.
- [../common/README.md](../common/README.md) — what `common/` holds and the rule for promoting repeated
  logic into it.
- [../tests/README.md](../tests/README.md) — the mirrored test layout and how to run the suite and the
  plan↔suite linter.
