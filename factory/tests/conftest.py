"""Put the factory's shared helpers on sys.path so tests import them by module name.

Mirrors how every script in this project resolves its dependencies: insert the helpers directory,
then import flat module names. Directory names never appear in an import statement, which is why the
numbered `process_NN_*` / `step_NN_*` folders are safe.
"""
import sys
from pathlib import Path

import pytest

HELPERS = Path(__file__).resolve().parents[1] / "common" / "helpers"
sys.path.insert(0, str(HELPERS))


@pytest.fixture
def format_doc(tmp_path):
    """Write a minimal format document with a ``## Skeleton`` fenced block.

    Returns a callable taking the skeleton body, so a test supplies only the contract it cares about.
    """
    def _write(skeleton_body: str, *, name: str = "thing-format.md", preamble: str = "") -> Path:
        p = tmp_path / name
        p.write_text(
            "# Thing format — standard\n\n"
            f"{preamble}\n\n"
            "## Skeleton\n\n"
            "```markdown\n"
            f"{skeleton_body}\n"
            "```\n",
            encoding="utf-8",
        )
        return p
    return _write


@pytest.fixture
def doc_tree(tmp_path):
    """Build a directory tree resembling the repo: an umbrella root with ``docs/``, a step folder,
    and a ``scripts/`` dir inside the step (where a ported validator lives).

    Returns (root, step_dir, scripts_dir).
    """
    root = tmp_path / "umbrella"
    docs = root / "docs"
    step = root / "factory" / "process_03_delivery" / "step_06_cluster_delivery_plan"
    scripts = step / "scripts"
    for d in (docs, scripts):
        d.mkdir(parents=True)
    return root, step, scripts
