# TODO-copier-package add notebooks to docs


rule docs_build:
    """Build the documentation."""

    # TODO check this rule is working as intended
    input:
        mkdocs_yml=(DOCS_DIR / "mkdocs.yml"),
        # TODO-copier-package add dag_svg to docs_build
        # dag_svg=rules.dag_svg.output,
    output:
        temp(DOCS_DIR / "site/index.html"),
    log:
        LOG_DIR / "docs_build.log",
    conda:
        get_localized_conda(config["CONDA"]["ENVS"]["DOCS"])
    shell:
        """
        exec 1>"{log}"
        exec 2>"{log}"
        export JUPYTER_PLATFORM_DIRS=1
        mkdocs build --config-file {input.mkdocs_yml}
        """


rule docs_deploy:
    """
    Deploy the documentation to the `gh-pages with
    [mike](https://github.com/jimporter/mike?tab=readme-ov-file#building-your-docs).
    """
    input:
        mkdocs_yml=(DOCS_DIR / "mkdocs.yml"),
        # TODO-copier-package add dag_svg to docs_build
        # dag_svg=rules.dag_svg.output,
    log:
        LOG_DIR / "docs.log",
    conda:
        get_localized_conda(config["CONDA"]["ENVS"]["DOCS"])
    shell:
        # TODO Configure versioning so `mike` grabs semantic tags
        """
        exec 1>"{log}"
        exec 2>"{log}"
        echo "TODO configure versioning"
        exit 1
        # mike deploy --config-file {input.mkdocs_yml}
        """


rule docs_serve_mike:
    """
    Serve the documentation committed to the `gh-pages` branch
    [using `mike`](https://github.com/jimporter/mike?tab=readme-ov-file#viewing-your-docs).
    NOTE: This rule is "blocking", and will not return until the server is stopped.
          This rule is only for development purposes.
    """
    input:
        mkdocs_yml=(DOCS_DIR / "mkdocs.yml"),
        # TODO-copier-package add dag_svg to docs_build
        # dag_svg=rules.dag_svg.output,
    log:
        LOG_DIR / "docs_serve.log",
    conda:
        get_localized_conda(config["CONDA"]["ENVS"]["DOCS"])
    shell:
        """
        exec 1>"{log}"
        exec 2>"{log}"
        export JUPYTER_PLATFORM_DIRS=1
        mike serve --config-file {input.mkdocs_yml}
        """


rule docs_serve:
    """
    Make and serve the documentation.
    NOTE: This rule is "blocking", and will not return until the server is stopped.
          This rule is only for development purposes.
    """
    input:
        mkdocs_yml=(DOCS_DIR / "mkdocs.yml"),
        # TODO-copier-package add dag_svg to docs_build
        # dag_svg=rules.dag_svg.output,
    log:
        LOG_DIR / "docs_serve.log",
    conda:
        get_localized_conda(config["CONDA"]["ENVS"]["DOCS"])
    shell:
        """
        exec 1>"{log}"
        exec 2>"{log}"
        export JUPYTER_PLATFORM_DIRS=1
        mkdocs serve --config-file {input.mkdocs_yml}
        """
