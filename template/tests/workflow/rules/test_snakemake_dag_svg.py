"""Integration tests for building documentation."""

import shutil
from pathlib import Path

import pytest

from .conftest import _snakemake


# --- Fixtures ---------------------------------------------------------------
@pytest.fixture(autouse=True)
def create_dummy_input_data(
    workspace: Path,
    request: pytest.FixtureRequest,
):
    """Create the expected input files so Snakemake can build the DAG."""

    # Copy the test data for the `all_data` rule
    repo_root = request.config.rootdir
    (workspace / "data" / "tests").mkdir(parents=True, exist_ok=True)
    shutil.copytree(repo_root / "data/tests", workspace / "data" / "tests")


# --- Tests ------------------------------------------------------------------
def test_dag_svg(workspace: Path) -> None:
    _snakemake(workspace, ["dag_svg_all"])

    # Ideally, we would check that the SVG file exists and is valid.
    # However, the file gets generated in the cached directory of the
    # workflow module under test within the dummy parent workspace.
    # For now, we just check that the rule runs without errors.
