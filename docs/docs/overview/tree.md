# Directory tree

- [`able-workflow-copier`]({{ able_workflow_copier_docs }})

## The `able-workflow-copier` project tree

```yaml
├── .github/
│   ├── workflows/
│   │   ├── github-labeler.yml  # (5)
│   │   └── ci.yml  # (1)
│   └── labels.yml  # (6)
├── .vscode  # (2)
├── able-workflow/  # (7)
├── docs/  # (3)
│   └── docs/  #(4)
├── extensions/  # (8)
├── hooks/  # (9)
├── includes/  # (15)
├── schemas/  # (10)
├── scripts/  # (11)
├── tasks/  # (14)
├── template/  # (12)
├── tests/  # (13)
```

1. GitHub action for pull requests
2. VSCode configuration files
3. `mkdocs` documentation directory
4. Documentation markdown and assets
5. GitHub action to maintain consistient GitHub issue labels and colors across projects
6. Configuration file for `github-labeler` GH action
7. Submodules to other `able-workflow-*-copier` projects
8. `jinja2` extensions to be used by `copier`
9. `pre-commit` hook scripts
10. Custom json/yaml schemas for validating Copier answers
11. Helper scripts for development
12. The Copier template to be generated
13. pytest tests to be run. SEE: `tox.ini`
14. Task scripts run by Copier after template generation.
15. Copier yaml files that are included in `copier.yml`

## The `able-workflow` project template tree

{%
    include-markdown "../../../template/docs/docs/overview/tree.snippet.md"
    heading-offset=1
    rewrite-relative-urls=false
%}
