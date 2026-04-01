# Minimal data for tests

This directory should not contain any large files or sensitive information.

Dry-run manifests live under `dry-run/` are YAML files with the following:

- `touch:` lists files to create relative to `data/` during dry runs.
- `include:` lists other manifest files to merge recursively.
- Include paths are resolved relative to the manifest that declares them.

Naming convention:

- `all.yaml` is the aggregate manifest used by workflow-wide dry-run targets (for example `dag_svg_all` and `all_data`).
- `<rule_name>.yaml` files are used for individual rule dry-run tests.
- Prefer composing `all.yaml` from shared and per-rule manifests with `include:` to avoid duplicated `touch:` paths.
