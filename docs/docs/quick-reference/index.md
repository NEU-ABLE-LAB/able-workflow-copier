# Quick Reference

First, [setup the environment](setup.md).

Apply this Copier template to create a new Snakemake workflow with an associated python package with the following commands:

```bash
copier copy --trust {{ able_workflow_copier_repo }}.git ./
```

If this template has been updated and you would like to apply those updates to your project, run the following command. You can see all the Copier templates that have been applied to your project in the `./copier-answers/` directory. (DO NOT EDIT THESE FILES.)

```bash
copier update --trust --answers-file ".copier-answers/project.yml"
```
