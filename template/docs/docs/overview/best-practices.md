# Best Practices this Project Implements

The following practices provide a solid foundation for building reproducible, maintainable, and scalable data workflows:

- Define reproducible pipelines with [**Snakemake**](https://snakemake.github.io/) or similar workflow engines
- Validate data explicitly using [**Pandera**](https://pandera.readthedocs.io/)
- Use [**Cookiecutter**](https://cookiecutter.readthedocs.io/) or [**Copier**](https://copier.readthedocs.io/) templates to scaffold projects and add pipeline steps
- Manage dependencies with [**Conda**](https://docs.conda.io/) (or [`mamba`](https://mamba.readthedocs.io/), [`micromamba`](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html))
- Use [**SLURM**](https://slurm.schedmd.com/documentation.html) or container-based execution for scaling
- Store intermediate outputs in [**Parquet**](https://parquet.apache.org/) or other flat files
- Publish data outputs to open repositories such as [**Zenodo**](https://zenodo.org/) (EU), [**Open Energy Data Initiative**](https://data.openei.org) (OEDI, US Dept. of Energy), [Kaggle](https://www.kaggle.com/datasets), or [Harvard Dataverse](https://dataverse.harvard.edu/)
- Add **type annotations** and run [**mypy**](https://mypy.readthedocs.io/) to catch type errors early
- Enforce code quality with [**Ruff**](https://docs.astral.sh/ruff/) and [**Black**](https://black.readthedocs.io/)
- Run tests in isolated environments with [**tox**](https://tox.wiki/)
- Use [**GitHub Actions**](https://docs.github.com/en/actions) or similar for CI and trunk-based development
