# What is the ABLE Workflow?

The ABLE Workflow is a suite of templates for generating a reproducible data science, machine learning, or simulation project. The projects include a Python package, conda environments, tests, and documentation. This template suite helps teams go from a project idea to a working, maintainable, documented, and reproducible workflow with less setup and fewer one-off decisions.

These templates aim to generate projects that that make it easier to follow best pratices:

- Rebuild data products from source data and code.
- Treat tests, typing, formatting, docs, environments, and CI as part of the project.
- Keep reusable package code and workflow code together during development.
- Keep one project shape across local and shared computing environments.
- Design workflows so other workflows can extend them.
- Publish stable interfaces with schemas and extraction helpers.

## Who should use it?

- **You want to run complex Python code in your Snakemake workflow**: Use this template suite if you already use Snakemake but need more reusable Python code, schemas, tests, and packaging structure than belongs in one script per rule.
- **Your Jupyter notebook is getting out of control**: Use it if your project has outgrown very large notebooks and you want a workflow that is easier to test, rerun, review, and maintain over time.
- **CookieCutter Datascience Users**: Use it if you like project templates such as Cookiecutter Data Science but want easier workflow authoring (*no more fighting whitespace*), generated documentation, and more explicit engineering defaults.

## About this Overview

- Use [Best Practices](best-practices.md) for the design principles the template is built around.
- Use [Features](features.md) for the tool-level rationale, implementation details, and major tradeoffs.
- Use [Inspiration](inspiration.md) for the adjacent projects, templates, and ecosystem gaps that helped shape the suite.
- Use [Template Output](template-output.md) to compare the template repository structure with the generated project structure.

If you are trying to scaffold or update a project right now, go back to
[Quick Reference](../quick-reference/). If you are trying to understand why the
project looks the way it does, keep reading in this section.
