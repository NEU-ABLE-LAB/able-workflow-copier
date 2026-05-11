# Project directory tree

## Copier templates variables

Copier uses a jinja2 syntax for rendering templates with the answers to the templates questions.

- [able-workflow-copier]({{ able_workflow_copier_docs }})
- [able-workflow-copier template]({{ able_workflow_copier_docs }})
  - **{{ project_name_slug }}**: The name of the project being created.
  - **{{ package_name }}**: The name of the Python package being created.
- [able-workflow-module-copier template]({{ able_workflow_module_copier_docs }})
  - **{{ module_type }}**: The type of module being created (e.g., datasets, features, or models).
  - **{{ module_name }}**: The name of the module being created.
- [able-workflow-etl-copier template]({{ able_workflow_etl_copier_docs }})
  - **{{ etl_name }}**: The name of the ETL process being created.
  - **{{ conda_env_key }}**: The key for the Conda environment from the workflow config (e.g., `config["CONDA"]["ENVS"]["{{ conda_env_key }}"]`).
- [able-workflow-rule-copier template]({{ able_workflow_rule_copier_docs }})
  - **{{ is_package_rule }}**: The rule uses the package.
  - **{{ rule_name }}**: The name of the Snakemake rule being created.

## Project Tree

This tree is validated against the first two directory levels of `template/` in all four copier repositories.
Files that are created by a template are marked with a + sign, and files that are modified by a Copier template are marked with a * sign.

Legend (first 4 characters before each path, left to right):

1. `able-workflow-copier`
2. `able-workflow-module-copier`
3. `able-workflow-etl-copier`
4. `able-workflow-rule-copier`

Symbol in each column:

- `+` = created by that template
- `*` = modified by that template
- ` ` = blank = untouched by that template

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
+   {{ project_name_slug }}  # (1)
+***├── .copier-answers/  # (2)
+***│   ├── post-copier-todos/  # (4)
+***│   └── {% raw %}{{ _copier_conf.answers_file }}.jinja{% endraw %}  # (3)
+   ├── .github/  # (5)
+   │   ├── workflows/  # (7)
+   │   └── labels.yml  # (6)
+   ├── .vscode/  # (8)
+   │   ├── extensions.json  # (9)
+   │   ├── launch.json  # (10)
+   │   └── settings.json  # (11)
+** ├── config/  # (15)
+** │   ├── {{ module_type }}/  # (18)
+   │   ├── config.local.example.yaml  # (16)
+   │   ├── config.yaml.jinja  # (17)
+   │   └── README.md.jinja  # (19)
+   ├── data/  # (20)
+ * │   ├── tests/  # (22)
+   │   └── README.md  # (21)
+***├── docs/  # (23)
+   │   ├── _gen-files-scripts/  # (24)
+***│   ├── docs/  # (25)
+   │   ├── gen_ref_pages.py.jinja  # (26)
+   │   ├── mkdocs.yml.jinja  # (27)
+   │   └── README.md.jinja  # (28)
+   ├── hooks/  # (30)
+   │   ├── README.md  # (31)
+   │   └── snakemake_pyproject2conda.py.jinja  # (32)
+   ├── scripts/  # (37)
+   │   └── copier-check-update.sh  # (38)
+***├── tests/  # (40)
+ * │   ├── {{ package_name }}/  # (43)
+***│   ├── workflow/  # (44)
+   │   ├── __init__.py  # (41)
+   │   └── conftest.py  # (42)
+***├── workflow/  # (46)
   │   ├── setup/  # (57)
   │   │   ├── index.md.jinja  # (58)
   │   │   ├── linux.md  # (59)
   │   │   ├── slurm.md  # (60)
   │   │   ├── SUMMARY.md  # (61)
   │   │   └── windows.md  # (62)
   │   ├── workflow/  # (63)
   │   │   ├── config.md  # (64)
   │   │   ├── index.md  # (65)
   │   │   ├── rules.md.jinja  # (66)
   │   │   └── SUMMARY.md  # (67)
 +* │   ├── {{ module_type }}/  # (68)
 +* │   │   └── {{ module_name }}/  # (69)
  + │   │       ├── {{ etl_name }}/  # (70)
  + │   │       │   ├── config.md.jinja  # (71)
  + │   │       │   ├── index.md.jinja  # (72)
  + │   │       │   ├── schema.md.jinja  # (73)
  + │   │       │   └── SUMMARY.md  # (74)
 +  │   │       ├── config.md.jinja  # (75)
 +  │   │       ├── index.md.jinja  # (76)
 +  │   │       └── SUMMARY.md  # (77)
+   │   ├── index.md.jinja  # (78)
+   │   └── SUMMARY.md  # (79)
+   ├── gen_ref_pages.py.jinja  # (80)
+   ├── mkdocs.yml.jinja  # (81)
+   └── README.md.jinja  # (82)
2. Copier answers directory used by all template runs.
3. Template answers file path used by Copier for each run.
4. Post-Copier todo directory appended by package/module/etl/rule templates.
5. GitHub metadata directory.
6. Standardized GitHub Issue and PR label definitions.
7. GitHub Actions workflow directory.
8. VS Code workspace configuration directory.
9. Recommended VS Code extensions list.
10. VS Code debug launch configurations.
11. VS Code workspace settings.
12. Agent instructions file template.
13. Agent setup instructions file template.
14. Project changelog file template.
15. Project configuration root; extended by module and ETL templates.
16. Example local override configuration file.
17. Main project configuration template.
18. Module-type configuration subtree (`datasets`, `features`, or `models`) created by module template and extended by ETL template.
19. Configuration documentation file template.
20. Data directory root.
21. Data directory README.
22. Data test fixtures/support directory.
23. Documentation directory root touched by all templates.
24. Documentation helper script directory.
25. MkDocs content directory touched by all templates.
26. MkDocs reference-page generation script template.
27. MkDocs configuration template.
28. Docs README template.
29. Git ignore rules template.
30. Hook scripts directory.
31. Hook directory README.
32. Hook script that syncs pyproject dependencies into Conda env definitions.
33. Project license file.
34. Pre-commit configuration file.
35. Python project metadata/configuration template.
36. Project README template.
37. Project scripts directory.
38. Copier update check helper script.
39. Snakefmt configuration file; also touched by module and ETL templates.
40. Test suite root touched by all templates.
41. Tests package initializer.
42. Top-level pytest shared fixtures.
43. Package tests directory created by base template and extended by ETL template.
44. Workflow tests directory extended by module, ETL, and rule templates.
45. Tox configuration template.
46. Snakemake workflow root touched by all templates.
47. Top-level Snakefile template.
48. Workflow environment definitions directory.
49. Workflow profile definitions directory (extended by module and ETL templates).
50. Snakemake rules directory touched by all templates.
51. Workflow schemas directory extended by module and ETL templates.
52. Workflow scripts directory created by base template and extended by rule template.
53. Python package source root touched by base/module/ETL templates.
54. Python package initializer template.
55. Package configuration loader template.
56. Dataset namespace directory (module and ETL templates touch this namespace when `{{ module_type }}` is `datasets`).
57. Feature namespace directory (module and ETL templates touch this namespace when `{{ module_type }}` is `features`).
58. Model namespace directory (module and ETL templates touch this namespace when `{{ module_type }}` is `models`).
59. Shared package utilities namespace directory.

