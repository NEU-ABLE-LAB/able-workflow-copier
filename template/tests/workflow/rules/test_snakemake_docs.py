"""Integration tests for building documentation."""

from pathlib import Path

import pytest

from .conftest import _snakemake


# --- Tests ------------------------------------------------------------------
@pytest.mark.order(1)
def test_localize_conda_envs(workspace: Path) -> None:
    """Step 1 - make the env YAML files local."""
    _snakemake(workspace, ["conda_localize"])


# TODO-copier-package implement this test when the docs build is ready
# @pytest.mark.order(2)
# def test_docs_build(workspace: Path) -> None:
#     _snakemake(workspace, ["--dry-run", "docs_build"])
