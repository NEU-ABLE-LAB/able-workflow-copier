rule dag_svg:
    """Create an SVG of the main Snakemake DAG"""
    localrule: True
    input:
        snakefile=workflow.source_path("../Snakefile"),
    output:
        svg=Path(config["DOCS_ASSETS_DIR"]) / "dag_all.svg",
    log:
        loguru=str(LOG_DIR / "dag_svg" / "loguru.log"),
        stderr=str(LOG_DIR / "dag_svg" / "stderr.log"),
    conda:
        get_localized_conda(config["CONDA"]["ENVS"]["DOCS"])
    script:
        str(WORKFLOW_BASE / "scripts/rules_conda_DOCS/dag_svg.py")
