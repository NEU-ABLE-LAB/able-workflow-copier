"""Integration test for the `dag_svg` rule in the Snakemake workflow."""

from pathlib import Path

import pytest

from .conftest import _snakemake


# --- Tests ------------------------------------------------------------------
@pytest.mark.order(1)
def test_localize_conda_envs(workspace: Path) -> None:
    """Step 1 - make the env YAML files local."""
    _snakemake(workspace, ["conda_localize"])


# @pytest.mark.order(2)
# def test_dag_svg(workspace: Path) -> None:
#     _snakemake(workspace, ["--dry-run", "dag_svg"])
