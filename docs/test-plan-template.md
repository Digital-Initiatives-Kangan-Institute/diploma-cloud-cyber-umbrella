# Test plan template

A copy-pastable starting point for a unit's test plan. **To use it: copy this file to the unit's
`docs/test-plan.md` (or `<unit>/docs/test-plan.md` in a multi-unit repo), delete this first note, rename
the H1 to the unit, and fill in the tables.** The format and the rules behind it are in
[test-first-process.md](test-first-process.md); the `test-plan-linter-<lang>` skill checks a filled-in
plan against its suite.

---

# Test plan — <unit>

Every case this unit commits to covering, and the test function that covers it. Built test-first: cases
are agreed here, tests are written against them, then the code is written to pass. The **Test function**
column is the auditable trail — an empty cell means the case is agreed but not yet covered.

## Prefix legend

Case IDs are prefixed by the surface they cover, and never renumbered (retire an ID rather than reuse
it).

| Prefix | Surface it covers |
|---|---|
| SM | smoke tests — the cheapest import/boot sanity checks, written first |
| XX | [TODO — name each surface and its case-ID prefix] |

## Fixtures

The fake objects the suite needs, named and purposed.

| Fixture | Purpose |
|---|---|
| [TODO] | [TODO] |

## Cases

Two smoke cases are seeded as the usual starting point — keep and adapt them to the unit (the wording is
language-specific), or replace if they don't fit.

| Case ID | Behaviour that must hold | Test function |
|---|---|---|
| SM-01 | the unit imports / loads without error | |
| SM-02 | the primary entry point constructs (or the app boots) with default config | |
| XX-01 | [TODO — first real behaviour case] | |

## Open decisions

Collect unresolved cases here, and mark the case itself. An unresolved case does not pass — resolve it
before the plan is green. (Write the marker as `\[TBD — …]` in this template so it does not itself count
as unresolved.)

- [none yet]
