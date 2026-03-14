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
from typing import Any, Dict, List, Union

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
    data = json.loads(authors_json)

    if not isinstance(data, list):
        raise TypeError("`authors_json` must decode to a JSON list")

    _validate(data)

    body = ",\n".join(textwrap.indent(_toml_repr(item), " " * indent) for item in data)
    return "[\n" + body + "\n]"


def author_names_csv(authors: Union[str, list[dict[str, Any]]]) -> str:
    """
    Return the authors' names joined by a delimiter::

        - Use *comma* (`, `) by default.
        - If **any** name already contains a comma, switch to *semicolon* (`; `).
        - If *any* name contains **both** a comma **and** a semicolon, emit a
          warning because the output delimiter is ambiguous.
    """
    # Parse input if needed
    if isinstance(authors, (bytes, bytearray)):
        authors = authors.decode()
    if isinstance(authors, str):
        data: Any = json.loads(authors)
    else:
        data = authors

    # Validate basic type
    if not isinstance(data, list):
        raise TypeError(
            "`authors` must be either a JSON string or a list of dicts representing authors"
        )

    names = [a["name"] for a in data if isinstance(a, dict) and "name" in a]

    # Choose delimiter
    use_semicolon = any("," in n for n in names)
    if any(("," in n) and (";" in n) for n in names):
        msg = (
            "Author name(s) contain both commas and semicolons - "
            "falling back to '; ' as the list delimiter."
        )
        logger.warning(msg)  # keeps Loguru output for normal runs
    delimiter = "; " if use_semicolon else ", "
    return delimiter.join(names)


class AuthorsFilter(Extension):
    def __init__(self, environment: Environment):
        super().__init__(environment)
        environment.filters["to_toml_authors"] = to_toml_authors
        # expose the new helper as an optional Jinja filter too
        environment.filters["author_names_csv"] = author_names_csv
