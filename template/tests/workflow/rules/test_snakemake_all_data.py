"""
Integration tests for running the `all_data` rule in the Snakemake workflow.
"""

import shlex
import subprocess
from pathlib import Path
from typing import List

import pytest
from loguru import logger

# --- Fixtures ---------------------------------------------------------------
# (workspace fixture is now provided by conftest.py)


# --- Helpers ----------------------------------------------------------------
def _snakemake(workspace: Path, extra: List[str]) -> None:
    """Thin wrapper so the command line is only written once."""

    cmd = [
        "snakemake",
        *extra,
    ]

    logger.debug(f"Executing: {shlex.join(cmd)}")

    subprocess.run(
        cmd,
        cwd=workspace,
        check=True,
    )


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
