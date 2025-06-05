# ABLE Workflow Copier

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

    Configure the `able-workflow-copier-dev` as the default python environment in the [Python Environments VSCode extension](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-python-envs).

3. Install pre-commit into the repo to run checks on every commit

   ```bash
   (able-workflow-copier-dev) pre-commit install
   ```
