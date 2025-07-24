import json
from typing import Any

import pytest
from jinja2 import Environment

# The module under test
from extensions import authors_filter

# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------


def _render(authors: list[dict[str, Any]], *, indent: int = 4) -> str:
    """Helper that mimics authors_filter.to_toml_authors for expected strings."""
    body = ",\n".join(
        (" " * indent)
        + "{ "
        + ", ".join(f'{k} = "{v}"' for k, v in author.items())  # pragma: no branch
        + " }"  # noqa: W503
        for author in authors
    )
    return "[\n" + body + "\n]"


# ---------------------------------------------------------------------------
# Happy‑path conversions
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "authors_json, expected",
    [
        (
            "[{'name': 'Alice', 'email': 'alice@example.com'}]".replace("'", '"'),
            _render(
                [
                    {"name": "Alice", "email": "alice@example.com"},
                ]
            ),
        ),
        (
            "[{'name': 'Bob'}]".replace("'", '"'),
            _render(
                [
                    {"name": "Bob"},
                ]
            ),
        ),
        (
            "[{'email': 'eve@example.com'}]".replace("'", '"'),
            _render(
                [
                    {"email": "eve@example.com"},
                ]
            ),
        ),
    ],
)
def test_to_toml_authors_valid(authors_json: str, expected: str) -> None:
    """The filter serialises well‑formed JSON strings into TOML inline tables."""
    result = authors_filter.to_toml_authors(authors_json)
    assert result == expected


def test_to_toml_authors_custom_indent() -> None:
    """Indentation width is honoured via the *indent* kwarg."""
    authors_json = "[{'name': 'Alice'}]".replace("'", '"')
    result = authors_filter.to_toml_authors(authors_json, indent=2)
    expected = _render([{"name": "Alice"}], indent=2)
    assert result == expected


# ---------------------------------------------------------------------------
# Failure cases
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad_json",
    ["{"],  # malformed JSON
)
def test_to_toml_authors_json_decode_error(bad_json: str) -> None:
    """Malformed JSON raises ``json.JSONDecodeError``."""
    with pytest.raises(json.JSONDecodeError):
        authors_filter.to_toml_authors(bad_json)


def test_to_toml_authors_not_list() -> None:
    """Decoded value must be a list; anything else raises ``TypeError``."""
    not_a_list = "{'name': 'Alice'}".replace("'", '"')
    with pytest.raises(TypeError):
        authors_filter.to_toml_authors(not_a_list)


@pytest.mark.skipif(
    authors_filter.jsonschema is None, reason="jsonschema not available"
)
def test_to_toml_authors_schema_validation() -> None:
    """An entry without *name* or *email* violates the schema and fails."""
    invalid_json = "[{}]"  # empty dict – fails the anyOf rule
    with pytest.raises(authors_filter.jsonschema.ValidationError):
        authors_filter.to_toml_authors(invalid_json)


# ---------------------------------------------------------------------------
# Jinja integration
# ---------------------------------------------------------------------------


def test_authors_filter_extension_registers_filter() -> None:
    """
    Instantiating the :class:`authors_filter.AuthorsFilter` extension
    on a Jinja :class:`Environment` must add the *to_toml_authors* filter.
    """

    # Create a bare Jinja environment with the extension installed
    env = Environment(extensions=[authors_filter.AuthorsFilter])

    assert "to_toml_authors" in env.filters
    assert env.filters["to_toml_authors"] is authors_filter.to_toml_authors

    # the new helper is exported too
    assert "author_names_csv" in env.filters
    assert env.filters["author_names_csv"] is authors_filter.author_names_csv


# ---------------------------------------------------------------------------
# author_names_csv helper
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "authors_json, expected",
    [
        (
            # plain names → comma-separated
            "[{'name': 'Alice'}, {'name': 'Bob'}]".replace("'", '"'),
            "Alice, Bob",
        ),
        (
            # any name with a comma → semicolon-separated
            "[{'name': 'Doe, John'}, {'name': 'Alice'}]".replace("'", '"'),
            "Doe, John; Alice",
        ),
    ],
)
def test_author_names_csv_delimiters(authors_json, expected):
    assert authors_filter.author_names_csv(authors_json) == expected


def test_author_names_csv_warns_on_mixed_delimiters(recwarn):
    """
    A name containing *both* ',' and ';' triggers a warning.
    """
    mixed = "[{'name': 'Doe, John; Jr.'}]".replace("'", '"')

    authors_filter.author_names_csv(mixed)

    # Grab the most-recent warning object
    w = recwarn.pop()
    assert issubclass(w.category, UserWarning)
    assert "contain both commas and semicolons" in str(w.message)


def test_author_names_csv_accepts_list():
    authors_list = [{"name": "Alice"}, {"name": "Bob"}]
    assert authors_filter.author_names_csv(authors_list) == "Alice, Bob"
