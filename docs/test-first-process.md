# Test-first process

The standard development process for any repo where code is written: behaviour is defined in a **test
plan** first, then the tests are written against it, then the code is written to pass them. This doc is
the human-and-LLM reference for *what* the process is; a `paths:`-scoped rule
(`.claude/rules/test-first.md`) is what makes an LLM follow it, and a per-language linter
(`test-plan-linter-<lang>`) is what checks it mechanically. It is not reserved for greenfield work — it
is how work is done wherever this convention is installed.

## The order

**1. Update the test plan.** Before any other work, the plan gets the cases that define the behaviour
being added or changed. Each case gets a stable ID and a description of what must be true. The **Test
function** column stays empty — nothing covers it yet. This is the step where behaviour is agreed, in a
table, rather than discovered halfway through an implementation.

**2. Write the tests.** One test per case, filling in the **Test function** column as each lands. If a
test can't be written because the thing it calls doesn't exist yet, **create the placeholder** — the
method/function/class with the real signature and a body that raises "not implemented" — so the test is
writable and fails for the right reason.

**3. Run them. Failures are expected.** A suite that is red at this point is the process working. The
red tests are the specification, expressed as something executable.

**4. Write the code.** Implement until the tests pass. The definition of done is the plan's cases going
green, not a subjective sense that the feature works.

## Why this order

The plan is a **commitment, not a wishlist** — a case in the table is a case the code will satisfy.
Agreeing the cases before writing anything is what makes that commitment meaningful; a plan written
after the code just describes whatever got built, a weaker document.

The **Test function** column is the coverage trail, readable both ways: from a case to the test proving
it, and from a test back to the behaviour it defends. An empty cell is a visible work item, so the plan
doubles as the work queue. Writing tests before the implementation also constrains its shape — a
surface awkward to test is usually awkward to use, surfaced while it is still cheap to change.

## What the plan and the suite must agree on

The trail is checked in both directions by the language linter. Four ways they can disagree, all errors:

- **A case names a test that does not exist** — the column is a coverage claim, so a name resolving to
  nothing (or to a helper rather than a test) is a false one.
- **A test no case names** — a *ghost test*. The case is agreed before the test is written, so a test
  outside the plan defends behaviour nobody agreed.
- **A case ID used twice** — IDs are referenceable, so reusing one makes a case invisible to the trail.
- **A case still carrying an unresolved `[TBD]`** — see below.

An empty **Test function** cell is *not* a disagreement — it is the normal in-progress state, and warns
rather than errors.

### Unresolved cases do not pass

A case carrying `[TBD — needs discussion: …]` is an **error**, not a warning: the decision is made
before the plan passes. Flagging an open question is still right — it just does not ship unresolved. To
write the marker in documentation without raising one, escape it with a backslash: `\[TBD]` is ignored.

## The test-plan format

The plan is a markdown file (conventionally `docs/test-plan.md`). It carries:

- **Stable case IDs**, prefixed by the surface they cover (`WC-01`, `PL-05`). Never renumber — retire an
  ID rather than reuse it.
- **A `Test function` column**, filled in as each test lands. An empty cell means the case is agreed but
  not yet covered — the coverage trail an auditor reads, checked both ways.
- **A fixtures table** — the fake objects the suite needs, named and purposed.
- **`[TBD — needs discussion: …]`** against the specific unresolved case, plus an **Open decisions**
  section collecting them. An unresolved case is still listed, but it does not pass.

A copy-pastable starter lives at `docs/test-plan-template.md` — copy it to a unit's `docs/test-plan.md`,
rename the heading, and fill in the tables. What counts as a "test function" is defined by the language
linter — for Python, a `test_*` def in a `tests.py` / `test_*.py` module, found by parsing the module
(test source inside a fixture string is data, not a test).

## Where the plan lives

`docs/test-plan.md` by default. A repo with more than one developed unit (many packages in one tree)
carries one plan per unit, next to that unit's docs. A caller supplies the linter the plan path and the
directories holding that plan's tests, so the rules above apply identically wherever a plan lives.

## Python conventions

### Test virtual environment — fixed location

Tests always run against a virtual environment at a **standardized, derivable path**, so anyone (human
or LLM) knows exactly where it is without searching:

- The **unit** is the directory that owns a developed package — the repo root for a single-package repo;
  each package directory (e.g. `libraries/<name>/`, an app dir) in a multi-package tree. A coordination
  or umbrella root is **not** a unit and holds no venv.
- Each unit keeps its environments in a **visible `venvs/` folder** (no leading dot) at the unit root.
  Environments sit inside it, named by purpose:
  - **`venvs/test/`** — reserved. Tests always run against this; the linter/rule key off it.
  - `venvs/demo/`, `venvs/run/`, … — other purposes, open per project.
- `venvs/` is **gitignored** (visible on disk, never committed).

```
<unit>/
├── src/            # the package
├── tests/          # test code
└── venvs/          # all environments for this unit, one visible place
    ├── test/       # ← tests run against this one
    └── demo/       # other purposes as needed
```

```bash
# from the unit root:
python -m venv venvs/test
source venvs/test/bin/activate          # macOS/Linux
# venvs\test\Scripts\Activate.ps1       # Windows PowerShell
```

## How this is enforced

- **The doc (this file)** — the human reference; also read by an LLM when pointed at it.
- **The rule** (`.claude/rules/test-first.md`) — `paths:`-scoped to code and test files, so it
  auto-fires whenever code is touched. It restates the order, the `venvs/test/` standard, and tells the
  model to run the project's language linter. It points back here for the full rationale.
- **The linter** (`test-plan-linter-<lang>`, e.g. `test-plan-linter-python`) — the mechanical check of
  the plan↔suite trail. Run it before committing a plan or a batch of tests, and as a CI gate.
