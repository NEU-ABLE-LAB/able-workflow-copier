# Project directory tree

## Copier templates variables

Copier uses a jinja2 syntax for rendering templates with the answers to the templates questions.

- [able-workflow-copier]({{ able_workflow_copier_docs }})
- [able-workflow-copier template]({{ able_workflow_copier_docs }})
  - **{{ project_name_slug }}**: The name of the project being created.
  - **{{ package_name }}**: The name of the Python package being created.
- [able-workflow-module-copier template]({{ able_workflow_module_copier_docs }})
  - **{{ module_type }}**: The type of module being created (e.g., datasets, features, or models).
  - **{{ module_name }}**: The name of the module being created.
- [able-workflow-etl-copier template]({{ able_workflow_etl_copier_docs }})
  - **{{ etl_name }}**: The name of the ETL process being created.
  - **{{ conda_env_key }}**: The key for the Conda environment from the workflow config (e.g., `config["CONDA"]["ENVS"]["{{ conda_env_key }}"]`).
- [able-workflow-rule-copier template]({{ able_workflow_rule_copier_docs }})
  - **{{ is_package_rule }}**: The rule uses the package.
  - **{{ rule_name }}**: The name of the Snakemake rule being created.

## Project Tree

Files that are created by a template are marked with a + sign, and files that are modified by a Copier template are marked with a * sign.

Legend (first 4 characters before each path, left to right):

1) `able-workflow-copier`
2) `able-workflow-module-copier`
3) `able-workflow-etl-copier`
4) `able-workflow-rule-copier`

Symbol in each column:

- `+` = created by that template
- `*` = modified by that template
- ` ` = blank = untouched by that template

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  {{ project_name_slug }}
 +  ├── .copier-answers/
 +  │   └── post-copier-todos/
 +  ├── .github/
 +  │   ├── ISSUE_TEMPLATE/
 +  │   └── workflows/
 +  ├── .vscode/
 +  │   ├── extensions.json
 +  │   ├── launch.json
 +  │   └── settings.json
 +  ├── config/
 +  │   ├── datasets/
 +  │   ├── features/
 +  │   └── models/
 +  ├── data/
 +* │   ├── {{ module_name }}/
 +  │   └── tests/
 +  ├── docs/
 +  │   ├── _gen-files-scripts/
 +  │   └── docs/
 +  ├── hooks/
 +  ├── features/
 +  ├── logs/
 +  │   └── rules/
 +  ├── models/
 +  ├── notebooks/
 +  ├── references/
 +  ├── reports/
 +  │   ├── datasets/
 +  │   ├── features/
 +  │   ├── models/
 +  │   └── notebook_templates/
 +  ├── scripts/
 +  ├── tests/
 +  │   ├── docs/
 +  │   ├── {{ package_name }}/
 +  │   └── workflow/
 +  ├── workflow/
 +  │   ├── envs/
 +  │   ├── profiles/
 +  │   ├── rules/
 +  │   ├── schemas/
 +  │   └── scripts/
 +  └── {{ package_name }}/
```

## .copier-answers/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  .copier-answers/  # (1)
 +  ├── project.yml
 +  ├── module-{{ module_type }}-{{ module_name }}.yml
  + ├── etl-{{ module_type }}-{{ module_name }}-{{ etl_name }}.yml
   +└── rule-{{ module_type }}-{{ module_name }}-{{ rule_name }}.yml
 +  └── post-copier-todos/
 +      ├── package.md
  +      ├── module-{{ module_type }}-{{ module_name }}.md
   +      ├── etl-{{ module_type }}-{{ module_name }}-{{ etl_name }}.md
   +      ├── etl-{{ module_type }}-{{ module_name }}-{{ etl_name }}-subissues/
   +      │   ├── 01-rule.md
   +      │   ├── 04-transform.md
   +      │   ├── 05-schema.md
   +      │   ├── 06-load.md
   +      │   ├── 07-extract.md
   +      │   ├── 08-main.md
   +      │   ├── 09-integration-tests.md
   +      │   └── 10-docs.md
   +      └── rule-{{ rule_name }}.md
```

