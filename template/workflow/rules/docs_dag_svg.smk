rule dag_svg:
    """Create an SVG of the main Snakemake DAG"""
    localrule: True
    input:
        # TODO: Define input files if needed. All inputs should be named.
        readme="data/README.md",
    # output:
    # TODO: Define output files if needed. All outputs should be named.
    # wildcards:
    # TODO: Add wildcards if needed. All wildcards should be named.
    log:
        loguru=str(LOG_DIR / "dag_svg" / "loguru.log"),
        stdout=str(LOG_DIR / "dag_svg" / "stdout.log"),
        stderr=str(LOG_DIR / "dag_svg" / "stderr.log"),
    conda:
        get_localized_conda(config["CONDA"]["ENVS"]["DOCS"])
    # params:
    # TODO: Define parameters if needed. All parameters should be named.
    script:
        str(WORKFLOW_BASE / "scripts/rules_conda_DOCS/dag_svg.py")
