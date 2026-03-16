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
import sys
import tempfile
from pathlib import Path

import pytest
from copier import run_copy
from loguru import logger

from scripts.copie_helpers import run_copie_with_output_control
from .conftest import answer_sets


# --- Helpers ----------------------------------------------------------------
def _answers_for(var_id: str):
    """
    Get the answers for a given variant ID from the global answer_sets.
    """
    return next(v["answers"] for v in answer_sets if v["id"] == var_id)


def _template_head_ref(template_root: Path) -> str:
    """Return the immutable git ref for the template root."""
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=template_root,
        text=True,
    ).strip()


def _assert_template_repo_is_clean(template_root: Path) -> None:
    """Raise a usage error when the template repository has local changes."""
    try:
        status = subprocess.check_output(
            ["git", "status", "--porcelain", "--ignore-submodules=none"],
            cwd=template_root,
            text=True,
        ).splitlines()
    except FileNotFoundError as exc:
        raise pytest.UsageError("`git` executable not found in PATH") from exc
    except subprocess.CalledProcessError as exc:
        raise pytest.UsageError(
            f"Failed to check git status for template root: {template_root}"
        ) from exc

    dirty = [line for line in status if line.strip()]
    if not dirty:
        return

    max_items = 20
    shown = "\n".join(f"  {line}" for line in dirty[:max_items])
    suffix = (
        f"\n  ... and {len(dirty) - max_items} more" if len(dirty) > max_items else ""
    )
    raise pytest.UsageError(
        "Template repo is dirty; refusing to run template-tox collection.\n"
        "Please commit/stash/discard local changes first.\n"
        f"Template root: {template_root}\n"
        "Dirty entries:\n"
        f"{shown}{suffix}"
    )


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
        template_root = Path(__file__).resolve().parents[3]
        _assert_template_repo_is_clean(template_root)
        template_ref = _template_head_ref(template_root)

        for entry in answer_sets:
            var_id = entry["id"]

            # Lazily copy template just once per variant *at collection time*
            if var_id not in env_matrix:

                tmpdir: Path = Path(tempfile.mkdtemp(prefix=f"collect_{var_id}_"))
                try:
                    run_copy(
                        src_path=str(template_root),
                        dst_path=str(tmpdir),
                        data=entry["answers"],
                        vcs_ref=template_ref,
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
            # environments for this variant.
            # This is done via the `--template-envs` option.
            # SEE: pytest_addoption() in conftest.py
            try:
                requested = set(metafunc.config.getoption("inner_envs") or [])
            except ValueError:
                # If the option is not set, use an empty set
                requested = set()

            for env in env_matrix[var_id]:
                # If the user asked for a subset (--inner-envs=*) keep only those
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


# --- Tests ------------------------------------------------------------------
def test_inner_tox_env_passes(copie_session, variant_id, env_name, request):
    """Run the tox tests within a rendered project variant."""

    # Render the template for this variant
    answers = _answers_for(variant_id)

    verbosity = request.config.getoption("verbose")
    if verbosity >= 2:
        logger.info(f"Rendering variant {variant_id}")

    result = run_copie_with_output_control(request.config, copie_session, answers)

    if verbosity >= 2:
        logger.info(f"Copier successfully rendered variant {variant_id}")

    # Ensure the project directory is a Git repo (for setuptools-scm)
    _bootstrap_git_repo(result.project_dir)

    # Determine if the tox environment should run in parallel or not.
    # If the user specified --tox-no-parallel, run tox in serial.
    # SEE: pytest_addoption() in conftest.py
    extra_args = ["--"]
    if request.config.getoption("tox_no_parallel"):
        run_args = ["run"]
    else:
        run_args = [
            "run-parallel",
            "--parallel-no-spinner",
        ]

    if request.config.getoption("capture") in ["no", "tee-sys"]:
        # If --capture=no or -s is specified, disable output capturing
        extra_args.extend(
            [
                "--force-sugar",
            ]
        )

    if request.config.getoption("template_no_capture"):
        # If --template-no-capture is specified, disable output capturing
        extra_args.extend(
            [
                "--capture=no",
            ]
        )

    verbosity = request.config.getoption("verbose")
    if verbosity >= 2:
        # If verbosity is 2 or higher, enable debug output
        extra_args.append("-vv")
    elif verbosity == 1:
        # If verbosity is 1, enable info output
        extra_args.append("-v")

    # Setup tox environments
    setup_args = [
        "tox",
        "run-parallel",
        "--parallel-no-spinner",
        "--notest",
        "--skip-missing-interpreters",
        "false",
        "-e",
        env_name,
    ]
    if verbosity >= 2:
        subprocess.run(
            setup_args,
            cwd=result.project_dir,
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True,
        )
    else:
        subprocess.run(
            setup_args,
            cwd=result.project_dir,
            check=True,
            capture_output=True,
            text=True,
        )

    # Run the tox tests within the rendered project
    process = subprocess.Popen(
        [
            "tox",
            *run_args,
            "--skip-pkg-install",
            "--quiet",
            "-e",
            env_name,
            *extra_args,
        ],
        cwd=result.project_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    stdout, stderr = [], []

    # Stream output live and capture
    for line in process.stdout:
        sys.stdout.write(line)
        stdout.append(line)
    for line in process.stderr:
        sys.stderr.write(line)
        stderr.append(line)

    process.wait()
    completed = subprocess.CompletedProcess(
        process.args, process.returncode, "".join(stdout), "".join(stderr)
    )

    # Assert the tox run was successful
    assert completed.returncode == 0, (
        f"variant={variant_id} env={env_name}\n"
        f"stdout:\n{completed.stdout}\n"
        f"stderr:\n{completed.stderr}"
    )
