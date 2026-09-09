#!/usr/bin/env python3
"""test-plan-linter — one test plan checked against the suite that covers it.

No model is in the loop: same input -> same output. It knows nothing about
libraries, gamedirs or any other repo shape — a caller supplies a plan path and
the directories holding its tests, and gets findings back as data. Any linter or
test suite can be a consumer, so a gap fixed here is fixed for all of them.

The plan and the suite must agree in both directions: every case names a test that
exists (forward), and every test is named by a case (reverse). An uncovered case is
the normal test-first in-progress state (warn); the ways the two disagree are
errors.

A case still carrying `[TBD` is an error — an open decision is resolved before the
plan passes. To write the marker without raising one (a plan documenting the
convention), escape it with a backslash: \\[TBD].

Every case this module covers is agreed in test-plan.md first.

Run standalone:  python lint_test_plan.py <plan.md> --tests <dir> [--json] [--strict]
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

# A case ID is a short surface prefix and a number: WC-01, PL-5, NTC-07.
CASE_ID = re.compile(r"^`?([A-Z]{1,5}-\d{1,3})`?$")
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
TEST_FUNCTION_HEADER = "test function"

# An unresolved decision. A backslash escapes it, so a plan can document the
# convention without tripping it.
TBD_MARKER = re.compile(r"(?<!\\)\[TBD")

# Test functions live in `tests.py` or `test_*.py`; the standalone Django test
# infrastructure matches that pattern but carries settings, not cases.
INFRA_MODULES = {"test_settings.py", "urls.py", "conftest.py"}
SKIP_DIRS = {"migrations", "__pycache__"}

# The checks this linter can emit. XC-01 holds this list and the plan together.
CHECK_NAMES = frozenset({
    "test_plan_missing",        # warn  — the plan file does not exist or is empty
    "test_plan_no_column",      # warn  — no case table carrying a `Test function` column
    "test_plan_uncovered",      # warn  — a case with an empty `Test function` cell
    "test_plan_dangling_ref",   # error — a named test function that is not a test
    "test_plan_ghost_test",     # error — a test function no case names
    "test_plan_duplicate_id",   # error — the same case ID on two rows
    "test_plan_tbd",            # error — a case still carrying an unresolved [TBD]
})


class Finding:
    """One problem with a plan. Plain data — a consumer wraps it in its own type."""

    __slots__ = ("check", "severity", "path", "message")

    def __init__(self, check, severity, path, message):
        self.check = check
        self.severity = severity      # "error" | "warn"
        self.path = path              # str, relative to the caller's root
        self.message = message

    def as_dict(self):
        return {"check": self.check, "severity": self.severity,
                "path": self.path, "message": self.message}

    def __repr__(self):
        return f"Finding({self.check!r}, {self.severity!r}, {self.path!r})"


# --- helpers -----------------------------------------------------------------
def _rel(p: Path, root):
    if root is None:
        return str(p)
    try:
        return str(Path(p).relative_to(root))
    except ValueError:
        return str(p)


def _cap(items, n=8):
    shown = ", ".join(items[:n])
    return shown + (f" (+{len(items) - n} more)" if len(items) > n else "")


def _split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _is_separator(cells):
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells)


# --- reading the plan --------------------------------------------------------
def scan_test_plan(text):
    """(rows, saw_column) — rows are (case_id, test_function_cell, line) from every
    table carrying a `Test function` column. Tables without that column (the prefix
    legend, the fixtures table) are ignored. PS-01..PS-08."""
    rows, col, saw_column = [], None, False
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            col = None                              # table ended
            continue
        cells = _split_row(line)
        if _is_separator(cells):
            continue
        if col is None:                             # header row
            lower = [c.lower() for c in cells]
            if TEST_FUNCTION_HEADER in lower:
                col = lower.index(TEST_FUNCTION_HEADER)
                saw_column = True
            continue
        m = CASE_ID.match(cells[0]) if cells else None
        if m and col < len(cells):
            rows.append((m.group(1), cells[col], line))
    return rows, saw_column


def ref_names(cell):
    """Test-function names referenced by a `Test function` cell.

    Tolerates backticks, markdown links, `Class.test_method` qualification and
    several comma-separated references; the last dotted segment is the name.
    RN-01..RN-07."""
    names = []
    for token in re.split(r"[,\s]+", cell.replace("`", "").replace("[", " ").replace("]", " ")):
        seg = token.strip("().").split(".")[-1]
        if seg and IDENT.fullmatch(seg):
            names.append(seg)
    return names


# --- reading the suite -------------------------------------------------------
def _is_test_module(path: Path):
    name = path.name
    if name in INFRA_MODULES or SKIP_DIRS & set(path.parts):
        return False
    return name == "tests.py" or (name.startswith("test_") and path.suffix == ".py")


def _test_defs(text):
    """The `test_*` functions a module defines. Parsed, not pattern-matched — a
    fixture string holding test source is data, not a test (TS-11). A module that
    does not parse contributes nothing rather than stopping the run (TS-12)."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    return [n.name for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            and n.name.startswith("test_")]


