rule dag_svg:
    """
    Create an SVG of the main Snakemake DAG

    output:
        svg: WORKFLOW_BASE is used here instead of workflow.source_path()
            since workflow.source_path() cannot cache an entire directory
            so instead just point to the mkdocs.yml file and assume the
            worker has access to the entire directory. This very well may
            break if the job is sent out to multiple workers each with
            their own cache of this workflow.
    """
    localrule: True
    input:
        snakefile=workflow.source_path("../Snakefile"),
    output:
        svg=Path(WORKFLOW_BASE / "../docs/docs/_assets/dag_all.svg"),
    log:
        loguru=str(LOG_DIR / "dag_svg" / "loguru.log"),
        stderr=str(LOG_DIR / "dag_svg" / "stderr.log"),
    conda:
        get_localized_conda(config["CONDA"]["ENVS"]["DOCS"])
    script:
        str(WORKFLOW_BASE / "scripts/rules_conda_DOCS/dag_svg.py")
