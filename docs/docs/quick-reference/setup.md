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

### Install [miniforge3](https://github.com/conda-forge/miniforge)

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

### Create the conda environment from the raw environment file URL

You can create the development environment directly from the raw GitHub URL:

```bash
conda env create --name able-workflow-copier --file "https://raw.githubusercontent.com/NEU-ABLE-LAB/able-workflow-copier/refs/heads/main/environment-py312-dev.yaml"
```

If you prefer to keep a local copy of the environment file, download it first:

```bash
wget -O environment-py312-dev.yaml "https://raw.githubusercontent.com/NEU-ABLE-LAB/able-workflow-copier/refs/heads/main/environment-py312-dev.yaml"
```

### Create environment

If the environment already exists, update and prune it with the local file:

```bash
conda env update --name able-workflow-copier --file environment-py312-dev.yaml --prune
```

### Activate the environment

```bash
conda activate able-workflow-copier
```
