"""Integration test for the `dag_svg` rule in the Snakemake workflow."""

import shlex
import subprocess
from pathlib import Path
from typing import List

import pytest
from loguru import logger


def _snakemake(workspace: Path, extra: List[str]) -> None:
    cmd = ["snakemake", *extra]
    logger.debug(f"Executing: {shlex.join(cmd)}")
    subprocess.run(cmd, cwd=workspace, check=True)


@pytest.mark.order(1)
def test_dag_svg(workspace: Path) -> None:
    _snakemake(workspace, ["--dry-run", "dag_svg"])