## .copier-answers/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
+*** .copier-answers/  # (1)
+***├── post-copier-todos/  # (2)
  + │   ├── etl-{{ module_type }}-{{ module_name }}-{{ etl_name }}-subissues/  # (3)
  + │   │   ├── 01-rule.md.jinja  # (4)
  + │   │   ├── {% if requires_extract_external %}02-extract_external.md{% endif %}.jinja  # (5)
  + │   │   ├── {% if requires_extract_external %}03-schema_external.md{% endif %}.jinja  # (6)
  + │   │   ├── 04-transform.md.jinja  # (7)
  + │   │   ├── 05-schema.md.jinja  # (8)
  + │   │   ├── 06-load.md.jinja  # (9)
  + │   │   ├── 07-extract.md.jinja  # (10)
  + │   │   ├── 08-main.md.jinja  # (11)
  + │   │   ├── 09-integration-tests.md.jinja  # (12)
  + │   │   └── 10-docs.md.jinja  # (13)
  + │   ├── etl-{{ module_type }}-{{ module_name }}-{{ etl_name }}.md.jinja  # (14)
 +  │   ├── module-{{ module_type }}-{{ module_name }}.md.jinja  # (15)
+   │   ├── package.md.jinja  # (16)
+   │   ├── README.md  # (17)
   +│   └── rule-{{ rule_name }}.md.jinja  # (18)
+   └── {% raw %}{{ _copier_conf.answers_file }}.jinja{% endraw %}  # (19)
```

1. `.copier-answers/` is the shared template directory for persisted Copier answers and follow-up task templates.
2. `post-copier-todos/` stores templated markdown TODO files written by package/module/etl/rule template runs.
3. `etl-...-subissues/` holds ETL subissue templates generated by the ETL copier.
4. `01-rule.md.jinja` template for rule-focused ETL follow-up tasks.
5. Conditional `02-extract_external.md.jinja` template, emitted only when external extraction is required.
6. Conditional `03-schema_external.md.jinja` template, emitted only when external schema work is required.
7. `04-transform.md.jinja` template for transform task planning.
8. `05-schema.md.jinja` template for schema implementation tasks.
9. `06-load.md.jinja` template for load-step implementation tasks.
10. `07-extract.md.jinja` template for extract-step implementation tasks.
11. `08-main.md.jinja` template for runner/main integration tasks.
12. `09-integration-tests.md.jinja` template for ETL integration test tasks.
13. `10-docs.md.jinja` template for ETL documentation tasks.
14. `etl-{{ module_type }}-{{ module_name }}-{{ etl_name }}.md.jinja` is the primary ETL post-copier TODO template.
15. `module-{{ module_type }}-{{ module_name }}.md.jinja` is the module post-copier TODO template.
16. `package.md.jinja` is the base package post-copier TODO template.
17. `README.md` documents the post-copier TODO template directory.
18. `rule-{{ rule_name }}.md.jinja` is the rule post-copier TODO template.
19. `{% raw %}{{ _copier_conf.answers_file }}.jinja{% endraw %}` is the shared answers-file template path used by all four copier templates.

## .github/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
+   .github/  # (1)
+   ├── workflows/  # (2)
+   │   ├── build.yml  # (3)
+   │   ├── ci.yml.jinja  # (4)
+   │   ├── github-labeler.yml  # (5)
+   │   └── release.yml  # (6)
+   └── labels.yml  # (7)
```

1. `.github/` is the repository GitHub metadata directory; only `able-workflow-copier` provides this template subtree.
2. `.github/workflows/` contains GitHub Actions workflow definitions.
3. `build.yml` defines the build automation workflow.
4. `ci.yml.jinja` is a templated CI workflow rendered into the generated project.
5. `github-labeler.yml` automates synchronization of labels from `labels.yml`.
6. `release.yml` defines release automation workflow steps.
7. `labels.yml` defines standardized GitHub issue and PR labels.

## .vscode/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
+   .vscode/  # (1)
+   ├── extensions.json  # (2)
+   ├── launch.json  # (3)
+   └── settings.json  # (4)
```

1. `.vscode/` is the workspace editor-configuration directory; only `able-workflow-copier` adds this template subtree.
2. `.vscode/extensions.json` recommends extensions for a consistent development setup.
3. `.vscode/launch.json` defines local debug launch configurations.
4. `.vscode/settings.json` stores workspace defaults for formatting and analysis behavior.

## config/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
+** config/  # (1)
 ** ├── {{ module_type }}/  # (2)
 ** │   └── {{ module_name }}/  # (3)
  * │       ├── {{ etl_name }}/  # (4)
  * │       │   └── config.yaml.jinja  # (5)
 *  │       └── config.yaml.jinja  # (6)
+   ├── config.local.example.yaml  # (7)
+   ├── config.yaml.jinja  # (8)
+   └── README.md.jinja  # (9)
```

