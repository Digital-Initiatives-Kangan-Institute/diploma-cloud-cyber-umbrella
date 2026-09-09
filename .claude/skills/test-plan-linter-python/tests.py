#!/usr/bin/env python3
"""Unit tests for the test-plan-linter. Stdlib only (no pytest) so they ship and
run with the skill anywhere:
    python .claude/skills/test-plan-linter/tests.py

Every case is agreed in test-plan.md first; each test names its case ID in its
docstring, so the coverage trail reads in both directions."""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lint_test_plan as lint  # noqa: E402

HERE = Path(__file__).resolve().parent
PLAN_PATH = HERE / "test-plan.md"

PLAN = """# Test plan

| Prefix | Covers |
|---|---|
| `WC` | `walk_contents` |

## Fixtures

| Fixture | Purpose |
|---|---|
| `FakeObj` | Base object with contents |

## WC — `walk_contents`

| ID | Case | Test function |
|---|---|---|
| WC-01 | Filters by predicate | `test_wc_filters` |
| WC-02 | Empty source returns [] | `WalkTests.test_wc_empty` |
"""

SUITE = '''"""The suite PLAN claims to cover."""


def make_obj():
    return object()


def test_wc_filters():
    """WC-01"""


class WalkTests:
    def setUp(self):
        pass

    def _build(self):
        pass

    def test_wc_empty(self):
        """WC-02"""
'''


SUITE_ONE = '''"""A suite of one test."""


def test_wc_filters():
    """WC-01"""
'''


def kinds(findings, severity=None):
    return {f.check for f in findings if severity is None or f.severity == severity}


def messages(findings):
    return " ".join(f.message for f in findings)


class PlanCase(unittest.TestCase):
    """Writes a plan and its test modules to a temp dir, then runs one entry point."""

    PLAN_NAME = "test-plan.md"

    def build(self, plan=PLAN, suite=SUITE, **extra):
        spec = {self.PLAN_NAME: plan}
        if suite is not None:
            spec["src/tests.py"] = suite
        spec.update(extra)
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        for relpath, content in spec.items():
            f = root / relpath
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(content, encoding="utf-8")
        return root

    def findings(self, plan=PLAN, suite=SUITE, roots=("src", "tests"), **extra):
        root = self.build(plan, suite, **extra)
        return lint.check_test_plan(root / self.PLAN_NAME,
                                    [root / r for r in roots], root)


class ScanTestPlan(PlanCase):
    """PS — locating case tables and rows."""

    def test_rows_come_only_from_tables_with_the_column(self):
        """PS-01"""
        rows, saw = lint.scan_test_plan(PLAN)
        self.assertEqual([r[0] for r in rows], ["WC-01", "WC-02"])
        self.assertTrue(saw)

    def test_legend_and_fixture_tables_contribute_no_cases(self):
        """PS-02"""
        rows, _ = lint.scan_test_plan(PLAN)
        self.assertNotIn("FakeObj", str(rows))
        self.assertNotIn("walk_contents", str(rows))

    def test_non_case_row_is_skipped(self):
        """PS-03"""
        plan = PLAN.replace("| WC-02 |", "| a note, not a case |")
        rows, _ = lint.scan_test_plan(plan)
        self.assertEqual([r[0] for r in rows], ["WC-01"])

    def test_case_id_forms_recognised(self):
        """PS-04"""
        plan = PLAN.replace("| WC-01 |", "| `LONGP-123` |").replace("| WC-02 |", "| A-1 |")
        rows, _ = lint.scan_test_plan(plan)
        self.assertEqual([r[0] for r in rows], ["LONGP-123", "A-1"])

    def test_table_ends_at_first_non_table_line(self):
        """PS-05 — a second table without the column must not inherit the first's."""
        plan = PLAN + "\nSome prose.\n\n| Name | Note |\n|---|---|\n| XX-01 | not a case |\n"
        rows, _ = lint.scan_test_plan(plan)
        self.assertEqual([r[0] for r in rows], ["WC-01", "WC-02"])

    def test_column_found_by_header_not_position(self):
        """PS-06"""
        plan = PLAN.replace("| ID | Case | Test function |", "| ID | Test function | Case |") \
                   .replace("| WC-01 | Filters by predicate | `test_wc_filters` |",
                            "| WC-01 | `test_wc_filters` | Filters by predicate |")
        rows, _ = lint.scan_test_plan(plan)
        self.assertEqual(rows[0][1], "`test_wc_filters`")

    def test_plan_without_the_column_is_warn(self):
        """PS-07 — test_plan_no_column"""
        plan = PLAN.replace("| ID | Case | Test function |", "| ID | Case | Notes |")
        f = self.findings(plan=plan)
        self.assertEqual(kinds(f), {"test_plan_no_column"})

    def test_row_carries_its_source_line(self):
        """PS-08"""
        rows, _ = lint.scan_test_plan(PLAN)
        self.assertIn("Filters by predicate", rows[0][2])


