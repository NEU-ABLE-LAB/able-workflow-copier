"""
Unit-tests for dag_svg.

Create an SVG of the main Snakemake DAG
"""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path
from types import SimpleNamespace

import pytest
from lxml import etree as ET

# --------------------------------------------------------------------------- #
# Load the script under test                                                  #
# --------------------------------------------------------------------------- #

ROOT = Path(__file__).parents[4]  # project root
SCRIPT = ROOT / "workflow/scripts/rules_conda_DOCS/dag_svg.py"
if not SCRIPT.exists():  # pragma: no cover
    pytest.skip(
        f"Cannot find {SCRIPT} - are you running tests from the repo root?",
        allow_module_level=True,
    )

spec = importlib.util.spec_from_file_location("dag_svg", str(SCRIPT))
if spec is None or spec.loader is None:  # pragma: no cover
    pytest.skip(f"Cannot import {SCRIPT}", allow_module_level=True)

module_under_test = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module_under_test)  # type: ignore[no-untyped-call]

# --------------------------------------------------------------------------- #
#  Inject a stub “snakemake” module so that the unconditional
#  “from snakemake.script import snakemake” import inside the script
#  under test succeeds even when the real Snakemake package is absent.
# --------------------------------------------------------------------------- #

_fake_sm = types.ModuleType("snakemake")
_fake_sm_script = types.ModuleType("snakemake.script")
# The script only references the *name* `snakemake` when run as __main__,
# so an empty namespace placeholder is sufficient:
_fake_sm_script.snakemake = SimpleNamespace()
_fake_sm.script = _fake_sm_script
sys.modules.setdefault("snakemake", _fake_sm)
sys.modules.setdefault("snakemake.script", _fake_sm_script)


# --------------------------------------------------------------------------- #
# Helper factories                                                            #
# --------------------------------------------------------------------------- #


def _fake_snakemake(tmp_path: Path) -> SimpleNamespace:
    """
    Return a *snakemake* stand-in with the attrs required by the
    ``main()`` function in the script under test.
    """

    smk = SimpleNamespace(
        output=SimpleNamespace(
            svg=tmp_path / "docs" / "docs" / "_images" / "dag.svg",
        ),
        log=SimpleNamespace(
            loguru=tmp_path / "logs" / "conda_localize.log",
            stderr=tmp_path / "logs" / "stderr.log",
        ),
    )

    # Create dummy directories and files
    smk.output.svg.parent.mkdir(parents=True, exist_ok=True)
    smk.log.loguru.parent.mkdir(parents=True, exist_ok=True)

    return smk


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #


def test_main_generates_expected_svg(monkeypatch, tmp_path):
    """Smoke-test ``main()`` and check the SVG post-processing."""

    # --------------------------------------------------------------------- #
    # Patch ``subprocess.run`` so no external commands are launched
    # --------------------------------------------------------------------- #
    dot_graph = "digraph G { A -> B }"
    raw_svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg">
  <g>
    <polygon stroke="none" fill="white" points="0,0 100,0 100,100 0,100"/>
  </g>
  <text x="10" y="10" fill="black">hello</text>
</svg>
"""

    calls: list[list[str]] = []

    def _fake_run(
        cmd, *, check, text, stdout, stderr=None, input=None
    ):  # noqa: D401,E501
        """Mimic ``subprocess.run`` for the two calls made in *main()*."""
        calls.append(cmd)

        if cmd and cmd[0] == "snakemake":
            return types.SimpleNamespace(stdout=dot_graph, returncode=0)
        elif cmd and cmd[0] == "dot":
            # ensure the DOT produced by the first call is piped into DOT
            assert input == dot_graph
            return types.SimpleNamespace(stdout=raw_svg, returncode=0)

        raise RuntimeError(f"Unexpected command: {cmd!r}")

    monkeypatch.setattr(module_under_test.subprocess, "run", _fake_run)

    # --------------------------------------------------------------------- #
    # Execute ``main()``
    # --------------------------------------------------------------------- #
    smk = _fake_snakemake(tmp_path)
    module_under_test.main(smk)

    # we should have invoked both external commands exactly once
    assert calls == [
        ["snakemake", "--forceall", "--dag"],
        ["dot", "-Tsvg"],
    ]

    # --------------------------------------------------------------------- #
    # Validate the written SVG
    # --------------------------------------------------------------------- #
    svg_path = Path(smk.output.svg)
    assert svg_path.exists(), "SVG file was not written"

    root = ET.parse(svg_path).getroot()

    # 1. root element must carry the extra "dag" class
    assert "dag" in root.attrib.get("class", ""), "<svg> missing 'dag' class"

    # 2. <style> block injected
    style_elems = root.findall("{http://www.w3.org/2000/svg}style")
    assert style_elems, "No <style> element injected"
    assert "--md-typeset-color" in style_elems[0].text

    # 3. white background polygon removed
    polygons = root.findall(".//{http://www.w3.org/2000/svg}polygon")
    assert not polygons, "White background <polygon> was *not* removed"
