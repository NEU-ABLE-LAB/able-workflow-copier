# 🐧 Native Linux / macOS installation

This page covers the **initial** steps needed to get the repository
running on a UNIX‑like workstation.

Once finished, return to the [set‑up index](index.md) for the common
post‑install commands.

## Prerequisites

```bash
# Basic developer tool‑chain – adapt for your distro
sudo apt update && sudo apt install -y git build-essential curl wget
```

## 1  Clone the repository

```bash
git clone {{ repository_url }}.git
cd {{ repo_name }}
```

## 2  Install Miniforge + Mamba

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh   # accept defaults + auto‑init
conda config --set solver libmamba
conda config --set channel_priority strict
conda install -n base -c conda-forge mamba conda-libmamba-solver
```

That’s **it** for the platform specifics – head back to the
top‑level guide to finish up.
