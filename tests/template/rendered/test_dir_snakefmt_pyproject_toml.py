"""Validate snakefmt configuration is sourced from pyproject.toml."""


def test_snakefmt_uses_pyproject_toml(rendered):
    project_dir, _ = rendered

    pyproject = (project_dir / "pyproject.toml").read_text(encoding="utf-8")
    assert "[tool.snakefmt]" in pyproject
    assert "line_length = 79" in pyproject

    tox_ini = (project_dir / "tox.ini").read_text(encoding="utf-8")
    assert "snakefmt --config pyproject.toml --check --diff workflow/" in tox_ini
