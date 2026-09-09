# test-plan-linter-python · v1.0.0 (created 2026-09-09)

## Purpose
**One Python test plan, checked against the suite that covers it.** A deterministic linter that reads a
plan's case tables and the test modules those cases claim, and reports where the two disagree. It is
repo-shape agnostic — a caller passes a plan path and the directories holding its tests — so any linter
or test suite can use it. No model in the loop: same input always gives the same findings.

The plan and the suite must agree **in both directions**: every case names a test that exists (forward),
and every test is named by a case (reverse). An uncovered case is the normal test-first in-progress
state (warn); the ways the two disagree are errors.

## Provenance — internally created
The Python member of a **language-keyed family**. The [test-first process](../../docs/test-first-process.md)
is language-independent; the *linter* is not — this one understands Python tests specifically (`test_*`
defs in `tests.py` / `test_*.py`, parsed via `ast`). Other languages get their own sibling package
(`test-plan-linter-<lang>`) built to the same contract. Extracted from the FCM umbrella. Pure Python
standard library — no third-party dependencies; runs anywhere Python 3.10+ does and ships with its own
tests.

## Prerequisites
- **Python 3.10+** on PATH (`python3`, or `python` / `py -3`). Standard library only — no venv, no
  `pip install`.

## What's in the folder
- `SKILL.md` — the model/user-facing contract: what it checks, how to run it, how to call it.
- `lint_test_plan.py` — the linter. `scan_test_plan` reads the plan, `scan_test_functions` reads the
  suite, `check_test_plan` compares them and returns `Finding` objects.
- `test-plan.md` — every case this linter covers and the test function covering it (its own dog food).
- `tests.py` — the suite. Stdlib `unittest`, no pytest.

## How to run
```bash
python .claude/skills/test-plan-linter-python/lint_test_plan.py <plan.md> --tests <dir> [--tests <dir>]
```
`--root DIR` reports paths relative to `DIR`; `--json` emits findings as data; `--strict` exits
non-zero on warnings too. Exits 1 on any error, so it doubles as a CI gate.

Call it from another linter by importing it as a sibling and wrapping the findings:
```python
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "test-plan-linter-python"))
import lint_test_plan as plan_linter
findings = plan_linter.check_test_plan(plan_path, test_roots, root)
```

## Calibration
A test function is a `test_*` def in a `tests.py` / `test_*.py` module, found by **parsing** the module
rather than pattern-matching it — test source inside a fixture string is data, not a test. Helpers,
fixtures and `setUp` are not tests; standalone test infrastructure (`test_settings.py`, `urls.py`,
`conftest.py`) is excluded by name; `migrations/` and `__pycache__/` are skipped. A module that does
not parse is skipped rather than stopping the run. A case row carrying `[TBD` is an error; escape it as
`\[TBD]` to document the convention without raising one.

## Running the tests
```bash
python .claude/skills/test-plan-linter-python/tests.py
```
Run it after any change to `lint_test_plan.py`. One case runs the linter over this skill's own plan and
suite, so the linter is its own first consumer.

## Version history
- **v1.0.0 (2026-09-09)** — initial documented version (extracted from FCM, renamed with the `-python`
  language suffix).