def scan_test_functions(roots, root=None):
    """{test function name: module path} for every test defined under `roots`.

    A test function is a `test_*` def in a `tests.py` / `test_*.py` module. Helpers,
    fixtures and `setUp` are not tests, and the standalone test infrastructure is
    excluded by name — so neither can be mistaken for an unclaimed case. A name
    defined in two modules maps to the first in sorted path order.
    TS-01..TS-12."""
    found = {}
    for r in (Path(p) for p in roots):
        if not r.is_dir():
            continue
        for f in sorted(r.rglob("*.py")):
            if not _is_test_module(f):
                continue
            for name in _test_defs(f.read_text(encoding="utf-8", errors="replace")):
                found.setdefault(name, _rel(f, root))
    return found


# --- the check ---------------------------------------------------------------
def check_test_plan(plan, test_roots=(), root=None):
    """Check one plan against its suite. Returns a list of `Finding`.

    `plan` is the plan file; `test_roots` are the directories holding its tests;
    `root` is what finding paths are reported relative to. With no test roots the
    suite is not read at all, so neither direction is checked against it.
    AP-01..AP-05."""
    plan = Path(plan)
    where = _rel(plan, root)
    text = plan.read_text(encoding="utf-8", errors="replace") if plan.is_file() else ""
    if not text.strip():
        return [Finding("test_plan_missing", "warn", where,
                        "no test plan — the agreed cases are recorded before the tests are "
                        "written, and the plan is the coverage trail")]
    rows, saw_column = scan_test_plan(text)
    if not saw_column:
        return [Finding("test_plan_no_column", "warn", where,
                        "no case table with a 'Test function' column — that column is the "
                        "auditable coverage trail")]

    out = []
    seen, duplicates = set(), []
    for cid, _, _ in rows:
        if cid in seen and cid not in duplicates:
            duplicates.append(cid)
        seen.add(cid)
    if duplicates:
        out.append(Finding("test_plan_duplicate_id", "error", where,
                           f"{len(duplicates)} case ID(s) used twice: {_cap(duplicates)} — IDs "
                           "are stable and referenceable; retire an ID rather than reuse it"))

    tbd = [cid for cid, _, line in rows if TBD_MARKER.search(line)]
    if tbd:
        out.append(Finding("test_plan_tbd", "error", where,
                           f"{len(tbd)} case(s) still carry an unresolved [TBD]: {_cap(tbd)} — "
                           "resolve the decision before the plan passes"))

    uncovered = [cid for cid, cell, line in rows if not cell and not TBD_MARKER.search(line)]
    if uncovered:
        out.append(Finding("test_plan_uncovered", "warn", where,
                           f"{len(uncovered)} of {len(rows)} case(s) have no test function yet: "
                           f"{_cap(uncovered)}"))

    if not test_roots:
        return out

    refs = {}
    for cid, cell, _ in rows:
        for name in ref_names(cell):
            refs.setdefault(name, []).append(cid)
    tests = scan_test_functions(test_roots, root)

    dangling = sorted(n for n in refs if n not in tests)
    if dangling:
        shown = ["{} ({})".format(n, ", ".join(refs[n])) for n in dangling]
        out.append(Finding("test_plan_dangling_ref", "error", where,
                           f"{len(dangling)} test function(s) named in the plan do not exist in "
                           f"the suite: {_cap(shown, 6)}"))

    ghosts = sorted(n for n in tests if n not in refs)
    if ghosts:
        shown = [f"{n} ({tests[n]})" for n in ghosts]
        out.append(Finding("test_plan_ghost_test", "error", where,
                           f"{len(ghosts)} test function(s) exist that no case in the plan names: "
                           f"{_cap(shown, 6)} — every test traces to an agreed case"))
    return out


# --- CLI ---------------------------------------------------------------------
SEV_ORDER = {"error": 0, "warn": 1}


def render_human(findings, plan):
    if not findings:
        return f"{plan} — OK"
    out = [f"\n{plan}"]
    for f in sorted(findings, key=lambda f: (SEV_ORDER[f.severity], f.check)):
        out.append(f"  [{f.severity}] {f.check}: {f.message}")
    e = sum(f.severity == "error" for f in findings)
    w = sum(f.severity == "warn" for f in findings)
    out.append(f"\n{e} error, {w} warn.")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check one test plan against its suite.")
    ap.add_argument("plan", help="path to the test plan markdown file")
    ap.add_argument("--tests", action="append", default=[], metavar="DIR",
                    help="directory holding the plan's tests (repeatable)")
    ap.add_argument("--root", default=None, help="report paths relative to this directory")
    ap.add_argument("--json", action="store_true", help="emit JSON findings")
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero on warnings too (default: errors only)")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve() if args.root else None
    findings = check_test_plan(Path(args.plan), [Path(t) for t in args.tests], root)

    if args.json:
        print(json.dumps({
            "findings": [f.as_dict() for f in
                         sorted(findings, key=lambda f: (SEV_ORDER[f.severity], f.check))],
            "summary": {
                "plan": _rel(Path(args.plan), root),
                "errors": sum(f.severity == "error" for f in findings),
                "warnings": sum(f.severity == "warn" for f in findings),
            },
        }, indent=2))
    else:
        print(render_human(findings, _rel(Path(args.plan), root)))

    fail = any(f.severity == "error" for f in findings)
    if args.strict:
        fail = fail or any(f.severity == "warn" for f in findings)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
