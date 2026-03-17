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
    python -m scripts.sandbox_examples_generate
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import List, Optional

import typer
from ruamel.yaml import YAML

from scripts.copie_helpers import make_copier_config, new_copie

TEMPLATE_DIR: Path = Path(__file__).resolve().parents[1]  # project root
EXAMPLE_ANSWERS_DIR: Path = TEMPLATE_DIR / "example-answers"
SANDBOX_ROOT: Path = TEMPLATE_DIR / "sandbox"  # output root

# List extra-answers YAML files to render as examples.
# Files whose name ends with ``_update.yml`` are *not* processed here.
# They are handled by :pyfile:`sandbox_examples_update.py`.
EXTRA_ANSWER_FILES: List[Path] = sorted(
    path
    for path in EXAMPLE_ANSWERS_DIR.glob("*.yml")
    if not path.name.endswith("_update.yml")
)


def _resolve_answers_file(answers_yml: Path) -> Path:
    """Resolve an answers file path from the repo root or example-answers directory."""
    if answers_yml.is_file():
        return answers_yml.resolve()

    if answers_yml.is_absolute():
        return answers_yml

    candidates = (
        TEMPLATE_DIR / answers_yml,
        EXAMPLE_ANSWERS_DIR / answers_yml.name,
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()

    return TEMPLATE_DIR / answers_yml


def _render_example(answers_yml: Path) -> None:
    """Run Copier once for ``answers_yml``.

    Parameters
    ----------
    answers_yml
        Extra-answers YAML file that overrides template defaults.
    """
    answers_yml = _resolve_answers_file(answers_yml)
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
    copier_cfg = make_copier_config(dest_dir / ".copier_config")

    # --- 3. run the copy through pytest-copie ---------------------------------
    copie = new_copie(
        template_dir=TEMPLATE_DIR,
        test_dir=dest_dir,
        config_file=copier_cfg,
    )
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
    python -m scripts.sandbox_examples_generate

    # Render only a subset
    python -m scripts.sandbox_examples_generate example-answers/example-answers-able.yml
    """
    SANDBOX_ROOT.mkdir(exist_ok=True)

    answers_files = files or EXTRA_ANSWER_FILES
    for answers in answers_files:
        _render_example(answers)


if __name__ == "__main__":
    app()
