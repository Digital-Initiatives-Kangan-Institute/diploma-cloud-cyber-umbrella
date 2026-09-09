"""Cases CDP-01 .. CDP-29 — factory/docs/test-plan.md.

The Step-6 gate: a completeness-for-generation check on one cluster's delivery/delivery-plan.md.
Each test mutates the passing baseline into exactly one defect, so a failure names one decision.
"""
import shutil

from conftest import FORMAT_DOC


def fmt(*extra):
    """Always pass the format doc explicitly, so tests never depend on discovery order."""
    return ("--format", str(FORMAT_DOC), *extra)


# --- invocation and contract resolution (CDP-01 .. CDP-05) -----------------

def test_plan_flag_names_the_file_directly(cluster, run_validator):
    """CDP-01"""
    _root, write_plan = cluster
    plan = write_plan()
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 0, out


def test_cluster_dir_flag_reaches_the_same_file(cluster, run_validator):
    """CDP-02 — a path convenience, not a different scope."""
    root, write_plan = cluster
    write_plan()
    code, out = run_validator("--cluster-dir", root, *fmt())
    assert code == 0, out


def test_missing_plan_file_fails_naming_the_path(cluster, run_validator):
    """CDP-03"""
    root, _write_plan = cluster
    code, out = run_validator("--cluster-dir", root, *fmt())
    assert code == 1
    assert "delivery-plan.md" in out


def test_unlocatable_format_doc_fails_telling_you_to_pass_it(cluster, run_validator, tmp_path):
    """CDP-04"""
    _root, write_plan = cluster
    plan = write_plan()
    code, out = run_validator("--plan", plan, "--format", tmp_path / "nope.md")
    assert code == 1
    assert "--format" in out


def test_format_doc_without_a_skeleton_fails(cluster, run_validator, tmp_path):
    """CDP-05"""
    _root, write_plan = cluster
    plan = write_plan()
    bad = tmp_path / "no-skeleton.md"
    bad.write_text("# A format doc\n\nProse only, no skeleton block.\n", encoding="utf-8")
    code, out = run_validator("--plan", plan, "--format", bad)
    assert code == 1
    assert "no-skeleton.md" in out


# --- contract structure (CDP-06 .. CDP-11) ---------------------------------

def test_missing_title_fails(cluster, run_validator, plan_text):
    """CDP-06"""
    _root, write_plan = cluster
    plan = write_plan(plan_text.replace("# S1-CL9 Test Cluster — Delivery Plan (2026-T2)", "# Something else"))
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 1
    assert "title" in out.lower()


def test_missing_instance_banner_fails(cluster, run_validator, plan_text):
    """CDP-07"""
    _root, write_plan = cluster
    plan = write_plan("\n".join(l for l in plan_text.splitlines() if not l.startswith("> **INSTANCE:")))
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 1
    assert "INSTANCE" in out


def test_missing_heading_fails_naming_it(cluster, run_validator, plan_text):
    """CDP-08"""
    _root, write_plan = cluster
    plan = write_plan(plan_text.replace("## 4. Notes / decisions", "## Some other heading"))
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 1
    assert "4. Notes / decisions" in out


def test_missing_header_field_fails_naming_it(cluster, run_validator, plan_text):
    """CDP-09"""
    _root, write_plan = cluster
    plan = write_plan(plan_text.replace("- Teaching days: Thursday, Friday\n", ""))
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 1
    assert "Teaching days" in out


def test_empty_header_field_fails(cluster, run_validator, plan_text):
    """CDP-10"""
    _root, write_plan = cluster
    plan = write_plan(plan_text.replace("- Intake: 2026-T2", "- Intake:"))
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 1
    assert "Intake" in out


def test_missing_grid_column_fails_naming_it(cluster, run_validator, plan_text):
    """CDP-11"""
    _root, write_plan = cluster
    plan = write_plan(
        plan_text.replace("| # | Date       | Week | Day | Time     | Mode   | Activity   | Placed |",
                          "| # | Date       | Week | Day | Time     | Mode   | Activity   |")
    )
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 1
    assert "Placed" in out


# --- grid consistency (CDP-12 .. CDP-18) -----------------------------------

def test_complete_consistent_plan_passes(cluster, run_validator):
    """CDP-12"""
    _root, write_plan = cluster
    plan = write_plan()
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 0, out
    assert "PASS" in out


def test_undecided_cell_fails(cluster, run_validator, plan_text):
    """CDP-13 — the case is per-cell, not per-column: any required column counts."""
    _root, write_plan = cluster
    plan = write_plan(plan_text.replace("| 1 | 2026-10-08 | 9    | Thu | 9am-12pm | online | teach      | T1     |",
                                        "| 1 | 2026-10-08 | 9    |     | 9am-12pm | online | teach      | T1     |"))
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 1
    assert "day" in out.lower()


def test_blank_placed_cell_fails(cluster, run_validator, plan_text):
    """CDP-14 — an intentionally empty session is written '—', never left blank."""
    _root, write_plan = cluster
    plan = write_plan(plan_text.replace("| 3 | 2026-10-09 | 9    | Fri | 9am-12pm | online | spare      | —      |",
                                        "| 3 | 2026-10-09 | 9    | Fri | 9am-12pm | online | spare      |        |"))
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 1
    assert "Placed" in out


def test_invalid_mode_fails_listing_permitted_values(cluster, run_validator, plan_text):
    """CDP-15"""
    _root, write_plan = cluster
    plan = write_plan(plan_text.replace("| 1 | 2026-10-08 | 9    | Thu | 9am-12pm | online | teach      | T1     |",
                                        "| 1 | 2026-10-08 | 9    | Thu | 9am-12pm | hybrid | teach      | T1     |"))
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 1
    assert "hybrid" in out and "classroom" in out


