rule dag_svg_file:
    """
    Create an SVG of the main Snakemake DAG

    output:
        svg: WORKFLOW_BASE is used here instead of workflow.source_path()
            since workflow.source_path() cannot cache an entire directory
            so instead just point to the mkdocs.yml file and assume the
            worker has access to the entire directory. This very well may
            break if the job is sent out to multiple workers each with
            their own cache of this workflow.
    wildcards:
        rule_name: The name of the rule to generate the DAG for.
            This is used to create a unique filename for the SVG.
    """
    localrule: True
    resources:
        snakemake_calls=1
    input:
        snakefile=Path(workflow.source_path("../Snakefile")).resolve(),
    output:
        svg=Path(WORKFLOW_BASE / "../docs/docs/_assets/dag_{rule_name}.svg").resolve(),
    wildcard_constraints:
        rule_name="[a-zA-Z_][a-zA-Z0-9_]*"
    log:
        loguru=str(LOG_DIR / "dag_svg_file" / "{rule_name}" / "loguru.log"),
        stderr=str(LOG_DIR / "dag_svg_file" / "{rule_name}" / "stderr.log"),
    conda:
        get_localized_conda(config["CONDA"]["ENVS"]["DOCS"])
    script:
        str(WORKFLOW_BASE / "scripts/rules_conda_DOCS/dag_svg.py")

rule dag_svg_all:
    """
    Create an SVG of the main Snakemake DAG for all rules.
    """
    input:
        svg=Path(WORKFLOW_BASE / "../docs/docs/_assets/dag_all.svg").resolve(),
