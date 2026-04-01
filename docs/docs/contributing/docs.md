# ABLE Workflow copier template documentation

{%
    include-markdown "../../README.md"
    start="<!--include-start-->"
    end="<!--include-end-->"
%}

## Tools and tips for writing documentation

### Serving multiple copier doc sites locally

Each copier repository serves its docs independently. Start each docs server
from the corresponding repository directory rather than using a single "serve
all" command.

Example layout (sibling repositories):

- `../able-workflow-copier`
- `../able-workflow-module-copier`
- `../able-workflow-etl-copier`
- `../able-workflow-rule-copier`

Launch one terminal per repository and run that repository's Snakemake
documentation serve rule in each directory:

```bash
# able-workflow-copier
cd ../able-workflow-copier
snakemake docs_serve

# able-workflow-module-copier
cd ../able-workflow-module-copier
snakemake docs_serve

# able-workflow-etl-copier
cd ../able-workflow-etl-copier
snakemake docs_serve

# able-workflow-rule-copier
cd ../able-workflow-rule-copier
snakemake docs_serve
```

Default local ports for each repository are:

- `able-workflow-copier`: `http://127.0.0.1:8001`
- `able-workflow-module-copier`: `http://127.0.0.1:8002`
- `able-workflow-etl-copier`: `http://127.0.0.1:8003`
- `able-workflow-rule-copier`: `http://127.0.0.1:8004`

Use these defaults (or override them in each repo's docs configuration) so all
servers can run at the same time.
If a repository exposes a different docs-serving rule, use that repository's
documented Snakemake rule name.

### [Admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/)

How to add note, info, tips, etc. blocks (and collapsable blocks).

???+ info "like this"

    Info block that can collapse away.

### [MathJax](https://squidfunk.github.io/mkdocs-material/reference/math/)

Write equations with latex and [mathjax](https://www.mathjax.org/).

???+ example "mathjax example"

    When $a \ne 0$, there are two solutions to \(ax^2 + bx + c = 0\) and they are

    $$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$

### [mkdocs include markdown](https://github.com/mondeja/mkdocs-include-markdown-plugin)

### [mkdocs literate nav](https://oprypin.github.io/mkdocs-literate-nav/index.html)

The navigation structure is specified with
[`literate-nav`](https://pypi.org/project/mkdocs-literate-nav/) in the
`SUMMARY.md` file within the `docs/docs/` directory and each subdirectory.

### [mkdocs macros](https://mkdocs-macros-plugin.readthedocs.io/en/latest/)

### [mkdocstrings](https://numpydoc.readthedocs.io/en/latest/format.html)

All python code should contain type hints and [numpy-style docstring](https://numpydoc.readthedocs.io/en/latest/format.html). These are rendered into the documentation using [`mkdocstrings`](https://mkdocstrings.github.io/).
