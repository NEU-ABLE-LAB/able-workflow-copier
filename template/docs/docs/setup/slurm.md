
# ⚡ SLURM cluster installation (NEU Discovery & friends)

These instructions assume you launch VS Code through **Open OnDemand**
(OOD) and use the bundled **workflow/profiles/slurm** profile.

> **TODO‑copier‑package:** Customize partition, account and e‑mail
> settings inside `workflow/profiles/slurm/config.yaml`.

## 1  Start a VS Code session via OOD

1. Log into your institution’s OOD portal and choose

   **VS Code Server Interactive Session**.

2. Suggested settings (adjust as needed):

    | Field     | Value      |
    | --------- | ---------- |
    | Partition | `short`    |
    | Wall‑time | `08:00:00` |
    | CPUs      | `4`        |
    | Memory    | `32G`      |

3. Press **Launch** and wait for the “Connect” button.

## 2  First‑time repository clone

Inside the VS Code terminal:

```bash
cd ~
git clone {{ repository_url }}.git
````

Subsequent sessions only need `git pull`.

## 3  Miniforge + environment

```bash
# One‑time install
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh   # choose a path in $HOME
```

### (Optional) keep rule envs local to $HOME

Run the following if the directory you are working in starts with `/mount/c/`

```bash
echo 'export SNAKEMAKE_CONDA_PREFIX=$HOME/.snakemake/conda' >> ~/.bashrc
```

All cluster‑independent tasks (e.g. pre‑commit, running the pipeline,
generating docs) are detailed in the [set‑up index](index.md).

Finish there once the environment solves successfully.
