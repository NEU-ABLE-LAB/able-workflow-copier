# `tests/workflow/rules`

Integration tests for Snakemake rules.

## Requirements

These tests should be run with the `workflow` and `tests` dependencies specified in the `dependency-groups` section of `pyproject.toml`.

## Shared Fixtures

A shared `workspace` fixture is defined in `conftest.py` in this directory. This fixture sets up a disposable Snakemake working directory for each test module and is automatically available to all tests in this directory—no import is necessary. Pytest will handle setup and teardown for each test module.