1. `config/` is present in the base project template and extended by module and ETL templates.
2. `{{ module_type }}/` is created by module and ETL templates; it resolves to one of `datasets`, `features`, or `models`.
3. `{{ module_name }}/` stores module-specific configuration under the selected module type.
4. `{{ etl_name }}/` is added by the ETL template beneath the module directory.
5. `{{ etl_name }}/config.yaml.jinja` is the ETL-specific configuration template file added by the ETL template.
6. `config.yaml.jinja` under `{{ module_name }}/` is the module-level configuration template file added by the module template.
7. `config.local.example.yaml` is the base local-override example configuration file.
8. `config.yaml.jinja` at the root of `config/` is the base project configuration template.
9. `README.md.jinja` documents the `config/` directory conventions.

## data/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
+   data/  # (1)
    ├── external/  # (2)
    ├── interim/  # (3)
    ├── processed/  # (4)
    ├── raw/  # (5)
+   ├── tests/  # (6)
+   │   ├── dry-run/  # (7)
+   │   │   ├── all.yaml  # (8)
+   │   │   └── common.yaml  # (9)
+   │   └── README.md  # (10)
+   └── README.md  # (11)
```

1. `data/` is the template data root; only `able-workflow-copier` adds this subtree.
2. `external/` stores data copied from external sources in non-standard formats; it is created by users in generated projects and is not committed to git.
3. `interim/` stores temporary data between workflow steps; it is created by users in generated projects and is not committed to git.
4. `processed/` stores processed data ready for reporting, feature extraction, or modeling; it is created by users in generated projects and is not committed to git.
5. `raw/` stores raw data in a standardized format; it is created by users in generated projects and is not committed to git.
6. `tests/` contains test fixture material used by workflow and dry-run tests.
7. `tests/dry-run/` stores expected dry-run YAML fixture sets.
8. `all.yaml` is a dry-run fixture covering the full workflow rule set.
9. `common.yaml` is a dry-run fixture containing shared/common rule expectations.
10. `tests/README.md` documents how data test fixtures are organized and used.
11. `data/README.md` documents the top-level data directory conventions.

## docs/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
+*** docs/  # (1)
+   ├── _gen-files-scripts/  # (2)
+   │   └── render_summaries.py  # (3)
+***├── docs/  # (4)
+   │   ├── _images/  # (5)
+   │   │   └── logo.png  # (6)
+   │   ├── _js/  # (7)
+   │   │   ├── mathjax.js  # (8)
+   │   │   └── svg-pan-zoom-init.js  # (9)
+***│   ├── contributing/  # (10)
+***│   │   ├── templates/  # (11)
+   │   │   │   ├── datasets/  # (12)
+   │   │   │   │   ├── index.md.jinja  # (13)
+   │   │   │   │   └── SUMMARY.md  # (14)
+   │   │   │   ├── features/  # (15)
+   │   │   │   │   ├── index.md.jinja  # (16)
+   │   │   │   │   └── SUMMARY.md  # (17)
+   │   │   │   ├── models/  # (18)
+   │   │   │   │   ├── index.md.jinja  # (19)
+   │   │   │   │   └── SUMMARY.md  # (20)
  + │   │   │   ├── module-{{ module_type }}-{{ module_name }}/  # (21)
  + │   │   │   │   └── etl-{{ etl_name }}/  # (22)
  + │   │   │   │       ├── index.md.jinja  # (23)
  + │   │   │   │       └── SUMMARY.md  # (24)
 +  │   │   │   ├── {{ module_type }}/  # (25)
 +  │   │   │   │   └── {{ module_name }}/  # (26)
 +  │   │   │   │       ├── index.md.jinja  # (27)
 +  │   │   │   │       └── SUMMARY.md  # (28)
+   │   │   │   ├── index.md.jinja  # (29)
   +│   │   │   ├── rule-{{ rule_name }}.md.jinja  # (30)
+   │   │   │   └── SUMMARY.md  # (31)
+   │   │   ├── ci.md  # (32)
+   │   │   ├── docs.md  # (33)
+   │   │   ├── index.md.jinja  # (34)
+   │   │   ├── python-package.md.jinja  # (35)
+   │   │   ├── SUMMARY.md  # (36)
+   │   │   ├── tests.md.jinja  # (37)
+   │   │   ├── vscode.md  # (38)
+   │   │   └── workflow.md.jinja  # (39)
+   │   ├── datasets/  # (40)
+   │   │   ├── index.md  # (41)
+   │   │   └── SUMMARY.md  # (42)
+   │   ├── features/  # (43)
+   │   │   ├── index.md  # (44)
+   │   │   └── SUMMARY.md  # (45)
+   │   ├── models/  # (46)
+   │   │   ├── index.md  # (47)
+   │   │   └── SUMMARY.md  # (48)
+   │   ├── overview/  # (49)
+   │   │   ├── best-practices.md  # (50)
+   │   │   ├── index.md.jinja  # (51)
+   │   │   ├── motivation.md  # (52)
+   │   │   ├── structure.md.jinja  # (53)
+   │   │   ├── SUMMARY.md  # (54)
+   │   │   ├── tree.md  # (55)
+   │   │   ├── tree.snippet.md  # (56)
+   │   ├── setup/  # (58)
+   │   │   ├── index.md.jinja  # (59)
+   │   │   ├── linux.md  # (60)
+   │   │   ├── slurm.md  # (61)
+   │   │   ├── SUMMARY.md  # (62)
+   │   │   └── windows.md  # (63)
+   │   ├── workflow/  # (64)
+   │   │   ├── config.md  # (65)
+   │   │   ├── index.md  # (66)
+   │   │   ├── rules.md.jinja  # (67)
+   │   │   └── SUMMARY.md  # (68)
 +* │   ├── {{ module_type }}/  # (69)
 +* │   │   └── {{ module_name }}/  # (70)
  + │   │       ├── {{ etl_name }}/  # (71)
  + │   │       │   ├── config.md.jinja  # (72)
  + │   │       │   ├── index.md.jinja  # (73)
  + │   │       │   ├── schema.md.jinja  # (74)
  + │   │       │   └── SUMMARY.md  # (75)
 +  │   │       ├── config.md.jinja  # (76)
 +  │   │       ├── index.md.jinja  # (77)
 +  │   │       └── SUMMARY.md  # (78)
+   │   ├── index.md.jinja  # (79)
+   │   └── SUMMARY.md  # (80)
+   ├── gen_ref_pages.py.jinja  # (81)
+   ├── mkdocs.yml.jinja  # (82)
+   └── README.md.jinja  # (83)
```