class RefNames(unittest.TestCase):
    """RN — resolving a Test function cell to names."""

    def test_bare_name_resolves(self):
        """RN-01"""
        self.assertEqual(lint.ref_names("test_wc_filters"), ["test_wc_filters"])

    def test_backticked_name_resolves(self):
        """RN-02"""
        self.assertEqual(lint.ref_names("`test_wc_filters`"), ["test_wc_filters"])

    def test_qualified_name_resolves_to_last_segment(self):
        """RN-03"""
        self.assertEqual(lint.ref_names("`WalkTests.test_wc_empty`"), ["test_wc_empty"])

    def test_several_names_in_one_cell(self):
        """RN-04"""
        self.assertEqual(lint.ref_names("`test_a`, `test_b`"), ["test_a", "test_b"])

    def test_markdown_link_resolves(self):
        """RN-05"""
        self.assertEqual(lint.ref_names("[test_a](tests.py#L10)"), ["test_a"])

    def test_empty_cell_yields_no_names(self):
        """RN-06"""
        self.assertEqual(lint.ref_names(""), [])

    def test_prose_in_the_cell_resolves_as_names(self):
        """RN-07 — prose surfaces as a dangling reference rather than passing as coverage."""
        self.assertTrue(lint.ref_names("not yet"))


class ScanTestFunctions(PlanCase):
    """TS — locating the tests a suite defines."""

    def scan(self, **extra):
        root = self.build(**extra)
        return lint.scan_test_functions([root / "src", root / "tests"], root)

    def test_module_level_test_is_found(self):
        """TS-01"""
        self.assertIn("test_wc_filters", self.scan())

    def test_method_test_is_found(self):
        """TS-02"""
        self.assertIn("test_wc_empty", self.scan())

    def test_async_test_is_found(self):
        """TS-03"""
        self.assertIn("test_async_case",
                      self.scan(suite=SUITE + "\n\nasync def test_async_case():\n    pass\n"))

    def test_helpers_and_setup_are_not_tests(self):
        """TS-04"""
        found = self.scan()
        self.assertNotIn("make_obj", found)
        self.assertNotIn("setUp", found)
        self.assertNotIn("_build", found)

    def test_test_prefixed_module_is_scanned(self):
        """TS-05"""
        self.assertIn("test_in_other_module",
                      self.scan(**{"src/test_extra.py": "def test_in_other_module():\n    pass\n"}))

    def test_infrastructure_modules_excluded(self):
        """TS-06"""
        found = self.scan(**{"tests/test_settings.py": "def test_db_alias():\n    pass\n",
                             "tests/urls.py": "def test_route():\n    pass\n",
                             "tests/conftest.py": "def test_fixture():\n    pass\n"})
        for name in ("test_db_alias", "test_route", "test_fixture"):
            self.assertNotIn(name, found)

    def test_migrations_and_pycache_skipped(self):
        """TS-07"""
        found = self.scan(**{"src/migrations/tests.py": "def test_migrated():\n    pass\n",
                             "src/__pycache__/tests.py": "def test_cached():\n    pass\n"})
        self.assertNotIn("test_migrated", found)
        self.assertNotIn("test_cached", found)

    def test_non_test_module_is_not_scanned(self):
        """TS-08"""
        self.assertNotIn("test_looks_like_one",
                         self.scan(**{"src/core.py": "def test_looks_like_one():\n    pass\n"}))

    def test_duplicate_name_reported_once_against_first_module(self):
        """TS-09"""
        found = self.scan(**{"src/test_extra.py": "def test_wc_filters():\n    pass\n"})
        self.assertEqual(found["test_wc_filters"], os.path.join("src", "test_extra.py"))

    def test_source_inside_a_string_is_not_a_test(self):
        """TS-11 — a fixture holding test source is data, not a test."""
        module = 'FIXTURE = """\n\ndef test_in_a_string():\n    pass\n"""\n'
        self.assertNotIn("test_in_a_string", self.scan(**{"src/test_fixtures.py": module}))

    def test_unparseable_module_is_skipped(self):
        """TS-12 — a module that does not parse does not stop the run."""
        found = self.scan(**{"src/test_broken.py": "def test_x(:\n    pass\n"})
        self.assertNotIn("test_x", found)
        self.assertIn("test_wc_filters", found)

    def test_each_test_maps_to_its_module_path(self):
        """TS-10"""
        found = self.scan()
        self.assertEqual(found["test_wc_filters"], os.path.join("src", "tests.py"))
        self.assertFalse(Path(found["test_wc_filters"]).is_absolute())


