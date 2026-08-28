"""Tests for the 'work check' in validate_at_traceability — the cross-check that a marking
criterion's UoC claims are actually evidenced by the run-sheet work that criterion covers.

WHY THIS CHECK EXISTS. An instrument states its traceability twice, independently: once per
run-sheet item (the `Evidences:` line under each task/test/question) and once per marking criterion.
Nothing compared the two. A criterion could therefore claim a real UoC item, on a properly tagged
criterion, while none of the work it covers demonstrated anything of the kind — and both pre-existing
hard checks (no phantom tags, no free-floating criteria) pass on that, because both ask only whether
tags EXIST and RESOLVE. That is how a performance criterion sat on a criterion whose tasks could not
evidence it, through validation and through delivery.

WHAT THESE TESTS ARE FOR. The dangerous direction is a FALSE NEGATIVE — the validator passing an
instrument whose traceability is invalid. Nearly every test below is therefore of the form "build an
instrument with a specific flavour of broken claim, assert the checker reports it". The handful of
must-PASS tests guard the opposite error: a checker so eager that it flags correct instruments would
be turned off within a week, which is the same as not having it.

Run:  python3 -m pytest .claude/skills/scripts/tests/test_validate_at_traceability_work_check.py
"""
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import validate_at_traceability as V  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures — synthetic instruments in the .md form load_text() accepts, so the
# whole validator can be driven end to end without building a .docx.
# ---------------------------------------------------------------------------

CONSOLIDATED = """
# Synthetic consolidated UoC

- [ICTTEST101 PC 1.1] Build a network
- [ICTTEST101 PC 1.2] Identify shared responsibility
- [ICTTEST101 PC 2.1] Deploy a database
- [ICTTEST101 PC 2.2] Define and expand storage
- [ICTTEST101 PC 3.1] Test connectivity
- [ICTTEST101 PC 4.1] File the documentation
- [ICTTEST101 KE 1] Some knowledge
- [ICTTEST101 FS Reading] Reading
- [ICTTEST101 PE 1] Build something
"""


def instrument(tasks, criteria, tests=(), questions=(), handover=None):
    """Render a synthetic instrument in the same shape the assessor .docx extracts to.

    tasks/tests/questions: list of (n, [tags]) — an empty tag list means the item carries no
    Evidences line at all (a prerequisite step), which is different from carrying an empty one.
    criteria: list of (id, statement, [tags]).
    """
    out = ["Assessment Task — synthetic", "", "Criteria", "Satisfactory?"]
    for cid, statement, tags in criteria:
        out += [f"{cid} {statement}", " · ".join(f"[{t}]" for t in tags), "☐ Yes  ☐ No"]
    out += ["", "Run sheet", ""]
    for n, tags in tasks:
        out += [f"TASK {n}", f"Do the thing numbered {n}"]
        if tags:
            out.append("Evidences: " + " · ".join(f"[{t}]" for t in tags))
        out.append("")
    for n, tags in tests:
        out += [f"TEST {n}", f"Prove thing {n}"]
        if tags:
            out.append("Evidences: " + " · ".join(f"[{t}]" for t in tags))
        out.append("")
    for n, tags in questions:
        out += [f"QUESTION {n}", f"Question {n}?"]
        if tags:
            out.append("Evidences: " + " · ".join(f"[{t}]" for t in tags))
        out.append("")
    if handover:
        out += ["Handover", "File the completed run sheet",
                "Evidences: " + " · ".join(f"[{t}]" for t in handover), ""]
    # The benchmark section has to exist or the validator fails for an unrelated reason.
    out += ["Marking Benchmark — UoC traceability (reverse map)", "UoC item",
            "Evidenced by criterion(ia)"]
    for cid, _, tags in criteria:
        for t in tags:
            out += [f"[{t}] item", cid]
    return "\n".join(out)