1. `docs/` is the template documentation root; all four templates touch this subtree.
2. `_gen-files-scripts/` contains helper scripts for documentation generation.
3. `render_summaries.py` rebuilds summary/navigation files used by docs pages.
4. `docs/docs/` is the MkDocs content root and is extended by module, ETL, and rule templates.
5. `_images/` stores static image assets for the documentation site.
6. `logo.png` is the main logo image referenced in documentation pages.
7. `_js/` stores JavaScript assets used by docs pages.
8. `mathjax.js` configures MathJax behavior for rendered documentation.
9. `svg-pan-zoom-init.js` initializes SVG pan/zoom behavior in docs pages.
10. `contributing/` contains contributor guidance and template-development docs.
11. `contributing/templates/` documents template-specific contribution flows and is touched by all four templates.
12. `contributing/templates/datasets/` stores base docs for dataset template contributions.
13. `contributing/templates/datasets/index.md.jinja` is the datasets contribution landing-page template.
14. `contributing/templates/datasets/SUMMARY.md` is the datasets contribution nav summary.
15. `contributing/templates/features/` stores base docs for feature template contributions.
16. `contributing/templates/features/index.md.jinja` is the features contribution landing-page template.
17. `contributing/templates/features/SUMMARY.md` is the features contribution nav summary.
18. `contributing/templates/models/` stores base docs for model template contributions.
19. `contributing/templates/models/index.md.jinja` is the models contribution landing-page template.
20. `contributing/templates/models/SUMMARY.md` is the models contribution nav summary.
21. `contributing/templates/module-{{ module_type }}-{{ module_name }}/` is the ETL template contribution-doc namespace for a selected module.
22. `etl-{{ etl_name }}/` scopes ETL-specific contribution docs under the selected module.
23. `etl-{{ etl_name }}/index.md.jinja` is the ETL contribution landing-page template.
24. `etl-{{ etl_name }}/SUMMARY.md` is the ETL contribution nav summary.
25. `contributing/templates/{{ module_type }}/` is the module template contribution-doc namespace for the selected module type.
26. `{{ module_name }}/` scopes module-specific contribution docs under the selected module type.
27. `{{ module_name }}/index.md.jinja` is the module contribution landing-page template.
28. `{{ module_name }}/SUMMARY.md` is the module contribution nav summary.
29. `contributing/templates/index.md.jinja` is the base templates-contributing landing-page template.
30. `rule-{{ rule_name }}.md.jinja` is the rule template contribution guide added by `able-workflow-rule-copier`.
31. `contributing/templates/SUMMARY.md` is the base templates-contributing nav summary.
32. `contributing/ci.md` documents CI expectations for template and project docs changes.
33. `contributing/docs.md` documents conventions for writing and organizing docs content.
34. `contributing/index.md.jinja` is the contributing section landing-page template.
35. `contributing/python-package.md.jinja` documents Python package contribution patterns.
36. `contributing/SUMMARY.md` is the contributing section nav summary.
37. `contributing/tests.md.jinja` documents testing expectations for template and generated-project changes.
38. `contributing/vscode.md` documents VS Code configuration and workflow guidance.
39. `contributing/workflow.md.jinja` documents Snakemake workflow contribution guidance.
40. `datasets/` contains base datasets documentation pages.
41. `datasets/index.md` is the base datasets documentation landing page.
42. `datasets/SUMMARY.md` is the datasets section nav summary.
43. `features/` contains base features documentation pages.
44. `features/index.md` is the base features documentation landing page.
45. `features/SUMMARY.md` is the features section nav summary.
46. `models/` contains base models documentation pages.
47. `models/index.md` is the base models documentation landing page.
48. `models/SUMMARY.md` is the models section nav summary.
49. `overview/` contains high-level project and template overview documentation.
50. `overview/best-practices.md` lists implementation and maintenance best practices.
51. `overview/index.md.jinja` is the overview landing-page template.
52. `overview/motivation.md` explains motivation and background for the workflow templates.
53. `overview/structure.md.jinja` describes project structure and generated layout behavior.
54. `overview/SUMMARY.md` is the overview section nav summary.
55. `overview/tree.md` contains the project tree documentation page that includes this snippet.
56. `overview/tree.snippet.md` is the embedded tree snippet used by the overview tree page.
57. `setup/` contains environment/setup instructions.
58. `setup/index.md.jinja` is the setup section landing-page template.
59. `setup/linux.md` documents Linux setup instructions.
60. `setup/slurm.md` documents Slurm/HPC setup guidance.
61. `setup/SUMMARY.md` is the setup section nav summary.
62. `setup/windows.md` documents Windows setup instructions.
63. `workflow/` contains workflow-specific documentation pages.
64. `workflow/config.md` documents workflow configuration structure and behavior.
65. `workflow/index.md` is the workflow docs landing page.
66. `workflow/rules.md.jinja` is the workflow-rules documentation template.
67. `workflow/SUMMARY.md` is the workflow section nav summary.
68. `{{ module_type }}/` is created by `able-workflow-module-copier` and extended by `able-workflow-etl-copier`.
69. `{{ module_name }}/` scopes module docs under the selected module type and is extended by ETL docs.
70. `{{ etl_name }}/` is the ETL docs namespace added by `able-workflow-etl-copier`.
71. `{{ etl_name }}/config.md.jinja` is the ETL config documentation template.
72. `{{ etl_name }}/index.md.jinja` is the ETL docs landing-page template.
73. `{{ etl_name }}/schema.md.jinja` is the ETL schema documentation template.
74. `{{ etl_name }}/SUMMARY.md` is the ETL docs nav summary.
75. `{{ module_name }}/config.md.jinja` is the module config documentation template.
76. `{{ module_name }}/index.md.jinja` is the module docs landing-page template.
77. `{{ module_name }}/SUMMARY.md` is the module docs nav summary.
78. `docs/index.md.jinja` is the overall docs-site landing-page template.
79. `docs/SUMMARY.md` is the primary literate-nav summary for the docs site.
80. `gen_ref_pages.py.jinja` is the template for reference-page generation scripting.
81. `mkdocs.yml.jinja` is the template for MkDocs site configuration.
82. `README.md.jinja` documents the docs template directory and usage.

