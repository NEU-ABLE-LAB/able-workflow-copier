"""
Parametrise a test *dynamically* so that:

  - every answer-set (variant)          --> 'variant_id'
  - every tox env inside that variant   --> 'env_name'

gets its own, independent pytest test.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
import pytest

from copier import run_copy
from loguru import logger

from .conftest import answer_sets


# --- PyTest Hooks -----------------------------------------------------------
def pytest_generate_tests(metafunc):
    """
    Dynamically parametrize tests for pytest with all template variants and
    the tox tests within those rendered templates. This hook is called for
    each test function to generate parameters. It will only apply to tests
    that request the 'variant_id' and 'env_name' parameters.
    """

    # Only apply to the test that asks for these args
    if {"variant_id", "env_name"} <= set(metafunc.fixturenames):

        argvalues: list[tuple[str, str]] = []
        argids: list[str] = []

        # The env_matrix cache is built by the session fixture in conftest.py
        env_matrix = metafunc.config._env_matrix_cache = getattr(
            metafunc.config, "_env_matrix_cache", {}
        )

        for entry in answer_sets:
            var_id = entry["id"]

            # Lazily copy template just once per variant *at collection time*
            if var_id not in env_matrix:

                tmpdir: Path = Path(tempfile.mkdtemp(prefix=f"collect_{var_id}_"))
                try:
                    run_copy(
                        src_path=str(
                            Path(__file__).resolve().parents[3]
                        ),  # template root
                        dst_path=str(tmpdir),
                        data=entry["answers"],
                        defaults=True,
                        quiet=True,
                        unsafe=True,
                    )
                    envs = subprocess.check_output(
                        ["tox", "-qq", "-l"], cwd=tmpdir, text=True
                    ).splitlines()
                    env_matrix[var_id] = [e.strip() for e in envs if e.strip()]
                finally:
                    shutil.rmtree(tmpdir, ignore_errors=True)

            if not env_matrix[var_id]:
                logger.warning(f"No tox envs found for {var_id}, skipping")

            # Retrieve the requested environments to run.
            # If the user did not specify any, use all available
            # SEE: pytest_addoption() in conftest.py
            try:
                requested = set(metafunc.config.getoption("inner_envs") or [])
            except ValueError:
                # If the option is not set, use an empty set
                requested = set()

            for env in env_matrix[var_id]:
                # If the user asked for a subset (-e ...) keep only those
                if requested and env not in requested:
                    continue
                argvalues.append((var_id, env))
                argids.append(f"{var_id}:{env}")

        metafunc.parametrize(
            ("variant_id", "env_name"), argvalues, ids=argids, scope="session"
        )

        # Stash matrix for later reuse by fixtures
        metafunc.config._env_matrix_cache = env_matrix

    else:
        logger.warning(f"Skipping dynamic param for {metafunc.function}")


# --- Helpers ----------------------------------------------------------------
def _answers_for(var_id: str):
    """
    Get the answers for a given variant ID from the global answer_sets.
    """
    return next(v["answers"] for v in answer_sets if v["id"] == var_id)


def _bootstrap_git_repo(path: Path) -> None:
    """
    Ensure *path* is a Git repo with one commit so that setuptools-scm can
    discover a version string.

    Safe to call repeatedly: it does nothing if .git/ already exists.
    """
    if (path / ".git").exists():
        return

    # Initialise repo
    subprocess.run(
        ["git", "init", "--quiet", "--initial-branch=main"],
        cwd=path,
        check=True,
    )

    # Stage everything
    subprocess.run(["git", "add", "-A"], cwd=path, check=True)

    # Commit with throw-away identity (avoids global git config leakage)
    env = os.environ.copy()
    env.update(
        {
            "GIT_AUTHOR_NAME": "CI",
            "GIT_AUTHOR_EMAIL": "ci@example.invalid",
            "GIT_COMMITTER_NAME": "CI",
            "GIT_COMMITTER_EMAIL": "ci@example.invalid",
        }
    )
    subprocess.run(
        ["git", "commit", "--quiet", "-m", "Initial commit"],
        cwd=path,
        env=env,
        check=True,
    )


# --- Tests ------------------------------------------------------------------
def test_inner_tox_env_passes(copie_session, variant_id, env_name):
    """Run the tox tests within a rendered project variant."""

    # Render the template for this variant
    answers = _answers_for(variant_id)
    result = copie_session.copy(extra_answers=answers)

    # Ensure the project directory is a Git repo (for setuptools-scm)
    _bootstrap_git_repo(result.project_dir)

    # Run the tox tests within the rendered project
    completed = subprocess.run(
        ["tox", "run-parallel", "--quiet", "-e", env_name],
        cwd=result.project_dir,
        capture_output=True,
        text=True,
    )

    # Assert the tox run was successful
    assert completed.returncode == 0, (
        f"variant={variant_id!s} env={env_name!s}\n"
        f"stdout:\n{completed.stdout}\n"
        f"stderr:\n{completed.stderr}"
    )
