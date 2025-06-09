"""Integration tests for building documentation."""

import shlex
import subprocess
from pathlib import Path
from typing import List

from loguru import logger


def _snakemake(workspace: Path, extra: List[str]) -> None:
    cmd = ["snakemake", *extra]
    logger.debug(f"Executing: {shlex.join(cmd)}")
    subprocess.run(cmd, cwd=workspace, check=True)


# TODO-copier-package implement this test when the docs build is ready
# @pytest.mark.order(1)
# def test_docs_build(workspace: Path) -> None:
#     _snakemake(workspace, ["--dry-run", "docs_build"])
