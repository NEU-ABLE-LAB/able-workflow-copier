from pathlib import Path
from typing import Any, Dict, cast
import pytest
from loguru import logger

from ruamel.yaml import YAML

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
# Session-scoped Copier rendering — *one per answer-set*
###############################################################################


@pytest.fixture(scope="session", params=answer_sets, ids=lambda p: p["id"])
def rendered(request, copie_session):
    """
    Render the template once for each variant and return (project_dir, answers_id)
    """

    variant = request.param

    # Generate the session scoped-project
    result = copie_session.copy(extra_answers=variant["answers"])

    # Basic smoke-tests
    if result.exit_code != 0 or result.exception:
        pytest.fail(f"Copier failed for {variant['id']}: {result.exception}")

    logger.debug(f"Rendered variant {variant['id']} at {result.project_dir}")
    return result.project_dir, variant["id"]
