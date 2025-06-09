# ABLE Workflow Copier

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-purple.json)](https://github.com/copier-org/copier)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A [copier](https://copier.readthedocs.io/en/stable/) template for generating a snakemake workflow with an associated python package for implementing dataset transformation, feature extraction, and modeling.

## Contributing

### Environment configuration

The following instructions assume you are working on Linux (or with WSL on Windows) and have [conda](https://github.com/conda-forge/miniforge) and [vscode](https://code.visualstudio.com/download).

1. Install the recommended VSCode extensions for this project.:

   1. **Open the Command Palette**: On macOS: `Cmd+Shift+P` On Windows/Linux: `Ctrl+Shift+P`.

   2. **Show recommended extensions**: Type and select `> Extensions: Show Recommended Extensions`

   3. Click the Install button for each recommended extension listed above.

2. Create a development environment with conda

    ```bash
    # Create the environment (or update and prune if it already exists)
    conda env update --name able-workflow-copier-dev --file environment-py312-dev.yaml --prune
    conda activate able-workflow-copier-dev
    ```

    Alternatively, run the script `scripts/conda_update.sh`.

    Configure the `able-workflow-copier-dev` as the default python environment in the [Python Environments VSCode extension](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-python-envs).

3. Install pre-commit into the repo to run checks on every commit

   ```bash
   (able-workflow-copier-dev) pre-commit install
   ```

4. Play around in the sandbox. (The `sandbox/` directory is in `.gitignore` and is a good place to explore how to use the template.)

   ```bash
   copier copy --trust --vcs-ref HEAD --pretend "./" "sandbox/example"
   ```

   - `--trust`: Required to run this "untrusted" `copier` template under development.
   - `--vcs-ref HEAD`: Use the `HEAD` of the git repo, not a tagged release version.
   - `--pretend`: Do not modify any files, just ask the questions.
   - `"./"`: The `copier.yaml` file is located in the current directory. When working in production, this will be replaced with the github link to `able-workflow-copier`.
   - `"sandbox/example"`: The directory to place the rendered template, if we were not pretending.
