# Testing with tox

This project uses [`tox`](https://tox.wiki/en/4.26.0/index.html) to orchestrate tests and pytest for running the tests. The generated template also uses tox, and tests can be run on the generated environments.

## Run all the tests in parallel

```bash
tox run-parallel
```

or, equivalently:

```bash
tox p
```

## Run all the tests in py312 except `tox` tests within the generated examples

```bash
tox run-parallel -f py312-unit -f py312-template-generate -f py312-lint -f py312-typecheck -f py312-docs
```
