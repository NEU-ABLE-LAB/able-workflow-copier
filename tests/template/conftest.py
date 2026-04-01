"""
Pytest configuration for rendering template variants from example answers.

This module mirrors the example-discovery style used in sibling template
repositories and keeps a legacy ``answer_sets`` export for tox tests that still
import it.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import Any, Dict, cast

import pytest
from loguru import logger
from ruamel.yaml import YAML

from scripts.copie_helpers import run_copie_with_output_control

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMPLE_ANSWERS_DIR = REPO_ROOT / "example-answers"
ANSWERS_YAMLS = sorted(EXAMPLE_ANSWERS_DIR.glob("*.yml"))


@dataclass
class Example:
    name: str
    answers: Dict[Any, Any]


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


class _LazyExamples:
    def __iter__(self):
        for answers_yaml in ANSWERS_YAMLS:
            try:
                yield Example(
                    name=answers_yaml.stem,
                    answers=read_answers_yaml(answers_yaml),
                )
            except (FileNotFoundError, OSError, ValueError, TypeError) as exc:
                pytest.fail(
                    f"Failed to load answers YAML {answers_yaml}: {exc}",
                    pytrace=False,
                )


EXAMPLES = _LazyExamples()


# Backward-compatibility for tox tests that import `answer_sets`.
answer_sets = [{"id": ex.name, "answers": ex.answers} for ex in EXAMPLES]


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

    variant = Example(name=answers_yaml.stem, answers=answers)

    if request.config.option.verbose >= 2:
        logger.info(f"Rendering variant {variant.name} with answers")

    result = run_copie_with_output_control(
        request.config,
        copie_session,
        variant.answers,
    )

    if request.config.option.verbose >= 2:
        logger.info(f"Copier successfully rendered variant {variant.name}")

    # Basic smoke-tests
    if result.exit_code != 0 or result.exception:
        pytest.fail(
            f"Copier failed for {variant.name}: {result.exception}", pytrace=False
        )

    logger.debug(f"Rendered variant {variant.name} at {result.project_dir}")
    return result.project_dir, variant.name
