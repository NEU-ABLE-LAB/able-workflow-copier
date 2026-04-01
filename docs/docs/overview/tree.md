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
├── docs/  # (3)
│   └── docs/  #(4)
├── extensions/  # (7)
├── hooks/  # (8)
├── includes/  # (14)
├── schemas/  # (9)
├── scripts/  # (10)
├── tasks/  # (13)
├── template/  # (11)
├── tests/  # (12)
```

1. GitHub action for pull requests
2. VSCode configuration files
3. `mkdocs` documentation directory
4. Documentation markdown and assets
5. GitHub action to maintain consistient GitHub issue labels and colors across projects
6. Configuration file for `github-labeler` GH action
7. `jinja2` extensions to be used by `copier`
8. `pre-commit` hook scripts
9. Custom json/yaml schemas for validating Copier answers
10. Helper scripts for development
11. The Copier template to be generated
12. pytest tests to be run. SEE: `tox.ini`
13. Task scripts run by Copier after template generation.
14. Copier yaml files that are included in `copier.yml`

## The `able-workflow` project template tree

{%
    include-markdown "../../../template/docs/docs/overview/tree.snippet.md"
    heading-offset=1
    rewrite-relative-urls=false
%}
