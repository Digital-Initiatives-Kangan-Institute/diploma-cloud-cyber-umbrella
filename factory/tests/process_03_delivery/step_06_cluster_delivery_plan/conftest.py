"""Fixtures for delivery step 06 — the cluster delivery-plan validator.

Puts the step's own scripts/ directory on sys.path (the project's standard resolution: insert the
directory, import the flat module name), and builds the on-disk shapes the validator reads.
"""
import subprocess
import sys
from pathlib import Path

import pytest

STEP = Path(__file__).resolve().parents[3] / "process_03_delivery" / "step_06_cluster_delivery_plan"
SCRIPTS = STEP / "scripts"
VALIDATOR = SCRIPTS / "validate_cluster_delivery_plan.py"
FORMAT_DOC = STEP / "_02_delivery-plan-format.md"
# The institutional template is course content, so it lives in the content repo, not the factory.
TEMPLATE = (Path(__file__).resolve().parents[4] / "diploma-cloud-cyber-content-s1"
            / "kangan-templates" / "Delivery_Plan_Template_v0.1.docx")

sys.path.insert(0, str(SCRIPTS))


# A baseline that PASSES: 3 sessions, one Topic, one assessment, one spare — matching the frame below.
BASELINE_PLAN = """\
# S1-CL9 Test Cluster — Delivery Plan (2026-T2)
> **INSTANCE: 2026-T2.** Frame: cluster-specification.md · Generates: S1_CL9_Delivery_Plan.docx

## 1. Instance prerequisites
- Intake: 2026-T2
- Total sessions available: 3
- Teaching days per week: 2
- Teaching days: Thursday, Friday
- Online/classroom split: all online
- Assessment types: AT1: Project

## 2. Document details
- Qualification code and title: ICT50220 Diploma of Information Technology
- Unit code and title: ICTCLD501 Design and implement a cloud disaster recovery strategy
- Cohort description: Test cohort, 2026-T2
- Materials and resources: AWS Academy Learner Lab; the cluster workbooks

## 3. Session grid
| # | Date       | Week | Day | Time     | Mode   | Activity   | Placed |
|---|------------|------|-----|----------|--------|------------|--------|
| 1 | 2026-10-08 | 9    | Thu | 9am-12pm | online | teach      | T1     |
| 2 | 2026-10-08 | 9    | Thu | 1pm-4pm  | online | assessment | AT1    |
| 3 | 2026-10-09 | 9    | Fri | 9am-12pm | online | spare      | —      |

## 4. Notes / decisions
- baseline used by the step-06 test suite.

## Changelog
- 2026-09-09 — created for testing.
"""

BASELINE_FRAME = """\
# S1-CL9 Test Cluster — Cluster Specification

## 1. Delivery frame
- Total sessions: 3

## 3. Topic budget
- Onboarding sessions: 0
- Spare sessions: 1
- Dedicated assessment sessions: 1
"""


ASSESSMENT_PLAN = """\
# S1-CL9 Test Cluster — Assessment Plan

### AT1 — Cloud Expansion: Design & DR Plan

Some prose about AT1.
"""


CONSOLIDATED_UOC = """\
# S1-CL9 Test Cluster — Consolidated UoC

## Foundation skills

- **Reading** — Interprets complex technical documentation [ICTCLD501 FS Reading]
- **Writing** — Develops complex documentation in required formats [ICTCLD503 FS Writing]
- **Planning and organising** — Evaluates and resolves risk events [ICTCLD501 FS Planning and organising]
"""


TOPIC_COVERAGE = """\
# Topic 01 — Test topic · Coverage

**Topic 01 of 1** · **AT1 content Topic**

### UoC mapping — taught / developed

| Component | Teaches |
|---|---|
| C1 | [ICTCLD501 PC 1.1] |
| C2 | [ICTCLD501 KE 2] |
"""


@pytest.fixture
def plan_text():
    """The valid baseline outline. A test mutates it to introduce exactly one defect."""
    return BASELINE_PLAN


@pytest.fixture
def cluster(tmp_path):
    """Build a cluster on disk and return a helper that writes its plan.

    Returns (cluster_dir, write_plan) where write_plan(text) writes delivery/delivery-plan.md
    and returns its path.
    """
    root = tmp_path / "S1-CL9-Test-Cluster"
    (root / "delivery" / "topic_01").mkdir(parents=True)
    (root / "assessments" / "AT1").mkdir(parents=True)
    (root / "cluster-specification.md").write_text(BASELINE_FRAME, encoding="utf-8")
    (root / "delivery" / "topic_01" / "coverage.md").write_text(TOPIC_COVERAGE, encoding="utf-8")
    (root / "consolidated_uoc.md").write_text(CONSOLIDATED_UOC, encoding="utf-8")
    (root / "assessments" / "assessment_plan.md").write_text(ASSESSMENT_PLAN, encoding="utf-8")

    def write_plan(text: str = BASELINE_PLAN) -> Path:
        p = root / "delivery" / "delivery-plan.md"
        p.write_text(text, encoding="utf-8")
        return p

    return root, write_plan


@pytest.fixture
def run_validator():
    """Invoke the validator as a subprocess; return (exit_code, combined output).

    Run as a subprocess rather than by importing main(): the exit code and the printed message are
    both part of the contract, and a human reads the message to learn what decision is outstanding.
    """
    def _run(*args) -> tuple[int, str]:
        proc = subprocess.run(
            [sys.executable, str(VALIDATOR), *map(str, args)],
            capture_output=True, text=True,
        )
        return proc.returncode, proc.stdout + proc.stderr
    return _run
