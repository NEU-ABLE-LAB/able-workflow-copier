# Best Practices

The ABLE Workflow Copier templates are meant to provide a repeatable starting point for building data science workflows that are modular, reproducible, and easier to maintain over time. At a high level, the templates are designed for projects where data-processing code, workflow orchestration, schemas, tests, and environment definitions should live together in one coherent repository rather than being scattered across notebooks, scripts, and ad hoc setup instructions. ***Finally, no more 10,000 line jupyter notebooks***.

The broader purpose is not just to scaffold a working Snakemake project, but to encourage a project structure that supports reuse. A generated workflow should be understandable by new contributors, testable in isolation, reusable by downstream workflows, and structured so that its outputs can be treated as stable data products rather than one-off files. ***Your future self will thank you***.

This page explains the design requirements that were followed when developing key [Features](features) of the templates.

## Rebuild data products from source data and code

The workflow should be defined as a sequence of extract (read from disk or external source), transform (e.g., analysis, simulation), and load (write to disk or external source) (ETL) steps. It should preserve raw data, serialize
intermediate products, and make it possible to rebuild final outputs from code
plus input data.

## Treat engineering checks as part of the project, not cleanup work

The project should encourage unit tests, integration tests, static typing,
formatting, declarative environment definitions, documentation, and continuous-integration workflows for quality assurance.

## Keep reusable python code and workflow code together during development

Developers should be able to work on reusable Python code and workflow code in
one repository and one development environment. ETL logic, schemas, extraction
helpers, rule wrappers, and tests tend to evolve together. Keeping them close
reduces release friction and makes the boundary between reusable code and
workflow entry points easier to reason about.

## One project runs can run on local machines, in shared computing clusters, or on the cloud

The workflow should be able to run on a standalone machine and in a shared HPC
environment without changing the overall project structure. That pushes the
template toward explicit workflow environments, thin workflow wrappers, and a
layout that does not depend on one machine-specific development setup.

## Design workflows so other workflows can extend them

Other workflows should be able to incorporate this workflow and run its steps
when configured correctly and given the needed inputs. That requires the project
to expose its boundaries intentionally instead of assuming every consumer lives
inside one repository with undocumented path conventions.

## Publish stable interfaces, not just files

Other workflows should be able to consume outputs through explicit schemas and
extraction helpers instead of depending on undocumented file internals. The goal
is to make outputs behave like stable data products that downstream code can
validate, read, and trust.

Continue reading about [Features](features.md) for the tool-level explanation of how the template implements these principles, or continue reading [Template Output](template-output.md) to see where those choices land in the repository structure.
