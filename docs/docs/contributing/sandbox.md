# A Sandbox to play around with examples

The `.gitignore` file tells git to ignore the entire `sandbox/` project directory.

## Example answer files

!!! note

    These do not contain all the information need to be read as `.copier-answers.yml` file using the `copier copy --answers-file` flag. These files can however be read in as a `dict` using [ruamel.yaml](https://yaml.dev/doc/ruamel.yaml/) and passed to [pytest-copie](https://pytest-copie.readthedocs.io/en/latest/index.html). This is what the scripts below do.

## Helper scripts

??? note "`scripts/sandbox_examples_generate.py`: Generate the examples in the sandbox"

    ```python
    --8<-- "scripts/sandbox_examples_generate.py"
    ```
