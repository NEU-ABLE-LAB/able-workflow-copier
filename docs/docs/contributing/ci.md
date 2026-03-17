# Continuous Integration (CI)

This repository uses GitHub Actions to run the tox test suite for Pull Requests. Test results are uploaded to [codecov](https://app.codecov.io) on pushes to `main`.

## Workflows

- `.github/workflows/ci.yml`: runs tox on pull requests, pushes to `main`, and manual dispatch.
- `.github/workflows/docs-pages.yml`: builds and publishes docs.

## Secrets policy

The CI workflow is configured so `secrets.CODECOV_TOKEN` is only used for coverage uploads on pushes to `main`.

Pull request runs execute tests and checks but do not use Codecov secrets.
