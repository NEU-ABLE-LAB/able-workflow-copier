rule dag_svg:
    """Create an SVG of the main Snakemake DAG"""
    localrule: True
    input:
        snakefile=WORKFLOW_BASE / "Snakefile",
        rules=lambda wc: (WORKFLOW_BASE / "rules").glob("*.smk"),
    output:
        svg=DOCS_DIR / "docs" / "_images" / "dag.svg",
    log:
        loguru=str(LOG_DIR / "dag_svg" / "loguru.log"),
        stderr=str(LOG_DIR / "dag_svg" / "stderr.log"),
    conda:
        get_localized_conda(config["CONDA"]["ENVS"]["DOCS"])
    script:
        str(WORKFLOW_BASE / "scripts/rules_conda_DOCS/dag_svg.py")
