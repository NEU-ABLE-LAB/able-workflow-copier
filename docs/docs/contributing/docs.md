# ABLE Workflow copier template documentation

{%
    include-markdown "../../README.md"
    start="<!--include-start-->"
    end="<!--include-end-->"
%}

## Tools and tips for writing documentation

### [Admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/)

How to add note, info, tips, etc. blocks (and collapsable blocks).

???+ info "like this"

    Info block that can collapse away.

### docstrings

All python code should contain type hints and [numpy-style docstring](https://numpydoc.readthedocs.io/en/latest/format.html). These are rendered into the documentation using [`mkdocstrings`](https://mkdocstrings.github.io/).

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
