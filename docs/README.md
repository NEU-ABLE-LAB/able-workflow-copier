# ABLE Workflow copier template documentation

<!--include-start-->

## Overview

The documentation for this project uses [MkDocs](https://www.mkdocs.org/) and the
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.

The documentation source files are located in the `docs/docs/` directory.

## Serving the documentation locally

The following assumes that you have already set up the development environment.

### Serving just the `able-workflow-copier` docs

```bash
./scripts/mkdocs_serve.sh
```

### Serving ALL the `able-workflow` docs

The following assumes that you cloned all the submodules in this repo

```bash
./scripts/mkdocs_serve_all.py
```

Logs for the local `mkdocs` servers for each of these processes can be found in `logs/mkdocs_serve_all/`

<!--include-end-->

## More information

For more information on developing the documentation, see the
`docs/contributing/docs.md` file or the equivalent in the hosted documentation.
