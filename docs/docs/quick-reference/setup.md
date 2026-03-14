# Environment Setup for Running Copier

The following instructions assume you are working on Linux (or with WSL on Windows) and have [conda](https://github.com/conda-forge/miniforge) and [vscode](https://code.visualstudio.com/download).

## Check/install `conda`

### Check that you have conda installed

   ```bash
   conda info
   ```

   You should see a list of parameters and values, which should include something like the following:

   ```bash
   base environment : /home/<USERNAME>/miniforge3
   ```

### Install [miniforge3](https://github.com/conda-forge/miniforge).

#### Download miniforge

      ```bash
      wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
      ```

#### Run the install script

      ```bash
      bash Miniforge3-$(uname)-$(uname -m).sh
      ```

      The interactive installation will prompt you to initialize conda with your shell. Do NOT do this if you are on a SLURM HPC. If you are on your personal computer it should be fine.

## Create a development environment with conda

### Create project directory

   Create the directory where you want to create your project

   ```bash
   mkdir my_project
   ```

### Downloan conda environment file

   Download the [environment YAML file]({{able_workflow_copier_repo }}/blob/main/environment-py312-dev.yaml) and move it into the project directory. (Alternatively, clone the entire [able-workflow-copier repository]({{ able_workflow_copier_repo }}) and copy `environment-py312-dev.yaml` into the new project directory.)

### Create environment

   Create the environment (or update and prune if it already exists)

   ```bash
   conda env update --name able-workflow-copier --file environment-py312.yaml --prune
   ```

### Activate the environment

   ```bash
   conda activate able-workflow-copier
   ```
