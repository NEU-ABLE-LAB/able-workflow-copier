# ---------------------------------------------------------------------------
#  Discover every template notebook and expose two wildcards:
#     * dpath  – all parent directories, e.g.  energy/usage/seasonal
#     * fname  – file stem, e.g.           heatmap
# ---------------------------------------------------------------------------
TEMPLATES = glob_wildcards(
    f"{REPORT_TEMPLATES_DIR}/{{dpath,.+}}/{{fname}}.ipynb"
)

# TODO-copier-package Write helper function to read inputs from notebooks
# `parameters` cell and add them to the rule below.

# ---------------------------------------------------------------------------
#  One-to-one rule
# ---------------------------------------------------------------------------
rule notebook_to_report:
    """
    Execute one template notebook and write the executed copy to

        reports/{dpath}/notebooks/{fname}.ipynb
    """
    input:
        tpl=lambda wc: f"{REPORT_TEMPLATES_DIR}/{wc.dpath}/{wc.fname}.ipynb",
        # TODO-copier-package add notebook inputs
    output:
        rpt=f"{REPORTS_DIR}/{{dpath}}/notebooks/{{fname}}.ipynb",
    wildcard_constraints:
        dpath=".+",
        fname=r"[A-Za-z0-9_\-]+",
    params:
        outdir=lambda wc: f"{REPORTS_DIR}/{wc.dpath}/notebooks",
    log:
        f"{LOG_DIR}/notebook_to_report/{{dpath}}/{{fname}}.log",
    conda:
        get_localized_conda(config["CONDA"]["ENVS"]["NOTEBOOK"])
    shell:
        r"""
        exec 1>"{log}" 2>&1
        mkdir -p "{params.outdir}" "$(dirname "{log}")"
        papermill "{input.tpl}" "{output.rpt}" --log-output
        """


# ---------------------------------------------------------------------------
#  Aggregate rule – run *all* discovered notebooks
# ---------------------------------------------------------------------------
rule notebook_to_report_all:
    localrule: True
    input:
        expand(
            rules.notebook_to_report.output.rpt,
            zip,
            dpath=TEMPLATES.dpath,
            fname=TEMPLATES.fname,
        ),
