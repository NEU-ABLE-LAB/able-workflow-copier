"""
Shared Loguru configuration helpers.

Call :func:`configure_file_logger` in a CLI once, *before* the first
``logger.info``.  It

1. removes existing sinks (avoids duplicate lines when the CLI is reused);
2. binds a *process-wide* ``ctx`` extra field (e.g. Snakemake wildcards);
3. adds a file sink with a human-friendly formatter; and
4. returns the **bound** logger so the caller can shadow the module-level
   ``logger`` without touching other code.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import loguru
from loguru import logger
from tqdm import tqdm


def _serialise_ctx(ctx: str | dict[str, str] | None) -> str:  # noqa: D401
    """Return a *string* representation; fallback to ``"-"`` when absent."""
    if ctx is None:
        return "-"
    if isinstance(ctx, dict):
        return ",".join(f"{k}={v}" for k, v in ctx.items())
    return str(ctx)


# --- Public API -------------------------------------------------------------
def configure_file_logger(
    log_path: Path,
    *,
    context: Any,
    enqueue: bool = True,
    log_level: str = "DEBUG",
) -> loguru.Logger:
    """
    Replace default Loguru sinks with a *context-aware* file sink.

    Parameters
    ----------
    log_path
        Destination log file (created parent dirs automatically).
    context
        Any JSON-serialisable object (usually `str` or `dict`) identifying
        the Snakemake job - printed on every log line via `{extra[ctx]}`.
    enqueue
        `True` enables process-safe queueing - **required** when Snakemake
        runs jobs in parallel.
    log_level
        "DEBUG", "INFO", "WARNING", "ERROR"

    Returns
    -------
    loguru.Logger
        A *bound* logger carrying the `ctx`; assign it to a local name:

            logger = configure_file_logger(path, context=wildcards)
            logger.info("hello")   # every line now shows the wildcards
    """

    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Provide a default for *all* records (even ones emitted before binding).
    logger.configure(extra={"ctx": _serialise_ctx(context)})

    # Wipe previous sinks (avoid duplicate emission)
    logger.remove()

    # Freeze the context for this *process*
    # bound = logger.bind(ctx=_serialise_ctx(context))

    # Add the context to the output format
    # Note: `ctx` is a bound extra field, so it can be used in the format string.
    #       It is not a global variable, so it won't leak into other modules.
    #       The format string is human-friendly, so it can be used in the terminal
    #       and in log files.
    #       The format string is compatible with the default Loguru format.
    log_fmt = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
        "{level:<8} | "
        "{extra[ctx]} | "
        "{name}:{function}:{line} | "
        "{message}"
    )

    # Wrap loguru around tqdm.write to ensure that tqdm progress bars
    # are not disrupted by log messages.
    # This is useful when running Snakemake jobs in parallel, where
    # log messages can interfere with the progress bars.
    # See: https://github.com/Delgan/loguru/issues/135
    def log_sink(message: str) -> None:
        """Custom sink that uses tqdm.write to print log messages."""

        # Open the log file in append mode
        # TODO Consider alternative approaches since this open/closes
        # the file for every log message.
        # This is not ideal for performance, but it ensures that the log file
        # is always up-to-date and avoids issues with concurrent writes.
        # Look into how this works with the `enqueue` parameter.
        with log_path.open("a", encoding="utf-8") as fh:
            # Write the log message to the file
            tqdm.write(
                str(message),
                file=fh,
                end="",  # Loguru already adds a newline
            )

    # Add the file sink with the context-aware format
    logger.add(
        log_sink,
        level=log_level,
        format=log_fmt,
        colorize=True,  # Assume the log viewer supports colors
        backtrace=True,  # Enable backtrace for exceptions
        diagnose=True,  # Enable detailed error messages
        enqueue=enqueue,
    )

    return logger
