# Project directory tree

## Copier templates variables

Copier uses a jinja2 syntax for rendering templates with the answers to the templates questions.

- [`able-workflow-copier`]({{ able_workflow_copier_docs }})

- [`able-workflow-copier` template]({{ able_workflow_copier_docs }})
  - **`{{ project_name_slug }}`**: The name of the project being created.
  - **`{{ package_name }}`**: The name of the Python package being created.

- [`able-workflow-module-copier` template]({{ able_workflow_module_copier_docs }})
  - **`{{ module_type }}`**: The type of module being created (e.g., `datasets`, `features`, or `models`).
  - **`{{ module_name }}`**: The name of the module being created.

- [`able-workflow-etl-copier` template]({{ able_workflow_etl_copier_docs }})
  - **`{{ etl_name }}`**: The name of the ETL process being created.
  - **`{{ requires_extras }}`**: Whether the ETL requires extra dependencies (boolean).
  - **`{{ extras_name }}`**: The name of the extras package (if `requires_extras` is `true`).
  - **`{{ conda_env_key }}`**: The key for the Conda environment from the workflow config (e.g., `config["CONDA"]["ENVS"]["{{ conda_env_key }}"]`).

- [`able-workflow-rule-copier` template]({{ able_workflow_rule_copier_docs }})
  - **`{{ is_package_rule }}`**: The rule uses the package.
  - **`{{ rule_name }}`**: The name of the Snakemake rule being created

## Directory tree

Files that are created by a template are marked with a `+` sign, and files that are created by a Copier template are marked with a `*` sign. The tree structure is as follows:

