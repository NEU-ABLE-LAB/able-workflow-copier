# Workflow configuration

The workflow loads configuration from files under `config/`.
By default, Snakemake uses the profile in `workflow/profiles/default/config.yaml`,
which defines the configuration files to include.

## Where to modify configuration

Configuration is organized by scope:

- `config/config.yaml`: project-wide settings.
- `config/<module_type>/<module_name>/config.yaml`: module-level settings.
- `config/<module_type>/<module_name>/<etl_name>/config.yaml`: ETL-specific settings.

If you use additional Snakemake profiles (for example SLURM), ensure those profile
`configfile:` entries include the same config files you rely on.

## Configuration files and schemas

Each committed config file should have a matching schema under `workflow/schemas/`.

- `config/config.yaml` ↔ `workflow/schemas/config.schema.yaml`
- `config/<module_type>/<module_name>/config.yaml` ↔
  `workflow/schemas/<module_type>/<module_name>/config.schema.yaml`
- `config/<module_type>/<module_name>/<etl_name>/config.yaml` ↔
  `workflow/schemas/<module_type>/<module_name>/<etl_name>/config.schema.yaml`

The schema defines types, allowed structure, and default values.

## Recommended update workflow

When you add or change a configuration option:

1. Update the committed config file under `config/`.
2. Update the matching schema under `workflow/schemas/`.
3. Add/adjust `type`, `description`, and `default` in the schema.
4. Use `required` only when the key must exist for all valid uses of that branch.

For schema authoring details (including `required` behavior in nested objects and
why committed config files should include all default values), see
[Contributing → Config and Schemas](../contributing/workflow.md#config-and-schemas).
