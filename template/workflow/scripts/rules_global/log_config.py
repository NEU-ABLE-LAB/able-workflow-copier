"""
Write the Snakemake config to log file.
"""

import sys
from typing import TYPE_CHECKING

from loguru import logger
from ruamel.yaml import YAML

if TYPE_CHECKING:  # pragma: no cover
    from snakemake.script import snakemake


def main(smk) -> None:  # type: ignore[no-untyped-def]

    # Setup logging
    logger.remove()
    logger.add(smk.log.loguru)

    # Save the Snakemake config to a YAML file
    yaml = YAML()
    with open(smk.log.config, "w") as config_file:
        yaml.dump(smk.config, config_file)


if __name__ == "__main__":
    try:
        main(snakemake)
    except NameError:
        logger.error(
            "This script is designed to be run as part of a Snakemake workflow. "
            "Please run it through Snakemake."
        )
        sys.exit(0)