def run(tmp_path, text):
    """Drive the whole validator; return (exit_code, combined_output)."""
    at = tmp_path / "AT-synthetic.md"
    con = tmp_path / "consolidated_uoc.md"
    at.write_text(text, encoding="utf-8")
    con.write_text(CONSOLIDATED, encoding="utf-8")
    p = subprocess.run([sys.executable, str(SCRIPTS / "validate_at_traceability.py"),
                        "--at", str(at), "--consolidated", str(con)],
                       capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def work_check(text):
    """The check in isolation: (orphan findings, how many criteria were actually checked)."""
    pre, _ = V.split_benchmark(text)
    evidence = V.instrument_evidence(pre)
    criteria = V.guide_criteria(text)
    checked = [cid for cid, (label, _) in criteria.items()
               if V.criterion_items(label, set(evidence))]
    return V.orphan_claims(criteria, evidence), checked


# ---------------------------------------------------------------------------
# The core false negative: a criterion claiming work that cannot evidence it
# ---------------------------------------------------------------------------

def test_claim_evidenced_by_no_covered_task_is_reported():
    """The original defect: the tag is real, the criterion is tagged, no task demonstrates it."""
    text = instrument(
        tasks=[(1, ["ICTTEST101 PC 1.1"]), (2, ["ICTTEST101 PC 1.1"])],
        criteria=[("A1", "Network (tasks 1-2) — student builds it",
                   ["ICTTEST101 PC 1.1", "ICTTEST101 PC 1.2"])])
    orphans, _ = work_check(text)
    assert len(orphans) == 1
    assert orphans[0][2] == ["ICTTEST101 PC 1.2"]


def test_claim_evidenced_by_a_task_outside_the_criterions_scope_is_reported():
    """The PC 2.4 case — the work exists, but under a different criterion. Attribution matters:
    an assessor marking A2 looks at the database and never sees the storage work in task 1."""
    text = instrument(
        tasks=[(1, ["ICTTEST101 PC 2.2"]), (2, ["ICTTEST101 PC 2.1"])],
        criteria=[("A1", "Compute (task 1) — student builds it", ["ICTTEST101 PC 2.2"]),
                  ("A2", "Database (task 2) — student deploys it",
                   ["ICTTEST101 PC 2.1", "ICTTEST101 PC 2.2"])])
    orphans, _ = work_check(text)
    assert [o[0] for o in orphans] == ["A2"]
    assert orphans[0][2] == ["ICTTEST101 PC 2.2"]


def test_orphan_in_the_middle_of_a_task_range_is_reported():
    """A range must be expanded, not just its endpoints checked."""
    text = instrument(
        tasks=[(1, ["ICTTEST101 PC 1.1"]), (2, []), (3, ["ICTTEST101 PC 1.1"])],
        criteria=[("A1", "Network (tasks 1-3) — student builds it",
                   ["ICTTEST101 PC 1.1", "ICTTEST101 PC 3.1"])])
    orphans, _ = work_check(text)
    assert orphans and orphans[0][2] == ["ICTTEST101 PC 3.1"]


def test_every_offending_criterion_is_reported_not_just_the_first():
    text = instrument(
        tasks=[(1, ["ICTTEST101 PC 1.1"]), (2, ["ICTTEST101 PC 2.1"])],
        criteria=[("A1", "Network (task 1) — builds", ["ICTTEST101 PC 1.1", "ICTTEST101 PC 1.2"]),
                  ("A2", "Database (task 2) — deploys", ["ICTTEST101 PC 2.1", "ICTTEST101 PC 3.1"])])
    orphans, _ = work_check(text)
    assert sorted(o[0] for o in orphans) == ["A1", "A2"]


# ---------------------------------------------------------------------------
# Scope parsing — every way a criterion names its work must be honoured, because
# a scope that fails to parse is silently skipped, which is a false negative.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("statement,tasks", [
    ("Network (task 1) — one task", [1]),
    ("Network (tasks 1-3) — a range", [1, 2, 3]),
    ("Network (tasks 1, 3) — a comma list", [1, 3]),
    ("Network (tasks 1, 3-4) — a list with a range", [1, 3, 4]),
    ("Network (tasks 1 and 4) — an 'and' pair", [1, 4]),
    ("Network (tasks 2-3 and 5) — a range plus an 'and'", [2, 3, 5]),
])
def test_task_scope_forms_all_parse(statement, tasks):
    known = {("task", n) for n in range(1, 6)}
    assert V.criterion_items(statement, known) == {("task", n) for n in tasks}


@pytest.mark.parametrize("statement,expected", [
    ("Testing (T1-T3) — a test range", {("test", 1), ("test", 2), ("test", 3)}),
    ("Testing (T2) — a single test", {("test", 2)}),
    ("Knowledge (Q1-Q2) — a question range", {("question", 1), ("question", 2)}),
    ("Knowledge (Q3) — a single question", {("question", 3)}),
])
def test_test_and_question_scope_forms_parse(statement, expected):
    known = {("test", n) for n in range(1, 4)} | {("question", n) for n in range(1, 4)}
    assert V.criterion_items(statement, known) == expected


