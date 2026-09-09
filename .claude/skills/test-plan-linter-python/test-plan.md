# Test plan — test-plan-linter

Every test case the linter commits to covering, and the test function that covers it. The linter is
built test-first: cases are agreed here, tests are written against them, then the implementation is
written to pass. The **Test function** column is the auditable trail — an empty cell means the case is
agreed but not yet covered.

Case IDs are stable and referenceable. Do not renumber; retire an ID rather than reuse it. Each test
function carries its case ID as its docstring, so the trail reads in both directions.

All test functions live in `tests.py`, beside this plan. Run them with
`python .claude/skills/test-plan-linter/tests.py`.

## What this linter checks

One test plan against the suite that claims to cover it. It knows nothing about libraries, gamedirs or
any other repo shape — a caller supplies a plan path and the directories holding its tests, and gets
findings back. `library-standards-linter` is the first consumer; any linter or test suite can be the
next, and a gap fixed here is fixed for all of them.

| Prefix | Covers |
|---|---|
| `PS` | `scan_test_plan` — locating case tables and rows |
| `RN` | `ref_names` — resolving a `Test function` cell to names |
| `TS` | `scan_test_functions` — locating the tests a suite defines |
| `FW` | Forward checks: uncovered cases, dangling references |
| `RV` | Reverse checks: ghost tests |
| `ID` | Case ID integrity |
| `TB` | Unresolved `[TBD]` cases |
| `MP` | A missing plan |
| `AP` | The callable API and its finding shape |
| `CL` | CLI: exit codes, `--json`, `--strict` |
| `XC` | Cross-cutting |

## Fixtures

The suite needs no real repo — every case writes a plan and, where relevant, test modules into a temp
dir.

| Fixture | Purpose |
|---|---|
| `PLAN` | A compliant plan: prefix legend table, fixtures table, one case table with two covered cases |
| `SUITE` | The matching test module — one module-level test, one test method, plus a helper and a `setUp` |
| `plan_and_suite(plan=…, suite=…, **extra)` | Writes a plan and any test modules to a temp dir, returns the root |
| `findings(...)` | Runs `check_test_plan` over a built tree and returns the finding list |
| `kinds(findings, severity)` | The set of `check` names at a severity — assertions name the check, not the message |
| `messages(findings)` | The findings' messages joined, for asserting a case ID or function name is named |

## PS — `scan_test_plan`

| ID | Case | Test function |
|---|---|---|
| PS-01 | Rows come only from tables carrying a `Test function` column | `ScanTestPlan.test_rows_come_only_from_tables_with_the_column` |
| PS-02 | The prefix legend and the fixtures table contribute no cases | `ScanTestPlan.test_legend_and_fixture_tables_contribute_no_cases` |
| PS-03 | A row whose first cell is not a case ID is skipped | `ScanTestPlan.test_non_case_row_is_skipped` |
| PS-04 | Case IDs are recognised bare or backticked, with a 1–5 letter prefix and 1–3 digits | `ScanTestPlan.test_case_id_forms_recognised` |
| PS-05 | A table ends at the first non-table line — two tables in one section do not bleed together | `ScanTestPlan.test_table_ends_at_first_non_table_line` |
| PS-06 | The `Test function` column is found by header name, at whatever position it sits | `ScanTestPlan.test_column_found_by_header_not_position` |
| PS-07 | A plan with no case table carrying that column is a warn (`test_plan_no_column`) | `ScanTestPlan.test_plan_without_the_column_is_warn` |
| PS-08 | Each row carries its whole source line, so a \[TBD] anywhere in the row is visible | `ScanTestPlan.test_row_carries_its_source_line` |

## RN — `ref_names`