class Forward(PlanCase):
    """FW — plan to suite."""

    def test_uncovered_case_is_warn(self):
        """FW-01 — test_plan_uncovered"""
        plan = PLAN.replace("`test_wc_filters`", "")
        f = self.findings(plan=plan)
        self.assertIn("test_plan_uncovered", kinds(f, "warn"))
        self.assertIn("WC-01", messages(f))

    def test_named_test_that_exists_is_clean(self):
        """FW-02"""
        self.assertEqual(self.findings(), [])

    def test_dangling_reference_is_error(self):
        """FW-03 — test_plan_dangling_ref"""
        plan = PLAN.replace("`test_wc_filters`", "`test_gone`")
        f = self.findings(plan=plan)
        self.assertIn("test_plan_dangling_ref", kinds(f, "error"))
        self.assertIn("test_gone", messages(f))
        self.assertIn("WC-01", messages(f))

    def test_non_test_symbol_is_dangling(self):
        """FW-04 — naming a helper does not make the case covered."""
        plan = PLAN.replace("`test_wc_filters`", "`make_obj`")
        f = self.findings(plan=plan)
        self.assertIn("test_plan_dangling_ref", kinds(f, "error"))
        self.assertIn("make_obj", messages(f))

    def test_one_test_may_cover_several_cases(self):
        """FW-05"""
        plan = PLAN.replace("`WalkTests.test_wc_empty`", "`test_wc_filters`")
        f = self.findings(plan=plan, suite=SUITE_ONE)
        self.assertEqual(kinds(f, "error"), set())
        self.assertNotIn("test_plan_ghost_test", kinds(f))


class Reverse(PlanCase):
    """RV — suite to plan."""

    GHOST = "\n\ndef test_not_in_the_plan():\n    pass\n"

    def test_unlisted_test_is_a_ghost(self):
        """RV-01 — test_plan_ghost_test"""
        f = self.findings(suite=SUITE + self.GHOST)
        self.assertIn("test_plan_ghost_test", kinds(f, "error"))
        self.assertIn("test_not_in_the_plan", messages(f))
        self.assertIn("tests.py", messages(f))

    def test_listed_test_is_not_a_ghost(self):
        """RV-02"""
        self.assertNotIn("test_plan_ghost_test", kinds(self.findings()))

    def test_helpers_are_not_ghosts(self):
        """RV-03"""
        f = self.findings(suite=SUITE + "\n\ndef build_fixture():\n    pass\n")
        self.assertNotIn("test_plan_ghost_test", kinds(f))

    def test_infrastructure_test_is_not_a_ghost(self):
        """RV-04"""
        f = self.findings(**{"tests/test_settings.py": "def test_db_alias():\n    pass\n"})
        self.assertNotIn("test_plan_ghost_test", kinds(f))

    def test_ghost_and_dangling_are_separate_findings(self):
        """RV-05"""
        plan = PLAN.replace("`test_wc_filters`", "`test_gone`")
        f = self.findings(plan=plan, suite=SUITE + self.GHOST)
        self.assertIn("test_plan_dangling_ref", kinds(f))
        self.assertIn("test_plan_ghost_test", kinds(f))

    def test_no_test_roots_means_no_ghosts(self):
        """RV-06 — the caller is checking the plan alone."""
        f = self.findings(suite=SUITE + self.GHOST, roots=())
        self.assertNotIn("test_plan_ghost_test", kinds(f))

    def test_clearing_a_cell_orphans_its_test(self):
        """RV-07 — the case goes uncovered and its test becomes a ghost."""
        plan = PLAN.replace("`test_wc_filters`", "")
        f = self.findings(plan=plan)
        self.assertEqual(kinds(f), {"test_plan_uncovered", "test_plan_ghost_test"})
        self.assertIn("WC-01", messages([x for x in f if x.check == "test_plan_uncovered"]))
        self.assertIn("test_wc_filters",
                      messages([x for x in f if x.check == "test_plan_ghost_test"]))


