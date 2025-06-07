"""
One test that merely proves the template rendered.
(Uses the session-scoped 'rendered' fixture.)
"""

from pathlib import Path


def test_template_rendered(rendered):
    project_dir, _ = rendered
    expected = project_dir / "pyproject.toml"
    assert expected.is_file(), f"{expected} not found"
