# Tests

One suite for the whole factory — `factory/` is the **unit of development**, so it carries one
`venvs/test/`, one `requirements.txt` and one test plan
([`factory/docs/test-plan.md`](../docs/test-plan.md)).

Processes and steps are organisation *within* the unit, not units of their own: their dependency
profiles cut across process boundaries (the deck and docx builders need python-docx/pptx/Pillow, the
validators are stdlib-only), `common/helpers/` is shared across processes, and a step imports helpers so
cannot be built or tested standalone.

## Layout

Tests mirror the implementation tree, so a test's location is derivable from the code's:

```
factory/tests/
├── common/helpers/                          ← factory/common/helpers/
├── process_01_extraction/step_NN_<name>/    ← factory/process_01_extraction/step_NN_<name>/
├── process_02_assessment/step_NN_<name>/
└── process_03_delivery/step_NN_<name>/
```

## Running

```bash
# from factory/
source venvs/test/bin/activate
python -m pytest tests/

# the plan <-> suite trail
python ../.claude/skills/test-plan-linter-python/lint_test_plan.py docs/test-plan.md --tests tests
```

`--tests` recurses, so one argument covers the mirrored tree.

## Status

Structure only — **nothing ported**, so the suite is empty. The legacy suites are still live and still
where the existing coverage lives: `scripts/tests/` (47 test functions over the helpers) and
`.claude/skills/scripts/tests/` (131 over six validators).
