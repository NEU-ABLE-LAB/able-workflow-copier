# Workflow configuration

The workflow loads configuration from files under `config/`.
By default, Snakemake uses the profile in `workflow/profiles/default/config.yaml`,
which loads `config/config.yaml` when that file is present and loads
`config/config.local.yaml` automatically if that file exists.

!!! note "Who should change which config?"

    Workflow runners should usually leave committed config files unchanged and use `config/config.local.yaml` for machine-specific overrides.

    Repository developers may update committed config files and matching schemas when changing the project's reproducible default behavior.

    Parent workflows that import this workflow should provide overrides from the parent workflow config instead of editing the child workflow repository.

## Configuration scopes

Configuration is organized by scope:

- `config/config.yaml`: project-wide committed defaults.
- `config/<module_type>/<module_name>/config.yaml`: module-level committed defaults.
- `config/<module_type>/<module_name>/<etl_name>/config.yaml`: ETL-specific committed defaults.
- `config/config.local.yaml`: optional local overrides for standalone runs from this repository.

If you use additional Snakemake profiles (for example SLURM), ensure those profile
`configfile:` entries include the same config files you rely on.

## Configuration files and schemas

Each committed config file should have a matching schema under `workflow/schemas/`.

- `config/config.yaml` ↔ `workflow/schemas/config.schema.yaml`
- `config/<module_type>/<module_name>/config.yaml` ↔
  `workflow/schemas/<module_type>/<module_name>/config.schema.yaml`
- `config/<module_type>/<module_name>/<etl_name>/config.yaml` ↔
  `workflow/schemas/<module_type>/<module_name>/<etl_name>/config.schema.yaml`

The schema defines types, allowed structure, and default values. Schema defaults are the fail-safe that keep the Snakefile and included `.smk` files safe to read when optional config branches are absent, such as when the workflow is imported into a parent workflow.

## Recommended update workflow

When you change reusable workflow defaults as a repository developer:

1. Update the committed config file under `config/` if the standalone default behavior should change.
2. Update the matching schema under `workflow/schemas/`.
3. Add/adjust `type`, `description`, and `default` in the schema.
4. Update the relevant docs and tests.

For machine-specific changes, create or update `config/config.local.yaml` instead of editing committed config files.

For schema authoring details, see
[Contributing → Config and Schemas](../contributing/workflow.md#config-and-schemas).