def test_invalid_activity_fails_listing_permitted_values(cluster, run_validator, plan_text):
    """CDP-16"""
    _root, write_plan = cluster
    plan = write_plan(plan_text.replace("| 1 | 2026-10-08 | 9    | Thu | 9am-12pm | online | teach      | T1     |",
                                        "| 1 | 2026-10-08 | 9    | Thu | 9am-12pm | online | lecture    | T1     |"))
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 1
    assert "lecture" in out and "onboarding" in out


def test_gap_in_session_numbering_fails(cluster, run_validator, plan_text):
    """CDP-17"""
    _root, write_plan = cluster
    plan = write_plan(plan_text.replace("| 2 | 2026-10-08 | 9    | Thu | 1pm-4pm  | online | assessment | AT1    |",
                                        "| 4 | 2026-10-08 | 9    | Thu | 1pm-4pm  | online | assessment | AT1    |"))
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 1
    assert "contiguous" in out


def test_duplicate_session_number_fails(cluster, run_validator, plan_text):
    """CDP-18"""
    _root, write_plan = cluster
    plan = write_plan(plan_text.replace("| 2 | 2026-10-08 | 9    | Thu | 1pm-4pm  | online | assessment | AT1    |",
                                        "| 1 | 2026-10-08 | 9    | Thu | 1pm-4pm  | online | assessment | AT1    |"))
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 1
    assert "duplicate" in out.lower()


# --- placement coverage (CDP-19 .. CDP-22) ---------------------------------

def test_unplaced_topic_fails_naming_it(cluster, run_validator, plan_text):
    """CDP-19"""
    root, write_plan = cluster
    (root / "delivery" / "topic_02").mkdir()
    plan = write_plan(plan_text)
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 1
    assert "T2" in out


def test_unplaced_assessment_fails_naming_it(cluster, run_validator, plan_text):
    """CDP-20"""
    root, write_plan = cluster
    (root / "assessments" / "AT2").mkdir()
    plan = write_plan(plan_text)
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 1
    assert "AT2" in out


def test_zero_padded_topic_reference_counts_as_placed(cluster, run_validator, plan_text):
    """CDP-21 — 'T01' satisfies Topic 1; padding is not a gap."""
    _root, write_plan = cluster
    plan = write_plan(plan_text.replace("| T1     |", "| T01    |"))
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 0, out


def test_no_built_topics_warns_rather_than_fails(cluster, run_validator, plan_text):
    """CDP-22 — nothing to place is not a defect in the plan."""
    root, write_plan = cluster
    shutil.rmtree(root / "delivery" / "topic_01")
    plan = write_plan(plan_text.replace("| T1     |", "| —      |"))
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 0, out
    assert "warn" in out.lower()


# --- frame reconciliation (CDP-23 .. CDP-27) -------------------------------

def test_row_count_differing_from_declared_total_fails(cluster, run_validator, plan_text):
    """CDP-23"""
    _root, write_plan = cluster
    plan = write_plan(plan_text.replace("- Total sessions available: 3", "- Total sessions available: 5"))
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 1
    assert "Total sessions available" in out


def test_budgeted_onboarding_missing_from_grid_fails(cluster, run_validator, plan_text):
    """CDP-24"""
    root, write_plan = cluster
    spec = root / "cluster-specification.md"
    spec.write_text(spec.read_text().replace("- Onboarding sessions: 0", "- Onboarding sessions: 1"))
    plan = write_plan(plan_text)
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 1
    assert "onboarding" in out.lower()


def test_budgeted_spare_missing_from_grid_fails(cluster, run_validator, plan_text):
    """CDP-25"""
    _root, write_plan = cluster
    plan = write_plan(plan_text.replace("| spare      | —      |", "| teach      | T1     |"))
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 1
    assert "spare" in out.lower()


def test_intake_total_differing_from_frame_is_reported_not_failed(cluster, run_validator, plan_text):
    """CDP-26 — the intake's real allocation is information, not an error."""
    root, write_plan = cluster
    spec = root / "cluster-specification.md"
    spec.write_text(spec.read_text().replace("- Total sessions: 3", "- Total sessions: 30"))
    plan = write_plan(plan_text)
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 0, out
    assert "30" in out


def test_missing_cluster_specification_warns_rather_than_fails(cluster, run_validator, plan_text):
    """CDP-27"""
    root, write_plan = cluster
    (root / "cluster-specification.md").unlink()
    plan = write_plan(plan_text)
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 0, out
    assert "warn" in out.lower()


# --- dates (CDP-28, CDP-29) -----------------------------------------------

def test_non_iso_date_fails_naming_the_value(cluster, run_validator, plan_text):
    """CDP-28 — dates are derived, but a wrong one schedules a session on a day that does not exist."""
    _root, write_plan = cluster
    plan = write_plan(plan_text.replace("| 1 | 2026-10-08 |", "| 1 | 8 Oct       |"))
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 1
    assert "8 Oct" in out


def test_dates_going_backwards_fail(cluster, run_validator, plan_text):
    """CDP-29 — sessions run forward in time."""
    _root, write_plan = cluster
    plan = write_plan(plan_text.replace("| 3 | 2026-10-09 |", "| 3 | 2026-10-01 |"))
    code, out = run_validator("--plan", plan, *fmt())
    assert code == 1
    assert "backwards" in out.lower() or "order" in out.lower()
