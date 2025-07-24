# Whitespace

TODO-copier-package add intro about why we care about the whitespace. Say how this project was created with `able-workflow-copier` to address the elements of this whitespace.

## Comparative Table: Projects and Their Tooling Practices

| Project & Link                                                                                | Description                                                 | Snakemake      | Pandera        | Template | Conda | HPC / Container                | Flat Files       | Open Data | mypy | Ruff / Black | tox | GH Actions |
| --------------------------------------------------------------------------------------------- | ----------------------------------------------------------- | -------------- | -------------- | -------- | ----- | ------------------------------ | ---------------- | --------- | ---- | ------------ | --- | ---------- |
| [**Mutator Mapping** (eLife, 2024)](https://github.com/arq5x/mutator_mapping)                 | Germline mutation pipeline using Snakemake + Pandera.       | ✅              | ✅              | ❌        | ❌     | ❌                              | ✅ (TSV/CSV)      | ❌         | ❌    | ❌            | ❌   | ✅          |
| [**CapCruncher** (Simpson Lab, 2023)](https://github.com/simpsonlab/CapCruncher)              | HPC-ready Capture-C analysis. Snakemake + Pandera, PyArrow. | ✅              | ✅              | ❌        | ✅     | ✅ (SLURM / Singularity)        | ✅                | ❌         | ❌    | ✅            | ❌   | ✅          |
| [**VPMBench** (BMC Bioinfo, 2021)](https://github.com/fmfi-genom/vpmbench)                    | Variant prioritization benchmarking suite.                  | ✅              | ✅              | ❌        | ✅     | ✅ (Docker)                     | ✅ (CSV/VCF)      | ❌         | ❌    | ❌            | ❌   | ❌          |
| [**aPhyloGeo-COVID** (SciPy, 2023)](https://github.com/latlab/aPhyloGeo)                      | SARS-CoV-2 phylogeography platform w/ Pandera + Snakemake.  | ✅              | ✅              | ❌        | ❌     | ✅                              | ✅ (CSV/FASTA)    | ❌         | ❌    | ✅            | ❌   | ✅          |
| [**SeqNado** (Milne Lab, 2025)](https://github.com/milne-lab/seqnado)                         | NGS workflow using Snakemake + Pandera + SLURM.             | ✅              | ✅              | ✅        | ✅     | ✅                              | ✅                | ❌         | ❌    | ✅            | ❌   | ✅          |
| [**Cookiecutter Data Snake**](https://github.com/martibosch/cookiecutter-data-snake)          | Cookiecutter Snakemake pipeline template w/ pre-commit.     | ✅              | ❌              | ✅        | ✅     | ✅                              | ✅ (user defined) | ❌         | ❌    | ✅            | ✅   | ✅          |
| [**Kedro** (QuantumBlack)](https://github.com/kedro-org/kedro)                                | Python ML pipeline framework with cataloging & CLI.         | ❌ (Own engine) | ✅ (via plugin) | ✅        | ✅     | ✅ (Docker, plugin-based SLURM) | ✅                | ❌         | ❌    | ✅            | ❌   | ✅          |
| [**Simpson Lab Template**](https://github.com/simpsonlab/snakemake-template)                  | Cookiecutter template for bioinformatics workflows.         | ✅              | ❌              | ✅        | ✅     | ◐ (User-added SLURM profile)   | ✅                | ❌         | ❌    | ❌            | ❌   | ❌          |
| [**Bibat** (2024)](https://github.com/timgroves/bibat)                                        | Bayesian analysis template w/ Pandera + Copier + Make.      | ❌ (Make)       | ✅              | ✅        | ❌     | ❌                              | ✅                | ❌         | ❌    | ✅            | ❌   | ✅          |
| [**MLOps Python Template**](https://github.com/FrancescoMind/machine-learning-template)       | Python ML template using Pandera, Ruff, Docker, mypy.       | ❌              | ✅              | ✅        | ✅     | ✅ (Docker)                     | ✅ (Parquet)      | ❌         | ✅    | ✅            | ❌   | ✅          |
| [**Cookiecutter Data Science** (v2)](https://github.com/drivendata/cookiecutter-data-science) | Popular DS project structure template (Make, no Snakemake). | ◐ (Make)       | ❌              | ✅        | ✅     | ◐ (Docker optional)            | ✅                | ❌         | ❌    | ✅            | ✅   | ❌          |
| [**Khuyen Tran Template**](https://github.com/khuyentran1401/data-science-template)           | Modern DS template (Hydra, DVC, Poetry, Pandera optional).  | ❌ (DVC)        | ❌              | ✅        | ❌     | ❌                              | ✅                | ❌         | ✅    | ✅            | ❌   | ❌          |

---

## Whitespace: Gaps in Adoption and What They Cost

Not every project needs all of the tools listed above. But too many projects skip most of them. Across many open-source and academic workflows, we still see long scripts that assume too much, notebooks with no tests, and no easy way to rerun or scale the work. This isn’t just about preference—it affects trust. If a model can’t be retrained or rerun, it’s hard to be confident in the conclusions. If a pipeline fails silently when upstream data changes, teams waste time chasing bugs. And if CI isn’t in place, small changes can break downstream results without warning.

Adoption of validation (like Pandera) and type-checking (like mypy) remains particularly sparse. These tools provide early warnings about problems that are otherwise easy to miss. Similarly, while Snakemake is growing in popularity, many pipelines still rely on manual scripts or stitched-together notebooks, which make reproducibility harder. Data sharing practices also lag behind—few projects publish intermediate or final outputs to open repositories, which means even if the pipeline is solid, the outputs aren’t always easy to verify.

This leaves a lot of room for improvement—and opportunity. Templates that bake in best practices can help new projects get started on the right foot. Pipelines that combine validation, workflows, CI, and environment isolation reduce technical debt and make collaboration easier. Teams that invest in these foundations spend less time debugging and more time delivering value. It’s not about compliance; it’s about working smarter.

And the bar isn’t that high. A `pyproject.toml` with Ruff and Black, a `tox.ini` with a basic test suite, and a GitHub Actions file to run them—those three files alone change the trajectory of a project. Add Snakemake, Pandera, and environment pinning, and you’ve got a pipeline that others can run, inspect, and trust. The goal isn’t to make things complicated. The goal is to make the important parts easy to understand and hard to break.

## Additional projects

- [Automatic Reproduction of Workflows in the Snakemake Workflow Catalog and nf-core Registries](https://dl.acm.org/doi/10.1145/3589806.3600037)
- [clio](https://clio.readthedocs.io/en/stable/): Uses `snakemake` but abstracts the interface to their own custom interface
  - [module_hydropower](https://github.com/calliope-project/module_hydropower)
  - [module_geo_boundaries](https://github.com/calliope-project/module_geo_boundaries)
  - [data-module-template](https://github.com/calliope-project/data-module-template)
