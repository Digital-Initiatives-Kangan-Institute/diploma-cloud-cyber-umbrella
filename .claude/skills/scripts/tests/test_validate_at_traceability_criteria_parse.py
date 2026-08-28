"""Tests for criterion parsing in validate_at_traceability — that the checks which operate on
"the marking criteria" actually find the marking criteria, in every instrument format in use.

WHY. Two checks are gated on the set of parsed criteria:
  * hard check — a criterion carrying no UoC reference at all (free-floating)
  * advisory   — a marking-guide criterion that never appears in the benchmark
Both iterate that set, so an EMPTY or WRONG set makes them pass silently. The run reports a clean
PASS and nothing indicates the checks did not run. That is the worst failure mode a validator has:
not a wrong answer, an unasked question.

Two formats are in use and both must parse:
  * run-sheet form (AT2/AT3) — `A1 Network foundation (tasks 2-7) - statement` then its tag line
    then a tick-box line, with the benchmark rendered as a reverse map (item -> criterion id).
  * narrative form (AT1)     — `A1 - Strategic Alignment - statement`, benchmark rendered as prose.

Run:  python3 -m pytest .claude/skills/scripts/tests/test_validate_at_traceability_criteria_parse.py
"""
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import validate_at_traceability as V  # noqa: E402

CONSOLIDATED = """
- [ICTTEST101 PC 1.1] Build a network
- [ICTTEST101 PC 1.2] Identify shared responsibility
- [ICTTEST101 PC 2.1] Deploy a database
- [ICTTEST101 PC 3.1] Test connectivity
"""


def runsheet_form(criteria, reverse_map, conditions=()):
    """An AT2/AT3-shaped instrument.

    criteria: (id, statement, [tags]) — tags may be empty, meaning the criterion carries none.
    reverse_map: (tag, criterion_id) rows rendered as the two-column benchmark table.
    """
    out = ["Assessment Task - synthetic", "", "Assessment conditions"]
    for cid, statement, tags in conditions:
        out += [f"{cid} {statement}", " · ".join(f"[{t}]" for t in tags)]
    out += ["", "Criteria", "Satisfactory?"]
    for cid, statement, tags in criteria:
        out.append(f"{cid} {statement}")
        if tags:
            out.append(" · ".join(f"[{t}]" for t in tags))
        out.append("☐ Yes  ☐ No")
    out += ["", "TASK 1", "Do it", "Evidences: " + " · ".join(
        f"[{t}]" for _, _, tags in criteria for t in tags) or "Evidences: [ICTTEST101 PC 1.1]", ""]
    out += ["Marking Benchmark - UoC traceability (reverse map)", "UoC item",
            "Evidenced by criterion(ia)"]
    for tag, cid in reverse_map:
        out += [f"[{tag}] some item", cid]
    return "\n".join(out)


def narrative_form(criteria):
    """An AT1-shaped instrument: `A1 - statement` criteria, prose benchmark."""
    out = ["Assessment Task - synthetic", "", "Criteria", "Satisfactory?"]
    for cid, statement, tags in criteria:
        line = f"{cid} - {statement}"
        if tags:
            line += "  " + " · ".join(f"[{t}]" for t in tags)
        out += [line, "☐ Yes  ☐ No"]
    out += ["", "Business Case Benchmark"]
    for i, (cid, statement, tags) in enumerate(criteria, 1):
        out += [f"{i}. Marking {statement}",
                "UoC evidenced: " + (" · ".join(f"[{t}]" for t in tags) if tags else "none"),
                "Satisfactory looks like:", "• something"]
    return "\n".join(out)