```.yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
Legend ── “+” = created | “*” = modified | blank = untouched
    {{ project_name_slug }}
    │
 +  ├── .copier-answers/ # (3)
 +  │   ├── module-{{ module_type }}-{{ module_name }}.yml
  + │   ├── etl-{{ module_type }}-{{ module_name }}-{{ etl_name }}.yml
   +│   └── rule-{{ module_type }}-{{ module_name }}-{{ rule_name }}.yml
    │
+   ├── .github/
+   │   ├── ISSUE_TEMPLATE/
  + │   │   ├── post-copier-etl.md
 +  │   │   ├── post-copier-module.md
+   │   │   ├── post-copier-package.md
   +│   │   └── post-copier-rule.md
+   │   └── workflows/
+   │       ├── build.yml
+   │       ├── ci.yml
+   │       └── release.yml
    │
+   ├── .vscode/
+   │   ├── extensions.json
+ * │   ├── launch.json
+  *│   └── settings.json
    │
+   ├── config/
+   │   ├── config.yaml
+   │   ├── config.local.example.yaml
+   │   ├── README.md
+   │   ├── datasets/
 +  │   │   └── {{ module_name }}/                # if {{ module_type }} == dataset
 +* │   │       └── config.yaml                   # +: module, *: etl tweaks
+   │   ├── features/
 +  │   │   └── {{ module_name }}/                # if {{ module_type }} == feature
 +* │   │       └── config.yaml
+   │   └── models/
 +  │       └── {{ module_name }}/                # if {{ module_type }} == model
 +* │           └── config.yaml
    │
+   ├── data/
+   │   ├── README.md
 +* │   └── {{ module_name }}/                    # dataset only
 +* │       ├── external/  # (12)
 +* │       ├── interim/  # (13)
 +* │       ├── processed/  # (14)
 +* │       ├── raw/  # (15)
 +* │       └── README.md
    │
+   ├── docs/
+   │   ├── docs/
+   │   │   ├── _css/
+   │   │   ├── _images/
+   │   │   ├── _js/
    │   │   │
    │   │   ├── datasets/
 +  │   │   │   └── {{ module_type }}/
 +  │   │   │       ├── index.md
 +  │   │   │       └── SUMMARY.md
    │   │   │
    │   │   ├── features/
 +  │   │   │   └── {{ module_type }}/
 +  │   │   │       ├── index.md
 +  │   │   │       └── SUMMARY.md
    │   │   │
    │   │   ├── models/
 +  │   │   │   └── {{ module_type }}/
 +  │   │   │       ├── index.md
 +  │   │   │       └── SUMMARY.md
    │   │   │
    │   │   ├── index.md
    │   │   ├── getting-started.md
    │   │   └── SUMMARY.md
    │   │
+   │   ├── gen_ref_pages.py
+   │   ├── mkdocs.yml
+   │   └── README.md
    │
+   ├── hooks/
+   │   └── snakemake_pyproject2conda.py
    │
+   ├── features/
+   │   └── README.md
 +  │   └── {{ module_name }}/README.md           # if feature module
    │
+   ├── logs/rules/
+   │   └── README.md
    │
+   ├── models/
+   │   └── README.md
 +  │   └── {{ module_name }}/README.md           # if model module
+   ├── notebooks/
+   │   └── README.md
+   ├── references/
+   │   └── README.md
+   ├── reports/
+   │   ├── datasets/
+   │   │   └── .gitkeep
 +  │   │   └── {{ module_name }}/README.md       # dataset report stub
+   │   ├── features/
+   │   │   └── .gitkeep
 +  │   │   └── {{ module_name }}/README.md       # feature report stub
+   │   ├── models/
+   │   │   └── .gitkeep
 +  │   │   └── {{ module_name }}/README.md       # model report stub
+   │   └── notebook_templates/
+   │       ├── datasets/
 +  │       │   └── {{ module_name }}/README.md
+   │       ├── features/
 +  │       │   └── {{ module_name }}/README.md
+   │       └── models/
 +  │           └── {{ module_name }}/README.md
    │
+   ├── {{ package_name }}/
    │   │
+   │   ├── datasets/
 +  │   │   ├── {{ module_name }}/
    │   │   │   ├── {{ etl_name }}.py
    │   │   │   │   ├── extras/
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
+   │   │   └── __init__.py
    │   │
+   │   ├── features/
 +  │   │   ├── {{ module_name }}/
    │   │   │   ├── {{ etl_name }}.py
    │   │   │   │   ├── extras/
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
+   │   │   └── __init__.py
    │   │
+   │   ├── models/
 +  │   │   ├── {{ module_name }}/
    │   │   │   ├── {{ etl_name }}.py
    │   │   │   │   ├── extras/
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
+   │   │   └── __init__.py
    │   │
+   │   ├── utils/
+   │   │   ├── __init__.py
+   │   │   └── logging.py
    │   │
+   │   ├── __init__.py
+   │   └── config.py
    │
+   ├── tests/
+   │   ├── docs/
+   │   │   └── test_dag.py
+   │   ├── {{ package_name }}/
+   │   │   ├── datasets/.gitkeep
+   │   │   ├── features/.gitkeep
+   │   │   ├── models/.gitkeep
+   │   │   ├── utils/.gitkeep
+   │   │   └── README.md
+   │   └── worflow/
+   │       ├── rules/
+   │       │   ├── conftext.py
+   │       │   └── README.md
+   │       └── scripts/
+  +│           ├── rules_conda_{{ conda_env_key }}/ # (6)
+   │           ├── rules_conda_CORE/ # (10)
+   │           ├── rules_conda_DOCS/ # (5)
+   │           ├── rules_global/ # (4)
+   │           │   ├── test_conda_localize_file.py
+   │           │   └── test_pyproject2conda.py
+   │           ├── utils/
+   │           └── README.md
+   ├── workflow/
+   │   ├── envs/
+   │   │   ├── localized/
+   │   │   ├── pyproject2conda/
+   │   │   ├── py312-tox.yaml
+   │   │   └── py312-workflow.yaml
+   │   ├── profiles/
+   │   │   ├── default/config.yaml
+   │   │   └── slurm/
+   │   ├── rules/
+   │   │   ├── datasets/
 +  │   │   │   └── {{ module_name }}/README.md   # dataset rules stub
+   │   │   ├── features/
 +  │   │   │   └── {{ module_name }}/README.md
+   │   │   ├── models/
 +  │   │   │   └── {{ module_name }}/README.md
+   │   │   ├── build.smk
+   │   │   ├── dev.smk
+   │   │   ├── docs.smk
+   │   │   ├── includes.smk  # (18)
+   │   │   ├── reports.smk
+   │   │   └── utils.smk
+   │   ├── schemas/
+   │   │   ├── datasets/
 +  │   │   │   └── {{ module_name }}/README.md
+   │   │   ├── features/
 +  │   │   │   └── {{ module_name }}/README.md
+   │   │   ├── models/
 +  │   │   │   └── {{ module_name }}/README.md
+   │   │   ├── config.schema.json
+   │   │   └── config.local.schema.json
+   │   ├── scripts/
+  +│   │   ├── rules_conda_{{ conda_env_key }}/ # (7)
+   │   │   ├── rules_conda_CORE/ # (11)
+   │   │   ├── rules_conda_DOCS/ # (8)
+   │   │   ├── rules_global/ # (9)
+   │   │   ├── rules/
+   │   │   │   ├── __init__.py
+   │   │   │   ├── conda_localize_file.py
+   │   │   │   ├── dag_svg.py
+   │   │   │   ├── pyproject2conda.py
+   │   │   │   └── weh_interviews_rules.py
+   │   │   └── utils/
+   │   │       ├── __init__.py
+   │   │       └── config_loader.py
+   │   └── Snakefile
+   ├── .env.example
+   ├── .copier-answers.yml
+   ├── .gitattributes
+   ├── .gitignore
+   ├── .pre-commit-config.yaml
+   ├── AGENTS.md
+   ├── CHANGELOG.md
+   ├── codecov.yml
+   ├── LICENSE
+   ├── pyproject.toml
+   ├── README.md
+   ├── snakefmt.toml # (16)
+   └── tox.ini # (17)
```

1. _
2. _
3. The copier answers files get stored here from each template applied to the project.
4. Tests for rule scripts that can run in the Snakemake global conda environment.
5. Tests for rule scripts that require the `config["CONDA"]["ENVS"]["DOCS"]` conda environment.
6. Tests for rule scripts that require the `config["CONDA"]["ENVS"]["{{ conda_env_key }}"]` conda environment.
7. Rule scripts that require the `config["CONDA"]["ENVS"]["{{ conda_env_key }}"]` conda environment.
8. Rule scripts that require the `config["CONDA"]["ENVS"]["DOCS"]` conda environment.
9. Rule scripts that can run in the Snakemake global conda environment.
10. Tests for rule scripts that require the {{ package_name }} core conda environment, `config["CONDA"]["ENVS"]["DOCS"]`.
11. Rule scripts that require the {{ package_name }} core conda environment, `config["CONDA"]["ENVS"]["DOCS"]`.
12. Data copied from an external source in a non-standard format. This folder may be a symlink to another location on disk.
13. Temporary data storage for intermediate workflow steps.
14. Processed data ready for reporting, feature extraction, or modeling.
15. Raw data in a standardized format.
16. Configuration settings for snakemake formatting
17. Main tox settings for resting template creation and code within generated example templates.
18. A singe file to aggregate all the includes.
