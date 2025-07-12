# Features

Features represent derived and engineered data elements that have been extracted, transformed, or computed from datasets. In the ABLE workflow framework, features typically have fewer columns and/or rows than their source datasets, often going through significant transformation to create analysis-ready variables for modeling and analysis. Features follow the same structured Extract-Transform-Load (ETL) pattern as datasets, ensuring reproducibility and modularity within the Snakemake workflow.

## Features vs. Datasets

While **datasets** contain raw or lightly processed data with many columns and rows, **features** represent:

- **Aggregated data**: Reduced dimensions through grouping, summarization, or statistical operations
- **Engineered variables**: Newly computed variables derived from existing data columns
- **Filtered subsets**: Focused data selections based on specific criteria or conditions
- **Transformed representations**: Data converted to different formats, scales, or encodings for specific analytical purposes

Features typically serve as direct inputs to machine learning models, statistical analyses, or specialized visualizations.

## ETL Processes in Module Structure

Features follow the same module organization pattern as datasets, but with transformations focused on feature engineering:

```txt
{{ package_name }}/
└── features/
    └── {{ module_name }}/
        └── {{ etl_name }}/
            ├── __init__.py       # Module documentation and interface
            ├── extract.py        # Read processed features from disk
            ├── schema.py         # Validate output feature structure
            └── runner/           # Full ETL implementation
                ├── __init__.py
                ├── extract_external.py  # Extract from external sources (if needed)
                ├── schema_external.py   # Validate external data (if needed)
                ├── transform.py         # Feature engineering logic
                ├── load.py             # Save features to disk
                └── main.py             # Orchestrate ETL steps
```

The `transform.py` module in features typically implements:

- **Feature extraction**: Computing new variables from raw data
- **Feature selection**: Choosing relevant variables for specific use cases
- **Feature scaling**: Normalizing or standardizing variables
- **Feature encoding**: Converting categorical variables to numerical representations
- **Dimensionality reduction**: Reducing feature space while preserving information

## ETL Processes in Snakemake Workflow

Features are organized in the workflow structure parallel to datasets:

```txt
workflow/
├── Snakefile                    # Main workflow entry point
├── rules/
│   ├── includes.smk            # Import all rule files
│   └── features/
│       └── {{ module_name }}/
│           └── {{ etl_name }}.smk  # Snakemake rules for feature ETL
├── scripts/
│   └── rules_CONDA_RUNNER/
│       └── {{ package_name }}_rules.py  # Python interface to ETL
├── schemas/
│   └── features/
│       └── {{ module_name }}/
│           └── {{ etl_name }}.config.schema.yaml  # Config validation
└── envs/
    └── *.yaml                  # Conda environment specifications
```

### Feature Dependencies

Features often depend on datasets or other features, creating dependency chains:

- **Feature rules** can reference dataset outputs as inputs
- **Downstream features** can depend on upstream feature outputs
- **Model rules** typically consume feature outputs as their primary inputs

This creates a natural data processing pipeline where raw data flows through datasets to features to models.

## Configuration and Validation

Feature ETL processes have associated configuration files for parameters specific to feature engineering:

- **`config/features/{{ module_name }}/{{ etl_name }}.config.yaml`**: Feature-specific parameters (scaling factors, encoding mappings, selection criteria)
- **`workflow/schemas/features/{{ module_name }}/{{ etl_name }}.config.schema.yaml`**: Configuration validation schema

Common feature configuration parameters include:

- Target variable definitions for supervised learning
- Feature selection thresholds and criteria
- Scaling and normalization parameters
- Time window specifications for temporal features
- Categorical encoding strategies

## Navigation Structure

The documentation for features follows the same hierarchical pattern as datasets:

```txt
docs/docs/features/
├── index.md                    # This overview page
└── {{ module_name }}/          # Module-specific documentation
    ├── index.md               # Module overview
    ├── SUMMARY.md             # Navigation outline
    └── {{ etl_name }}/        # ETL-specific documentation
        ├── index.md           # ETL process description
        ├── config.md          # Configuration options
        ├── schema.md          # Feature schemas
        └── SUMMARY.md         # ETL navigation outline
```

This structure allows users to navigate from general feature engineering concepts to specific implementation details, with clear documentation of how features are derived from their source data and configured for different analytical purposes.
