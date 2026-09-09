---
description: Test-first — the test plan defines behaviour before code is written; fires on code + test files
paths:
  - "**/*.{py,js,mjs,cjs,jsx,ts,tsx,go,rs,java,c,cpp,h,hpp,rb,php,cs,swift,kt}"
  - "**/tests.py"
  - "**/test_*.py"
  - "**/docs/test-plan.md"
---

# Test-first

**Never write code before the test plan says what it should do.** Full rationale and the test-plan
format: `docs/test-first-process.md`. The order is fixed:

1. **Update the test plan** (`docs/test-plan.md`) with the cases defining the behaviour — this is where
   behaviour is agreed. Each case gets a stable ID; the **Test function** column starts empty.
2. **Write the tests.** One per case, filling in the **Test function** column. If the thing under test
   doesn't exist yet, create the placeholder with the real signature and a not-implemented body so the
   test is writable.
3. **Run them.** Failures here are expected and correct.
4. **Write the code** until they pass. Done = the plan's cases green.

An unresolved `[TBD]` case is an error, not a warning — resolve it before the plan passes.

## Test environment — fixed location

Tests run against a virtual environment at a **standardized, derivable path** — never search for it,
never create it somewhere ad-hoc:

- The **unit** is the directory owning a developed package (repo root for a single package; each package
  directory in a multi-package tree). A coordination/umbrella root is not a unit.
- Each unit keeps environments in a visible **`venvs/`** folder (no dot) at its root; the test env is
  always **`venvs/test/`**. `venvs/` is gitignored.
- Activate from the unit root: `source venvs/test/bin/activate` (macOS/Linux) or
  `venvs\test\Scripts\Activate.ps1` (Windows). *(Python; other languages get their own convention.)*

## Check the trail

Before committing a plan or a batch of tests, run the project's language linter to confirm the
plan↔suite trail is honest in both directions — for Python:

```bash
python .claude/skills/test-plan-linter-python/lint_test_plan.py docs/test-plan.md --tests <test-dir>
```
