# General info about the [mkdocs](https://www.mkdocs.org/) project

## Building the documentation

Use Snakemake to manage documentation tasks:

- **`docs_build`**: Build the site locally to verify it compiles.
- **`docs_deploy`**: Build and deploy the docs to the `gh-pages` branch with [`mike`](https://squidfunk.github.io/mkdocs-material/setup/setting-up-versioning/).
- **`docs_serve`**: Build and serve the documentation from the files in `docs/`.
- **`docs_serve_mike`**: serve the most recent version of the docs stored on `gh-pages`.

## Contributing to the documentation

TODO-copier-package Add best-practices and overviiew of contributing to the documentation

## Tools and tips for writing documentation

### [Admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/)

How to add note, info, tips, etc. blocks (and collapsable blocks).

???+ info "like this"

    Info block that can collapse away.

### [mkdocstrings](https://mkdocstrings.github.io/)

All python code should contain type hints and [numpy-style docstring](https://numpydoc.readthedocs.io/en/latest/format.html). These are rendered into the documentation using [`mkdocstrings`](https://mkdocstrings.github.io/).

### [mkdocs-macros](https://mkdocs-macros-plugin.readthedocs.io/en/latest/)

Used to by `mike` and to render jinja2 templates in markdown files.

### [mkdocs-include-markdown](https://github.com/mondeja/mkdocs-include-markdown-plugin)

Used to include markdown. Preferred over [snippets](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/) since `include-markdown` allows for changing header levels.

### [mkdocs-gen-files](https://oprypin.github.io/mkdocs-gen-files/)

- Renders jinja2 in SUMMARY.md files.
- Generates pages containing mkdocstrings.

### [mkdocs-literate-nav](https://oprypin.github.io/mkdocs-literate-nav/index.html)

The navigration tree for each directory is defined by the `SUMMARY.md` instead of defining the whole site in `mkdocs.yml`.

### MathJax

Write equations with latex and [mathjax](https://www.mathjax.org/).

???+ example "mathjax example"

    When $a \ne 0$, there are two solutions to \(ax^2 + bx + c = 0\) and they are

    $$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$

### [mkdocks macros](https://mkdocs-macros-plugin.readthedocs.io/en/latest/)

??? info "Detailed info about mkdocs macros"

    /// html | div
    {{ macros_info() }}
    ///
