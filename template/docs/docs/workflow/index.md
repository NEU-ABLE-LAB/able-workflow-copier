# Workflow

The data processing and reporting pipeline is orchestrated with [Snakemake](https://snakemake.readthedocs.io/).

## Directed Acyclic Graph (DAG)

A **DAG (Directed Acyclic Graph)** is a fundamental concept in Snakemake that represents the structure and dependencies of your workflow. In this context:

- **Directed**: The graph has arrows showing the flow from input files to output files through processing steps
- **Acyclic**: There are no circular dependencies - the workflow flows in one direction without loops
- **Graph**: A network of interconnected nodes (rules/jobs) and edges (dependencies)

Each node in the DAG represents a rule or job that processes data, while the edges show which outputs from one rule serve as inputs to another. Snakemake automatically constructs this DAG from your rules and their input/output specifications, then executes jobs in the correct order to satisfy all dependencies.

This DAG visualization helps you understand:

- The overall structure of your data processing pipeline
- Which steps depend on others
- Potential bottlenecks or parallelization opportunities
- The flow from raw data to final outputs

## Target rules

### `all`

![Snakemake DAG](../_assets/filegraph-all.svg)
