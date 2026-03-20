---
render_macros: false
---

# Contributing to `able-workflow`

## Tools

- [`copier`](https://copier.readthedocs.io/en/stable/): The library and CLI app for rendering project templates.
- [`pytest-copie`](https://pytest-copie.readthedocs.io/en/latest/index.html): wrapper on top of the copier API for generating projects. Used in pytest tests and [sandbox scripts](sandbox.md).

## Checking for updates

See [Checking for updates](updates.md) for the `scripts/copier-check-update.sh` helper included in rendered projects.

## `copier` extensions

See top of `copier.yml`

??? info "`copier.yml`"

    /// html | div
    ```yaml
    {%
        include "../../../copier.yml"
    %}
    ```
    ///
