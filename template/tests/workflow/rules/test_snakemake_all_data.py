"""
Integration tests for running the `all_data` rule in the Snakemake workflow.
"""

from pathlib import Path

import pytest
from loguru import logger

from .conftest import _snakemake

# --- Fixtures ---------------------------------------------------------------
# Track which workspaces have had the dummy file created
_CREATED_DUMMY_INPUT = set()


@pytest.fixture(autouse=True)
def create_dummy_input_file(workspace):
    """Create the expected input file so Snakemake can build the DAG, only once per workspace."""
    workspace_id = str(workspace.resolve())
    if workspace_id in _CREATED_DUMMY_INPUT:
        return

    # Create a dummy input file for the `all_data` rule
    readme = workspace / "data" / "README.md"
    readme.parent.mkdir(parents=True, exist_ok=True)
    readme.touch()

    logger.debug(f"Created dummy input file: {readme}")
    _CREATED_DUMMY_INPUT.add(workspace_id)


# --- Tests ------------------------------------------------------------------
@pytest.mark.order(1)
def test_localize_conda_envs(workspace: Path) -> None:
    """Step 1 - make the env YAML files local."""
    _snakemake(workspace, ["conda_localize"])


@pytest.mark.order(2)
def test_snakemake_conda_localize(workspace: Path) -> None:
    """Create required conda environments"""
    _snakemake(workspace, ["--conda-create-envs-only", "all_data"])


@pytest.mark.order(3)
def test_snakemake_all_data(workspace: Path) -> None:
    """Dry run the `all_data` rule to ensure it can be executed."""
    _snakemake(workspace, ["--dry-run", "all_data"])
