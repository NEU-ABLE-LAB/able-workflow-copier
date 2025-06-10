"""
Wrapper for the ``pyproject2conda`` rule that runs the converter and logs
its output. Each call generates a single environment file.
"""

import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:  # pragma: no cover
    from snakemake.script import snakemake


def main(smk) -> None:  # type: ignore[no-untyped-def]

    # Parse Snakemake directives
    toml_path = Path(smk.input.toml)
    env_name = smk.params.env_name

    # Setup logging
    logger.remove()
    logger.add(smk.log.loguru)

    Path(smk.output.yaml).parent.mkdir(parents=True, exist_ok=True)

    # Run pyproject2conda, capturing all output in *append* mode.
    with open(smk.log.stdout, "a") as stdout_log:
        subprocess.run(
            [
                "pyproject2conda",
                "project",
                "-f",
                str(toml_path),
                "--envs",
                env_name,
            ],
            check=True,
            stdout=stdout_log,
            stderr=stdout_log,
        )

    logger.info(f"[pyproject2conda] Generated env: {env_name}")


if __name__ == "__main__":
    try:
        main(snakemake)
    except NameError:
        logger.error(
            "This script is designed to be run as part of a Snakemake workflow. "
            "Please run it through Snakemake."
        )
        sys.exit(0)
