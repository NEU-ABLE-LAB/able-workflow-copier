# ABLE Workflow Copier

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-purple.json)](https://github.com/copier-org/copier)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Common Changelog](https://common-changelog.org/badge.svg)](https://common-changelog.org)
[![codecov](https://codecov.io/gh/NEU-ABLE-LAB/able-workflow-copier/graph/badge.svg?token=8BX19PLPQ8)](https://codecov.io/gh/NEU-ABLE-LAB/able-workflow-copier)
[![tox Main Tests](https://github.com/NEU-ABLE-LAB/able-workflow-copier/actions/workflows/ci.yml/badge.svg)](https://github.com/NEU-ABLE-LAB/able-workflow-copier/actions/workflows/ci.yml)

The ABLE Workflow is a suite of templates for generating a reproducible data science, machine learning, or simulation project. The proejcts include a Python package, conda environments, tests, and documentation. This template suite helps teams go from a project idea to a working, maintainable, documented, and reproducible workflow with less setup and fewer one-off decisions.

Learn if the [ABLE Workflow is right for you](overview/index.md#who-should-use-it).

## Start Here

1. If you want to scaffold a new project, start with
   [Quick Reference](quick-reference/).
2. If you want to learn more about the design decisions behind these
   templates and how they can help you, go to [Overview](overview/).
3. If you want to help maintain and improve these templates,
   go to [Contributing](contributing/).
4. If you only need to run or import a generated workflow,
   use that generated project's own documentation instead of
   this template repository. Go to [Overview](overview/)
   if you want to understand why that project was structured
   the way it was.

## Template Ecosystem

- [`able-workflow-copier`]({{ able_workflow_copier_docs }}): creates the base project with the workflow, package, docs, tests, and environment scaffolding.
- [`able-workflow-module-copier`]({{ able_workflow_module_copier_docs }}): adds a datasets, features, or models module inside an existing project.
- [`able-workflow-etl-copier`]({{ able_workflow_etl_copier_docs }}): adds an ETL process inside an existing module.
- [`able-workflow-rule-copier`]({{ able_workflow_rule_copier_docs }}): adds an individual Snakemake rule and its associated tests and docs.

## Who Is This For?

- **Project developers** use this repo to create a new workflow project and should usually start with [Quick Reference](quick-reference/).
- **Template contributors** use this repo to maintain and improve the template suite and should usually start with [Contributing](contributing/).
- **Project users and project integrators** should primarily use the generated project's documentation, but may use this to understand the project's [design principals](overview/best-practices.md).
