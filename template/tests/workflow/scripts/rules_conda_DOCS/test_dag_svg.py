"""
Unit-tests for ``workflow/scripts/rules_conda_DOCS/dag_svg.py``.

Every public helper is exercised in isolation, with very limited monkey-patching.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

import pytest
from lxml import etree as ET
from snakemake.io.container import (
    InputFiles,
    OutputFiles,
    Log,
    Params,
    ResourceList,
    Wildcards,
)
from snakemake.script import Snakemake


# --------------------------------------------------------------------------- #
# Load script under test once per module                                      #
# --------------------------------------------------------------------------- #


@pytest.fixture(scope="module")
def dag_svg_module() -> Any:
    """Import the *runtime* module object for dag_svg.py (without executing it)."""
    root = Path(__file__).parents[4]  # project root
    script = root / "workflow/scripts/rules_conda_DOCS/dag_svg.py"

    spec = importlib.util.spec_from_file_location("dag_svg", script)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    assert spec and spec.loader
    spec.loader.exec_module(module)  # type: ignore[arg-type]
    return module


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #

RAW_SVG = """\
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg">
  <g>
    <polygon stroke="none" fill="white" points="0,0 100,0 100,100 0,100"/>
  </g>
  <text x="10" y="10" fill="black">Hello-world</text>
</svg>
"""


def fake_snakemake(tmp_path: Path) -> Snakemake:  # noqa: D401
    """
    Build a minimal but *real* ``Snakemake`` instance for the wrapper.

    Only those attributes the script touches are populated.
    """
    svg_path = tmp_path / "docs" / "_images" / "dag.svg"
    log_dir = tmp_path / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    return Snakemake(
        input_=InputFiles([]),
        output=OutputFiles(fromdict={"svg": str(svg_path)}),
        params=Params(),
        wildcards=Wildcards(
            fromdict={
                "rule_name": "all",
                "graph_type": "dag",
            }
        ),
        resources=ResourceList(),
        threads=4,
        log=Log(
            fromdict={
                "stderr": str(log_dir / "stderr.log"),
                "loguru": str(log_dir / "loguru.log"),
            }
        ),
        config={},
        rulename="test_dag_svg",
        bench_iteration=None,
    )


# --------------------------------------------------------------------------- #
# _neutralise_only_problematic_colours                                        #
# --------------------------------------------------------------------------- #


def test_neutralise_removes_background_polygon(dag_svg_module):
    SVG_NS = "{http://www.w3.org/2000/svg}"

    root = ET.fromstring(RAW_SVG.encode())
    # sanity-check: the polygon is there initially
    assert root.find(f".//{SVG_NS}polygon") is not None

    dag_svg_module._neutralise_only_problematic_colours(root)  # noqa: SLF001

    # After the call, no white background polygon should remain
    assert root.find(f".//{SVG_NS}polygon") is None


# --------------------------------------------------------------------------- #
# _process_svg_content                                                        #
# --------------------------------------------------------------------------- #


def test_process_svg_content_adds_class_injects_style_and_neutralises_bg(
    dag_svg_module,
):
    root = dag_svg_module._process_svg_content(RAW_SVG)  # noqa: SLF001

    # 1. Dag-scoping class
    assert "dag" in root.attrib["class"]

    # 2. <style> block injected
    style_elems = root.findall("{http://www.w3.org/2000/svg}style")
    assert style_elems and "--md-typeset-color" in style_elems[0].text

    # 3. Background polygon removed
    polygons = root.findall(".//{http://www.w3.org/2000/svg}polygon")
    assert not polygons


# --------------------------------------------------------------------------- #
# main() + main_smk() (integration smoke-test)                                #
# --------------------------------------------------------------------------- #


def test_main_smk_writes_processed_svg(monkeypatch, tmp_path, dag_svg_module):
    """
    Integration smoke-test of *everything* without touching the real filesystem
    outside *tmp_path* and without running external commands.
    """
    # We only patch the heavy part: _generate_dag_svg
    monkeypatch.setattr(
        dag_svg_module,
        "_generate_dag_svg",
        lambda _, __, ___: RAW_SVG,
    )

    smk = fake_snakemake(tmp_path)
    dag_svg_module.main_smk(smk)

    svg_path = Path(smk.output[0])
    assert svg_path.exists()

    root = ET.parse(svg_path).getroot()
    # Final SVG should already have the class and no white poly
    assert "dag" in root.attrib["class"]
    assert not root.findall(".//{http://www.w3.org/2000/svg}polygon")
