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

## Run tests within the rendered examples

```bash
tox -e py312-template-tox
```

### Run only specific tests within the rendered examples

See `template/tox.ini.jinja` for tests within the redered template that can be run.

The `--template-envs` argument is passed to the inner tox as `-e`

The `--no-parallel` argument tells the inner tox to run `tox run` instead of `tox run-parallel --parallel-no-spinner`

The `--template-no-capture` argument tells the inner pytest to propagate the output to the outer tox

```bash
tox -e py312-template-tox -- --template-envs=py312-unit-core --no-parallel --template-no-capture
```
