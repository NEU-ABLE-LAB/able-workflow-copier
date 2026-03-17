"""
Integration tests for running the `all_data` rule in the Snakemake workflow.
"""

from pathlib import Path

import pytest

from . import _load_touch_paths, _snakemake


# --- Fixtures ---------------------------------------------------------------
@pytest.fixture(autouse=True)
def create_dummy_input_data(
    workspace: Path,
    request: pytest.FixtureRequest,
):
    """Create the expected input files so Snakemake can build the DAG."""

    project_root = request.config.rootdir
    yaml_manifest = project_root / "data" / "tests" / "dry-run" / "all.yaml"

    # Touch the required input files based on the manifest
    for rel_path in _load_touch_paths(yaml_manifest):
        fp = workspace / "data" / rel_path
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.touch()


# --- Tests ------------------------------------------------------------------
def test_snakemake_all_data(workspace: Path) -> None:
    """Dry run the `all_data` rule to ensure it can be executed."""
    _snakemake(workspace, ["--dry-run", "all_data"])
