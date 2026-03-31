"""Validate committed workflow config files against matching schemas."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from snakemake.utils import validate

ROOT = Path(__file__).parents[4]
SCHEMAS_DIR = ROOT / "workflow" / "schemas"
CONFIG_DIR = ROOT / "config"


def _discover_pairs() -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []

    for schema_path in sorted(SCHEMAS_DIR.rglob("config.schema.yaml")):
        relative_parent = schema_path.relative_to(SCHEMAS_DIR).parent
        config_path = CONFIG_DIR / relative_parent / "config.yaml"
        if config_path.is_file():
            pairs.append((schema_path, config_path))

    return pairs


PAIRS = _discover_pairs()
if not PAIRS:
    msg = (
        "No schema/config pairs discovered; expected files matching "
        f"{SCHEMAS_DIR}/**/config.schema.yaml with corresponding "
        f"{CONFIG_DIR}/**/config.yaml."
    )
    raise AssertionError(msg)


@pytest.mark.parametrize(
    ("schema_path", "config_path"),
    PAIRS,
    ids=[str(schema_path.relative_to(SCHEMAS_DIR)) for schema_path, _ in PAIRS],
)
def test_committed_config_validates_against_schema(
    schema_path: Path,
    config_path: Path,
) -> None:
    with config_path.open("r", encoding="utf-8") as fh:
        config = yaml.safe_load(fh) or {}

    validate(config, str(schema_path))