## hooks/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
+   hooks/  # (1)
+   ├── README.md  # (2)
+   └── snakemake_pyproject2conda.py.jinja  # (3)
```

1. `hooks/` is the hook-template directory; only `able-workflow-copier` creates this subtree under `template/`.
2. `README.md` documents hook purpose and usage expectations.
3. `snakemake_pyproject2conda.py.jinja` is the hook script template that syncs pyproject dependencies into Conda environment specifications.

## features/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  features/
 +  ├── {{ module_name }}/
 +  │   └── README.md
 +  └── README.md
```

1. `features/README.md` defines conventions for organizing feature outputs.
2. `features/{{ module_name }}/README.md` is the module-specific landing page for feature artifacts.

## logs/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  logs/
 +  └── rules/
 +      └── README.md
```

1. `logs/rules/README.md` documents where rule logs are written and how to inspect failures.

## models/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  models/
 +  ├── {{ module_name }}/
 +  │   └── README.md
 +  └── README.md
```

1. `models/README.md` describes conventions for model outputs and artifacts.
2. `models/{{ module_name }}/README.md` captures module-specific model documentation.

## notebooks/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  notebooks/
 +  └── README.md
```

1. `notebooks/README.md` documents notebook storage, naming, and maintenance expectations.

## references/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  references/
 +  └── README.md
```

1. `references/README.md` is the location for external links, citations, and source metadata notes.

## reports/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
 +  reports/
 +  ├── datasets/
 +  │   ├── {{ module_name }}/README.md
 +  │   └── .gitkeep
 +  ├── features/
 +  │   ├── {{ module_name }}/README.md
 +  │   └── .gitkeep
 +  ├── models/
 +  │   ├── {{ module_name }}/README.md
 +  │   └── .gitkeep
 +  └── notebook_templates/
 +      ├── datasets/{{ module_name }}/README.md
 +      ├── features/{{ module_name }}/README.md
 +      └── models/{{ module_name }}/README.md
