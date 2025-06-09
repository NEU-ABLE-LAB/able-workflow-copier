# Package & Workflow

TODO-copier-package clean this up and make it generic to any `able-workflow-copier` project.

Welcome to the **WH Interviews** code‑base – an opinionated template for data‑centric Python
projects that need a **repeatable ETL pipeline, isolated run‑time environments, and a fully
typed, continuously‑tested code‑base**.
The layout you see here was pioneered in Michael Kane’s lab and will be reused in several
up‑coming repos (e.g. _maharshi‑analysis_).
This page summarises the key ideas Michael presented on the recorded call and should help
new contributors get productive quickly.

---

## Big‑picture architecture

|Layer|Tooling|What lives here|Why it matters|
|---|---|---|---|
|**Package**|`weh_interviews/`|Pure Python code that converts raw Excel sheets to tidy parquet. Extras (e.g. `extras_excel`) hold _optional_ dependencies that are **only** needed for that sub‑module.|Keeps the core install light and lets other repos depend on the parquet output without pulling in every heavy library.|
|**Workflow**|**Snakemake**|Declarative DAG of ETL steps (each a rule). Every rule points at a dedicated _Conda_ YAML generated from _pyproject.toml_ so each step runs in the **minimal** environment it really needs.|Re‑running is deterministic, parallel, and cache‑aware. You never “just run a script”.|
|**Environments**|`pyproject‑to‑conda`, `conda‑inject`, `snakemake conda localize`|Generates per‑rule YAMLs from the dependency **groups** defined in _pyproject.toml_. The `conda localize` helper then pip‑installs **your local clone** into each env so rules can `import weh_interviews`.|Makes CI and HPC jobs reproducible **without** uploading the package to PyPI/GH packages.|
|**Quality‑gate**|pre‑commit (Black, Ruff), MyPy, Pytest, Tox|Auto‑formatting, linting, type‑checking and unit tests. Tox spins up **matrix** envs so optional extras are tested as well.|You get immediate feedback locally and in CI before code lands on `main`.|
|**Docs**|MkDocs + mkdocstrings|API reference is built from the type‑hinted docstrings, narrative docs live under `docs/`.|“Docs as code” – updated on every push.|

---

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
│   └── extras_excel/       # optional Excel‑only code & deps
├── tests/                  # pytest suites (core & extras)
├── docs/                   # MkDocs site source
└── README.md               # quick‑start
```

### Extras pattern

Any sub‑package whose **runtime** requirements go beyond the core
(`openpyxl`, `xlrd`, heavy ML libs, …) lives in a folder that starts with
`extras_`.
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

- **Full matrix:** `tox` (runs core, `extras_excel`, docs build, etc.)

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
