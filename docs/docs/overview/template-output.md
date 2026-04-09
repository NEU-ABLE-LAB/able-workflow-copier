# Template Output

## The `able-workflow-copier` repository tree

```yaml
├── .github/
│   ├── workflows/
│   │   └── ci.yml  # (2)
│   └── labels.yml  # (3)
├── .vscode  # (4)
├── docs/  # (5)
│   └── docs/  # (6)
├── extensions/  # (7)
├── hooks/  # (8)
├── includes/  # (9)
├── schemas/  # (10)
├── scripts/  # (11)
├── tasks/  # (12)
├── template/  # (13)
└── tests/  # (14)
```

1. _Configuration file for the `github-labeler` GitHub Action_
2. GitHub Actions workflows for pull requests and automation
3. GitHub Action that maintains issue labels and colors across projects
4. VS Code configuration files
5. MkDocs project directory
6. Documentation markdown and assets
7. `jinja2` extensions used by Copier
8. `pre-commit` hook scripts
9. Copier YAML files that are included in `copier.yml`
10. Custom JSON and YAML schemas for validating Copier answers
11. Helper scripts for development
12. Task scripts run by Copier after template generation
13. The Copier template that gets rendered into a project
14. Tests for the template repository itself

{%
    include-markdown "../../../template/docs/docs/overview/tree.snippet.md"
    heading-offset=1
    rewrite-relative-urls=false
%}
