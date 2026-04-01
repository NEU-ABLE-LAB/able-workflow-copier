# Models

TODO-copier-package overview of the models concept. This is about fitting models to datasets and features. Not running simulations. A simulation run would generate a new dataset.

TODO-copier-package genericly explain ETL processes within modules and directory structure.

TODO-copier-package genericly explain ETL processes within Snakemake and `workflow/` directory.

TODO-copier-package explain nav-tree

## Configuration and Validation

Model ETL processes should keep committed configuration and schemas aligned:

- `config/models/<module_name>/<etl_name>/config.yaml`
- `workflow/schemas/models/<module_name>/<etl_name>/config.schema.yaml`

When updating model configuration values, update both files and keep schema
`default` values equal to the committed config values.

For schema authoring guidance (including nested `required` behavior), see
[Contributing → Config and Schemas](../contributing/workflow.md#config-and-schemas).
