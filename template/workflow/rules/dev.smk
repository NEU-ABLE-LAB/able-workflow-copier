rule conda_localize:
    """
    Aggregate rule: forces localisation of **every** environment YAML
    listed in ``config["CONDA"]["ENVS"]``.
    """
    localrule: True
    input:
        yamls=expand(
            str(
                Path(config["CONDA"]["LOCALIZED_DIR"]) / "{environment}.yaml"
            ),
            environment=config["CONDA"]["ENVS"].values(),
        ),


rule conda_localize_file:
    """
    Localize a single conda environment YAML file from pyproject2conda.
    """
    localrule: True
    input:
        src=str(
            Path(config["CONDA"]["PYPROJECT2CONDA_DIR"])
            / "{environment}.yaml"
        ),
    output:
        dst=str(Path(config["CONDA"]["LOCALIZED_DIR"]) / "{environment}.yaml"),
    wildcard_constraints:
        environment=RE_VALID_FNAME_STEM,
    params:
        project_root=str((WORKFLOW_BASE / "..").resolve()),
    log:
        loguru=LOG_DIR / "conda_localize_file/{environment}.log",
    script:
        str(WORKFLOW_BASE / "scripts/rules_global/conda_localize_file.py")


rule conda_update_yaml:
    """
    Update the conda environment from the yaml file for the user.
    NOTE: Snakemake recreates these environments in a separate location
          when called using the `conda:` directive in the pipeline.
          This rule is only for development purposes.
    """
    localrule: True
    group:
        "conda_group"
    input:
        yaml=(Path("{yaml_dir}") / "{environment}.yaml"),
    output:
        stamp=touch(
            Path("{yaml_dir}") / "{environment}.snakemake_conda_update_stamp"
        ),
    wildcard_constraints:
        yaml_dir=f"{config['CONDA']['LOCALIZED_DIR']}|{config['CONDA']['ENVS_DIR']}",
        environment=RE_VALID_FNAME_STEM,
    log:
        stdout=LOG_DIR / "conda_update/{yaml_dir}/{environment}/stdout.log",
        stderr=LOG_DIR / "conda_update/{yaml_dir}/{environment}/stderr.log",
    shell:
        """
        exec 1>"{log.stdout}"
        exec 2>"{log.stderr}"
        conda env update \
          --name {wildcards.environment} \
          --file {input.yaml} \
          --prune \
          --quiet
        """


rule conda_update:
    """
    Update the conda environments for the user.

    This rule should be run with the `--cores 1` option to ensure
    that the environments are updated sequentially and not in parallel
    since conda does not support parallel updates well.

    NOTE: Snakemake recreates these environments in a separate location
          when called using the `conda:` directive in the pipeline.
          This rule is only for development purposes.
    """
    localrule: True
    input:
        expand(
            str(
                Path(
                    Path(config["CONDA"]["LOCALIZED_DIR"])
                    / f"{{environment}}"
                ).with_suffix(".snakemake_conda_update_stamp")
            ),
            environment=config["CONDA"]["ENVS"].values(),
        ),
        expand(
            str(
                Path(
                    Path(config["CONDA"]["ENVS_DIR"]) / f"{{environment}}"
                ).with_suffix(".snakemake_conda_update_stamp")
            ),
            environment=config["CONDA"]["ENVS_META"].values(),
        ),


rule logs_to_watch:
    """
    Create a json list of all rules that have a log directive.
    This can be pasted into the workspace's .vscode/settings.json file
    to enable the Log Viewer extension to track all log files.
    """
    localrule: True
    log:
        json_out=LOG_DIR / "logs_to_watch.log",
    run:
        watches = []
        for rule in workflow.rules:
            if rule.log:
                watches.append(
                    {
                        "title": rule.name,
                        "pattern": [
                            (
                                r"${workspaceFolder}/logs/rules/"
                                + f"{rule.name}/**/*.log"
                            ),
                            (
                                r"${workspaceFolder}/logs/rules/"
                                + f"{rule.name}.log"
                            ),
                        ],
                    }
                )
        with open(log.json_out, "w") as out_json:
            out_json.write(json.dumps(watches, indent=4))


rule precommit:
    """
    Run pre-commit hooks on the codebase.
    """
    localrule: True
    log:
        LOG_DIR / "precommit.log",
    shell:
        """
        exec 1>"{log}"
        exec 2>"{log}"
        pre-commit run --all-files --show-diff-on-failure
        """
