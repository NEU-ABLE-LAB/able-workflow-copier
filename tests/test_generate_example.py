"""Integration tests for the 'generate example' command."""

from pathlib import Path
from typing import Any, Dict, cast

from pytest_copie.plugin import Copie
from ruamel.yaml import YAML

ANSWERS_YAML = Path("example-answers.yml")


# Read ANSWERS_YAML into a dictionary
def read_answers_yaml(answers_yaml: Path) -> Dict[Any, Any]:
    """Read the example answers YAML file into a dictionary."""
    if not answers_yaml.is_file():
        raise FileNotFoundError(f"Answers YAML file not found: {answers_yaml}")
    yaml = YAML(typ="safe")
    with answers_yaml.open("r") as file:
        return cast(Dict[Any, Any], dict(yaml.load(file)))


# --- TESTS ------------------------------------------------------------------
def test_template(copie: Copie) -> None:
    """Test the 'generate example' command with answers."""

    # Read the example answers YAML file
    answers = read_answers_yaml(ANSWERS_YAML)

    # Generate the example project
    result = copie.copy(
        extra_answers=answers,
    )

    assert result.exit_code == 0
    assert result.exception is None
    assert isinstance(result.project_dir, Path)
    assert result.project_dir.is_dir()
