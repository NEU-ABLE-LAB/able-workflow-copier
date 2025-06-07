"""
Parametrise a test *dynamically* so that:

  - every answer-set (variant)          --> 'variant_id'
  - every tox env inside that variant   --> 'env_name'

gets its own, independent pytest test.
"""

from __future__ import annotations
import subprocess
import pytest
from pathlib import Path

from .conftest import answer_sets


###############################################################################
# 1.  Dynamic parametrisation --------------------------------------------------
###############################################################################


def pytest_generate_tests(metafunc):
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

                from copier import run_copy
                import tempfile, shutil, textwrap, os

                tmpdir: Path = Path(tempfile.mkdtemp(prefix=f"collect_{var_id}_"))
                try:
                    run_copy(
                        src_path=str(
                            Path(__file__).resolve().parents[2]
                        ),  # template root
                        dst_path=str(tmpdir),
                        data=entry["answers"],
                        quiet=True,
                        unsafe=True,
                    )
                    envs = subprocess.check_output(
                        ["tox", "-qq", "-l"], cwd=tmpdir, text=True
                    ).splitlines()
                    env_matrix[var_id] = [e.strip() for e in envs if e.strip()]
                finally:
                    shutil.rmtree(tmpdir, ignore_errors=True)

            for env in env_matrix[var_id]:
                argvalues.append((var_id, env))
                argids.append(f"{var_id}:{env}")

        metafunc.parametrize(
            ("variant_id", "env_name"), argvalues, ids=argids, scope="session"
        )

        # Stash matrix for later reuse by fixtures
        metafunc.config._env_matrix_cache = env_matrix


###############################################################################
# 2.  The actual test ---------------------------------------------------------
###############################################################################


def _answers_for(var_id: str):
    return next(v["answers"] for v in answer_sets if v["id"] == var_id)


def test_inner_tox_env_passes(copie_session, variant_id, env_name):
    """
    1. Render the template for *this* variant
    2. Run its tox env
    3. Assert success
    """
    answers = _answers_for(variant_id)
    result = copie_session.copy(extra_answers=answers)

    completed = subprocess.run(
        ["tox", "-qq", "-e", env_name],
        cwd=result.project_dir,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, (
        f"variant={variant_id!s} env={env_name!s}\n"
        f"stdout:\n{completed.stdout}\n"
        f"stderr:\n{completed.stderr}"
    )
