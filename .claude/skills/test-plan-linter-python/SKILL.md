---
name: test-plan-linter-python
version: 1.0.0
description: |
  Deterministic linter that checks one Python test plan against the suite that
  covers it, in both directions — cases with no test function yet, names in the plan
  that are not tests, tests no case claims (ghost tests), duplicate case IDs, and
  cases still carrying an unresolved [TBD]. Repo-shape agnostic: it takes a plan path
  and the directories holding its tests, so any linter or test suite can call it. The
  Python member of the language-keyed test-plan-linter family (a test is a `test_*`
  def in a tests.py / test_*.py module). Use to check a test plan is honest, before
  committing a plan or a batch of tests, or as a step inside another linter. Pure
  Python, no model in the loop: same input always gives the same findings.
allowed-tools:
  - Bash
---

# test-plan-linter-python

One test plan, checked against the suite that claims to cover it. It knows nothing
about libraries, gamedirs or any other repo shape — a caller supplies a plan path
and the directories holding its tests, and gets findings back as data.

The plan and the suite must agree **in both directions**: every case names a test
that exists, and every test is named by a case. An uncovered case is the normal
test-first in-progress state; the ways the two disagree are errors.

## What it checks

| Check | Severity |
|---|---|
| `test_plan_dangling_ref` — a name in the `Test function` column that is not a test | error |
| `test_plan_ghost_test` — a test function no case in the plan names | error |
| `test_plan_duplicate_id` — the same case ID on two rows | error |
| `test_plan_tbd` — a case still carrying an unresolved `[TBD]` | error |
| `test_plan_missing` — the plan does not exist, or is empty | warn |
| `test_plan_no_column` — no case table carrying a `Test function` column | warn |
| `test_plan_uncovered` — a case with an empty `Test function` cell | warn |

## Running it

```bash
python .claude/skills/test-plan-linter-python/lint_test_plan.py <plan.md> --tests <dir> [--tests <dir>]
```

`--root DIR` reports paths relative to `DIR`; `--json` emits findings as data;
`--strict` exits non-zero on warnings too. It exits 1 on any error, so it doubles
as a CI gate. With no `--tests` the suite is not read at all, so neither direction
is checked against it.

From another linter, import it and wrap the findings:

```python
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "test-plan-linter-python"))
import lint_test_plan as plan_linter

findings = plan_linter.check_test_plan(plan_path, test_roots, root)
```

Each `Finding` carries `check`, `severity`, `path` and `message`. `CHECK_NAMES` is
the full set of checks it can emit.

## What counts as a test

A `test_*` function in a `tests.py` or `test_*.py` module, found by parsing the
module rather than pattern-matching it — so test source inside a fixture string is
data, not a test. Helpers, fixtures and `setUp` are not tests. The standalone test
infrastructure (`test_settings.py`, `urls.py`, `conftest.py`) is excluded by name,
and `migrations/` and `__pycache__/` are skipped.

## The `[TBD]` escape

A case row carrying `[TBD` is an error — an open decision is resolved before the
plan passes. To write the marker without raising one, escape it with a backslash:
`\[TBD]` documents the convention and is ignored.

## Running the tests

```bash
python .claude/skills/test-plan-linter-python/tests.py
```

Every case is agreed in `test-plan.md` first, and each test names its case ID in
its docstring. The suite includes XC-03, which runs the linter over this skill's
own plan and suite — it eats its own dog food.