| ID | Case | Test function |
|---|---|---|
| RN-01 | A bare name resolves | `RefNames.test_bare_name_resolves` |
| RN-02 | A backticked name resolves | `RefNames.test_backticked_name_resolves` |
| RN-03 | A `Class.test_method` reference resolves to the last dotted segment | `RefNames.test_qualified_name_resolves_to_last_segment` |
| RN-04 | Several comma-separated references in one cell all resolve | `RefNames.test_several_names_in_one_cell` |
| RN-05 | A markdown-link reference `[test_x](tests.py#L10)` resolves to `test_x` | `RefNames.test_markdown_link_resolves` |
| RN-06 | An empty cell yields no names | `RefNames.test_empty_cell_yields_no_names` |
| RN-07 | Prose in the cell (`not yet`, `TODO`) resolves as names, so it surfaces as a dangling reference rather than passing as coverage | `RefNames.test_prose_in_the_cell_resolves_as_names` |

## TS — `scan_test_functions`

| ID | Case | Test function |
|---|---|---|
| TS-01 | A `test_*` def in `tests.py` is a test | `ScanTestFunctions.test_module_level_test_is_found` |
| TS-02 | A `test_*` method inside a class is a test | `ScanTestFunctions.test_method_test_is_found` |
| TS-03 | An `async def test_*` is a test | `ScanTestFunctions.test_async_test_is_found` |
| TS-04 | Helpers, fixtures, `setUp`/`tearDown` and other non-`test_` defs are not tests | `ScanTestFunctions.test_helpers_and_setup_are_not_tests` |
| TS-05 | A module named `test_*.py` is scanned | `ScanTestFunctions.test_test_prefixed_module_is_scanned` |
| TS-06 | The standalone test infrastructure (`test_settings.py`, `urls.py`, `conftest.py`) is excluded by name | `ScanTestFunctions.test_infrastructure_modules_excluded` |
| TS-07 | `migrations/` and `__pycache__/` are skipped | `ScanTestFunctions.test_migrations_and_pycache_skipped` |
| TS-08 | A `test_*` def in a non-test module is not a test | `ScanTestFunctions.test_non_test_module_is_not_scanned` |
| TS-09 | The same test name in two modules is reported once, against the first module found | `ScanTestFunctions.test_duplicate_name_reported_once_against_first_module` |
| TS-10 | Each test maps to its module path, relative to the supplied root | `ScanTestFunctions.test_each_test_maps_to_its_module_path` |
| TS-11 | Test source inside a string literal is data, not a test — modules are parsed, not pattern-matched | `ScanTestFunctions.test_source_inside_a_string_is_not_a_test` |
| TS-12 | A module that does not parse is skipped rather than stopping the run | `ScanTestFunctions.test_unparseable_module_is_skipped` |

## FW — forward checks (plan → suite)

| ID | Case | Test function |
|---|---|---|
| FW-01 | A case with an empty `Test function` cell is a warn naming the case ID (`test_plan_uncovered`) | `Forward.test_uncovered_case_is_warn` |
| FW-02 | A case naming a test that exists produces no finding | `Forward.test_named_test_that_exists_is_clean` |
| FW-03 | A case naming a test that exists nowhere is an error naming the function and its case ID (`test_plan_dangling_ref`) | `Forward.test_dangling_reference_is_error` |
| FW-04 | A case naming a real symbol that is not a test (a helper, a class) is a dangling reference, not coverage | `Forward.test_non_test_symbol_is_dangling` |
| FW-05 | Several cases naming the same test is legitimate — one test may cover several cases | `Forward.test_one_test_may_cover_several_cases` |

## RV — reverse checks (suite → plan)

A **ghost test** is a test function no case names.

| ID | Case | Test function |
|---|---|---|
| RV-01 | A test no case names is an error naming the function and its module (`test_plan_ghost_test`) | `Reverse.test_unlisted_test_is_a_ghost` |
| RV-02 | A test the plan names is not a ghost | `Reverse.test_listed_test_is_not_a_ghost` |
| RV-03 | Helpers and `setUp` are never ghosts | `Reverse.test_helpers_are_not_ghosts` |
| RV-04 | A test in an excluded infrastructure module is never a ghost | `Reverse.test_infrastructure_test_is_not_a_ghost` |
| RV-05 | A ghost and a dangling reference in the same run are two separate findings | `Reverse.test_ghost_and_dangling_are_separate_findings` |
| RV-06 | No test roots supplied means no ghost findings — the caller is checking the plan alone | `Reverse.test_no_test_roots_means_no_ghosts` |
| RV-07 | Clearing a case's `Test function` cell is reported twice — the case as uncovered, its orphaned test as a ghost — and the finding set is exactly those two |`Reverse.test_clearing_a_cell_orphans_its_test` |

