
# 🪟 Windows 10/11 + WSL 2 installation

The recommended Windows workflow is **WSL 2** running Ubuntu.
This keeps a single POSIX code‑base across all platforms and avoids
maintaining separate Windows‑specific scripts.

Follow the steps below, then return to [set‑up index](index.md).

## 1.  Enable WSL 2 with Ubuntu

Open an *elevated* PowerShell and execute:

```powershell
wsl --install
```

Reboot when prompted, then launch “Ubuntu” from the Start menu and
create your UNIX username.

## 2.  Inside the WSL shell

```bash
# ①  Clone on the native ext4 file‑system, not /mnt/c
git clone {{ repository_url }}.git
cd {{ project_name }}
```

## 3.  Install Miniforge + Mamba

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
conda config --set solver libmamba
conda config --set channel_priority strict
conda install -n base -c conda-forge mamba conda-libmamba-solver
```

That completes the Windows‑specific portion.
Jump back to the main guide for the universal post‑install steps.
