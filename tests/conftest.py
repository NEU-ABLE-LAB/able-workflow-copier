import warnings

from loguru import logger

# Forward every WARNING‐level log to the Python warnings subsystem
logger.add(
    warnings.warn,  # the sink
    format="{message}",  # plain message text
    level="WARNING",  # only WARNING and above
    filter=lambda r: r["level"].name == "WARNING",  # safety net
)
