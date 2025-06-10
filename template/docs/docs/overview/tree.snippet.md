### Copier templates variables

Copier uses a jinja2 syntax for rendering templates with the answers to the templates questions.

- [`able-workflow-copier` template](https://github.com/NEU-ABLE-LAB/able-workflow-copier-dev)
  - **`{{ project_name }}`**: The name of the project being created.
  - **`{{ package_name }}`**: The name of the Python package being created.

- [`able-workflow-module-copier` template](https://github.com/NEU-ABLE-LAB/able-workflow-module-copier-dev)
  - **`{{ module_type }}`**: The type of module being created (e.g., `datasets`, `features`, or `models`).
  - **`{{ module_name }}`**: The name of the module being created.

- [`able-workflow-etl-copier` template](https://github.com/NEU-ABLE-LAB/able-workflow-etl-copier-dev)
  - **`{{ etl_name }}`**: The name of the ETL process being created.
  - **`{{ requires_extras }}`**: Whether the ETL requires extra dependencies (boolean).
  - **`{{ extras_name }}`**: The name of the extras package (if `requires_extras` is `true`).
  - **`{{ conda_env_key }}`**: The key for the Conda environment from the workflow config (e.g., `config["CONDA"]["ENVS"]["{{ conda_env_key }}"]`).

- [`able-workflow-rule-copier` template](https://github.com/NEU-ABLE-LAB/able-workflow-rule-copier-dev)
  - **`{{ is_package_rule }}`**: The rule uses the package.
  - **`{{ rule_name }}`**: The name of the Snakemake rule being created

### Directory tree

Files that are created by a template are marked with a `+` sign, and files that are created by a Copier template are marked with a `*` sign. The tree structure is as follows:

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
Legend ── “+” = created | “*” = modified | blank = untouched
    {{ project_name }}
    │
 +  ├── .copier-answers/
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
+   │   └── README.md
 +* │   └── {{ module_name }}/                    # dataset only
 +* │       ├── external/
 +* │       ├── interim/
 +* │       ├── processed/
 +* │       ├── raw/
 +* │       └── README.md
    │
+   ├── docs/
+   │   ├── docs/
+   │   │   ├── _css/           … (static scaffold — created by project template)
    │   │   │
    │   │   ├── datasets/
 +  │   │   │   └── {{ module_type }}/            # dataset docs
 +  │   │   │       ├── index.md
 +  │   │   │       └── SUMMARY.md
    │   │   │
    │   │   ├── features/
 +  │   │   │   └── {{ module_type }}/            # feature docs
 +  │   │   │       ├── index.md
 +  │   │   │       └── SUMMARY.md
    │   │   │
    │   │   ├── models/
 +  │   │   │   └── {{ module_type }}/            # model docs
 +  │   │   │       ├── index.md
 +  │   │   │       └── SUMMARY.md
    │   │   └── weh.md
+   │   ├── gen_ref_pages.py
+   │   ├── mkdocs.yml
+   │   └── README.md
+   ├── hooks/
+   │   └── snakemake_pyproject2conda.py
+   ├── features/
+   │   └── README.md
 +  │   └── {{ module_name }}/README.md           # if feature module
+   ├── logs/rules/
+   │   └── README.md
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
+   ├── {{ package_name }}/
+   │   ├── datasets/
+   │   │   └── __init__.py
 +  │   │   └── {{ module_name }}/__init__.py     # dataset Python entry-point
+   │   ├── features/
+   │   │   └── __init__.py
 +  │   │   └── {{ module_name }}/__init__.py
+   │   ├── models/
+   │   │   └── __init__.py
 +  │   │   └── {{ module_name }}/__init__.py
+   │   ├── utils/
+   │   │   ├── __init__.py
+   │   │   └── logging.py
+   │   ├── __init__.py
+   │   └── config.py
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
+   │           ├── rules/
+   │           │   ├── test_conda_localize_file.py
+   │           │   └── test_pyproject2conda.py
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
+   ├── snakefmt.toml # (1)
+   └── tox.ini # (2)
```

1. Hello
2. World
