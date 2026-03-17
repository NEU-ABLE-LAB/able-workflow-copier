"""
This is not intended to be used as a module.

This __init__.py is only here to support coverage.py,
which needs to import the package in order to calculate coverage.
"""

import shlex
import subprocess
import sys
from pathlib import Path
from typing import List

from loguru import logger
from ruamel.yaml import YAML


def _snakemake(workspace: Path, extra: List[str], verbose: bool = True) -> None:
    cmd = [
        "snakemake",
        "--show-failed-logs",
        *extra,
    ]

    logger.debug(f"Executing: {shlex.join(cmd)}")

    try:
        cp = subprocess.run(
            cmd,
            cwd=workspace,
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        sys.stderr.write(
            f"\n===== Snakemake Error stdout =====\n{e.stdout.decode('utf-8')}"
            f"\n===== Snakemake Error stderr =====\n{e.stderr.decode('utf-8')}\n"
        )
        raise

    if cp.returncode:
        sys.stderr.write(
            f"\n===== Snakemake Return Code stdout =====\n{cp.stdout.decode('utf-8')}"
            f"\n===== Snakemake Return Code stderr =====\n{cp.stderr.decode('utf-8')}\n"
        )
        cp.check_returncode()

    if verbose:
        sys.stdout.write(
            f"\n===== Snakemake Verbose stdout =====\n{cp.stdout.decode('utf-8')}"
            f"\n===== Snakemake Verbose stderr =====\n{cp.stderr.decode('utf-8')}\n"
        )


def _manifest_entries(
    entries: object,
    key: str,
    manifest_path: Path,
) -> list[str]:
    if entries is None:
        return []
    if not isinstance(entries, list) or any(
        not isinstance(item, str) for item in entries
    ):
        raise TypeError(
            f"Manifest key '{key}' in {manifest_path} must be a list of strings."
        )
    return entries


def _load_touch_paths(
    manifest_path: Path,
    seen: set[Path] | None = None,
) -> list[str]:
    manifest_path = manifest_path.resolve()
    if seen is None:
        seen = set()
    if manifest_path in seen:
        raise ValueError(
            f"Recursive dry-run manifest include detected: {manifest_path}"
        )
    if not manifest_path.exists():
        raise FileNotFoundError(f"Dry-run manifest not found: {manifest_path}")

    yaml = YAML(typ="safe")
    with manifest_path.open("r", encoding="utf-8") as fh:
        manifest = yaml.load(fh) or {}

    if not isinstance(manifest, dict):
        raise TypeError(f"Dry-run manifest must be a mapping: {manifest_path}")

    next_seen = seen | {manifest_path}
    touch_paths: list[str] = []

    for include_rel in _manifest_entries(
        manifest.get("include"), "include", manifest_path
    ):
        touch_paths.extend(
            _load_touch_paths(manifest_path.parent / include_rel, next_seen)
        )

    touch_paths.extend(_manifest_entries(manifest.get("touch"), "touch", manifest_path))
    return list(dict.fromkeys(touch_paths))