## ID — case ID integrity

| ID | Case | Test function |
|---|---|---|
| ID-01 | A case ID used on two rows is an error naming the ID (`test_plan_duplicate_id`) | `CaseIds.test_duplicate_case_id_is_error` |
| ID-02 | The same ID reused across two different tables of one plan is still a duplicate | `CaseIds.test_duplicate_across_tables_is_still_a_duplicate` |
| ID-03 | A duplicated ID is reported once, however many times it repeats | `CaseIds.test_duplicate_reported_once` |

## TB — unresolved `[TBD]`

| ID | Case | Test function |
|---|---|---|
| TB-01 | A case row carrying an unresolved marker is an error naming the case ID (`test_plan_tbd`) | `Tbd.test_unresolved_tbd_case_is_error` |
| TB-02 | An unresolved case is not also reported as uncovered — one finding per row | `Tbd.test_tbd_case_is_not_also_uncovered` |
| TB-03 | A marker in the plan's prose, outside any case row, is not a finding | `Tbd.test_tbd_in_prose_is_not_a_finding` |
| TB-04 | A marker escaped with a backslash — \[TBD] — documents the convention and is not a finding | `Tbd.test_escaped_marker_is_documentation` |

## MP — a missing plan

| ID | Case | Test function |
|---|---|---|
| MP-01 | A plan path that does not exist is a warn and the only finding (`test_plan_missing`) | `MissingPlan.test_missing_plan_is_warn_and_only_finding` |
| MP-02 | An empty plan file is a warn, not a crash (`test_plan_missing`) | `MissingPlan.test_empty_plan_is_warn_not_a_crash` |

## AP — the callable API

The seam `library-standards-linter` consumes. Findings are data, not printed output.

| ID | Case | Test function |
|---|---|---|
| AP-01 | `check_test_plan(plan, test_roots, root)` returns a list of findings, each carrying `check`, `severity`, `path` and `message` | `Api.test_findings_carry_check_severity_path_and_message` |
| AP-02 | A clean plan and suite returns an empty list | `Api.test_clean_plan_and_suite_returns_empty` |
| AP-03 | Finding paths are relative to the supplied root, never absolute | `Api.test_paths_are_relative_to_root` |
| AP-04 | Severities are only `error` or `warn` | `Api.test_severities_are_error_or_warn` |
| AP-05 | The same input always produces the same findings, in the same order | `Api.test_same_input_gives_same_findings` |

## CL — CLI

| ID | Case | Test function |
|---|---|---|
| CL-01 | A clean plan exits 0 | `Cli.test_clean_plan_exits_zero` |
| CL-02 | Any error exits 1 | `Cli.test_error_exits_one` |
| CL-03 | Warnings alone exit 0, and exit 1 under `--strict` | `Cli.test_warnings_exit_zero_unless_strict` |
| CL-04 | `--json` emits parseable JSON carrying every finding and the error/warning counts | `Cli.test_json_output` |

## XC — Cross-cutting

| ID | Case | Test function |
|---|---|---|
| XC-01 | Every check name the linter can emit is named by a case in this plan | `CrossCutting.test_every_check_name_is_in_the_plan` |
| XC-02 | Every test function in `tests.py` is named by a case in this plan | `CrossCutting.test_every_test_is_named_in_the_plan` |
| XC-03 | The linter run over its own `test-plan.md` and `tests.py` reports no errors | `CrossCutting.test_linter_passes_its_own_plan` |
