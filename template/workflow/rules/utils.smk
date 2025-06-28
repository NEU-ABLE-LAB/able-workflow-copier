"""
Helpers for rules in the workflow.
"""

# TODO-copier-package Should this be moved to a pure python file under `workflow/scripts/utils/`?


rule log_config:
    """
    Log the configuration of the workflow.
    """
    localrule: True
    log:
        loguru=LOG_DIR / "log_config.log",
        config=LOG_DIR / "config.yaml",
    script:
        str(WORKFLOW_BASE / "scripts/rules_global/log_config.py")


def get_localized_conda(env_name: str) -> str:
    """
    Return the path to a localized conda environment file.

    Parameters
    ----------
    env_name : str
        The name of the conda environment.

    Returns
    -------
    str
        The path to the conda environment file.
    """

    # When the `snakemake` command is executed from the project root,
    # and the `Snakefile` is in the project root,
    # then `workflow.basedir` will point to the `workflow` directory,
    # and we do not need to append the `workflow` directory to the path.
    workflow_dir = Path(workflow.basedir)

    # When the `snakemake` command is executed from the project root,
    # and the `Snakefile` is in the `workflow` directory,
    # then `workflow.basedir` will point to the project root,
    # and we need to append the `workflow` directory to the path.
    if (workflow_dir / "workflow").exists():
        workflow_dir = workflow_dir / "workflow"
    #     logger.debug(f"Found workflow directory: {workflow_dir}")
    # else:
    #     logger.debug(f"Using workflow directory: {workflow_dir}")

    # Remove the `workflow/` prefix from LOCALIZED_DIR
    # to get the correct path to the conda environment file.
    workflow_localized_dir = Path(
        config["CONDA"]["LOCALIZED_DIR"]
    ).relative_to("workflow")

    env_path = (
        workflow_dir / workflow_localized_dir / f"{env_name}"
    ).with_suffix(".yaml")
    logger.debug(f"Localized conda environment path: {env_path}")

    if not env_path.exists():
        logger.warning(
            f"Missing localized conda environment {env_path}. "
            "Run `snakemake conda_localize` to create it."
        )

    return str(env_path)
