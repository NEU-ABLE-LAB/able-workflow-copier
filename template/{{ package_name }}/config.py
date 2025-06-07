"""
Package-wide configurations
"""

from pathlib import Path

from loguru import logger


def get_project_root() -> Path:
    """
    Get the root directory of the project.

    Returns:
        Path: The resolved path to the project's root directory.
    """
    logger.warning(
        "This function could be deprecated and may be removed in a future version."
    )
    return Path(__file__).resolve().parents[1]


# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass
