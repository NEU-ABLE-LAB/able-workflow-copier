# ABLE Workflow Copier

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-purple.json)](https://github.com/copier-org/copier)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Common Changelog](https://common-changelog.org/badge.svg)](https://common-changelog.org)
[![codecov](https://codecov.io/gh/NEU-ABLE-LAB/able-workflow-copier/graph/badge.svg?token=8BX19PLPQ8)](https://codecov.io/gh/NEU-ABLE-LAB/able-workflow-copier)
[![tox Main Tests](https://github.com/NEU-ABLE-LAB/able-workflow-copier/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/NEU-ABLE-LAB/able-workflow-copier/actions/workflows/main.yml)

A [copier](https://copier.readthedocs.io/en/stable/) template for generating a snakemake workflow with an associated python package for implementing dataset transformation, feature extraction, and modeling.

## Overview of ABLE Workflow copier templates

- [`able-workflow-copier`]({{ able_workflow_copier_docs }})
- [`able-workflow-module-copier`]({{ able_workflow_module_copier_docs }})
- [`able-workflow-etl-copier`]({{ able_workflow_etl_copier_docs }})
- [`able-workflow-rule-copier`]({{ able_workflow_rule_copier_docs }})

## Contributing

### Environment configuration

The following instructions assume you are working on Linux (or with WSL on Windows) and have [conda](https://github.com/conda-forge/miniforge) and [vscode](https://code.visualstudio.com/download).

1. Check/install `conda`

   Check that you have conda installed:

   ```bash
   conda info
   ```

   You should see a list of parameters and values, which should include something like the following:

   ```bash
   base environment : /home/<USERNAME>/miniforge3
   ```

   If not, install [miniforge3](https://github.com/conda-forge/miniforge).

   1. Download miniforge

      ```bash
      wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
      ```

   2. Run the install script

      ```bash
      bash Miniforge3-$(uname)-$(uname -m).sh
      ```

      The interactive installation will prompt you to initialize conda with your shell. Do NOT do this if you are on a SLURM HPC. If you are on your personal computer it should be fine.

      TODO-copier-package point to docs for more info.

2. Install the recommended VSCode extensions for this project.:

   1. **Open the Command Palette**: On macOS: `Cmd+Shift+P` On Windows/Linux: `Ctrl+Shift+P`.

   2. **Show recommended extensions**: Type and select `> Extensions: Show Recommended Extensions`

   3. Click the Install button for each recommended extension listed above.

3. Create a development environment with conda

   ```bash
   # Create the environment (or update and prune if it already exists)
   conda env update --name able-workflow-copier --file environment-py312-dev.yaml --prune
   conda activate able-workflow-copier
   ```

   Alternatively, run the script `scripts/conda_update.sh`.

   Configure the `able-workflow-copier` as the default python environment in the [Python Environments VSCode extension](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-python-envs).

4. Install pre-commit into the repo to run checks on every commit

   ```bash
   (able-workflow-copier) pre-commit install
   ```

5. Play around in the sandbox. (The `sandbox/` directory is in `.gitignore` and is a good place to explore how to use the template.)

   ```bash
   copier copy --trust --vcs-ref HEAD --pretend "./" "sandbox/example"
   ```

   - `--trust`: Required to run this "untrusted" `copier` template under development.
   - `--vcs-ref HEAD`: Use the `HEAD` of the git repo, not a tagged release version.
   - `--pretend`: Do not modify any files, just ask the questions.
   - `"./"`: The `copier.yaml` file is located in the current directory. When working in production, this will be replaced with the github link to `able-workflow-copier`.
   - `"sandbox/example"`: The directory to place the rendered template, if we were not pretending.
