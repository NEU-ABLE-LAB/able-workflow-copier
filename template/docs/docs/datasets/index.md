# Datasets

Each dataset follows a structured Extract-Transform-Load (ETL) pattern that ensures reproducibility, modularity, and maintainability within the Snakemake workflow orchestration system.

## ETL Concept and Snakemake Integration

The ETL (Extract-Transform-Load) concept forms the atomic unit of data processing in this workflow. Each dataset ETL process:

- **Extracts** data from external sources (APIs, files, databases) or from other ETL processes (by importing their `extract` and `schema` modules.)
- **Transforms** the data through cleaning, validation, aggregation, or reshaping operations
- **Loads** the processed data to disk in a standardized format (typically Parquet files)

These ETL processes are orchestrated by Snakemake rules that define:

- **Input dependencies**: What data files or external sources are required
- **Output targets**: What processed files will be generated
- **Execution logic**: How the ETL process transforms inputs to outputs. This is typically handled with a ETL module in the python package.
- **Environment requirements**: What conda environments and dependencies are needed. This is typically the package dependencies with the `runner` extras.

Each ETL process produces outputs that can serve as inputs to downstream processes, creating a directed acyclic graph (DAG) of data dependencies that Snakemake can execute efficiently.

## Data Directory Structure

The `data/` directory implements a standardized organization pattern that separates data by processing stage and supports flexible storage through symlinks:

```yaml
data/
├── {{ module_name }}/
│   ├── external/     # (1)
│   ├── raw/          # (2)
│   ├── interim/      # (3)
│   ├── processed/    # (4)
│   └── README.md
├── tests/            # Test data for validation
└── README.md
```

1. Data from third-party sources in their original format (APIs, downloaded files, external databases). This data should be considered immutable and may require special handling for licensing or access control.
2. The original or validated external data in a standardized format. This represents the first stage of data processing where external data is converted to a consistent internal format but remains otherwise unmodified.
3. Intermediate data that has undergone partial transformation. This stage contains data between raw and final processing steps, useful for debugging and incremental development.
4. The final, canonical datasets ready for modeling and analysis. These datasets have undergone full validation, cleaning, and transformation according to the project's data requirements.

### Symlink Flexibility

The data directories may be symlinks to other locations on disk to support various storage scenarios:

- Large datasets stored on network drives or external storage
- Shared datasets accessed by multiple projects
- Datasets requiring special security or compliance considerations

When using symlinks, the target locations should be specified in the `config/**/*.yml` files rather than using relative `data/` paths, ensuring that Snakemake rules reference the correct absolute paths.