```

1. `reports/datasets/{{ module_name }}/README.md`, `reports/features/{{ module_name }}/README.md`, and `reports/models/{{ module_name }}/README.md` describe expected report outputs.
2. `reports/notebook_templates/*/{{ module_name }}/README.md` files define starter notebook report templates.

## scripts/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
+   scripts/  # (1)
+   └── copier-check-update.sh  # (2)
```

1. `scripts/` is the project utility-scripts directory; only `able-workflow-copier` creates this subtree under `template/`.
2. `copier-check-update.sh` checks for upstream Copier template updates and supports template maintenance workflows.

## {{ package_name }}/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
+** {{ package_name }}/  # (1)
+   ├── datasets/  # (2)
+   │   └── __init__.py  # (3)
+   ├── features/  # (4)
+   │   └── __init__.py  # (5)
+   ├── models/  # (6)
+   │   └── __init__.py  # (7)
+   ├── utils/  # (8)
+   │   ├── logging/  # (9)
+   │   │   ├── runner/  # (10)
+   │   │   │   └── test_logging.py.jinja  # (11)
+   │   │   ├── __init__.py  # (12)
+   │   │   └── logging.py  # (13)
+   │   └── __init__.py  # (14)
 +* ├── {{ module_type }}/  # (15)
 +* │   └── {{ module_name }}/  # (16)
  + │       ├── {{ etl_name }}/  # (17)
  + │       │   ├── runner/  # (18)
  + │       │   │   ├── __init__.py  # (19)
  + │       │   │   ├── {% if requires_extract_external %}extract_external.py{% endif %}.jinja  # (20)
  + │       │   │   ├── load.py.jinja  # (21)
  + │       │   │   ├── main.py.jinja  # (22)
  + │       │   │   ├── {% if requires_extract_external %}schema_external.py{% endif %}.jinja  # (23)
  + │       │   │   └── transform.py.jinja  # (24)
  + │       │   ├── __init__.py.jinja  # (25)
  + │       │   ├── extract.py.jinja  # (26)
  + │       │   └── schema.py  # (27)
 +  │       └── __init__.py.jinja  # (28)
+   ├── __init__.py.jinja  # (29)
+   └── config.py.jinja  # (30)
```

1. `{{ package_name }}/` is created by `able-workflow-copier` and extended by module and ETL templates.
2. `datasets/` is the base datasets namespace in the package template.
3. `datasets/__init__.py` initializes the datasets package namespace.
4. `features/` is the base features namespace in the package template.
5. `features/__init__.py` initializes the features package namespace.
6. `models/` is the base models namespace in the package template.
7. `models/__init__.py` initializes the models package namespace.
8. `utils/` contains shared package utilities.
9. `utils/logging/` contains logging-specific utilities.
10. `utils/logging/runner/` contains logging runner test helpers.
11. `utils/logging/runner/test_logging.py.jinja` is the template for logging utility tests.
12. `utils/logging/__init__.py` initializes the logging utilities namespace.
13. `utils/logging/logging.py` implements shared logging helpers.
14. `utils/__init__.py` initializes the top-level utils namespace.
15. `{{ module_type }}/` is created by `able-workflow-module-copier` and extended by `able-workflow-etl-copier`.
16. `{{ module_name }}/` scopes module code under the selected module type and is extended by ETL template content.
17. `{{ etl_name }}/` is the ETL package namespace added by `able-workflow-etl-copier`.
18. `runner/` contains ETL runner implementation files.
19. `runner/__init__.py` initializes the ETL runner namespace.
20. `runner/{% if requires_extract_external %}extract_external.py{% endif %}.jinja` conditionally adds external extract logic when external extraction is required.
21. `runner/load.py.jinja` is the ETL load-step implementation template.
22. `runner/main.py.jinja` is the ETL runner entry-point template.
23. `runner/{% if requires_extract_external %}schema_external.py{% endif %}.jinja` conditionally adds external schema handling when external extraction is required.
24. `runner/transform.py.jinja` is the ETL transform-step implementation template.
25. `{{ etl_name }}/__init__.py.jinja` initializes the ETL package namespace.
26. `{{ etl_name }}/extract.py.jinja` is the ETL extract-step implementation template.
27. `{{ etl_name }}/schema.py` defines ETL schema logic.
28. `{{ module_name }}/__init__.py.jinja` initializes the module namespace added by `able-workflow-module-copier`.
29. `__init__.py.jinja` initializes the root package namespace.
30. `config.py.jinja` provides package configuration loading helpers.

## tests/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
+*** tests/  # (1)
+ * ├── {{ package_name }}/  # (2)
+   │   ├── datasets/  # (3)
+   │   │   └── __init__.py  # (4)
+   │   ├── features/  # (5)
+   │   │   └── __init__.py  # (6)
+   │   ├── models/  # (7)
+   │   │   └── __init__.py  # (8)
+   │   ├── utils/  # (9)
+   │   │   ├── logging/  # (10)
+   │   │   │   ├── __init__.py  # (11)
+   │   │   │   └── test_logging.py.jinja  # (12)
+   │   │   ├── runner/  # (13)
+   │   │   │   ├── __init__.py  # (14)
+   │   │   │   └── test_runner_extras.py  # (15)
+   │   │   └── __init__.py  # (16)
+  + │   ├── {{ module_type }}/  # (17)
+  + │   │   └── {{ module_name }}/  # (18)
+  + │   │       ├── {{ etl_name }}/  # (19)
+  + │   │       │   ├── runner/  # (20)
+  + │   │       │   │   ├── __init__.py  # (21)
+  + │   │       │   │   ├── {% if requires_extract_external %}test_extract_external.py{% endif %}.jinja  # (22)
+  + │   │       │   │   ├── {% if requires_extract_external %}test_schema_external.py{% endif %}.jinja  # (23)
+  + │   │       │   │   ├── test_load.py  # (24)
+  + │   │       │   │   ├── test_main.py.jinja  # (25)
+  + │   │       │   │   └── test_transform.py  # (26)
+  + │   │       │   ├── __init__.py  # (27)
+  + │   │       │   ├── test_extract.py  # (28)
+  + │   │       │   └── test_schema.py  # (29)
+  + │   │       └── __init__.py  # (30)
++   │   ├── __init__.py  # (31)
++   │   └── README.md.jinja  # (32)
+***├── workflow/  # (33)
+***│   ├── rules/  # (34)
+ +* │   │   ├── {{ module_type }}/  # (35)
+ +* │   │   │   └── {{ module_name }}/  # (36)
+ +  │   │   │       ├── __init__.py  # (37)
+ +  │   │   │       ├── test_snakemake_invalid_config.py  # (38)
+  + │   │   │       └── test_snakemake_{{ etl_name }}.py.jinja  # (39)
++   │   │   ├── __init__.py  # (40)
++   │   │   ├── conftest.py.jinja  # (41)
++   │   │   ├── README.md  # (42)
++   │   │   ├── test_snakemake_all_data.py  # (43)
++   │   │   ├── test_snakemake_all_data_imported_empty_config.py  # (44)
++   │   │   ├── test_snakemake_dag_svg.py  # (45)
++   │   │   ├── test_snakemake_docs.py  # (46)
++   │   │   ├── test_snakemake_invalid_config.py  # (47)
+   +│   │   └── test_snakemake_{{ rule_name }}.py.jinja  # (48)
++  *│   ├── scripts/  # (49)
++   │   │   ├── rules_conda_CORE/  # (50)
++   │   │   │   ├── __init__.py  # (51)
++   │   │   │   └── test_placeholder.py  # (52)
++   │   │   ├── rules_conda_DOCS/  # (53)
++   │   │   │   ├── __init__.py  # (54)
++   │   │   │   └── test_dag_svg.py  # (55)
++   │   │   ├── rules_conda_RUNNER/  # (56)
++   │   │   │   ├── __init__.py  # (57)
++  +│   │   │   ├── test_{{ rule_name }}.py.jinja  # (69)
++   │   │   │   └── test_{{ package_name }}_rules.py.jinja  # (58)
++   │   │   ├── rules_global/  # (59)
++   │   │   │   ├── __init__.py  # (60)
++  +│   │   │   ├── test_{{ rule_name }}.py.jinja  # (73)
++   │   │   │   ├── test_conda_localize_file.py.jinja  # (61)
++   │   │   │   ├── test_config_schema_validity.py  # (62)
++   │   │   │   ├── test_log_config.py.jinja  # (63)
++   │   │   │   └── test_pyproject2conda.py  # (64)
++   │   │   ├── utils/  # (65)
++   │   │   │   └── __init__.py  # (66)
++   │   │   ├── __init__.py  # (67)
++   │   │   └── README.md.jinja  # (68)
++   │   └── __init__.py  # (70)
++   ├── __init__.py  # (71)
++   └── conftest.py  # (72)
```

1. `tests/` is created by `able-workflow-copier` and extended by module, ETL, and rule templates.
2. `{{ package_name }}/` is the package-unit-test namespace created by base template and extended by ETL tests.
3. `datasets/` contains dataset package unit tests.
4. `datasets/__init__.py` initializes the datasets test namespace.
5. `features/` contains feature package unit tests.
6. `features/__init__.py` initializes the features test namespace.
7. `models/` contains model package unit tests.
8. `models/__init__.py` initializes the models test namespace.
9. `utils/` contains utility-focused unit tests.
10. `utils/logging/` contains logging utility tests.
11. `utils/logging/__init__.py` initializes the logging test namespace.
12. `utils/logging/test_logging.py.jinja` is the template for logging utility tests.
13. `utils/runner/` contains runner utility tests.
14. `utils/runner/__init__.py` initializes the runner test namespace.
15. `utils/runner/test_runner_extras.py` tests runner helper extras.
16. `utils/__init__.py` initializes the utils test namespace.
17. `{{ module_type }}/` is ETL-added unit-test namespace for the selected module type.
18. `{{ module_name }}/` scopes ETL unit tests to the selected module.
19. `{{ etl_name }}/` is the ETL-specific unit-test namespace.
20. `runner/` contains ETL runner unit tests.
21. `runner/__init__.py` initializes ETL runner tests.
22. `runner/{% if requires_extract_external %}test_extract_external.py{% endif %}.jinja` conditionally adds external extract tests.
23. `runner/{% if requires_extract_external %}test_schema_external.py{% endif %}.jinja` conditionally adds external schema tests.
24. `runner/test_load.py` tests ETL load behavior.
25. `runner/test_main.py.jinja` is the template for ETL main-runner tests.
26. `runner/test_transform.py` tests ETL transform behavior.
27. `{{ etl_name }}/__init__.py` initializes ETL test namespace.
28. `{{ etl_name }}/test_extract.py` tests ETL extract behavior.
29. `{{ etl_name }}/test_schema.py` tests ETL schema behavior.
30. `{{ module_name }}/__init__.py` initializes the module test namespace in ETL tests.
31. `{{ package_name }}/__init__.py` initializes package test namespace.
32. `{{ package_name }}/README.md.jinja` documents package-test layout and conventions.
33. `workflow/` contains workflow-level tests and script tests, and is touched by all templates.
34. `workflow/rules/` contains Snakemake rule tests and shared fixtures.
35. `workflow/rules/{{ module_type }}/` is module/ETL rule-test namespace.
36. `workflow/rules/{{ module_type }}/{{ module_name }}/` scopes rule tests for the selected module.
37. `workflow/rules/{{ module_type }}/{{ module_name }}/__init__.py` initializes module-scoped rule tests.
38. `workflow/rules/{{ module_type }}/{{ module_name }}/test_snakemake_invalid_config.py` tests invalid-config behavior for module-scoped rules.
39. `workflow/rules/{{ module_type }}/{{ module_name }}/test_snakemake_{{ etl_name }}.py.jinja` is the ETL rule-test template.
40. `workflow/rules/__init__.py` initializes the workflow rules test namespace.
41. `workflow/rules/conftest.py.jinja` is the template for shared pytest fixtures in workflow rule tests.
42. `workflow/rules/README.md` documents workflow rule test organization.
43. `workflow/rules/test_snakemake_all_data.py` tests all-data rule execution behavior.
44. `workflow/rules/test_snakemake_all_data_imported_empty_config.py` tests all-data behavior with imported empty config.
45. `workflow/rules/test_snakemake_dag_svg.py` tests DAG SVG generation behavior.
46. `workflow/rules/test_snakemake_docs.py` tests documentation rule behavior.
47. `workflow/rules/test_snakemake_invalid_config.py` tests invalid-config handling for base workflow rules.
48. `workflow/rules/test_snakemake_{{ rule_name }}.py.jinja` is the rule-copier rule-test template.
49. `workflow/scripts/` contains unit tests for workflow helper scripts and is extended by rule template.
50. `workflow/scripts/rules_conda_CORE/` contains tests for scripts that run in the CORE Conda environment.
51. `rules_conda_CORE/__init__.py` initializes CORE script test namespace.
52. `rules_conda_CORE/test_placeholder.py` is a placeholder CORE script test.
53. `workflow/scripts/rules_conda_DOCS/` contains tests for scripts that run in the DOCS Conda environment.
54. `rules_conda_DOCS/__init__.py` initializes DOCS script test namespace.
55. `rules_conda_DOCS/test_dag_svg.py` tests DOCS-environment DAG SVG script behavior.
56. `workflow/scripts/rules_conda_RUNNER/` contains tests for scripts that run in the RUNNER Conda environment.
57. `rules_conda_RUNNER/__init__.py` initializes RUNNER script test namespace.
58. `rules_conda_RUNNER/test_{{ package_name }}_rules.py.jinja` is the template for RUNNER script tests.
59. `workflow/scripts/rules_global/` contains tests for scripts executed in the global Snakemake environment.
60. `rules_global/__init__.py` initializes global script test namespace.
61. `rules_global/test_conda_localize_file.py.jinja` templates tests for conda-localization behavior.
62. `rules_global/test_config_schema_validity.py` tests configuration schema validity checks.
63. `rules_global/test_log_config.py.jinja` templates tests for logging configuration behavior.
64. `rules_global/test_pyproject2conda.py` tests pyproject-to-conda conversion behavior.
65. `workflow/scripts/utils/` contains shared helpers for script tests.
66. `workflow/scripts/utils/__init__.py` initializes script-test utilities namespace.
67. `workflow/scripts/__init__.py` initializes workflow scripts test namespace.
68. `workflow/scripts/README.md.jinja` documents workflow scripts test layout.
69. {% raw %}`{% if not uses_conda %}rules_global{% else %}rules_conda_{{ conda_env_key }}{% endif %}{{ _copier_conf.sep }}test_{{ rule_name }}.py.jinja`{% endraw %} conditionally adds rule-copier script tests in global or rule-specific conda namespace.
70. `workflow/__init__.py` initializes workflow test namespace.
71. `tests/__init__.py` initializes the top-level tests package.
72. `tests/conftest.py` provides shared top-level pytest fixtures.
73. {% raw %}`{% if not uses_conda %}rules_global{% else %}rules_conda_{{ conda_env_key }}{% endif %}{{ _copier_conf.sep }}test_{{ rule_name }}.py.jinja`{% endraw %} conditionally adds rule-copier script tests in global or rule-specific conda namespace.

## workflow/

```yaml
┌───── [1] able-workflow-copier
│┌──── [2] able-workflow-module-copier
││┌─── [3] able-workflow-etl-copier
│││┌── [4] able-workflow-rule-copier
││││
+*** workflow/  # (1)
+   ├── envs/  # (2)
+   │   ├── {{ package_name }}-py312-tox.yaml  # (3)
+   │   └── {{ package_name }}-py312-workflow.yaml  # (4)
+** ├── profiles/  # (5)
+** │   ├── default/  # (6)
+** │   │   └── config.yaml  # (7)
+   │   └── slurm/  # (8)
+   │       └── config.yaml  # (9)
+***├── rules/  # (10)
+   │   ├── datasets/  # (11)
+   │   │   └── .gitkeep  # (12)
+   │   ├── features/  # (13)
+   │   │   └── .gitkeep  # (14)
+   │   ├── models/  # (15)
+   │   │   └── .gitkeep  # (16)
 +* │   ├── {{ module_type }}/  # (17)
 +* │   │   └── {{ module_name }}/  # (18)
  + │   │       └── {{ etl_name }}.smk.jinja  # (19)
 +  │   ├── {{ module_name }}.smk.jinja  # (20)
+   │   ├── build.smk.jinja  # (21)
+   │   ├── dev.smk  # (22)
+   │   ├── docs.smk.jinja  # (23)
+   │   ├── docs_dag_svg.smk  # (24)
+***│   ├── includes.smk  # (25)
+   │   ├── reports.smk  # (26)
+   │   ├── utils.smk.jinja  # (27)
   +│   └── {{ smk_file_name }}.jinja  # (28)
+** ├── schemas/  # (29)
 +* │   ├── {{ module_type }}/  # (30)
 +* │   │   └── {{ module_name }}/  # (31)
  + │   │       ├── {{ etl_name }}/  # (32)
  + │   │       │   └── config.schema.yaml.jinja  # (33)
 +  │   │       └── config.schema.yaml.jinja  # (34)
+   │   └── config.schema.yaml.jinja  # (35)
+  *├── scripts/  # (36)
+   │   ├── rules_conda_DOCS/  # (37)
+   │   │   └── dag_svg.py.jinja  # (38)
+   │   ├── rules_conda_RUNNER/  # (39)
+   │   │   ├── __init__.py  # (40)
   +│   │   ├── {{ rule_name }}.py.jinja  # (49)
+   │   │   └── {{ package_name }}_rules.py.jinja  # (41)
+   │   ├── rules_global/  # (42)
+   │   │   ├── __init__.py  # (43)
   +│   │   ├── {{ rule_name }}.py.jinja  # (51)
+   │   │   ├── conda_localize_file.py.jinja  # (44)
+   │   │   ├── log_config.py  # (45)
+   │   │   └── pyproject2conda.py  # (46)
+   │   ├── utils/  # (47)
+   │   │   └── __init__.py  # (48)
+   └── Snakefile.jinja  # (50)
```

1. `workflow/` is created by `able-workflow-copier` and extended by module, ETL, and rule templates.
2. `envs/` contains base workflow Conda environment definitions.
3. `{{ package_name }}-py312-tox.yaml` is the tox-focused workflow environment definition.
4. `{{ package_name }}-py312-workflow.yaml` is the primary runtime workflow environment definition.
5. `profiles/` is created by base template and extended by module and ETL templates.
6. `profiles/default/` stores default Snakemake profile configuration.
7. `profiles/default/config.yaml` defines default profile execution settings.
8. `profiles/slurm/` stores Slurm-specific Snakemake profile configuration.
9. `profiles/slurm/config.yaml` defines Slurm profile execution settings.
10. `rules/` is created by base template and extended by module, ETL, and rule templates.
11. `rules/datasets/` is the datasets rules namespace scaffold.
12. `rules/datasets/.gitkeep` preserves the datasets rules directory when empty.
13. `rules/features/` is the features rules namespace scaffold.
14. `rules/features/.gitkeep` preserves the features rules directory when empty.
15. `rules/models/` is the models rules namespace scaffold.
16. `rules/models/.gitkeep` preserves the models rules directory when empty.
17. `rules/{{ module_type }}/` is created by module template and extended by ETL template.
18. `rules/{{ module_type }}/{{ module_name }}/` scopes rules to the selected module.
19. `{{ etl_name }}.smk.jinja` is the ETL rule file template added by `able-workflow-etl-copier`.
20. `{{ module_name }}.smk.jinja` is the module-level rule template added by `able-workflow-module-copier`.
21. `build.smk.jinja` is the base build rule template.
22. `dev.smk` contains base development workflow rules.
23. `docs.smk.jinja` is the base documentation rules template.
24. `docs_dag_svg.smk` contains base DAG SVG rule wiring.
25. `includes.smk` is the shared include-aggregation file touched by all four templates.
26. `reports.smk` contains base reporting rule wiring.
27. `utils.smk.jinja` is the base utility-rules template.
28. `{% if module_type == 'none' %}{{ smk_file_name }}{% endif %}.jinja` is a rule-template file added by `able-workflow-rule-copier` when no module type is used.
29. `schemas/` is created by base template and extended by module and ETL templates.
30. `schemas/{{ module_type }}/` is created by module template and extended by ETL template.
31. `schemas/{{ module_type }}/{{ module_name }}/` scopes schemas to the selected module.
32. `schemas/{{ module_type }}/{{ module_name }}/{{ etl_name }}/` is the ETL schema namespace added by `able-workflow-etl-copier`.
33. `{{ etl_name }}/config.schema.yaml.jinja` is the ETL configuration schema template.
34. `{{ module_name }}/config.schema.yaml.jinja` is the module configuration schema template.
35. `schemas/config.schema.yaml.jinja` is the base top-level workflow configuration schema template.
36. `scripts/` is created by base template and extended by `able-workflow-rule-copier`.
37. `scripts/rules_conda_DOCS/` contains scripts that run in the DOCS Conda environment.
38. `rules_conda_DOCS/dag_svg.py.jinja` templates DAG SVG script behavior for docs generation.
39. `scripts/rules_conda_RUNNER/` contains scripts that run in the RUNNER Conda environment.
40. `rules_conda_RUNNER/__init__.py` initializes the runner scripts namespace.
41. `rules_conda_RUNNER/{{ package_name }}_rules.py.jinja` templates package-specific runner rule helpers.
42. `scripts/rules_global/` contains scripts that run in the global Snakemake environment.
43. `rules_global/__init__.py` initializes the global scripts namespace.
44. `rules_global/conda_localize_file.py.jinja` templates environment-localization logic for generated workflows.
45. `rules_global/log_config.py` provides base log configuration helpers for workflow scripts.
46. `rules_global/pyproject2conda.py` converts pyproject dependency declarations into Conda-compatible definitions.
47. `scripts/utils/` contains shared workflow script utilities.
48. `scripts/utils/__init__.py` initializes workflow script utilities namespace.
49. {% raw %}`{% if not uses_conda %}rules_global{% else %}rules_conda_{{ conda_env_key }}{% endif %}{{ _copier_conf.sep }}{{ rule_name }}.py.jinja`{% endraw %} conditionally adds a rule script in global or Conda-scoped namespace from `able-workflow-rule-copier`.
50. `Snakefile.jinja` is the base top-level Snakemake entrypoint template.
51. {% raw %}`{% if not uses_conda %}rules_global{% else %}rules_conda_{{ conda_env_key }}{% endif %}{{ _copier_conf.sep }}{{ rule_name }}.py.jinja`{% endraw %} conditionally adds a rule script in global or Conda-scoped namespace from `able-workflow-rule-copier`.