def run(tmp_path, text):
    at = tmp_path / "AT-synthetic.md"
    con = tmp_path / "consolidated_uoc.md"
    at.write_text(text, encoding="utf-8")
    con.write_text(CONSOLIDATED, encoding="utf-8")
    p = subprocess.run([sys.executable, str(SCRIPTS / "validate_at_traceability.py"),
                        "--at", str(at), "--consolidated", str(con)],
                       capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


# ---------------------------------------------------------------------------
# The criteria must be found at all — an empty set makes every check below vacuous
# ---------------------------------------------------------------------------

def test_run_sheet_form_criteria_are_parsed(tmp_path):
    """AT2/AT3 report `benchmark criteria: 0`, so everything keyed off that set is inert."""
    text = runsheet_form(
        criteria=[("A1", "Network (task 1) - builds it", ["ICTTEST101 PC 1.1"]),
                  ("A2", "Database (task 1) - deploys it", ["ICTTEST101 PC 2.1"])],
        reverse_map=[("ICTTEST101 PC 1.1", "A1"), ("ICTTEST101 PC 2.1", "A2")])
    code, out = run(tmp_path, text)
    assert "marking criteria: 0" not in out, "no criteria parsed — every criterion check is vacuous"
    assert "marking criteria: 2" in out, out


def test_narrative_form_criteria_are_parsed(tmp_path):
    """AT1 parses Q1-Q9 (its knowledge questions) rather than its A-series marking criteria, so
    the criterion checks have never run against the criteria on any instrument."""
    text = narrative_form(
        criteria=[("A1", "Strategic alignment", ["ICTTEST101 PC 1.1"]),
                  ("A2", "Current state", ["ICTTEST101 PC 2.1"])])
    code, out = run(tmp_path, text)
    assert "marking criteria: 2" in out, out


# ---------------------------------------------------------------------------
# Free-floating criteria — the hard check that is currently inert
# ---------------------------------------------------------------------------

def test_untagged_criterion_in_run_sheet_form_fails(tmp_path):
    text = runsheet_form(
        criteria=[("A1", "Network (task 1) - builds it", ["ICTTEST101 PC 1.1"]),
                  ("A2", "Orphan (task 1) - carries no UoC reference at all", [])],
        reverse_map=[("ICTTEST101 PC 1.1", "A1")])
    code, out = run(tmp_path, text)
    assert code == 1, out
    assert "free-floating" in out and "A2" in out


def test_untagged_criterion_in_narrative_form_fails(tmp_path):
    text = narrative_form(
        criteria=[("A1", "Strategic alignment", ["ICTTEST101 PC 1.1"]),
                  ("A2", "Orphan criterion", [])])
    code, out = run(tmp_path, text)
    assert code == 1, out
    assert "free-floating" in out and "A2" in out


def test_all_criteria_tagged_does_not_fire(tmp_path):
    text = runsheet_form(
        criteria=[("A1", "Network (task 1) - builds it", ["ICTTEST101 PC 1.1"])],
        reverse_map=[("ICTTEST101 PC 1.1", "A1")])
    code, out = run(tmp_path, text)
    assert "free-floating" not in out, out


# ---------------------------------------------------------------------------
# Guide vs benchmark — the advisory that is currently inert
# ---------------------------------------------------------------------------

def test_criterion_absent_from_the_reverse_map_is_reported(tmp_path):
    """A criterion nothing maps to: the tick-list marks work no UoC claim points at."""
    text = runsheet_form(
        criteria=[("A1", "Network (task 1) - builds it", ["ICTTEST101 PC 1.1"]),
                  ("A2", "Database (task 1) - deploys it", ["ICTTEST101 PC 2.1"])],
        reverse_map=[("ICTTEST101 PC 1.1", "A1")])
    code, out = run(tmp_path, text)
    assert "A2" in out and "benchmark" in out.lower()


def test_reverse_map_pointing_at_a_criterion_that_does_not_exist_is_reported(tmp_path):
    """The dangling direction: a UoC item claims to be evidenced by a criterion nobody marks."""
    text = runsheet_form(
        criteria=[("A1", "Network (task 1) - builds it", ["ICTTEST101 PC 1.1"])],
        reverse_map=[("ICTTEST101 PC 1.1", "A1"), ("ICTTEST101 PC 3.1", "A9")])
    code, out = run(tmp_path, text)
    assert "A9" in out, out


def test_matching_guide_and_reverse_map_does_not_fire(tmp_path):
    text = runsheet_form(
        criteria=[("A1", "Network (task 1) - builds it", ["ICTTEST101 PC 1.1"]),
                  ("A2", "Database (task 1) - deploys it", ["ICTTEST101 PC 2.1"])],
        reverse_map=[("ICTTEST101 PC 1.1", "A1"), ("ICTTEST101 PC 2.1", "A2")])
    code, out = run(tmp_path, text)
    assert "not found in the benchmark" not in out
    assert "no such criterion" not in out


# ---------------------------------------------------------------------------
# Noise guards — a parser that over-collects is as bad as one that under-collects
# ---------------------------------------------------------------------------

def test_assessment_conditions_are_not_treated_as_marking_criteria(tmp_path):
    """C-series rows are pre-conditions, not criteria; counting them would fire the free-floating
    check on every instrument and get the whole check switched off."""
    text = runsheet_form(
        criteria=[("A1", "Network (task 1) - builds it", ["ICTTEST101 PC 1.1"])],
        reverse_map=[("ICTTEST101 PC 1.1", "A1")],
        conditions=[("C1", "The lab is available to the student", [])])
    code, out = run(tmp_path, text)
    assert "marking criteria: 1" in out, out
    assert "C1" not in out.split("RESULT")[0] or "free-floating" not in out


def test_criteria_count_is_reported_so_a_silent_zero_is_visible(tmp_path):
    text = runsheet_form(
        criteria=[("A1", "Network (task 1) - builds it", ["ICTTEST101 PC 1.1"])],
        reverse_map=[("ICTTEST101 PC 1.1", "A1")])
    code, out = run(tmp_path, text)
    assert "marking criteria:" in out


def test_the_criteria_table_standard_is_what_parses(tmp_path):
    """Pins the standard a conforming instrument meets, so it is stated rather than implied.

    A marking criterion is a row an assessor ticks:
        <id> <statement>
        <its UoC tag line>
        <Yes/No tick box>
    The tick box is load-bearing — it is what makes the row a marked criterion rather than an
    assessment condition. An instrument that does not present its criteria this way cannot have its
    criteria checked, and says so (see the test below).

    S1-CL2 and S1-CL3 do not currently meet this standard; they are scheduled for rework and are
    expected to come up to it. The validator holds the line rather than growing a second parser.
    """
    text = runsheet_form(
        criteria=[("A1", "Network (task 1) - builds it", ["ICTTEST101 PC 1.1"])],
        reverse_map=[("ICTTEST101 PC 1.1", "A1")],
        conditions=[("C1", "The lab is available", [])])
    parsed = V.marking_criteria(text)
    assert parsed == {"A1": {"ICTTEST101 PC 1.1"}}, parsed
    code, out = run(tmp_path, text)
    assert code == 0 and "no marking criteria" not in out


def test_no_criteria_found_is_reported_rather_than_passing_quietly(tmp_path):
    """An instrument the parser cannot read must say so. Reporting 0 as though it were a result
    is exactly how this went unnoticed."""
    text = "\n".join(["Assessment Task", "", "Some prose with no criteria table at all.",
                      "Marking Benchmark - UoC traceability", "nothing here either"])
    code, out = run(tmp_path, text)
    assert "no marking criteria" in out.lower(), out
