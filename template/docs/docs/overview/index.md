# Package & Workflow

TODO-copier-package clean this up and make it generic to any `able-workflow-copier` project.

Welcome to the **WH Interviews** code‑base – an opinionated template for data‑centric Python projects that need a **repeatable ETL pipeline, isolated run‑time environments, and a fully typed, continuously‑tested code‑base**. The layout you see here was pioneered in the Automation for the Built and Living Environment (ABLE lab)[https://www.thisismikekane.com] and will be reused in several up‑coming repos. This page summarises the key concepts and opinions that drove the development of this template.

## Foundation opinions

This work started with a foundation and shared opinions of the [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/) project template:

1. Data analysis is a directed acyclic graph

   *Don't ever edit your raw data. Especially not manually. And especially not in Excel.*

2. Raw data is immutable

   *Data analysis is a directed acylcic graph (DAG)*

   - ✅ **Do** write code that moves the raw data through a pipeline to your final analysis.
   - ✅ **Do** serialize or cache the intermediate outputs of long-running steps.
   - ✅ **Do** make it possible (and ideally, documented and automated) for anyone to reproduce your final data products with only the code in {{ cookiecutter.module_name }} and the data in data/raw/ (and data/external/).
   - ⛔ **Don't** ever edit your raw data, especially not manually, and especially not in Excel. This includes changing file formats or fixing errors that might break a tool that's trying to read your data file.
   - ⛔ **Don't** overwrite your raw data with a newly processed or cleaned version.
   - ⛔ **Don't** save multiple versions of the raw data.

3. Data should (mostly) *not* be kept in source control

4. Notebooks are for exploration and communication, source files are for repetition

   *Source code is superior for replicability because it is more portable, can be tested more easily, and is easier to code review.*

5. Build from the environment up

6. Keep secrets and configuration out of version control

## Snakemake

Cookiecutter Data Science uses [GNU Make](https://www.gnu.org/software/make/) to determine the relationships between each analysis/modeling step with `rules` (e.g., run process `A` with inputs `x` and `y`) and `targets` (e.g., to produce output `z`). While `make` is the defacto standard for building software from a DAG of source files. However, you'll spend a longer time explaining its terse verses written in invisible white spaces than you will explain your machine-learning model to the next person working on your project.

**Snakemake** to the rescue: a workflow management system is a tool to create reproducible and scalable data analyses. Workflows are described via a human readable, Python based language. They can be seamlessly scaled to server, cluster, grid and cloud environments, without the need to modify the workflow definition. Snakemake workflows can entail a description of required software, which will be automatically deployed to any execution environment.

Snakemake's [common use cases](https://snakemake.github.io/snakemake-workflow-catalog/docs/workflows_by_stars.html) seem to imply that Snakemake was developed with the assumption that the data analsys and modeling processes executed by each `rule` can be succinctly written in a single [python script](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#python), in a Jupyter notebook (see opinion 4 above) and/or use standard domain specific command-line tools (e.g., [`bwa`](https://bio-bwa.sourceforge.net/bwa.shtml) for genomic analys.)

However, for exploratory data analysis and machine learning, each analysis step can be 100-1,000s of lines of custom code that should be well formatted, typed, and tested.

The "pure-snakemake" way to achieve this would be to keep your python source code and unit-tests [`https://www.github.com/YOUR_ORG/YOUR_PYTHON_PACKAGE`] and snakemake workflow and integration tests [`https://www.github.com/YOUR_ORG/YOUR_PYTHON_PACKAGE`] in separate git repositories. For every source code change you want to test while you simultaneously debug your source code and workflow, you have to do the following:

- Commit that change to the `YOUR_PYTHON_PACKAGE` repo
- Push it to GitHub
- Pull that into a separate project on your machine
- Run the test on your machine

This can become very tedious (and embarassing in public repositories) if you are debugging a missed comma or trying to understand an algorithm. While separating the python source code and snakemake workflow may be the ideal solution (similar to the separation of integrations and their communication wrappers in [Home Assistant integrations](https://developers.home-assistant.io/docs/development_checklist/)), an approach for faster development iterations is proposed.

## Big‑picture **architecture**

| Layer            | Tooling                                                          | What lives here                                                                                                                                                                                             | Why it matters                                                                                                         |
| ---------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Package**      | `weh_interviews/`                                                | Pure Python code that converts raw Excel sheets to tidy parquet. Extras (e.g. `runner`) hold _optional_ dependencies that are **only** needed for that sub‑module.                                          | Keeps the core install light and lets other repos depend on the parquet output without pulling in every heavy library. |
| **Workflow**     | **Snakemake**                                                    | Declarative DAG of ETL steps (each a rule). Every rule points at a dedicated _Conda_ YAML generated from _pyproject.toml_ so each step runs in the **minimal** environment it really needs.                 | Re‑running is deterministic, parallel, and cache‑aware. You never “just run a script”.                                 |
| **Environments** | `pyproject‑to‑conda`, `conda‑inject`, `snakemake conda localize` | Generates per‑rule YAMLs from the dependency **groups** defined in _pyproject.toml_. The `conda localize` helper then pip‑installs **your local clone** into each env so rules can `import weh_interviews`. | Makes CI and HPC jobs reproducible **without** uploading the package to PyPI/GH packages.                              |
| **Quality‑gate** | pre‑commit (Black, Ruff), MyPy, Pytest, Tox                      | Auto‑formatting, linting, type‑checking and unit tests. Tox spins up **matrix** envs so optional extras are tested as well.                                                                                 | You get immediate feedback locally and in CI before code lands on `main`.                                              |
| **Docs**         | MkDocs + mkdocstrings                                            | API reference is built from the type‑hinted docstrings, narrative docs live under `docs/`.                                                                                                                  | “Docs as code” – updated on every push.                                                                                |

## 2. Repository layout (top‑level)

```text
.
├── pyproject.toml          # single source‑of‑truth for ALL deps
├── workflow/               # Snakemake pipeline lives here
│   ├── Snakefile
│   ├── rules/
│   └── envs/               # auto‑generated YAMLs
├── weh_interviews/         # your actual Python package
│   ├── __init__.py
│   ├── extract.py          # light‑weight schema description
│   └── runner/             # optional Excel‑only code & deps
├── tests/                  # pytest suites (core & runner)
├── docs/                   # MkDocs site source
└── README.md               # quick‑start
```

### ETL Process Runtime Extras

Any sub‑package whose **runtime** requirements go beyond the core
(`openpyxl`, `xlrd`, heavy ML libs, …) lives in the `runner` folder.
Inside `pyproject.toml` those optional deps are declared under a
_dependency group_ of the **same name** so they can be installed
selectively:

```toml
[project.optional-dependencies]
excel = ["pandas>=2", "openpyxl"]
```

---

## 3. Getting started

```bash
# clone
git clone https://github.com/ABLE-Lab/wh-interviews.git
cd wh-interviews

# create base dev env (includes docs, linting, etc.)
micromamba create -n weh_dev python=3.12
micromamba activate weh_dev
pip install -e .[dev]

# one‑off → generate per‑rule envs *and* localise the package path
snakemake conda localize

# run the full ETL (4 cores here)
snakemake -j4 all
```

> **Tip:** When you switch branches or edit `pyproject.toml` remember to
> re‑run `snakemake conda localize` so every rule picks up the change.

---

## 4. Adding a new ETL step

1. Create a **function** that takes an **input path(s)** and produces an
    **output file** inside `weh_interviews/<new_module>/`.

2. Add a _dependency group_ for any new libraries in _pyproject.toml_.

3. Run `pyproject2conda project -f pyproject.toml --envs workflow`
    (or use the helper script) to regenerate the YAML for this step.

4. Write a **Snakemake rule** in `workflow/rules/<something>.smk`:

    ```snakemake
    rule parquetify_sensor_csv:
        input:  "data/raw/{sensor}.csv"
        output: "data/curated/{sensor}.parquet"
        conda:  "workflow/envs/py312-workflow-sensor.snakemake_conda.yaml"
        script: "workflow/scripts/rules/parquetify_sensor_csv.py"
    ```

5. Add **unit tests** under `tests/{new_module}/`.

6. `pre-commit run --all-files` should now pass; push and open a PR.


---

## 5. Development workflow & quality gates

- **Formatting / lint:** `black .` + `ruff .`

- **Static types:** `mypy --strict weh_interviews`

- **Unit tests:** `pytest -q`

- **Full matrix:** `tox` (runs core, `runner`, docs build, etc.)

- **Docs live‑reload:** `mkdocs serve`


All of the above (plus Snakemake’s DAG check) run automatically in CI
before a pull‑request can be merged.

---

## 6. FAQ

|Question|Answer|
|---|---|
|_Why not a single giant environment?_|Pinning the **minimal** deps per rule slashes cold‑start times on HPC / CI and avoids version conflicts across ETL stages.|
|_Do I have to learn Snakemake?_|Only for adding new stages. Day‑to‑day you usually type `snakemake -j`.|
|_Can I install everything at once?_|Sure: `pip install -e .[excel,dev,workflow]` but remember larger wheels = slower CI.|
|_Where does the data live?_|The DAG writes to `data/` relative to the repo root. Commit **code**, not data.|
|_What if `conda localize` fails?_|Make sure the env definition for that rule ends with `pip: -e .` and that your working directory is the repo root when you run the command.|

---

## 7. Next steps

_Skim through the generated `docs/` site (built from this file) and pull
open the **API Reference** tab – every public function in
`weh_interviews` is type‑hinted and documented with examples._

Happy hacking!
– The ABLE Lab tooling team
