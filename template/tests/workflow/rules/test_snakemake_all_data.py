"""
Integration tests for running the `all_data` rule in the Snakemake workflow.
"""

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
    shutil.copytree(repo_root / "data/tests", workspace / "data")


# --- Tests ------------------------------------------------------------------
def test_snakemake_all_data(workspace: Path) -> None:
    """Dry run the `all_data` rule to ensure it can be executed."""
    _snakemake(workspace, ["--dry-run", "all_data"])
