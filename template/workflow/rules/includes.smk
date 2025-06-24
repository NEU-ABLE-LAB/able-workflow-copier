"""
This file lists all the other snakefiles (*.smk)
that are used by the workflow.

All these file paths should be relative to the
`workflow/rules/` directory.
"""


# Helper functions
# Needs to be imported first so that the rules can use them.
include: "utils.smk"
# Rules for development, building, and testing
include: "build.smk"
include: "dev.smk"
include: "docs_dag_svg.smk"
include: "docs.smk"
# Append additional rules below
include: "reports.smk"
