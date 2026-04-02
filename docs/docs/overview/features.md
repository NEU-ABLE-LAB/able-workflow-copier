# Features

This page explains the major technical features the template suite uses to
implement the principles described in [Best Practices](best-practices.md). While not every individual tool is universally best, the tradeoffs are explicit, documented, and connected back to the project principals the template is trying to make easier to adopt.

If you want to see where these choices land in the filesystem, use
[Template Output](template-output.md).

<!-- markdownlint-disable MD024 -->

## Workflow orchestration with Snakemake

[Snakemake](https://snakemake.readthedocs.io/) takes individual extract-transform-load (e.g., **E**:read a file from disk, **T**: analyze the data, **L** write the output data to disk) steps and uses rules that define input-output relationships between ETL steps to generate and execute a sequence (i.e., directed acyclic graph, DAG) that produces the fully processed output files from the raw and external input files.

These rules and resulting DAG are a definitive workflow for reproducing the output. Instead of guessing which script to rerun or rebuilding everything by hand, Snakemake can follow the chain from raw inputs to final outputs, rerun only the steps that changed, and inspect intermediate files when something looks wrong.

### Best Practices

- [Rebuild data products from source data and code](best-practices.md#rebuild-data-products-from-source-data-and-code)
- [One project shape across local and shared computing environments](best-practices.md#one-project-runs-can-run-on-local-machines-in-shared-computing-clusters-or-on-the-cloud)
- [Design workflows so other workflows can extend them](best-practices.md#design-workflows-so-other-workflows-can-extend-them)

### Implementation details

The Snakemake workflow sits in the `workflow/` directory where the workflow steps, their dependencies, and their software environments are declared.

```.yaml
├── config/ # (7)
└── workflow/
    ├── envs/ # (1)
    ├── profiles/ # (2)
    ├── rules/ # (3)
    ├── schemas/ # (4)
    ├── scripts/ # (5)
    └── Snakefile # (6)
```

1. Conda environment files defining the dependencies required to run rules
2. Separate configuration profiles depending on computing environment
3. The rules that define how ETL steps link together to form the DAG that generates the desired output data from available input data
4. Configuration file schemas for validation and definiting default values.
5. Scripts that execute a rule's specified actions
6. The main `Snakefile` that defines the workflow
7. Standard configuration files to run the workflow

Snakemake’s [rules](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html), [modularization](https://snakemake.readthedocs.io/en/stable/snakefiles/modularization.html), [external scripts](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#external-scripts), and [Conda deployment](https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html) features support file-based rule execution, reusable workflow pieces, and per-rule software environments. That combination also makes it easier to run the workflow in different computing environments by only changing configuration files without changing the overall project structure.

### Tradeoffs and rejected alternatives

The following alternatives to Snakemake were considered:

- [make](https://cookiecutter-data-science.drivendata.org/opinions/) was not chosen because its syntax is hard to read and maintain for a project with many data-processing steps and environment-specific rules.

The ability to run across computing environments is one of the main reasons these alternatives were not chosen, especially in shared clusters where running shared persistent services is difficult.

- [Apache Airflow](https://airflow.apache.org/) was not a good fit because its normal architecture includes a scheduler, a webserver, and a metadata database.
- [Luigi](https://luigi.readthedocs.io/en/stable/) is lighter weight, but its recommended production model still uses the central `luigid` scheduler as a long-running server, and optional task-history features add a database as well.
- [Prefect](https://www.prefect.io/) was not a good fit because even self-hosted deployments are built around a server backed by a database, and many deployment patterns also rely on workers and work pools.
- [Dagster](https://dagster.io/) was not a good fit because it is designed around a richer orchestration stack with a webserver, daemon processes, and persistent run and event-log storage.
- [Joblib](https://joblib.readthedocs.io/) was not chosen because it is a filesystem-based caching tool for Python functions, not a full workflow engine for expressing and running a large dependency graph.

In other words, many of these tools are less convenient when the same workflow needs to run both on a standalone PC and in a shared HPC environment without depending on always-on infrastructure. That leaves Snakemake as the best fit here because it can express a real file-based workflow DAG while still keeping workflow state closely tied to the filesystem instead of to always-on infrastructure.

## Python package and workflow monorepo

The generated projects keep an installable Python package next to the workflow in the same repository. Reusable ETL logic, schemas, extraction helpers, tests, and workflow wrappers usually need to evolve together during development. Keeping them together makes it faster to change both layers without cutting package releases just to try a workflow change.

### Best Practices

- [Rebuild data products from source data and code](best-practices.md#rebuild-data-products-from-source-data-and-code)
- [Treat engineering checks as part of the project, not cleanup work](best-practices.md#treat-engineering-checks-as-part-of-the-project-not-cleanup-work)
- [Keep reusable python code and workflow code together during development](best-practices.md#keep-reusable-python-code-and-workflow-code-together-during-development)
- [Design workflows so other workflows can extend them](best-practices.md#design-workflows-so-other-workflows-can-extend-them)
- [Publish stable interfaces, not just files](best-practices.md#publish-stable-interfaces-not-just-files)

### Implementation details

The project's python package lives under {% raw %}`{{ package_name }}/`{% endraw %}. Each ETL step is encapsulated in a submodule organized under a module that groups together similar ETL steps, which is organized depending on if it generates processed `datasets`, machine learning `features`, or machine learning `models`.

```.yaml
├── {{ package_name }}/
│   │
│   ├── datasets/
│   │   ├── {{ module_name }}/
│   │   │   ├── {{ etl_name }}/
│   │   │   │   ├── runner/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── extract_external.py
│   │   │   │   │   ├── load.py
│   │   │   │   │   ├── main.py
│   │   │   │   │   ├── transform.py
│   │   │   │   │   └── utils.py
│   │   │   │   ├── __init__.py
│   │   │   │   ├── extract.py
│   │   │   │   └── schema.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   │
│   ├── features/ # (1)
│   │
│   ├── models/ # (2)
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logging.py
│   │
│   ├── __init__.py
│   └── config.py
└── pyproject.toml
```

1. The `features/` directories are organized the same as `dataset/`
2. The `models/` directories are organized the same as `dataset/`

The python package is defined using the standard `pyproject.toml` and converted to conda environment YAML files with [`pyproject2conda`](#generate-conda-environments-from-project-metadata). The workflow calls the desired functions within the package using the `workflow/scripts/rules_conda_RUNNER/{{ package_name }}_rules.py` script.

### Tradeoffs and rejected alternatives

Putting each ETL process in one large script under `workflow/scripts/` makes the workflow runnable, but it makes schemas, extract helpers, tests, and type checking harder to share and maintain.

Putting helper modules next to scripts in `workflow/scripts/` can work for local execution, but it is not a robust contract for imported workflows where cached script locations become the stable import anchor. Snakemake documents helper scripts and `workflow.source_path()`, but local adjacency imports become fragile once a workflow is imported from GitHub and cached elsewhere. That is why the generated projects lean on an installable package boundary instead of local import luck.

??? note "The long-running issue of importing custom Python in Snakemake"
    - [Snakemake: github module using python module in repo](https://stackoverflow.com/questions/76471741/snakemake-github-module-using-python-module-in-repo)
    - [Importing a Python module within a Snakemake module raises a `ModuleNotFoundError` #2914](https://github.com/snakemake/snakemake/issues/2914)
    - [problems with local python imports within snakemake modules #1063](https://github.com/snakemake/snakemake/issues/1063)
    - [Helper function to be able to call a Python script by its module name (`python -m`) #4003](https://github.com/snakemake/snakemake/issues/4003)
    - [Import local module in script #956](https://github.com/snakemake/snakemake/issues/956)
    - [ModuleNotFoundError when importing from sibling directory #412](https://github.com/snakemake/snakemake/issues/412)
    - [Relative import in python script not working when using a module from Gitlab #1632](https://github.com/snakemake/snakemake/issues/1632)
    - [Importing utility modules into scripts or notebooks? #1089](https://github.com/snakemake/snakemake/issues/1089)
    - [Local imports incompatible with submodules #3951](https://github.com/snakemake/snakemake/issues/3951)

Splitting the package and workflow into separate repositories can work, but it makes day-to-day development slower because reusable code and workflow behavior stop evolving in the same place.

## Code generation with Copier

[Copier](https://copier.readthedocs.io/) is a tool that creates a project from a template and can later pull template improvements back into that project. As the ABLE Workflow improves and adapts to changing best practices, so can your project.

### Best Practices

- [Rebuild data products from source data and code](best-practices.md#rebuild-data-products-from-source-data-and-code)
- [Treat engineering checks as part of the project, not cleanup work](best-practices.md#treat-engineering-checks-as-part-of-the-project-not-cleanup-work)
- [Keep reusable python code and workflow code together during development](best-practices.md#keep-reusable-python-code-and-workflow-code-together-during-development)
- [Design workflows so other workflows can extend them](best-practices.md#design-workflows-so-other-workflows-can-extend-them)
- [Publish stable interfaces, not just files](best-practices.md#publish-stable-interfaces-not-just-files)

### Implementation details

In the tempalte repository, the `template/` directory contains [jinja2 templates](https://copier.readthedocs.io/en/stable/creating/) used to generate the project. The `copier.yml` defines the questions for the user to fill out the template and the autoamted tasks to run from `tasks/` after the template has rendered.

In a generated project, the most visible sign is the answers file that records how the project was created and which follow-on templates were applied.

```.yaml
└── .copier-answers
    ├── post-copier-todos/ # (1)
    └── *.yml # (2)
```

1. Each Copier template generates a to-do list that can be easily copied into a Github issue to help you go from the code scaffold to your working code.
2. Each Copier template generates an "answers file" containing the necessary information to regenerate the project. DO NOT MANUALLY EDIT THESE FILES.

Copier's answers files and update workflow are what make this more than a one time scaffold.

### Tradeoffs and rejected alternatives

Tools such as [Cookiecutter](https://cookiecutter.readthedocs.io/) and [Yeoman](https://yeoman.io/) are useful for initial scaffolding, but they are not built around template updates as a primary part of the workflow. Update support is important for this project, because the template is meant to improve over time and existing projects should be able to adopt those improvements without being recreated from scratch. [`Cruft`](https://cruft.github.io/cruft/) does add update support for Cookiecutter-based templates, but that support sits on top of Cookiecutter rather than being part of the primary template tool itself.

## Durable tabular outputs with Parquet

[Apache Parquet](https://parquet.apache.org/docs/overview/) is the default filetype for saving dataframes in the generated project workflows.

### Best Practices

- [Rebuild data products from source data and code](best-practices.md#rebuild-data-products-from-source-data-and-code)

### Implementation details

In a generated project, you will most often see this choice in the workflow outputs under `data/` (except for `data/**/external/` which may be in a different externally defined format) and in the load, extract, and schemas that serve as the interface between the parquet file and python.

```.yaml
└── data/
    └── {{ module_name }}/
        ├── external/  # (1)
        ├── raw/  # (2)
        ├── interim/  # (3)
        └── processed/  # (4)
```

1. **External data** comes from a 3rd party and may not be in tabular parquet format that can be validated with a pandera schema.
2. **Raw data** imported data that is parquet format with an associated pandera schema
3. **Interim data** saved from intermediate steps in the workflow to avoid reprocessing the whole workflow
4. **Processed data** the final processed output

Parquet’s [columnar layout](https://parquet.apache.org/docs/overview/motivation/), built-in metadata, and strong support in `pandas`, `dask`, and `polars` are the main reasons it works well for analytical workflows, especially when downstream code repeatedly reads subsets of columns or large tabular outputs.

### Tradeoffs and rejected alternatives

**CSV.** Too weak on types, metadata, and efficient large-scale analytical reads.

**SQLite.** Useful for small relational workloads, but not as natural a fit for columnar analytics outputs.

**Pickle.** Python-specific and not a good interchange format for durable analytical artifacts.

**HDF5.** Powerful, but less aligned with the cross-tool, columnar analytics ecosystem this project targets.

## Automated Quality Assurance

[tox](https://tox.wiki/) is the common entry point for the project's repeatable checks, such as tests, linting, type checking, packaging validation, and docs tasks. It is there to make those tasks runnable in a consistent way across
developers and CI.

[GitHub Actions](https://docs.github.com/en/actions) is the default way the generated projects run those checks automatically on pull requests and other Git events.

[pre-commit](https://pre-commit.com/) adds one more practical layer: it runs a small set of checks automatically before each commit so contributors can catch simple problems before they even open a pull request.

### Best Practices

- [Rebuild data products from source data and code](best-practices.md#rebuild-data-products-from-source-data-and-code)
- [Treat engineering checks as part of the project, not cleanup work](best-practices.md#treat-engineering-checks-as-part-of-the-project-not-cleanup-work)

### Implementation details

The tox configuration file `tox.ini` specifies the tests (with `pytest`), linting (with `black`, `ruff`, and `snakefmt`), type checking (with `mypy`), and packaging validation tasks to be run. Each test runs in an isolated environment mimicking the environment the tested code would run in.

The Github actions in `.github/workflows/ci.yml` run the tox checks in a clean, repeatable environment instead of relying on one developer's machine to catch problems. In practice, that means missing dependencies, packaging mistakes, docs breakage, and workflow regressions are more likely to be caught before they land on the default branch.

In generated projects, formatting, linting, and other fast checks are enforced through `.pre-commit-config.yaml` when changes are committed to git. This keeps routine quality checks close to day-to-day development while leaving heavier test suites to `tox` and GitHub Actions.

```.yaml
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   └── tests/ # (1)
├── hooks/ # (8)
├── tests/
│   ├── {{ package_name }}/
│   │   ├── **runner/test_*.py # (2)
│   │   ├── **/test_*.py # (3)
│   └── workflow/
│       ├── rules/ # (4)
│       └── scripts/ # (5)
├── .pre-commit-config.yaml # (7)
└── tox.ini # (6)
```

1. Small datasets for tests to validate
2. Unit tests of the python package that require the `runner` extra dependencies
3. Unit tests of the python package that only require the core package dependencies
4. Integration test of a full Snakemake rule from input data to output data.
5. Unit tests of scripts directly executed by Snakemake, in the conda environment specified by the associated Snakemake rule.
6. The tox configuration file that defines test environments and tasks.
7. Pre-commit configuration file that specifies the checks to run before every git commit
8. Pre-commit "hooks", scripts that run in custom pre-commit checks

### Tradeoffs and rejected alternatives

Running only `pytest` in one ad hoc environment can be fine for a small package, but it makes typing, formatting, packaging checks, and multiple dependency environments more manual and likely to be skipped.

Github actions can offload to the cloud the computationally intense task of running all the tests, and automate the process to make sure it never get skipped. For public open-source project, Github actions are free to run.

## Formatting, linting, and type checking

[Black](https://black.readthedocs.io/), [Ruff](https://docs.astral.sh/ruff/), and [mypy](https://mypy.readthedocs.io/) are tools that help keep the code readable and consistent: Black formats code, Ruff catches common problems, and mypy checks type hints. Together with CI, they help the project catch problems early instead of after a workflow output has already drifted.

### Best Practices

- [Treat engineering checks as part of the project, not cleanup work](best-practices.md#treat-engineering-checks-as-part-of-the-project-not-cleanup-work)

### Implementation details

You see these choices in `pyproject.toml`, the tox configuration, and the CI workflow files under `.github/workflows/`. Those are the places where formatting, linting, and type-checking rules are configured and enforced.

Black’s [opinionated formatting model](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html), Ruff’s support for both [linting](https://docs.astral.sh/ruff/linter/) and [formatting](https://docs.astral.sh/ruff/formatter/), and mypy’s [static type checking](https://mypy.readthedocs.io/en/stable/getting_started.html) together explain the division of labor used in this template.

### Tradeoffs and rejected alternatives

Using only Ruff for both linting and formatting is a viable alternative, but the generated project use Black as the explicit formatting contract and Ruff as the main linter. That split is conservative, consistent, and easy to review.

## Generate Conda environments from project metadata

[`pyproject2conda`](https://github.com/usnistgov/pyproject2conda) turns Python dependency metadata into Conda environment files. It reduces duplication between package metadata and workflow environment definitions while still producing the conda environment files Snakemake needs.

### Best Practices

- [Rebuild data products from source data and code](best-practices.md#rebuild-data-products-from-source-data-and-code)
- [Treat engineering checks as part of the project, not cleanup work](best-practices.md#treat-engineering-checks-as-part-of-the-project-not-cleanup-work)

### Implementation details

Running `snakemake pyproject2conda_all` (defined in `build.smk`) will convert the various dependency groups in `pyproject.toml` into conda environment yaml files in `workflow/envs/`.

```.yaml
├── workflow/
│   ├── envs/
│   │   ├── pyproject2conda/ # (1)
│   │   ├── py312-tox.yaml # (2)
│   │   └── py312-workflow.yaml # (3)
│   └── rules/
│       └── build.smk # (4)
└── pyproject.toml # (5)
```

1. Conda environment yaml files with dependencies required by Snakemake rules; they do not yet include the projects python package.
2. The minimal conda environment to run the tox tests.
3. The minimal conda environment to run the Snakemake workflow
4. The snakefile where the `pyproject2conda_all` rule is defined.
5. The python package configuration file.

The key idea is to keep `pyproject.toml` as the sole source of truth for dependency declarations while still generating Conda environment files that match Snakemake's execution model.

### Tradeoffs and rejected alternatives

Hand-maintaining both `pyproject.toml` and multiple Conda environment YAML files creates drift risk and makes the reproducibility story harder to uphold.

## Data schemas with Pandera

[`pandera`](https://pandera.readthedocs.io/) provides a flexible and expressive API for performing data validation on dataframe-like objects. The goal of Pandera is to make data processing pipelines more readable and robust with statistically typed dataframes. It lets the project describe what a dataframe should look like and check whether a dataset matches that description.

### Best Practices

- [Treat engineering checks as part of the project, not cleanup work](best-practices.md#treat-engineering-checks-as-part-of-the-project-not-cleanup-work)
- [Publish stable interfaces, not just files](best-practices.md#publish-stable-interfaces-not-just-files)

### Implementation details

You see this choice in package modules that define pandera schemas and in the tests that validate example data against those schemas. Other ETL steps that consume data from this one can validate their input against this schema.

```.yaml
└── {{ package_name }}/
    └── datasets/
        └── {{ module_name }}/
            └── {{ etl_name }}/
                ├── runner/
                └── schema.py # (1)
```

1. File containing the pandera schema for the data produced by this ETL step.

Pandera fits this project because the primary contract is tabular data. The generated project needs dataframe-oriented schemas, checks, and extraction helpers more than generic object validation.

### Tradeoffs and rejected alternatives

Pydantic is strongest for Python object models and application or configuration contracts. JSON Schema is interoperable, but it is not the most natural way to express dataframe-specific checks and extraction helpers. Pandera is a better fit for the data products this template is centered on.

## Lightweight reusable interfaces

An ETL step may require large or very strict python dependencies; however, other workflows that read the output data from this workflow will want to read the pandera dataframe schemas and functions for extract the output data. The generated projects therefore separates reusable interfaces such as schemas and extraction helpers from the main ETL code that executes the workflow.

### Best Practices

- [Keep reusable python code and workflow code together during development](best-practices.md#keep-reusable-python-code-and-workflow-code-together-during-development)
- [Publish stable interfaces, not just files](best-practices.md#publish-stable-interfaces-not-just-files)

### Implementation details

You see this split inside ETL modules, where reusable interface modules sit next to a `runner/` directory that holds heavier workflow-only code. The public, output-facing surface stays light enough for downstream consumers to install and use without pulling in the entire execution stack.

```.yaml
├── {{ package_name }}/
│   └── datasets/
│       └── {{ module_name }}/
│           └── {{ etl_name }}/
│               ├── runner/
│               │   ├── load.py
│               │   ├── main.py
│               │   └── transform.py
│               ├── extract.py
│               └── schema.py
└── pyproject.toml
```

The same split also shows up in the unit tests under `tests/{{ package_name }}/`. The tox lint and typechecks also run against the core package and core+runner in separate environments.

### Tradeoffs and rejected alternatives

Putting all dependencies together is simpler up front, but it forces downstream consumers of workflow outputs to install the same heavy stack the runner needs. Using only JSON Schema as the main contract is also less attractive here because the core contract is a dataframe contract, not a generic JSON document.

## Local development environment localization

The `conda_localize` snakemake rule is a setup step that prepares workflow environment files for local development and execution. It gives the workflow a way to install the local project package from the correct path on the current machine without pretending that the same path will also make sense once the workflow is imported elsewhere.

### Best Practices

- [Keep reusable python code and workflow code together during development](best-practices.md#keep-reusable-python-code-and-workflow-code-together-during-development)
- [One project shape across local and shared computing environments](best-practices.md#one-project-runs-can-run-on-local-machines-in-shared-computing-clusters-or-on-the-cloud)
- [Design workflows so other workflows can extend them](best-practices.md#design-workflows-so-other-workflows-can-extend-them)

### Implementation details

Running the `snakemake conda_localize` rule appends the conda environment yaml files in `workflow/envs/pyproject2conda/` with a `pip` statement to install the project's python package from the full path and writes them to `workflow/envs/localized`. The `get_localized_conda()` function is used in the snakefiles (`.smk`) to get the path to this localized environment file from the environment name.

```.yaml
├── workflow/
│   ├── envs/
│   │   ├── localized/ # (1)
│   │   ├── pyproject2conda/ # (2)
│   └── rules/
│       └── dev.smk # (3)
└── pyproject.toml # (4)
```

1. The directory of conda environment files that install the project's python package from its full path.
2. The directory of conda environment files generated from the `pyproject.toml` file, without the project's package installed.
3. The snakefile that defines `conda_localize`
4. The python project file that defines the environment dependencies.

Snakemake’s [Conda integration](https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html) is what makes per-rule environments practical here, but it also means the workflow engine manages those environment files as part of execution. In practice, cached scripts and cached source files introduce path-related edge cases for imported workflows. The practical constraint this template works around is that paths that are local and obvious in the repository do not always keep the same meaning once workflow-managed files are copied into cache locations.

### Tradeoffs and rejected alternatives

**Relative local pip installs inside version-controlled env YAML files.** In a plain pip workflow this can work, but in Snakemake-managed Conda environments the anchor becomes unstable because Snakemake manages environment files as part of its [Conda deployment workflow](https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html), so a relative path in the repository is not a reliable long-term contract.

**Put helper Python modules in `workflow/scripts` and import them directly.** This again relies on local-script import behavior that does not generalize well to GitHub-imported modules. 

??? note "The long-running issue of importing custom Python in Snakemake"
    - [Snakemake: github module using python module in repo](https://stackoverflow.com/questions/76471741/snakemake-github-module-using-python-module-in-repo)
    - [Importing a Python module within a Snakemake module raises a `ModuleNotFoundError` #2914](https://github.com/snakemake/snakemake/issues/2914)
    - [problems with local python imports within snakemake modules #1063](https://github.com/snakemake/snakemake/issues/1063)
    - [Helper function to be able to call a Python script by its module name (`python -m`) #4003](https://github.com/snakemake/snakemake/issues/4003)
    - [Import local module in script #956](https://github.com/snakemake/snakemake/issues/956)
    - [ModuleNotFoundError when importing from sibling directory #412](https://github.com/snakemake/snakemake/issues/412)
    - [Relative import in python script not working when using a module from Gitlab #1632](https://github.com/snakemake/snakemake/issues/1632)
    - [Importing utility modules into scripts or notebooks? #1089](https://github.com/snakemake/snakemake/issues/1089)
    - [Local imports incompatible with submodules #3951](https://github.com/snakemake/snakemake/issues/3951)

**Publish the package first, even for local development.** That improves uniformity but makes defeats the workflow and Python package mono-repo principal, and worse by slowing down the development loop.

## Environment selection across local and imported workflows

`get_conda_env(...)` is a helper that decides which environment file a rule should use. It is what allows the same workflow code to work both in local development and in contexts where the package should be installed from GitHub instead of the current checkout.

### Best Practices

- [Keep reusable python code and workflow code together during development](best-practices.md#keep-reusable-python-code-and-workflow-code-together-during-development)
- [One project shape across local and shared computing environments](best-practices.md#one-project-runs-can-run-on-local-machines-in-shared-computing-clusters-or-on-the-cloud)
- [Design workflows so other workflows can extend them](best-practices.md#design-workflows-so-other-workflows-can-extend-them)

### Implementation details

You see this most directly in `workflow/Snakefile` and in helper modules that centralize environment-file selection for workflow rules. In practice, the helper should read a config value such as `py_pkg_src` and return the appropriate environment file for either local development or a GitHub-based install.

This exists because imported workflows and cached scripts can change where code is loaded from. The package install source therefore needs to be selected explicitly instead of left to incidental path behavior.

### Tradeoffs and rejected alternatives

Hard-coding a Git ref in version-controlled environment files duplicates release information into source files. Trying to infer the package install ref from the workflow import ref would be convenient, but Snakemake does not promise that the same ref will automatically be exposed for reuse in package installation logic. Using `workflow.source_path()` to cache an entire package tree is also the wrong abstraction. It is a better fit for auxiliary source files than for the primary packaging strategy of a Python codebase.

## How the pieces fit together

Any one of these choices can help on its own. The real value comes from combining them. A project that has a workflow engine but no tests can still regress silently. A project with good linting but no explicit environments can still be hard to rerun elsewhere. A project with schemas but no orchestration can still become operationally messy.

The template tries to establish a baseline where those pieces reinforce one another.

- Snakemake makes the workflow explicit.
- The package boundary makes reusable logic and output contracts importable.
- Pandera and Parquet make outputs more durable and reviewable.
- tox, Black, Ruff, mypy, and CI make changes safer.
- Copier keeps the whole baseline updateable.
- Conda-localization helpers keep local development and imported workflow usage
  from collapsing into path-specific hacks.

That combination is what the suite is really optimizing for: generated projects that are easier to trust, extend, and share.

<!-- markdownlint-enable MD024 -->