1. The Copier answers files written by each template run (package, then optional module, etl, and rule) are stored here.

## .github/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  .github/
 +  ├── ISSUE_TEMPLATE/
  + │   ├── post-copier-etl.md
 +  │   ├── post-copier-module.md
 +  │   ├── post-copier-package.md
   +│   └── post-copier-rule.md
 +  ├── labels.yml
 +  └── workflows/
 +      ├── build.yml
 +      ├── ci.yml
 +      ├── github-labeler.yml
 +      └── release.yml
```

1. `.github/ISSUE_TEMPLATE/post-copier-*.md` files provide guided issue templates for post-Copier follow-up tasks.
2. `.github/labels.yml` defines shared labels used for issue and PR triage.
3. `.github/workflows/ci.yml` runs core checks that validate docs, template logic, and test changes.

## .vscode/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  .vscode/
 +  ├── extensions.json
 +* ├── launch.json
 +* └── settings.json
```

1. `.vscode/extensions.json` recommends workspace extensions for a consistent development setup.
2. `.vscode/settings.json` stores workspace defaults for formatting and analysis behavior.
3. `.vscode/launch.json` provides local debug launch configurations.

## config/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  config/
 +  ├── config.yaml
 +  ├── config.local.example.yaml
 +  ├── README.md
 +  ├── datasets/
 +  │   └── {{ module_name }}/  # (1)
 +* │       └── config.yaml  # (4)
 +  ├── features/
 +  │   └── {{ module_name }}/  # (2)
 +* │       └── config.yaml  # (4)
 +  └── models/
 +      └── {{ module_name }}/  # (3)
 +*         └── config.yaml  # (4)
```

1. config/datasets/{{ module_name }}/ is created when {{ module_type }} == "datasets".
2. config/features/{{ module_name }}/ is created when {{ module_type }} == "features".
3. config/models/{{ module_name }}/ is created when {{ module_type }} == "models".
4. config.yaml files under module paths are created by able-workflow-module-copier and may be updated by able-workflow-etl-copier.

## data/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  data/
 +  ├── README.md
 +  ├── tests/
 +  │   └── dry-run/
 +* └── {{ module_name }}/
 +*     ├── external/  # (1)
 +*     ├── interim/  # (2)
 +*     ├── processed/  # (3)
 +*     ├── raw/  # (4)
 +*     └── README.md
```

1. Data copied from an external source in a non-standard format.
2. Temporary data storage for intermediate workflow steps.
3. Processed data ready for reporting, feature extraction, or modeling.
4. Raw data in a standardized format.

## docs/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  docs/
 +  ├── mkdocs.yml
 +  ├── gen_ref_pages.py
 +  ├── README.md
 +  ├── _gen-files-scripts/
 +  │   └── render_summaries.py
 +  └── docs/
 +      ├── index.md
 +      ├── SUMMARY.md
 +      ├── _images/
 +      ├── _js/
 +      ├── overview/
 +      │   ├── index.md
 +      │   ├── best-practices.md
 +      │   ├── motivation.md
 +      │   ├── whitespace.md
 +      │   ├── tree.md
 +      │   └── tree.snippet.md
 +      ├── setup/
 +      │   ├── index.md
 +      │   └── SUMMARY.md
 +      ├── workflow/
 +      │   ├── index.md
 +      │   ├── config.md
 +      │   ├── rules.md
 +      │   └── SUMMARY.md
 +      ├── datasets/
 +      │   ├── index.md
 +      │   ├── SUMMARY.md
 +      │   └── {{ module_name }}/
 +      │       ├── index.md
 +      │       ├── config.md
  +      │       ├── {{ etl_name }}/
  +      │       │   ├── index.md
  +      │       │   ├── config.md
  +      │       │   ├── schema.md
  +      │       │   └── SUMMARY.md
 +      │       └── SUMMARY.md
 +      ├── features/
 +      │   ├── index.md
 +      │   └── SUMMARY.md
 +      ├── models/
 +      │   ├── index.md
 +      │   └── SUMMARY.md
 +      └── contributing/
 +          ├── index.md
 +          ├── SUMMARY.md
 +          └── templates/
 +              ├── index.md
 +              ├── SUMMARY.md
 +              └── {{ module_type }}/{{ module_name }}/{{ etl_name }}/
