# Changelog

Human-readable log of changes between versions. Follows the [Common Changelog style guide](https://common-changelog.org/).

## v0.1.5-dev

### Changed

- Removed depreciated `tenacity` dependency

### Added

- Added regression tests for YAML indentation handling in `able-workflow/module-copier/tasks/append_config_include.py` and template workflow scripts.
- `min_version("9.16.3")` to `template/workflow/Snakefile.jinja`
- `template/CHANGELOG.md`

### Removed

### Fixed

- Standardized ruamel YAML dump indentation (`mapping=2`, `sequence=4`, `offset=2`) for remaining YAML writers so sequence items stay indented under their parent keys.

## v0.1.4 - 2026-03-18

### Changed

- `docs_dag_svg.smk` can no longer be `copier upate` from within this repo. The following files must be manually updated if needed:
  - `template/workflow/rules/docs_dag_svg.smk`
  - `template/workflow/scripts/rules_conda_DOCS/dag_svg.py.jinja`
  - `template/tests/workflow/rules/test_snakemake_dag_svg.py`
  - `template/tests/workflow/scripts/rules_conda_DOCS/test_dag_svg.py`
- Dry-run manifests now live under `template/data/tests/dry-run/`, use `include:` plus `touch:`, and are passed into `dag_svg.py` through Snakemake rule inputs instead of being derived inside the script.
- Bump submodules to track their `main` branches.
- Moved `example-answers-*.yml` into `example-answers/` directory.
- Consolidated `.github/workflows/pr.yml` and `.github/workflows/main.yml` into `.github/workflows/ci.yml`, with Codecov secret usage guarded to pushes on `main`.
- Updated CI badge links in `README.md` and `docs/docs/index.md` to reference `.github/workflows/ci.yml`.

### Added

- Better comments in code
- Added CI contribution docs pages at `docs/docs/contributing/ci.md` and `template/docs/docs/contributing/ci.md`.

### Removed

- Removed `able-workflow-rule-copier` files that were used within template to generate `docs_dag_svg.smk`
  - `template/.copier-answers/project.yml`
  - `template/.copier-answers/rule-dag_svg.yml`
  - `template/docs/docs/contributing/templates/rule-dag_svg.md`
- Workaround for fixed [snakemake bug](https://github.com/snakemake/snakemake/issues/3719)
- Removed duplicate install of tox in `pr.yml`
- `"python-envs.pythonProjects": [],` from template `settings.json`

### Fixed

- syntax in docs example (#42)
- Updated contributor docs and post-copier guidance to describe the dry-run manifest layout and recursive includes.
- unrendered jinja

## v0.1.3 - 2026-03-16

### Changed

- Enforced uniformity of scripts and tests across `able-workflow*-copier` repos
- `sandbox_examples_generate` is now module `scripts.sandbox_examples_generate` instead of script

### Added

- Refactored `copie_helpers.py` functions into their own file.

### Removed

### Fixed

- Added explicit `tenacity` dependency to `pyrpoject.toml.jinja`. See #46 to remove this.

## v0.1.2 - 2026-03-15

### Changed

- Codecov only gets uploaded on pushes to main. (#14)
- Removed duplicate tox installs in gh-actions (#23)
- Limited mkdocs to <v2 (#10)
- Unpinned snakemake, now >9.16.3 (where last breaking change occured)

### Added

- Concurrency limit for GH actions from PRs. (#14)

### Removed

### Fixed

- GH actions from PRs no longer require secrets. (#14)

## v0.1.1 - 2026-03-14

### Changed

- Github actions `pr.yaml` test name to `tox Tests`
- gh-pages `dev` alias now tracks `main` and `latest` alias tracks last release.

### Added

- Codecov and Github actions CI badges

### Removed

### Fixed

- `copier.yml` no longer `_exclude` answer file

## v0.1.0 - 2026-03-14

Initial commit to public `able-workflow-etl-copier` repository from `NEU-ABLE-LAB` private repository.
