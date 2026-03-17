# Minimal data for tests

This directory should not contain any large files or sensitive information.

Dry-run manifests live under `dry-run/` are YAML files with the following:

- `touch:` lists files to create relative to `data/` during dry runs.
- `include:` lists other manifest files to merge recursively.
- Include paths are resolved relative to the manifest that declares them.
