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
    rotation: str | int = "25 MB",
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
    rotation
        Forwarded to :pyfunc:`loguru.logger.add` (size or time-based rotation).
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
    logger.configure(extra={"ctx": "-"})

    # Wipe previous sinks (avoid duplicate emission)
    logger.remove()

    # Freeze the context for this *process*
    bound = logger.bind(ctx=_serialise_ctx(context))

    # Add the file sink with a readable format
    log_fmt = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
        "{level:<8} | "
        "{extra[ctx]:<25} | "
        "{message}"
    )
    bound.add(
        log_path,
        rotation=rotation,
        enqueue=enqueue,
        backtrace=True,
        diagnose=True,
        format=log_fmt,
        level=log_level,
    )

    return bound
