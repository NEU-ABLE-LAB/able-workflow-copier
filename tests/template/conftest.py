"""
Global fixtures & helpers for testing a Copier template with:

▪ multiple answer-sets (variants)
▪ one pytest test *per* tox env inside each rendered variant
"""

from __future__ import annotations
from pathlib import Path
import subprocess
import pytest
from typing import Any, Dict, cast
from ruamel.yaml import YAML


###############################################################################
# 1.  Define every permutation of answers you want to exercise
###############################################################################

ANSWERS_YAMLS = [
    Path("example-answers-able.yml"),
    Path("example-answers-weh_interviews.yml"),
]


def read_answers_yaml(answers_yaml: Path) -> Dict[Any, Any]:
    """
    Read the example answers YAML file into a dictionary.
    """
    if not answers_yaml.is_file():
        raise FileNotFoundError(f"Answers YAML file not found: {answers_yaml}")
    yaml = YAML(typ="safe")
    with answers_yaml.open("r") as file:
        return cast(Dict[Any, Any], dict(yaml.load(file)))


answer_sets = []
for answers_yaml in ANSWERS_YAMLS:
    answers = read_answers_yaml(answers_yaml)
    if not isinstance(answers, dict):
        raise TypeError(f"Answers YAML must decode to a dictionary: {answers_yaml}")

    # Create a single answer-set for this YAML file
    answer_set = {
        "id": answers_yaml.stem,  # Use the filename without extension as ID
        "answers": answers,
    }
    answer_sets.append(answer_set)

###############################################################################
# 2.  Session-scoped Copier rendering — *one per answer-set*
###############################################################################


@pytest.fixture(scope="session", params=answer_sets, ids=lambda p: p["id"])
def rendered(request, copie_session):
    """
    Render the template once for each variant and return (project_dir, answers_id)
    """
    variant = request.param
    result = copie_session.copy(extra_answers=variant["answers"])
    if result.exit_code != 0 or result.exception:
        pytest.fail(f"Copier failed for {variant['id']}: {result.exception}")
    return result.project_dir, variant["id"]


###############################################################################
# 3.  Return the list of tox envs for *that* rendered project
###############################################################################


def _list_tox_envs(project_dir: Path) -> list[str]:
    out = subprocess.check_output(["tox", "-qq", "-l"], cwd=project_dir, text=True)
    return [line.strip() for line in out.splitlines() if line.strip()]


@pytest.fixture(scope="session")
def env_matrix(rendered) -> dict[str, list[str]]:
    """
    Cache {variant_id: [toxenv1, toxenv2, …]} for all variants.
    """
    project_dir, var_id = rendered
    # Build the cache lazily the first time each variant appears
    _matrix = getattr(env_matrix, "_cache", {})
    if var_id not in _matrix:
        _matrix[var_id] = _list_tox_envs(project_dir)
        env_matrix._cache = _matrix
    return _matrix
