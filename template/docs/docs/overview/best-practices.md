# Best Practices this Project Implements

The following practices provide a solid foundation for building reproducible, maintainable, and scalable data workflows:

- Define reproducible pipelines with **Snakemake** or similar workflow engines
- Validate data explicitly using **Pandera**
- Use **Cookiecutter** or **Copier** templates to scaffold projects and add pipeline steps
- Manage dependencies with **Conda** (or `mamba`, `micromamba`)
- Use **SLURM** or container-based execution for scaling
- Store intermediate outputs in **Parquet** or other flat files
- Publish data outputs to open repositories (e.g. **Zenodo**, **Hugging Face Datasets**)
  - [ ] TODO Add energy focused data repos
- Add **type annotations** and run **mypy** to catch type errors early
- Enforce code quality with **Ruff** and **Black**
- Run tests in isolated environments with **tox**
- Use **GitHub Actions** or similar for CI and trunk-based development

TODO-copier-package consider organizing this list to align with the columns of the whitespace table.
