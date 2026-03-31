"""Dry-run integration test for an imported workflow with no committed config."""

from pathlib import Path

import pytest

from . import _load_touch_paths, _snakemake


@pytest.fixture(autouse=True)
def create_dummy_input_data(
    workspace_empty_config: Path,
    request: pytest.FixtureRequest,
) -> None:
    """Create the expected input files so Snakemake can build the DAG."""

    project_root = request.config.rootdir
    yaml_manifest = project_root / "data" / "tests" / "dry-run" / "all.yaml"

    for rel_path in _load_touch_paths(yaml_manifest):
        fp = workspace_empty_config / "data" / rel_path
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.touch()


def test_snakemake_all_data_imported_empty_config(
    workspace_empty_config: Path,
) -> None:
    """Dry run `all_data` with no committed config files in the outer workflow."""
    _snakemake(workspace_empty_config, ["--dry-run", "all_data"])