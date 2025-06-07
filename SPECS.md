
# ABLE workflow copier template suite specification

This is the specification document for a suite of [`copier`](https://copier.readthedocs.io) templates `able_workflow_copier`, `able_workflow_module_copier` and `able_workflow_etl_copier`. These `copier` templates are combined together by using [separate `.copier-answers.*.yml` files](https://copier.readthedocs.io/en/stable/configuring/#applying-multiple-templates-to-the-same-subproject).

## `able_workflow_copier`

Template for creating the root project that contains a python package and snakemake workflow. Specified by `copier.able_workflow.yml`

### Issue template

Create a `post-copy` hook to copier that creates a github issue for the user to complete the project. Assume that the user has the `gh` CLI installed and authenticated.

```markdown
# Finish initializing the `{{ project_name }}` project

## Checklist
- [ ] Create at least one module with `able_workflow_module_copier`.

```

### Resulting files of project

```txt
{{ project_name }}
├── .copier-answers/
│
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── add-etl.yml
│   └── workflows/
│       ├── build.yml ✓
│       ├── ci.yml
│       └── release.yml
│
├── .vscode/
│   ├── extensions.json
│   ├── launch.json
│   └── settings.json
│
├── config/
│   ├── config.yaml
│   ├── config.local.example.yaml
│   └── README.md
│
├── data/
│   └── README.md
│
├── docs/
│   ├── docs/
│   │   ├── assets/
│   │   │   ├── css/
│   │   │   ├── images/
│   │   │   └── js/
│   │   ├── contributing/
│   │   │   ├── docs.md
│   │   │   ├── etl.md
│   │   │   ├── index.md
│   │   │   ├── SUMMARY.md
│   │   │   └── vscode.md
│   │   ├── datasets/
│   │   │   ├── index.md
│   │   │   └── SUMMARY.md
│   │   ├── features/
│   │   │   ├── index.md
│   │   │   └── SUMMARY.md
│   │   ├── models/
│   │   │   ├── index.md
│   │   │   └── SUMMARY.md
│   │   ├── overview/
│   │   │   ├── best-practices.md
│   │   │   ├── index.md
│   │   │   ├── motivation.md
│   │   │   ├── SUMMARY.md
│   │   │   └── whitespace.md
│   │   ├── setup/
│   │   │   ├── index.md
│   │   │   ├── linux.md
│   │   │   ├── slurm.md
│   │   │   ├── SUMMARY.md
│   │   │   └── windows.md
│   │   ├── workflow/
│   │   │   ├── config.md
│   │   │   ├── index.md
│   │   │   ├── rules.md
│   │   │   └── SUMMARY.md
│   │   ├── getting-started.md
│   │   ├── index.md
│   │   ├── SUMMARY.md
│   │   └── weh.md
│   │
│   ├── gen_ref_pages.py
│   ├── mkdocs.yml
│   └── README.md
│
├── hooks/
│   └── snakemake_pyproject2conda.py
│
├── features/
│   └── README.md
│
├── logs/rules/
│   └── README.md
│
├── models/
│   └── README.md
│
├── notebooks/
│   └── README.md
│
├── references/
│   └── README.md
│
├── reports/
│   ├── datasets/
│   │   └── .gitkeep
│   ├── features/
│   │   └── .gitkeep
│   ├── models/
│   │   └── .gitkeep
│   ├── notebook_templates/
│   │   ├── datasets/
│   │   ├── features/
│   │   └── models/
│   └── publications/
│       └── .gitkeep
│
├── {{ package_name }}
│   ├── datasets/
│   │   └── __init__.py
│   ├── features/
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logging.py
│   ├── __init__.py
│   └── config.py
│
├── tests/
│   ├── docs/
│   │   └── test_dag.py
│   ├── {{ package_name }}/
│   │   ├── datasets/
│   │   │   └── .gitkeep
│   │   ├── features/
│   │   │   └── .gitkeep
│   │   ├── models/
│   │   │   └── .gitkeep
│   │   ├── utils/
│   │   │   └── .gitkeep
│   │   └── README.md
│   └── worflow/
│       ├── rules/
│       │   ├── conftext.py
│       │   └── READMEmd
│       └── scripts/
│           ├── rules/
│           │   ├── test_conda_localize_file.py
│           │   └── test_pyproject2conda.py
│           ├── utils/
│           │   └── test_snakemake_helpers.py
│           └── README.md
│
├── workflow/
│   ├── envs/
│   │   ├── localized/
│   │   ├── pyproject2conda/
│   │   ├── py312-tox.yaml
│   │   └── py312-workflow.yaml
│   │
│   ├── profiles/
│   │   ├── default/
│   │   │   └── config.yaml
│   │   └── slurm/
│   │
│   ├── rules/
│   │   ├── datasets/
│   │   │   └── README.md
│   │   ├── features/
│   │   │   └── README.md
│   │   ├── models/
│   │   │   └── README.md
│   │   ├── build.smk
│   │   ├── dev.smk
│   │   ├── docs.smk
│   │   ├── reports.smk
│   │   └── utils.smk
│   │
│   ├── schemas/
│   │   ├── datasets/
│   │   │   └── .gitkeep
│   │   ├── features/
│   │   │   └── .gitkeep
│   │   ├── models/
│   │   │   └── .gitkeep
│   │   ├── config.schema.json
│   │   └── config.local.schema.json
│   │
│   ├── scripts/
│   │   ├── rules/
│   │   │   ├── __init__.py
│   │   │   ├── conda_localize_file.py
│   │   │   ├── dag_svg.py
│   │   │   ├── pyproject2conda.py
│   │   │   └── weh_interviews_rules.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── config_loader.py
│   │
│   └── Snakefile
│
├── .env.example
├── .copier-answers.yml
├── .gitattributes
├── .gitignore
├── .pre-commit-config.yaml
├── AGENTS.md
├── CHANGELOG.md
├── codecov.yml
├── LICENSE
├── pyproject.toml
├── README.md
├── snakefmt.toml
└── tox.ini
```

### Hypothetical `whole_energy_homes_interviews/.copier-answers.yml`

```yaml
project_name: "whole_energy_homes_interviews"
project_description: "Analysis of qualitative codes from interview transcripts."
package_name: "weh_interviews"
```

### Example `.copier-answers.yml`

```yaml
project_name: "able_workflow"
project_description: "Example analysis of workflow using a package."
package_name: "able"
```

## `able_workflow_module_copier`

When already inside a project generated by `able_workflow_copier`, this template adds one of the following types of modules to the package, and adds associated files throughout the project.

- dataset (`{{ package_name }}/datasets/{{ module_name }}/`)
- feature (`{{ package_name }}/features/{{ module_name }}/`)
- model (`{{ package_name }}/models/{{ module_name }}/`)

### `copier.able_workflow_module_copier.yml`

```yaml
module_type:
  type: "str"
  choices:
   - "dataset"
   - "feature"
   - "model"
module_description:
  type: "str"
  help: "Describe what this module does in a sentence or two."
module_name:
  type: "str"
  help: "The name of this module. (Must be a valid python module name.)"
    validator: "^[a-zA-Z_][a-zA-Z0-9_]*$"
```

### Issue template

After the user answer the questions and copier creates the module, copier should create a github issue for the user to complete the module.

```markdown
# Finish initializing the `{{ module_name }}` module

## Checklist
- [ ] Create at least one ETL process with `able_workflow_etl_copier`.

```

### Resulting files of module

The following files are added to the project

```txt
{{ project_name }}
├── .copier-answers/
│   └── .copier-answers.module-{{ module_type }}-{{ module_name }}.yml
│
├── config/
│   ├── datasets/
│   │   └── {{ module_name }}/     # IF {{ module_type }} == dataset
│   │       └── config.yaml
│   ├── features/
│   │   └── {{ module_name }}/     # IF {{ module_type }} == feature
│   │       └── config.yaml
│   └── models/
│       └── {{ module_name }}/     # IF {{ module_type }} == model
│           └── config.yaml
│
├── data/
│   └── {{ module_name }}/         # IF {{ module_type }} == dataset
│       ├── external/
│       ├── interim/
│       ├── processed/
│       ├── raw/
│       └── README.md
│
├── docs/
│   └── docs/
│       ├── datasets/
│       │   └── {{ module_type }}/ # IF {{ module_type }} == dataset
│       │       ├── index.md
│       │       └── SUMMARY.md
│       ├── features/
│       │   └── {{ module_type }}/ # IF {{ module_type }} == feature
│       │       ├── index.md
│       │       └── SUMMARY.md
│       └── models/
│           └── {{ module_type }}/ # IF {{ module_type }} == model
│               ├── index.md
│               └── SUMMARY.md
│
├── features/
│   └── {{ module_name }}/         # IF {{ module_type }} == feature
│       └── README.md
│
├── models/
│   └── {{ module_name }}/         # IF {{ module_type }} == model
│       └── README.md
│
├── reports/
│   ├── datasets/
│   │   └── {{ module_name }}/     # IF {{ module_type }} == dataset
│   │       └── README.md
│   ├── features/
│   │   └── {{ module_name }}/     # IF {{ module_type }} == feature
│   │       └── README.md
│   ├── models/
│   │   └── {{ module_name }}/     # IF {{ module_type }} == model
│   │       └── README.md
│   └── notebook_templates/
│       ├── datasets/
│       │   └── {{ module_name }}/     # IF {{ module_type }} == dataset
│       │       └── README.md
│       ├── features/
│       │   └── {{ module_name }}/     # IF {{ module_type }} == feature
│       │       └── README.md
│       └── models/
│           └── {{ module_name }}/     # IF {{ module_type }} == model
│               └── README.md
│
├── {{ package_name }}
│   ├── datasets/
│   │   └── {{ module_name }}/     # IF {{ module_type }} == dataset
│   │       └── __init__.py
│   ├── features/
│   │   └── {{ module_name }}/     # IF {{ module_type }} == feature
│   │       └── __init__.py
│   └── models/
│       └── {{ module_name }}/     # IF {{ module_type }} == model
│           └── __init__.py
│
└── workflow/
    ├── rules/
    │   ├── datasets/
    │   │   └── {{ module_name }}/     # IF {{ module_type }} == dataset
    │   │       └── README.md
    │   ├── features/
    │   │   └── {{ module_name }}/     # IF {{ module_type }} == feature
    │   │       └── README.md
    │   └── models/
    │       └── {{ module_name }}/     # IF {{ module_type }} == model
    │           └── README.md
    │
    └── schemas/
        ├── datasets/
        │   └── {{ module_name }}/     # IF {{ module_type }} == dataset
        │       └── README.md
        ├── features/
        │   └── {{ module_name }}/     # IF {{ module_type }} == feature
        │       └── README.md
        └── models/
            └── {{ module_name }}/     # IF {{ module_type }} == model
                └── README.md
```

### Hypothetical `whole_energy_homes_interviews/.copier-answers/module-dataset-coding_matrix.yml

```yaml
module_type: "dataset"
module_description: "Matrix of coded interview data for each participant."
module_name: "coding_matrix"
```

### Example `able_workflow/.copier-answers/module-dataset-sensing_platform.yml`

```yaml
module_type: "dataset"
module_description: "This dataset starts as external zip file backups from the sensing platform. The data then gets converted to raw parquet files, combined into a single merged file, and then cleaned."
module_name: "sensing_platform"
```

### Example `able_workflow/.copier-answers/module-dataset-weather.yml`

```yaml
module_type: "dataset"
module_description: "This dataset is queried from an API and saved to a raw parquet file"
module_name: "weather"
```

### Example `able_workflow/.copier-answers/module-feature-peaks.yml`

```yaml
module_type: "feature"
module_description: "This feature extracts all the sensor data during peak weather events."
module_name: "peaks"
```

## `able_workflow_etl_copier`

Template for adding an extract-transform-load (ETL) step to a module, and adding associated files throughout the project.

### `copier.able_workflow_etl_copier.yml`

```yaml
etl_name:
  type: "str"
  help: "The name of this ETL step. (Must be a valid python module name.)"
    validator: "^[a-zA-Z_][a-zA-Z0-9_]*$"
etl_description:
  type: "str"
  help: "Describe this ETL step in a sentence or two."
requires_extras:
  type: "bool"
  help: "Will the extraction, transformation, loading, or validation require especially large or strict python requirements that should be isolated from the rest of the package?"
parent_module:
  type: "str"
  help: "Select the module within the {{ package_name }} package to place this ETL step."
 # TODO implement choices that finds all the modules within `{{ package_name }}/{{ module_type }}/{{ module_name }}`.
extras_name:
  when: "{{ requires_extras }}"
  type: "str"
  help: "Provide a name for the group of extra dependencies (Must be a valid python variable name and should be unique within this package.)"
    validator: "^[a-zA-Z_][a-zA-Z0-9_]*$"
optional-dependencies:
  when: "{{ requires_extras }}"
  type: json
  help: "Provide a valid JSON list of extra packages and minimal versions required by this module. For example: `['openpyxl>=3.1.5']`"
```

### Resulting files of ETL step

The following files are added to the project

```txt
{{ project_name }}
├── .copier-answers/
│   └── .copier-answers.module-{{ module_type }}-{{ module_name }}-{{ etl_name }}.yml
│
├── config/
│   └── datasets/ OR features/ OR models/
│       └── {{ module_name }}/
│           └── {{ etl_name }}/
│               └── config.yaml
│
├── docs/
│   └── docs/
│       └── datasets/ OR features/ OR models/
│           └── {{ module_type }}/
│               └── {{ etl_name }}/
│                   ├── index.md
│                   └── SUMMARY.md
│
├── {{ package_name }}
│   └── datasets/ OR features/ OR models/
│       └── {{ module_name }}/
│           ├── {{ etl_name }}/  # IF {{ requires_extras }}
│           │   ├── extras_{{ extras_name }}/
│           │   │   ├── __init__.py
│           │   │   ├── extract_external.py
│           │   │   ├── load.py
│           │   │   ├── main.py
│           │   │   └── transform.py
│           │   ├── __init__.py
│           │   ├── extract.py
│           │   ├── schema.py
│           │   └── utils.py
│           └── {{ etl_name }}/  # IF NOT {{ requires_extras }}
│               ├── __init__.py
│               ├── extract.py
│               ├── extract_external.py
│               ├── load.py
│               ├── main.py
│               ├── schema.py
│               ├── transform.py
│               └── utils.py
│
├── tests/
│   └── {{ package_name }}/
│       └── datasets/ OR features/ OR models/
│           └── {{ module_name }}/
│               ├── {{ etl_name }}/  # IF {{ requires_extras }}
│               │   ├── extras_{{ extras_name }}/
│               │   │   ├── test_extract_external.py
│               │   │   ├── test_load.py
│               │   │   ├── test_main.py
│               │   │   └── test_transform.py
│               │   ├── test_extract.py
│               │   ├── test_schema.py
│               │   └── test_utils.py
│               └── {{ etl_name }}/  # IF NOT {{ requires_extras }}
│                   ├── test_extract.py
│                   ├── test_extract_external.py
│                   ├── test_load.py
│                   ├── test_main.py
│                   ├── test_schema.py
│                   ├── test_transform.py
│                   └── test_utils.py
│
└── workflow/
    └── rules/
        └── datasets/ OR features/ OR models/
            └── {{ etl_name }}.smk/
```

### Hypothetical `whole_energy_homes_interviews/weh_interviews/datasets/coding_matrix/raw.copier-answers.yml`

```yaml
etl_name: "raw"
etl_description: "Converts the interview coding matrix Excel spreadsheet into a validated parquet file"
requires_extras: "yes"
extras_name: "excel"
optional-dependencies:
  - "openpyxl>=3.1.5"
```
