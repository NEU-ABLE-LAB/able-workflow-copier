"""
Integration tests for running the `all_data` rule in the Snakemake workflow.
"""

import shutil
from pathlib import Path

import pytest
from ruamel.yaml import YAML

from .conftest import _snakemake


# --- Fixtures ---------------------------------------------------------------
@pytest.fixture(autouse=True)
def create_dummy_input_data(
    workspace: Path,
    request: pytest.FixtureRequest,
):
    """Create the expected input files so Snakemake can build the DAG."""

    # Get the file manifest for the `all` rule
    rule_name = "all"
    project_root = request.config.rootdir
    yaml_manifest = project_root / "data" / "tests" / f"{rule_name}.yaml"
    if not yaml_manifest.exists():
        raise FileNotFoundError(
            f"Manifest file for rule '{rule_name}' not found: {yaml_manifest}"
        )

    # Load the YAML manifest to get the required input files
    yaml = YAML(typ="safe")
    with yaml_manifest.open("r", encoding="utf-8") as fh:
        manifest = yaml.load(fh) or {}

    # Touch the required input files based on the manifest
    for rel_path in manifest.get("files", []):
        fp = workspace / "data" / rel_path
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.touch()


# --- Tests ------------------------------------------------------------------
def test_snakemake_all_data(workspace: Path) -> None:
    """Dry run the `all_data` rule to ensure it can be executed."""
    _snakemake(workspace, ["--dry-run", "all_data"])
