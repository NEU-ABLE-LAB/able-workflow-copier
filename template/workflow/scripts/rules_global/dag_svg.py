"""
Create a SVG of the snakemake DAG.
The SVG should be light/dark mode compatible and
should not contain any hard-coded paths.
This script is designed to be run as part of a Snakemake workflow.
"""

# TODO-copier-package: Be able to generate DAGs for specific rules only.

import subprocess
import sys
import textwrap
from pathlib import Path
from typing import TYPE_CHECKING

from loguru import logger
from lxml import etree as ET

if TYPE_CHECKING:  # pragma: no cover
    from snakemake.script import snakemake


STYLE = textwrap.dedent(
    """
    <style>
      /*  Use MkDocs-Material palette tokens
          ──────────────────────────────────
          default  : data-md-color-scheme="default"
          dark/slate: data-md-color-scheme="slate"
      */

      /* Labels */
      svg.dag text { fill: var(--md-typeset-color, #000000de); }
    </style>
    """
).strip()


def _neutralise_only_problematic_colours(root: ET.Element) -> None:
    """
    Remove the white *background* polygon so the page background shows
    through in both themes.
    """
    SVG_NS = "{http://www.w3.org/2000/svg}"

    # Background polygon: first <polygon> child of the outermost <g>
    for poly in root.findall(f".//{SVG_NS}polygon"):
        if poly.get("stroke") == "none" and poly.get("fill", "").lower() == "white":
            parent = poly.getparent()
            if parent is not None:
                parent.remove(poly)
            break  # there’s only one like this


def main(smk) -> None:  # type: ignore[no-untyped-def]

    # Parse Snakemake directives
    svg_path = Path(smk.output.svg)

    # Setup logging
    logger.remove()
    logger.add(smk.log.loguru)

    # Generate DAG as SVG via graphviz
    logger.debug("Generating DAG SVG using Snakemake")
    with open(smk.log.stdout, "a") as stdout_log:
        dag_dot = subprocess.run(
            ["snakemake", "--forceall", "--dag"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=stdout_log,
        ).stdout

        # Convert DOT → SVG with Graphviz
        raw_svg = subprocess.run(
            ["dot", "-Tsvg"],
            input=dag_dot,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=stdout_log,
        ).stdout

    # Parse & manipulate
    logger.debug("Parsing SVG DAG output")
    parser = ET.XMLParser(ns_clean=True, recover=True)
    root = ET.fromstring(raw_svg.encode(), parser=parser)

    # mark root for CSS scoping
    logger.debug("Marking SVG root element with 'dag' class")
    if "class" in root.attrib:
        root.attrib["class"] += " dag"
    else:
        root.attrib["class"] = "dag"

    # neutralise only background + text colour
    logger.debug("Neutralising problematic colours (background + text)")
    _neutralise_only_problematic_colours(root)

    # inject <style> block
    logger.debug("Injecting CSS style into SVG")
    root.insert(0, ET.fromstring(STYLE))

    # 3 - write out pretty-printed SVG
    logger.debug(f"Writing SVG DAG to {svg_path}")
    svg_path.write_bytes(
        ET.tostring(root, xml_declaration=True, encoding="utf-8", pretty_print=True)
    )


if __name__ == "__main__":
    try:
        main(snakemake)
    except NameError:
        logger.error(
            "This script is designed to be run as part of a Snakemake workflow. "
            "Please run it through Snakemake."
        )
        sys.exit(0)
