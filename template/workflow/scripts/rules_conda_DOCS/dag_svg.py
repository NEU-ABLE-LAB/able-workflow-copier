"""
Script for the dag_svg rule

Create an SVG of the main Snakemake DAG
"""

import subprocess
import sys
import textwrap
from pathlib import Path
from typing import TYPE_CHECKING

from loguru import logger
from lxml import etree as ET

from snakemake.script import Snakemake

if TYPE_CHECKING:  # pragma: no cover
    # For type checking only, when called as a `script:` in a Snakemake rule
    # the `snakemake` object is injected at the top of the script
    from snakemake.script import snakemake


STYLE = textwrap.dedent(
    """
    <style xmlns="http://www.w3.org/2000/svg">
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


def _generate_dag_svg(stderr_log: Path, rule_name: str = "all") -> str:
    """
    Generate DAG as SVG via graphviz.

    Args:
        stderr_log: Path to the stderr log file
        rule_name: Name of the rule to generate the DAG for

    Returns:
        The raw SVG string
    """
    logger.debug("Generating DAG SVG using Snakemake")
    with open(stderr_log, "a") as stderr_log_file:

        dag_dot = subprocess.run(
            [
                "snakemake",
                "--forceall",
                "--rulegraph",
                "dot",
                rule_name,
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=stderr_log_file,
        ).stdout

        # Convert DOT → SVG with Graphviz
        raw_svg = subprocess.run(
            ["dot", "-Tsvg"],
            input=dag_dot,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=stderr_log_file,
        ).stdout

    return raw_svg


def _process_svg_content(raw_svg: str) -> ET.Element:
    """
    Parse and manipulate SVG content.

    Args:
        raw_svg: Raw SVG string content

    Returns:
        Processed SVG root element
    """
    # Parse & manipulate SVG as XML
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

    return root


def main(
    svg_path: Path,
    rule_name: str,
    stderr_log: Path,
) -> None:
    """
    Generate a Snakemake DAG as an SVG file.
    """

    # Generate DAG as SVG via graphviz
    raw_svg = _generate_dag_svg(stderr_log, rule_name)

    # Process SVG content
    root = _process_svg_content(raw_svg)

    # Write out pretty-printed SVG
    logger.debug(f"Writing SVG DAG to {svg_path}")
    svg_path.write_bytes(
        ET.tostring(root, xml_declaration=True, encoding="utf-8", pretty_print=True)
    )


def main_smk(smk: Snakemake) -> None:
    """
    Wrapper for the main function that accepts a Snakemake object.
    """

    # Setup logging
    logger.remove()
    logger.add(smk.log.loguru)

    # Ensure the output directory exists
    svg_path = Path(smk.output.svg)
    svg_path.parent.mkdir(parents=True, exist_ok=True)

    # Call the main function with the provided paths
    main(svg_path, smk.wildcards.rule_name, smk.log.stderr)


if __name__ == "__main__":
    try:
        main_smk(snakemake)
    except NameError:
        logger.error(
            "This script is designed to be run as part of a Snakemake workflow. "
            "Please run it through Snakemake."
        )
        sys.exit(0)