```

1. `docs/mkdocs.yml` is the root MkDocs configuration for site build behavior and plugins.
2. `docs/docs/SUMMARY.md` is the primary navigation source used by literate-nav.
3. `docs/_gen-files-scripts/render_summaries.py` helps regenerate section summary files.

## hooks/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  hooks/
 +  ├── README.md
 +  └── snakemake_pyproject2conda.py
```

1. `hooks/snakemake_pyproject2conda.py` syncs dependency declarations into Conda environment specs used by workflow execution.
2. `hooks/README.md` documents hook purpose and usage expectations.

## features/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  features/
 +  ├── README.md
 +  └── {{ module_name }}/
 +      └── README.md
```

1. `features/README.md` defines conventions for organizing feature outputs.
2. `features/{{ module_name }}/README.md` is the module-specific landing page for feature artifacts.

## logs/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  logs/
 +  └── rules/
 +      └── README.md
```

1. `logs/rules/README.md` documents where rule logs are written and how to inspect failures.

## models/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  models/
 +  ├── README.md
 +  └── {{ module_name }}/
 +      └── README.md
```

1. `models/README.md` describes conventions for model outputs and artifacts.
2. `models/{{ module_name }}/README.md` captures module-specific model documentation.

## notebooks/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  notebooks/
 +  └── README.md
```

1. `notebooks/README.md` documents notebook storage, naming, and maintenance expectations.

## references/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  references/
 +  └── README.md
```

1. `references/README.md` is the location for external links, citations, and source metadata notes.

## reports/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  reports/
 +  ├── datasets/
 +  │   ├── .gitkeep
 +  │   └── {{ module_name }}/README.md
 +  ├── features/
 +  │   ├── .gitkeep
 +  │   └── {{ module_name }}/README.md
 +  ├── models/
 +  │   ├── .gitkeep
 +  │   └── {{ module_name }}/README.md
 +  └── notebook_templates/
 +      ├── datasets/{{ module_name }}/README.md
 +      ├── features/{{ module_name }}/README.md
 +      └── models/{{ module_name }}/README.md
```

1. `reports/datasets/{{ module_name }}/README.md`, `reports/features/{{ module_name }}/README.md`, and `reports/models/{{ module_name }}/README.md` describe expected report outputs.
2. `reports/notebook_templates/*/{{ module_name }}/README.md` files define starter notebook report templates.

## scripts/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  scripts/
 +  ├── conda_env_update.py
 +  └── workflow_requirements_generate.py
```

1. `scripts/conda_env_update.py` updates environment configuration artifacts used by the workflow.
2. `scripts/workflow_requirements_generate.py` generates workflow requirements metadata.

## {{ package_name }}/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  {{ package_name }}/
 +  ├── __init__.py
 +  ├── config.py
 +  ├── datasets/
 +  │   ├── __init__.py
 +  │   └── {{ module_name }}/
 +  │       ├── __init__.py
  + │       └── {{ etl_name }}/
  + │           ├── __init__.py
  + │           ├── extract.py
  + │           ├── schema.py
  + │           └── runner/
  + │               ├── __init__.py
  + │               ├── extract_external.py
  + │               ├── load.py
  + │               ├── main.py
  + │               ├── transform.py
  + │               └── utils.py
 +  ├── features/
 +  │   ├── __init__.py
 +  │   └── {{ module_name }}/
  + │       └── {{ etl_name }}/  # same layout as datasets/{{ module_name }}/{{ etl_name }}/
 +  ├── models/
 +  │   ├── __init__.py
 +  │   └── {{ module_name }}/
  + │       └── {{ etl_name }}/  # same layout as datasets/{{ module_name }}/{{ etl_name }}/
 +  └── utils/
 +      ├── __init__.py
 +      └── logging/
 +          ├── __init__.py
 +          ├── logging.py
 +          └── runner/test_logging.py
```