class CaseIds(PlanCase):
    """ID — case ID integrity."""

    def test_duplicate_case_id_is_error(self):
        """ID-01 — test_plan_duplicate_id"""
        plan = PLAN.replace("| WC-02 |", "| WC-01 |")
        f = self.findings(plan=plan)
        self.assertIn("test_plan_duplicate_id", kinds(f, "error"))
        self.assertIn("WC-01", messages(f))

    def test_duplicate_across_tables_is_still_a_duplicate(self):
        """ID-02"""
        plan = PLAN + ("\n## WC — more\n\n| ID | Case | Test function |\n|---|---|---|\n"
                       "| WC-01 | Same ID again | `test_wc_filters` |\n")
        self.assertIn("test_plan_duplicate_id", kinds(self.findings(plan=plan), "error"))

    def test_duplicate_reported_once(self):
        """ID-03"""
        plan = PLAN.replace("| WC-02 | Empty source returns [] | `WalkTests.test_wc_empty` |",
                            "| WC-01 | Again | `test_wc_filters` |\n"
                            "| WC-01 | And again | `test_wc_filters` |")
        f = [x for x in self.findings(plan=plan) if x.check == "test_plan_duplicate_id"]
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0].message.count("WC-01"), 1)


class Tbd(PlanCase):
    """TB — unresolved decisions."""

    OPEN = "| WC-01 | Filters by predicate [TBD — needs discussion: which] | `test_wc_filters` |"

    def test_unresolved_tbd_case_is_error(self):
        """TB-01 — test_plan_tbd"""
        plan = PLAN.replace("| WC-01 | Filters by predicate | `test_wc_filters` |", self.OPEN)
        f = self.findings(plan=plan)
        self.assertIn("test_plan_tbd", kinds(f, "error"))
        self.assertIn("WC-01", messages(f))

    def test_tbd_case_is_not_also_uncovered(self):
        """TB-02 — one finding per row."""
        plan = PLAN.replace("| WC-01 | Filters by predicate | `test_wc_filters` |",
                            self.OPEN.replace("`test_wc_filters`", ""))
        f = self.findings(plan=plan)
        self.assertIn("test_plan_tbd", kinds(f))
        self.assertNotIn("WC-01", " ".join(x.message for x in f
                                           if x.check == "test_plan_uncovered"))

    def test_escaped_marker_is_documentation(self):
        """TB-04 — a backslash-escaped marker documents the convention."""
        plan = PLAN.replace("| WC-01 | Filters by predicate |",
                            "| WC-01 | Filters by predicate, unlike \\[TBD] rows |")
        self.assertNotIn("test_plan_tbd", kinds(self.findings(plan=plan)))

    def test_tbd_in_prose_is_not_a_finding(self):
        """TB-03"""
        plan = PLAN.replace("## WC — `walk_contents`",
                            "Still open: [TBD — needs discussion: the prefix]\n\n"
                            "## WC — `walk_contents`")
        self.assertNotIn("test_plan_tbd", kinds(self.findings(plan=plan)))


class MissingPlan(PlanCase):
    """MP — a plan that is not there."""

    def test_missing_plan_is_warn_and_only_finding(self):
        """MP-01 — test_plan_missing"""
        root = self.build()
        f = lint.check_test_plan(root / "no-such-plan.md", [root / "src"], root)
        self.assertEqual(kinds(f), {"test_plan_missing"})
        self.assertEqual(kinds(f, "warn"), {"test_plan_missing"})

    def test_empty_plan_is_warn_not_a_crash(self):
        """MP-02"""
        self.assertEqual(kinds(self.findings(plan="")), {"test_plan_missing"})


