# How to use this workflow and package

TODO-copier-package write overview of what is needed to run the workflow. Point user to separate instructions for setting up the development environment if they plan to edit the workflow or package. Explain `able-workflow-module-copier` and `able-workflow-etl-copier` in a sentence or two to cover the concept of adding to the package and workflow.

TODO-copier-package Explain `conda_localize` rule. Why is it necessary? The environment yamls could pip install from github, but that would mean every commit needs to be pushed in order to test it. The pacakge can't simply be placed in the `workflow/scripts` because Snakemake only copies the script being requested by the `script:` directive, not its dependencies. The environment yaml cannot use a relative path, because when Snakemake makes its cache of the environment, it is in a path that changes based on file hashes.

TODO-copier-package Once sentence explaination about why WSL is required. Point user to Windows setup instructions. Then tell them to follow Linux instructions once WSL is setup.
TODO-copier-package point user to Linux setup instructions.
TODO-copier-package point user to SLURM setup instructions.