1. `{{ package_name }}/config.py` centralizes project configuration loading for package code.
2. `{{ package_name }}/datasets/{{ module_name }}/{{ etl_name }}/runner/main.py` is the ETL runner entry point.
3. `{{ package_name }}/utils/logging/logging.py` provides shared logging configuration utilities.

## tests/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  tests/
 +  ├── conftest.py
 +  ├── {{ package_name }}/
 +  │   ├── README.md
 +  │   ├── datasets/
 +  │   ├── features/
 +  │   ├── models/
 +  │   └── utils/
 +  │       ├── logging/test_logging.py
 +  │       └── runner/test_runner_extras.py
 +  └── workflow/
 +      ├── rules/
 +      │   ├── conftest.py
 +      │   ├── README.md
 +      │   ├── test_snakemake_all_data.py
 +      │   ├── test_snakemake_docs.py
  +      │   └── {{ module_type }}/{{ module_name }}/test_snakemake_{{ etl_name }}.py
 +      └── scripts/
 +          ├── rules_global/  # (1)
 +          ├── rules_conda_DOCS/  # (2)
 +          ├── rules_conda_{{ conda_env_key }}/  # (3)
 +          ├── rules_conda_CORE/  # (4)
 +          ├── rules_conda_RUNNER/  # (5)
 +          └── utils/
```

1. Unit tests for workflow scripts that run in the global Snakemake environment (rules_global).
2. Unit tests for workflow scripts that require the docs Conda environment (`config["CONDA"]["ENVS"]["DOCS"]`).
3. Unit tests for workflow scripts added by able-workflow-rule-copier for `config["CONDA"]["ENVS"]["{{ conda_env_key }}"]`.
4. Unit tests for workflow scripts that require the package core Conda environment (`config["CONDA"]["ENVS"]["CORE"]`).
5. Unit tests for workflow scripts that require the runner Conda environment (`config["CONDA"]["ENVS"]["RUNNER"]`).

## workflow/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  workflow/
 +  ├── Snakefile
 +  ├── envs/
 +  │   ├── localized/
 +  │   ├── pyproject2conda/
 +  │   ├── {{ package_name }}-py312-tox.yaml
 +  │   └── {{ package_name }}-py312-workflow.yaml
 +  ├── profiles/
 +  │   ├── default/config.yaml
 +  │   └── slurm/config.yaml
 +  ├── rules/
 +  │   ├── build.smk
 +  │   ├── dev.smk
 +  │   ├── docs.smk
 +  │   ├── includes.smk  # (1)
 +  │   ├── reports.smk
 +  │   ├── utils.smk
 +  │   └── {{ module_type }}/{{ module_name }}/{{ etl_name }}.smk
 +  ├── schemas/
 +  │   ├── config.schema.yaml
 +  │   └── {{ module_type }}/{{ module_name }}/{{ etl_name }}/config.schema.yaml
 +  └── scripts/
 +      ├── rules_conda_{{ conda_env_key }}/  # (2)
 +      ├── rules_conda_CORE/  # (3)
 +      ├── rules_conda_DOCS/  # (4)
 +      ├── rules_global/  # (5)
 +      ├── rules_conda_RUNNER/  # (6)
 +      └── utils/
```

1. Single include file that aggregates rule include statements.
2. Workflow scripts added by able-workflow-rule-copier for `config["CONDA"]["ENVS"]["{{ conda_env_key }}"]`.
3. Workflow scripts that require the package core Conda environment.
4. Workflow scripts that require the docs Conda environment.
5. Workflow scripts that run in the global Snakemake environment.
6. Workflow scripts that require the runner Conda environment.

## Root files

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  .copier-answers.yml
 +  .gitattributes
 +  .gitignore
 +  .pre-commit-config.yaml
 +  AGENTS-setup.md
 +  AGENTS.md
 +  CHANGELOG.md
 +  LICENSE
 +  pyproject.toml
 +  README.md
 +  snakefmt.toml  # (1)
 +  tox.ini  # (2)
```

1. Configuration settings for Snakemake formatting.
2. Main tox settings for testing template code and generated project code.
