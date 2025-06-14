#!/usr/bin/env python3
"""
Render template “sandbox examples” from *extra-answers* YAML files.

The files listed in ``EXTRA_ANSWER_FILES`` contain **partial / overriding
answers** that supplement the defaults defined in the template’s
``copier.yml`` (or ``copier.yaml``).  They are **not** the
``.copier-answers.yml`` files created during an interactive run.

For each YAML file we:

1. Derive an output directory   →  ``sandbox/<stem>/``.
2. Clean that directory if it already exists.
3. Invoke ``copier copy`` with ``--defaults`` & ``--answers-file`` so
   the run is fully non-interactive.

Usage
-----
    python scripts/sandbox_examples_generate.py
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import List, Optional

import typer
from pytest_copie.plugin import Copie
from ruamel.yaml import YAML

# List extra-answers YAML files to render as examples.
# Files whose name ends with ``_update.yml`` are *not* processed here.
# They are handled by :pyfile:`sandbox_examples_update.py`.
EXTRA_ANSWER_FILES: List[Path] = [
    Path("example-answers-able.yml"),
    Path("example-answers-weh_interviews.yml"),
]


TEMPLATE_DIR: Path = Path(__file__).resolve().parents[1]  # project root
SANDBOX_ROOT: Path = TEMPLATE_DIR / "sandbox"  # output root


def _render_example(answers_yml: Path) -> None:
    """Run Copier once for ``answers_yml``.

    Parameters
    ----------
    answers_yml
        Extra-answers YAML file that overrides template defaults.
    """
    if not answers_yml.is_file():
        raise FileNotFoundError(f"Answers file not found: {answers_yml}")

    dest_dir = SANDBOX_ROOT / answers_yml.stem
    if dest_dir.exists():
        shutil.rmtree(dest_dir)

    # --- 1. read answers YAML -> dict -----------------------------------------
    yaml = YAML(typ="safe")
    with answers_yml.open() as fp:
        answers_dict = yaml.load(fp) or {}

    # --- 2. build a minimal copier configuration ------------------------------
    copier_cfg = _create_copier_config(dest_dir / ".copier_config")

    # --- 3. run the copy through pytest-copie ---------------------------------
    copie = Copie(TEMPLATE_DIR, dest_dir, copier_cfg)
    result = copie.copy(extra_answers=answers_dict)

    if result.exception:
        typer.echo(
            f"❌  Generating {answers_yml.name} failed "
            f"(exit={result.exit_code}): {result.exception}",
            err=True,
        )
        raise SystemExit(result.exit_code or 1)

    # pytest-copie nests the project inside dest_dir/copie000…  Flatten it.
    inner = result.project_dir
    if inner and inner.parent == dest_dir:
        for p in inner.iterdir():
            target = dest_dir / p.name
            if target.exists():
                shutil.rmtree(target) if target.is_dir() else target.unlink()
            p.rename(target)
        shutil.rmtree(inner, ignore_errors=True)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _create_copier_config(base: Path) -> Path:
    """Create the minimal config file expected by `Copie` and return its path."""
    copier_dir = base / "copier"
    replay_dir = base / "copier_replay"
    copier_dir.mkdir(parents=True, exist_ok=True)
    replay_dir.mkdir(exist_ok=True)

    cfg = {"copier_dir": str(copier_dir), "replay_dir": str(replay_dir)}
    cfg_path = base / "config"

    yaml = YAML(typ="safe")
    with cfg_path.open("w") as fp:
        yaml.dump(cfg, fp)

    return cfg_path


app = typer.Typer(help="Render sandbox examples from Copier extra-answer files.")


@app.command()
def generate(
    files: Optional[List[Path]] = typer.Argument(
        None,
        help="Extra-answers YAML files to render. "
        "If omitted, uses the hard-coded EXTRA_ANSWER_FILES list.",
    ),
) -> None:
    """
    Render each *extra-answers* YAML file into ``sandbox/<stem>/``.

    Examples
    --------

    # Render all defaults
    python scripts/sandbox_examples_generate.py

    # Render only a subset
    python scripts/sandbox_examples_generate.py example-answers-able.yml
    """
    SANDBOX_ROOT.mkdir(exist_ok=True)

    answers_files = files or EXTRA_ANSWER_FILES
    for answers in answers_files:
        _render_example(answers)


if __name__ == "__main__":
    app()
