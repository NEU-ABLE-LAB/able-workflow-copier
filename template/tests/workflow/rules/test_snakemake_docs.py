"""Integration tests for building documentation."""

import shutil
from pathlib import Path

import pytest

from . import _snakemake


# --- Fixtures ---------------------------------------------------------------
@pytest.fixture(autouse=True)
def create_dummy_input_data(
    workspace: Path,
    request: pytest.FixtureRequest,
):
    """Create the expected input files so Snakemake can build the DAG."""

    # Copy the test data for the `all_data` rule
    repo_root = request.config.rootdir
    shutil.copytree(repo_root / "data/tests", workspace / "data")


# --- Tests ------------------------------------------------------------------
def test_docs_build(workspace: Path) -> None:
    _snakemake(workspace, ["--force", "docs_build"])