class Api(PlanCase):
    """AP — the seam a consumer calls."""

    def test_findings_carry_check_severity_path_and_message(self):
        """AP-01"""
        f = self.findings(plan=PLAN.replace("`test_wc_filters`", "`test_gone`"))
        self.assertTrue(f)
        for x in f:
            for attr in ("check", "severity", "path", "message"):
                self.assertIsInstance(getattr(x, attr), str)
            self.assertIn(x.check, lint.CHECK_NAMES)

    def test_clean_plan_and_suite_returns_empty(self):
        """AP-02"""
        self.assertEqual(self.findings(), [])

    def test_paths_are_relative_to_root(self):
        """AP-03"""
        root = self.build(plan=PLAN.replace("`test_wc_filters`", "`test_gone`"))
        f = lint.check_test_plan(root / self.PLAN_NAME, [root / "src"], root)
        self.assertTrue(f)
        for x in f:
            self.assertFalse(Path(x.path).is_absolute())
            self.assertNotIn(str(root), x.path)

    def test_severities_are_error_or_warn(self):
        """AP-04"""
        plan = PLAN.replace("`test_wc_filters`", "`test_gone`").replace(
            "`WalkTests.test_wc_empty`", "")
        for x in self.findings(plan=plan, suite=SUITE + "\n\ndef test_extra():\n    pass\n"):
            self.assertIn(x.severity, ("error", "warn"))

    def test_same_input_gives_same_findings(self):
        """AP-05"""
        plan = PLAN.replace("`test_wc_filters`", "`test_gone`")
        first = [x.as_dict() for x in self.findings(plan=plan)]
        second = [x.as_dict() for x in self.findings(plan=plan)]
        self.assertEqual(first, second)


class Cli(PlanCase):
    def run_cli(self, *argv, **build_kwargs):
        root = self.build(**build_kwargs)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = lint.main([str(root / self.PLAN_NAME), "--tests", str(root / "src"),
                              "--root", str(root), *argv])
        return code, buf.getvalue()

    def test_clean_plan_exits_zero(self):
        """CL-01"""
        self.assertEqual(self.run_cli()[0], 0)

    def test_error_exits_one(self):
        """CL-02"""
        plan = PLAN.replace("`test_wc_filters`", "`test_gone`")
        self.assertEqual(self.run_cli(plan=plan)[0], 1)

    def test_warnings_exit_zero_unless_strict(self):
        """CL-03"""
        plan = PLAN + "| WC-03 | Not written yet | |\n"
        self.assertEqual(self.run_cli(plan=plan)[0], 0)
        self.assertEqual(self.run_cli("--strict", plan=plan)[0], 1)

    def test_json_output(self):
        """CL-04"""
        plan = PLAN + "| WC-03 | Gone | `test_gone` |\n| WC-04 | Not written yet | |\n"
        _, out = self.run_cli("--json", plan=plan)
        payload = json.loads(out)
        self.assertEqual(payload["summary"]["errors"], 1)
        self.assertEqual(payload["summary"]["warnings"], 1)
        self.assertEqual(len(payload["findings"]), 2)


class CrossCutting(unittest.TestCase):
    """XC — the linter's own coverage trail, checked the way it checks anyone's."""

    def test_every_check_name_is_in_the_plan(self):
        """XC-01"""
        plan = PLAN_PATH.read_text(encoding="utf-8")
        self.assertEqual(sorted(n for n in lint.CHECK_NAMES if n not in plan), [])

    def test_every_test_is_named_in_the_plan(self):
        """XC-02"""
        rows, _ = lint.scan_test_plan(PLAN_PATH.read_text(encoding="utf-8"))
        named = {n for _, cell, _ in rows for n in lint.ref_names(cell)}
        defined = set(lint.scan_test_functions([HERE], HERE))
        self.assertEqual(sorted(defined - named), [])

    def test_linter_passes_its_own_plan(self):
        """XC-03 — the dog food: run it over this skill's own plan and suite."""
        f = lint.check_test_plan(PLAN_PATH, [HERE], HERE)
        self.assertEqual([x.as_dict() for x in f if x.severity == "error"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