def test_orphan_under_a_test_scope_is_reported():
    text = instrument(
        tasks=[(1, ["ICTTEST101 PC 1.1"])],
        tests=[(1, ["ICTTEST101 PC 3.1"]), (2, ["ICTTEST101 PC 3.1"])],
        criteria=[("A1", "Build (task 1) — builds", ["ICTTEST101 PC 1.1"]),
                  ("A2", "Testing (T1-T2) — tests it",
                   ["ICTTEST101 PC 3.1", "ICTTEST101 PE 1"])])
    orphans, _ = work_check(text)
    assert [o[0] for o in orphans] == ["A2"] and orphans[0][2] == ["ICTTEST101 PE 1"]


def test_orphan_under_a_question_scope_is_reported():
    text = instrument(
        tasks=[(1, ["ICTTEST101 PC 1.1"])],
        questions=[(1, ["ICTTEST101 KE 1"])],
        criteria=[("A1", "Build (task 1) — builds", ["ICTTEST101 PC 1.1"]),
                  ("A2", "Knowledge (Q1) — answers",
                   ["ICTTEST101 KE 1", "ICTTEST101 PC 1.2"])])
    orphans, _ = work_check(text)
    assert [o[0] for o in orphans] == ["A2"] and orphans[0][2] == ["ICTTEST101 PC 1.2"]


def test_orphan_under_a_named_section_is_reported():
    """A titled block renders as heading + title + Evidences; a criterion may name either."""
    text = instrument(
        tasks=[(1, ["ICTTEST101 PC 1.1"])],
        handover=["ICTTEST101 PC 4.1"],
        criteria=[("A1", "Build (task 1) — builds", ["ICTTEST101 PC 1.1"]),
                  ("A2", "Handover — student files it",
                   ["ICTTEST101 PC 4.1", "ICTTEST101 PC 1.2"])])
    orphans, checked = work_check(text)
    assert "A2" in checked, "the Handover criterion must be cross-checked, not silently skipped"
    assert [o[0] for o in orphans] == ["A2"] and orphans[0][2] == ["ICTTEST101 PC 1.2"]


# ---------------------------------------------------------------------------
# Evidence parsing — a run-sheet item whose tags are missed reads as evidencing
# nothing, which turns a correct instrument into a false alarm.
# ---------------------------------------------------------------------------

def test_a_task_with_no_evidences_line_contributes_nothing_and_does_not_crash():
    """A prerequisite step carries no Evidences line at all; the criterion covering it is still
    checked against the tasks that do."""
    text = instrument(
        tasks=[(1, []), (2, ["ICTTEST101 PC 1.1"])],
        criteria=[("A1", "Network (tasks 1-2) — builds", ["ICTTEST101 PC 1.1"])])
    orphans, checked = work_check(text)
    assert orphans == [] and checked == ["A1"]


def test_multiple_tags_on_one_evidences_line_are_all_collected():
    text = instrument(
        tasks=[(1, ["ICTTEST101 PC 1.1", "ICTTEST101 PC 2.1", "ICTTEST101 PE 1"])],
        criteria=[("A1", "Everything (task 1) — builds",
                   ["ICTTEST101 PC 1.1", "ICTTEST101 PC 2.1", "ICTTEST101 PE 1"])])
    orphans, _ = work_check(text)
    assert orphans == []


def test_evidence_is_keyed_per_item_not_pooled_across_the_instrument():
    """The check is worthless if every criterion is measured against every tag in the document —
    it would then never fire. Task 2's tag must not satisfy a criterion scoped to task 1."""
    text = instrument(
        tasks=[(1, ["ICTTEST101 PC 1.1"]), (2, ["ICTTEST101 PC 1.2"])],
        criteria=[("A1", "Network (task 1) — builds",
                   ["ICTTEST101 PC 1.1", "ICTTEST101 PC 1.2"])])
    orphans, _ = work_check(text)
    assert orphans and orphans[0][2] == ["ICTTEST101 PC 1.2"]


# ---------------------------------------------------------------------------
# Criteria parsing — a criterion whose tags are missed is a criterion never checked
# ---------------------------------------------------------------------------

def test_criteria_and_their_tags_are_paired_correctly():
    text = instrument(
        tasks=[(1, ["ICTTEST101 PC 1.1"]), (2, ["ICTTEST101 PC 2.1"])],
        criteria=[("A1", "Network (task 1) — builds", ["ICTTEST101 PC 1.1"]),
                  ("A2", "Database (task 2) — deploys", ["ICTTEST101 PC 2.1"])])
    criteria = V.guide_criteria(text)
    assert criteria["A1"][1] == {"ICTTEST101 PC 1.1"}
    assert criteria["A2"][1] == {"ICTTEST101 PC 2.1"}


