# Development Environment Setup

The following instructions assume you are working on Linux (or with WSL on Windows) and have [conda](https://github.com/conda-forge/miniforge) and [vscode](https://code.visualstudio.com/download).

## Check/install `conda`

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

## Install recommended VSCode extensions

1. **Open the Command Palette**: On macOS: `Cmd+Shift+P` On Windows/Linux: `Ctrl+Shift+P`.

2. **Show recommended extensions**: Type and select `> Extensions: Show Recommended Extensions`

3. Click the Install button for each recommended extension listed above.

At minimum, install extensions for Python, YAML, Markdown, and GitHub Actions editing.

## Set up VS Code profile and multi-root workspace

1. Open Command Palette and create/switch to a dedicated profile (for example, `ABLE Copiers`).
2. Clone each copier repository into sibling folders (not nested submodules).
3. In VS Code, run `File: Add Folder to Workspace...` and add each repository folder.
4. Save the workspace as a `.code-workspace` file (for example, `able-workflow-copiers.code-workspace`).
5. In profile settings, set the default Python environment for each workspace folder as needed.

Example folder set:

- `../able-workflow-copier`
- `../able-workflow-module-copier`
- `../able-workflow-etl-copier`
- `../able-workflow-rule-copier`

## Create development environment with conda

```bash
# Create the environment (or update and prune if it already exists)
conda env update --name able-workflow-copier --file environment-py312-dev.yaml --prune
conda activate able-workflow-copier
```

Alternatively, run the script `scripts/conda_update.sh`.

Configure the `able-workflow-copier` as the default python environment in the [Python Environments VSCode extension](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-python-envs).

## Install pre-commit

```bash
(able-workflow-copier) pre-commit install
```

## Use the sandbox

The `sandbox/` directory is in `.gitignore` and is a good place to explore how to use the template.

```bash
copier copy --trust --vcs-ref HEAD --pretend "./" "sandbox/example"
```

- `--trust`: Required to run this "untrusted" `copier` template under development.
- `--vcs-ref HEAD`: Use the `HEAD` of the git repo, not a tagged release version.
- `--pretend`: Do not modify any files, just ask the questions.
- `"./"`: The `copier.yaml` file is located in the current directory. When working in production, this will be replaced with the github link to `able-workflow-copier`.
- `"sandbox/example"`: The directory to place the rendered template, if we were not pretending.
