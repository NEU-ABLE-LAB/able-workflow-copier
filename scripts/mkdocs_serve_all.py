#!/usr/bin/env python3
"""
Serve every MkDocs site in the *able-workflow* workspace.

Four `mkdocs serve` processes are launched in parallel:

1. **main** - project-root docs (`docs/mkdocs.yml`)
2. **module-copier** - `able-workflow/module-copier/docs/mkdocs.yml`
3. **etl-copier** - `able-workflow/etl-copier/docs/mkdocs.yml`
4. **rule-copier** - `able-workflow/rule-copier/docs/mkdocs.yml`

Each site is served on 127.0.0.1:801{1-3} and writes logs to

    logs/mkdocs_serve_all/{site}/{stdout,stderr}.log

Python-side logs use *loguru*:

    logs/mkdocs_serve_all/loguru.log
    logs/mkdocs_serve_all/{site}/loguru.log

Ctrl-C (SIGINT) or SIGTERM stops every server gracefully.
"""
from __future__ import annotations

import atexit
import os
import signal
import sys
import time
from pathlib import Path
from subprocess import Popen
from types import FrameType
from typing import Dict, List, Tuple

from loguru import logger

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
ROOT: Path = Path(__file__).resolve().parent.parent
LOG_ROOT: Path = ROOT / "logs" / "mkdocs_serve_all"

# (site-name, mkdocs-config-file, port)
SITES: List[Tuple[str, Path, int]] = [
    ("main", ROOT / "docs" / "mkdocs.yml", 8011),
    (
        "module-copier",
        ROOT / "able-workflow" / "module-copier" / "docs" / "mkdocs.yml",
        8012,
    ),
    (
        "etl-copier",
        ROOT / "able-workflow" / "etl-copier" / "docs" / "mkdocs.yml",
        8013,
    ),
    (
        "rule-copier",
        ROOT / "able-workflow" / "rule-copier" / "docs" / "mkdocs.yml",
        8014,
    ),
]


# -----------------------------------------------------------------------------
# Environment variables propagated to every MkDocs subprocess
# -----------------------------------------------------------------------------


ENV_VARS: Dict[str, str] = {
    "ABLE_WORKFLOW_COPIER_REPO": "https://github.com/NEU-ABLE-LAB/able-workflow-copier-dev",
    "ABLE_WORKFLOW_COPIER_DOCS": "http://localhost:8011",
    "ABLE_WORKFLOW_MODULE_COPIER_REPO": "https://github.com/NEU-ABLE-LAB/able-workflow-module-copier-dev",
    "ABLE_WORKFLOW_MODULE_COPIER_DOCS": "http://localhost:8012",
    "ABLE_WORKFLOW_ETL_COPIER_REPO": "https://github.com/NEU-ABLE-LAB/able-workflow-etl-copier-dev",
    "ABLE_WORKFLOW_ETL_COPIER_DOCS": "http://localhost:8013",
    "ABLE_WORKFLOW_RULE_COPIER_REPO": "https://github.com/NEU-ABLE-LAB/able-workflow-rule-copier-dev",
    "ABLE_WORKFLOW_RULE_COPIER_DOCS": "http://localhost:8014",
}


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def _ensure_logging_dirs() -> None:
    """Create ``logs/mkdocs_serve_all`` and per-site sub-directories."""
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    for site, *_ in SITES:
        (LOG_ROOT / site).mkdir(parents=True, exist_ok=True)


def _configure_loguru() -> None:
    """Attach global and per-site sinks to *loguru*."""
    logger.add(LOG_ROOT / "loguru.log", enqueue=True, rotation="10 MB")
    for site, *_ in SITES:
        logger.add(
            LOG_ROOT / site / "loguru.log",
            enqueue=True,
            rotation="5 MB",
            filter=lambda record: record["extra"].get("site") == site,
        )
    # Provide a default 'site' key so filters don't raise KeyError
    logger.patch(lambda record: record["extra"].setdefault("site", "global"))


def _start_mkdocs(site: str, cfg: Path, port: int) -> Popen[str]:
    """
    Spawn ``mkdocs serve`` for a documentation site.

    Parameters
    ----------
    site
        Short site identifier (e.g., ``"main"``).
    cfg
        Path to the site's ``mkdocs.yml``.
    port
        Port for the development server (e.g., ``8001``).

    Returns
    -------
    subprocess.Popen[str]
        Handle to the running process.
    """
    if not cfg.exists():
        raise FileNotFoundError(cfg)

    log_dir = LOG_ROOT / site
    stdout_f = (log_dir / "stdout.log").open("w", encoding="utf-8")
    stderr_f = (log_dir / "stderr.log").open("w", encoding="utf-8")

    cmd = [
        "mkdocs",
        "serve",
        "-f",
        str(cfg),
        "-a",
        f"127.0.0.1:{port}",
    ]

    logger.bind(site=site).info("Launching: {}", " ".join(cmd))

    # Include the custom environment variables for this subprocess
    env = os.environ.copy()
    env.update(ENV_VARS)
    proc = Popen(cmd, stdout=stdout_f, stderr=stderr_f, text=True, env=env)

    # Keep handles alive so files stay open as long as the process lives
    proc.stdout_fp = stdout_f  # type: ignore[attr-defined]
    proc.stderr_fp = stderr_f  # type: ignore[attr-defined]
    return proc


def _teardown(processes: Dict[str, Popen[str]]) -> None:
    """Terminate every running MkDocs process."""
    logger.info("Shutting down all MkDocs subprocesses …")
    for site, proc in processes.items():
        if proc.poll() is None:
            logger.bind(site=site).info("Terminating PID {}", proc.pid)
            proc.terminate()

    deadline = time.time() + 5.0
    while any(p.poll() is None for p in processes.values()) and time.time() < deadline:
        time.sleep(0.1)

    for site, proc in processes.items():
        if proc.poll() is None:
            logger.bind(site=site).warning("Killing PID {}", proc.pid)
            proc.kill()
        for attr in ("stdout_fp", "stderr_fp"):
            fp = getattr(proc, attr, None)
            if fp:
                fp.close()

    logger.info("All subprocesses stopped.")


def _install_signal_handlers(processes: Dict[str, Popen[str]]) -> None:
    """Ensure SIGINT/SIGTERM shut everything down cleanly."""

    def handler(signum: int, _frame: FrameType | None) -> None:
        logger.info("Received signal {} - initiating shutdown.", signum)
        _teardown(processes)
        sys.exit(0)

    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, handler)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main() -> None:
    """Script entry point."""
    _ensure_logging_dirs()
    _configure_loguru()

    processes: Dict[str, Popen[str]] = {}
    try:
        for site, cfg, port in SITES:
            processes[site] = _start_mkdocs(site, cfg, port)

        _install_signal_handlers(processes)
        atexit.register(_teardown, processes)

        logger.success("All MkDocs dev-servers are running.")
        while True:  # keep parent alive; detect premature exits
            finished = [s for s, p in processes.items() if p.poll() is not None]
            if finished:
                logger.error("Process(es) %s exited unexpectedly.", finished)
                _teardown(processes)
                sys.exit(1)
            time.sleep(1)
    except Exception:  # pragma: no cover
        logger.exception("Unhandled exception - aborting.")
        _teardown(processes)
        sys.exit(1)


if __name__ == "__main__":
    main()
