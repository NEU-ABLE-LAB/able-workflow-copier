"""
Expose a Jinja filter ``to_toml_authors`` that:

1.  Accepts the JSON *string* stored in your copier answers file (e.g.
    '{ "name": "Alice" }' or '[{…}, …]').
2.  Parses & (optionally) validates it against the JSON-Schema above.
3.  Returns a TOML-formatted string that you can inject straight after
       authors =               # <-- in pyproject.toml
"""

from __future__ import annotations

import json
import pathlib
import textwrap
from typing import Any, Dict, List

import jsonschema
from jinja2 import Environment
from jinja2.ext import Extension
from loguru import logger

SCHEMA_PATH = (
    pathlib.Path(__file__).parents[1] / "schemas" / "project-authors.schema.json"
)


def _validate(data: Any) -> None:
    """Validate *data* against the JSON-Schema on disk (no-op if jsonschema missing)."""
    if jsonschema is None:  # keep this file dependency-free
        return
    schema = json.loads(SCHEMA_PATH.read_text())
    jsonschema.validate(data, schema)  # raises jsonschema.ValidationError if bad


def _toml_repr(author: Dict[str, str]) -> str:
    """Convert one author dict to 'TOML inline-table' form."""
    parts: List[str] = []
    if "name" in author:
        parts.append(f'name = "{author["name"]}"')
    if "email" in author:
        parts.append(f'email = "{author["email"]}"')
    return "{ " + ", ".join(parts) + " }"


def to_toml_authors(authors_json: str, *, indent: int = 4) -> str:
    """
    Turn the JSON string into the TOML snippet expected by PEP 621.

    >>> to_toml_authors('[{"name": "Alice", "email": "a@example.com"}]')
    '[\\n    { name = "Alice", email = "a@example.com" }\\n]'
    """
    logger.debug(f"Converting authors JSON: {authors_json!r}")
    data = json.loads(authors_json)
    _validate(data)

    if not isinstance(data, list):
        raise TypeError("`authors_json` must decode to a JSON list")

    body = ",\n".join(textwrap.indent(_toml_repr(item), " " * indent) for item in data)
    return "[\n" + body + "\n]"


class AuthorsFilter(Extension):
    def __init__(self, environment: Environment):
        super().__init__(environment)
        environment.filters["to_toml_authors"] = to_toml_authors
