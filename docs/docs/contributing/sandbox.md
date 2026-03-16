# A Sandbox to play around with examples

The `.gitignore` file tells git to ignore the entire `sandbox/` project directory.

## Example answer files

- **`example-answers-able.yml`**: A generic example.
- **`example-answers-weh_interviews.yml`**: This should produce results similar to the [`whole_energy_homes_interviews`](https://github.com/NEU-ABLE-LAB/whole_energy_homes_interviews) project. Use winmerge or a similar program to compare the results in sandbox from this example against a local copy of the `whole_energy_homes_interviews` repo.

!!! note

    These do not contain all the information need to be read as `.copier-answers.yml` file using the `copier copy --answers-file` flag. These files can however be read in as a `dict` using [ruamel.yaml](https://yaml.dev/doc/ruamel.yaml/) and passed to [pytest-copie](https://pytest-copie.readthedocs.io/en/latest/index.html). This is what the scripts below do.

## Helper scripts

??? note "`scripts/sandbox_examples_generate.py`: Generate the examples in the sandbox"

    ```python
    {%
        include "../../../scripts/sandbox_examples_generate.py"
    %}
    ```

After generating the sandbox with the follwoing command:

    ```bash
    python -m scripts.sandbox_examples_generate
    ```

You can then run `cd ./sandbox/example-answers-able` to enter `able` example in the sandbox. To run snakemake, you need to activate

The package requires that it runs within a git repository, so run the following:

    ```bash
    git init
    git add -A
    git commit -m "initial commit"
    ```

In order to run any Snakemake commands, be sure to localize the package path in the Snakemake environment files

    ```bash
    snakemake conda_localize
    ```
