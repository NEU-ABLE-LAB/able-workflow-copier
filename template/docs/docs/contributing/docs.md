# General info about the [mkdocs](https://www.mkdocs.org/) project

## Building the documentation

Use Snakemake to manage documentation tasks:

- **`docs_build`**: Build the site locally to verify it compiles.
- **`docs_deploy`**: Build and deploy the docs to the `gh-pages` branch with [`mike`](https://squidfunk.github.io/mkdocs-material/setup/setting-up-versioning/).
- **`docs_serve`**: Build and serve the documentation from the files in `docs/`.
- **`docs_serve_mike`**: serve the most recent version of the docs stored on `gh-pages`.

## Contributing to the documentation

Welcome! This section covers best practices and guidelines for contributing to the project documentation.

### Getting started

1. **Set up your environment**: Ensure you have the development environment configured with all required dependencies.
2. **Understand the structure**: Familiarize yourself with the documentation structure and tools described below.
3. **Test locally**: Always build and test documentation changes locally before submitting.

### Best practices

#### Writing guidelines

- **Write clearly and concisely**: Use simple, direct language that's accessible to users of different skill levels.
- **Be consistent**: Follow existing patterns for headings, formatting, and style throughout the documentation.
- **Include examples**: Provide practical examples and code snippets to illustrate concepts.
- **Use proper grammar**: Proofread your content and use tools like spell checkers.

#### Documentation structure

- **Follow the existing hierarchy**: Place content in appropriate sections and maintain the logical flow.
- **Use descriptive headings**: Make headings clear and searchable.
- **Cross-reference appropriately**: Link to related sections and external resources when helpful.
- **Keep navigation in mind**: Consider how users will discover and navigate to your content.

#### Code documentation

- **Add type hints**: All Python functions should include proper type annotations.
- **Write numpy-style docstrings**: Use the established docstring format for consistency with `mkdocstrings`.
- **Document parameters and returns**: Clearly describe function inputs, outputs, and any exceptions.
- **Include usage examples**: Add practical examples in docstrings when appropriate.

#### Technical considerations

- **Test your changes**: Run `docs_build` locally to ensure your changes compile without errors.
- **Check links**: Verify that all internal and external links work correctly.
- **Optimize images**: Use appropriate formats and sizes for any images or diagrams.
- **Consider accessibility**: Use alt text for images and ensure content is screen-reader friendly.

### Workflow for contributing

1. **Create a branch**: Work on documentation changes in a dedicated feature branch.
2. **Make your changes**: Edit the relevant `.md` files in the `docs/` directory.
3. **Test locally**: Use `docs_serve` to preview your changes in a browser.
4. **Review and refine**: Check formatting, links, and overall presentation.
5. **Submit for review**: Create a pull request with a clear description of your changes.

### Common pitfalls to avoid

- **Don't break existing functionality**: Ensure your changes don't break existing documentation features.
- **Avoid orphaned content**: Make sure new content is properly linked and discoverable.
- **Don't ignore build warnings**: Address any warnings that appear during the build process.
- **Keep formatting consistent**: Follow the established markdown patterns and conventions.

## Tools for building documentation

### Snakemake workflow graph

??? info "`dag_svg`" rules

    ```python
    {%
      include "../../../workflow/rules/docs_dag_svg.smk"
    %}
    ```

## Tools for writing documentation

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
