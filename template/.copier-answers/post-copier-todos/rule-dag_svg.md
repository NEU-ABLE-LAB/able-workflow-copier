# Post Copier To-Do's for Rule dag_svg

This issue is for tracking the development of a rule that was copied from the `able-workflow-rule-copier` template.

## Next steps

### Required

1. [ ] `workflow/rules/docs_dag_svg.smk`
   1. [ ] Specify `input:` directives as needed.
   2. [ ] Specify `output:` directives as needed.
   3. [ ] Specify `params:` directives as needed.
   4. [ ] Specify `wildcards:` directives as needed.
2. [ ] `workflow/scripts/rules_conda_DOCS/dag_svg.py`
   1. [ ] Assign the desired snakemake directives (e.g., `input` to variables.
   2. [ ] Fill in the rule logic within main().
   3. [ ] Confirm typecheck and lint checks pass with the following commands
     - `tox -e py312-typecheck-core`
     - `tox -e py312-lint`
3. [ ] `test/workflow/scripts/rules_conda_DOCS/test_dag_svg.py.jinja`
   1. [ ] Update the `Snakemake()` parameters of `_build_snakemake()` with the structure to match the `input:`, `output:`, `wildcards:` and `params:` directives provided by the rule under test.
   2. [ ] Provide dummy or tiny subsets of data for tests in the appropriate location under `data/tests/`.
   3. [ ] Replace `test_main_runs()` with the desired test logic for the script under test.
   4. [ ] Confim tests pass with one of the following commands depending on the conda environment needed to run the test.
     - `tox -e py312-workflow-unit-global`
     - `tox -e py312-workflow-unit-core`
     - `tox -e py312-workflow-unit-extras`
     - `tox -e py312-workflow-unit-docs`
4. [ ] `tests/workflow/rules/test_snakemake_dag_svg.py`
   1. [ ] Modify `create_dummy_input_file()` to create the dummy to subsets of data for tests.
   2. [ ] Moidfy `test_rule_dag_svg()` to check that output data was created.
   3. [ ] Confirm tests pass with the following command:
     - `tox -e py312-workflow-rules`
5. [ ] Update documentation in `docs/docs/contributing/templates/rule-dag_svg.md` on how to use rule or expected output.
6. [ ] Run the `logs_to_watch` rule and update the `"logViewer.watch"` section of `.vscode/settings.json` with the results found in `logs/rules/logs_to_watch.log`.
