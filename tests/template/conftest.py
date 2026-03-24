from pathlib import Path
from typing import Any, Dict, cast

import pytest
from loguru import logger
from ruamel.yaml import YAML

from scripts.copie_helpers import run_copie_with_output_control

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMPLE_ANSWERS_DIR = REPO_ROOT / "example-answers"
ANSWERS_YAMLS = sorted(EXAMPLE_ANSWERS_DIR.glob("*.yml"))


def _answers_id(answers_yaml: Path | None) -> str:
    if answers_yaml is None:
        return "no-example-answers"
    return answers_yaml.stem


def read_answers_yaml(answers_yaml: Path) -> Dict[Any, Any]:
    """
    Read the example answers YAML file into a dictionary.
    """
    if not answers_yaml.is_file():
        raise FileNotFoundError(f"Answers YAML file not found: {answers_yaml}")
    yaml = YAML(typ="safe")
    with answers_yaml.open("r") as file:
        return cast(Dict[Any, Any], dict(yaml.load(file)))


answers_yaml_params = ANSWERS_YAMLS or [None]


# --- Fixtures ---------------------------------------------------------------
@pytest.fixture(scope="session", params=answers_yaml_params, ids=_answers_id)
def rendered(request, copie_session):
    """
    Render the template once for each variant and return (project_dir, answers_id)
    """

    answers_yaml = request.param

    if answers_yaml is None:
        pytest.fail(
            "No example answer sets discovered; expected at least one *.yml under "
            f"{EXAMPLE_ANSWERS_DIR}.",
            pytrace=False,
        )

    try:
        answers = read_answers_yaml(answers_yaml)
    except (FileNotFoundError, OSError, ValueError, TypeError) as exc:
        pytest.fail(f"Failed to load answers YAML {answers_yaml}: {exc}", pytrace=False)

    if not isinstance(answers, dict):
        pytest.fail(
            f"Answers YAML must decode to a dictionary: {answers_yaml}",
            pytrace=False,
        )

    variant = {
        "id": answers_yaml.stem,
        "answers": answers,
    }

    if request.config.option.verbose >= 2:
        logger.info(f"Rendering variant {variant['id']} with answers")

    result = run_copie_with_output_control(
        request.config,
        copie_session,
        variant["answers"],
    )

    if request.config.option.verbose >= 2:
        logger.info(f"Copier successfully rendered variant {variant['id']}")

    # Basic smoke-tests
    if result.exit_code != 0 or result.exception:
        pytest.fail(
            f"Copier failed for {variant['id']}: {result.exception}", pytrace=False
        )

    logger.debug(f"Rendered variant {variant['id']} at {result.project_dir}")
    return result.project_dir, variant["id"]
