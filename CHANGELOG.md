# Changelog

Human-readable log of changes between versions. Follows the [Common Changelog style guide](https://common-changelog.org/).

## dev

### Changed

- Codecov only gets uploaded on pushes to main. (#14)
- Removed duplicate tox installs in gh-actions (#23)

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