def test_prose_quoting_a_tag_is_not_mistaken_for_a_criterions_tag_line():
    """If narrative text can be read as a criterion's tag line, the criterion's real claims are
    replaced by whatever the prose happened to mention — and the check silently measures the
    wrong thing."""
    text = "\n".join([
        "Criteria", "Satisfactory?",
        "A1 Network (task 1) — student builds it",
        "This criterion relates to [ICTTEST101 PC 3.1] and is worth reading carefully before use",
        "☐ Yes  ☐ No", "",
        "TASK 1", "Do the thing", "Evidences: [ICTTEST101 PC 1.1]", "",
        "Marking Benchmark — UoC traceability", "UoC item", "A1",
    ])
    criteria = V.guide_criteria(text)
    assert "A1" not in criteria or criteria["A1"][1] != {"ICTTEST101 PC 3.1"}


# ---------------------------------------------------------------------------
# Must NOT fire — a checker that flags correct instruments gets switched off
# ---------------------------------------------------------------------------

def test_a_correct_instrument_passes(tmp_path):
    text = instrument(
        tasks=[(1, ["ICTTEST101 PC 1.1"]), (2, ["ICTTEST101 PC 2.1"])],
        tests=[(1, ["ICTTEST101 PC 3.1"])],
        handover=["ICTTEST101 PC 4.1"],
        criteria=[("A1", "Network (task 1) — builds", ["ICTTEST101 PC 1.1"]),
                  ("A2", "Database (task 2) — deploys", ["ICTTEST101 PC 2.1"]),
                  ("A3", "Testing (T1) — tests", ["ICTTEST101 PC 3.1"]),
                  ("A4", "Handover — files", ["ICTTEST101 PC 4.1"])])
    code, out = run(tmp_path, text)
    assert code == 0, out
    assert "claim a UoC item that none of the work" not in out


def test_foundation_skills_are_not_treated_as_orphans():
    """FS items are genuinely cross-cutting and are carried at criterion level by convention;
    flagging them would bury the real findings in noise."""
    text = instrument(
        tasks=[(1, ["ICTTEST101 PC 1.1"])],
        criteria=[("A1", "Network (task 1) — builds",
                   ["ICTTEST101 PC 1.1", "ICTTEST101 FS Reading"])])
    orphans, _ = work_check(text)
    assert orphans == []


def test_criterion_naming_no_scope_is_skipped_rather_than_failed():
    """Deliberate limitation: with no stated scope there is nothing to measure against. It must
    not be guessed at, and it must not fail."""
    text = instrument(
        tasks=[(1, ["ICTTEST101 PC 1.1"])],
        criteria=[("A1", "Network (task 1) — builds", ["ICTTEST101 PC 1.1"]),
                  ("C1", "Assessment conditions — the lab is available", ["ICTTEST101 PC 1.2"])])
    orphans, checked = work_check(text)
    assert orphans == [] and checked == ["A1"]


def test_instrument_without_evidences_lines_is_not_applicable(tmp_path):
    """Instruments that do not carry per-item Evidences lines must pass, and must say the check
    did not apply rather than implying it ran."""
    text = instrument(
        tasks=[(1, []), (2, [])],
        criteria=[("A1", "Network (tasks 1-2) — builds", ["ICTTEST101 PC 1.1"])])
    code, out = run(tmp_path, text)
    assert code == 0, out
    assert "not applicable" in out


# ---------------------------------------------------------------------------
# End to end — the finding has to reach the exit code, not just a helper's return
# ---------------------------------------------------------------------------

def test_orphan_claim_fails_the_run_and_names_the_criterion(tmp_path):
    text = instrument(
        tasks=[(1, ["ICTTEST101 PC 1.1"])],
        criteria=[("A1", "Network (task 1) — builds",
                   ["ICTTEST101 PC 1.1", "ICTTEST101 PC 1.2"])])
    code, out = run(tmp_path, text)
    assert code == 1, out
    assert "A1" in out and "ICTTEST101 PC 1.2" in out


def test_summary_reports_how_many_criteria_were_actually_cross_checked(tmp_path):
    """A criterion that silently fails to be checked is the failure mode this whole check exists
    to remove, so the count has to be visible."""
    text = instrument(
        tasks=[(1, ["ICTTEST101 PC 1.1"])],
        criteria=[("A1", "Network (task 1) — builds", ["ICTTEST101 PC 1.1"]),
                  ("C1", "Assessment conditions — lab available", ["ICTTEST101 PC 1.2"])])
    code, out = run(tmp_path, text)
    assert "Work check:" in out
    assert "1/2 criteria" in out, out
