"""Tests for validate_mapping_doc.build_oracle — the Gate 10 accuracy oracle.

The oracle is what the gate measures a mapping docx against. For CL2/CL3 it inverts the assessors'
machine-readable benchmarks, which is genuinely independent of the mapping generator. For CL1 it
reads the generator's own DATA_* dicts, so it can only ever agree with itself.

Every fixture below builds a synthetic cluster (S1-CL9) whose assessor reverse maps DISAGREE with
its DATA_* dicts. A correct oracle follows the assessors; the current one follows DATA_*.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate_mapping_doc as V  # noqa: E402


# ---------------------------------------------------------------------------
# Fixture: a synthetic cluster whose assessor and DATA_* deliberately disagree
# ---------------------------------------------------------------------------

ASSESSOR = '''
MARKING = [
    ["A1 Network foundation", "[ICTTEST101 PC 1.2]"],
    ["A5 Monitoring", "[ICTTEST101 PC 3.1]"],
    ["A10 Handover", "[ICTTEST101 PC 1.1]"],
]

ASSESSOR_BODY = [
    ("h1", "UoC coverage verification (reverse map)"),
    ("p", "ICTTEST101 - Test unit"),
    ("tbl", [
        ["UoC item", "Evidenced by criterion(ia)"],
        ["PC 1.1 - Handover and filing", "A10"],
        ["PC 1.2 - Build the network", "A1"],
        ["PC 2.1 - Something retired", "A1"],
    ]),
]
'''

BUILD = '''
DATA_101 = {
    "pcs": {
        # DISAGREES with the assessor: its reverse map says A10.
        "1.1": {"AT1": "A9", "AT2": "", "AT3": ""},
        # AGREES with the assessor.
        "1.2": {"AT1": "A1", "AT2": "", "AT3": ""},
        # PHANTOM: B11 appears in no marking guide in this cluster.
        "2.1": {"AT1": "B11", "AT2": "", "AT3": ""},
    },
    "pes": [],
    "kes": [],
    "fss": {},
    "acs": [],
}

UNIT_DATA = {"101": ("ICTTEST101_Assessment_Mapping.docx", DATA_101)}
'''


@pytest.fixture
def cluster(tmp_path):
    """A cluster laid out the way build_oracle expects to find one."""
    cdir = tmp_path / "S1-CL9-Test"
    (cdir / "mappings").mkdir(parents=True)
    scripts = tmp_path / "scripts" / "s1_cl9"
    scripts.mkdir(parents=True)
    (scripts / "build_s1_cl9_mapping_docs.py").write_text(BUILD)
    (scripts / "build_s1_cl9_at1_assessor.py").write_text(ASSESSOR)
    yield cdir
    for m in ("build_s1_cl9_mapping_docs", "build_s1_cl9_at1_assessor"):
        sys.modules.pop(m, None)


def codes_for(oracle, pc, at="AT1"):
    return oracle.get(("PC", pc), {}).get(at, set())


# ---------------------------------------------------------------------------
# The defects
# ---------------------------------------------------------------------------

def test_oracle_follows_the_assessor_not_the_generator(cluster):
    """PC 1.1: the assessor's reverse map says A10; DATA_* says A9.

    The oracle exists to catch exactly this drift, so it must report A10. Reporting A9 means the
    gate is comparing the docx against the data that produced it and can only agree with itself.
    """
    oracle, note = V.build_oracle(cluster, "ICTTEST101")
    assert oracle is not None, note
    assert codes_for(oracle, "1.1") == {"A10"}


def test_oracle_rejects_a_code_no_marking_guide_defines(cluster):
    """PC 2.1: DATA_* claims B11, which appears in no marking guide in this cluster.

    A criterion code that does not exist cannot evidence anything. The oracle must not bless it.
    """
    oracle, note = V.build_oracle(cluster, "ICTTEST101")
    assert oracle is not None, note
    assert "B11" not in codes_for(oracle, "2.1")


def test_oracle_is_independent_of_the_generator(cluster):
    """Editing DATA_* alone must not move the oracle — otherwise it is not an oracle.

    Rewrite DATA_*'s cells and rebuild. An assessor-derived oracle is unchanged; a DATA_*-derived
    one follows the edit. The replacement changes the file's length deliberately: same-length,
    same-second rewrites are served from importlib's bytecode cache and the edit silently no-ops.
    """
    build = cluster.parent / "scripts" / "s1_cl9" / "build_s1_cl9_mapping_docs.py"
    edited = BUILD.replace('"A9"', '"A7, A8, A9, A12"')
    assert len(edited) != len(BUILD), "the edit must change the file size to defeat the .pyc cache"
    build.write_text(edited)
    for m in ("build_s1_cl9_mapping_docs", "build_s1_cl9_at1_assessor"):
        sys.modules.pop(m, None)

    oracle, note = V.build_oracle(cluster, "ICTTEST101")
    assert oracle is not None, note
    # The assessor still says A10 and nothing about it changed, so the oracle must still say A10.
    assert codes_for(oracle, "1.1") == {"A10"}


def test_accuracy_fails_a_docx_that_matches_only_the_generator(cluster):
    """End-to-end: a docx carrying DATA_*'s A9 for PC 1.1 must FAIL, because the assessor says A10.

    This is the shape of the real defect — 16 wrong AT2 codes shipped through a green Gate 10.
    """
    oracle, note = V.build_oracle(cluster, "ICTTEST101")
    assert oracle is not None, note
    mapping = {s: [] for s in V.SECTIONS}
    mapping["PC"] = [("1.1 Handover and filing", ("A9", "", ""))]
    hard_fails, _ = V.check_accuracy(mapping, oracle)
    assert hard_fails, "a docx that agrees only with DATA_* should not pass Gate 10"


# ---------------------------------------------------------------------------
# Regression guard — must pass before AND after the rewrite
# ---------------------------------------------------------------------------

def test_agreeing_cells_still_validate(cluster):
    """PC 1.2 agrees in both sources. It must keep passing; the fix must not break the good path."""
    oracle, note = V.build_oracle(cluster, "ICTTEST101")
    assert oracle is not None, note
    mapping = {s: [] for s in V.SECTIONS}
    mapping["PC"] = [("1.2 Build the network", ("A1", "", ""))]
    hard_fails, _ = V.check_accuracy(mapping, oracle)
    assert not hard_fails, hard_fails
