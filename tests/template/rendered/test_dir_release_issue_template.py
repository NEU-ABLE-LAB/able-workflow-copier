"""Validate the generated release issue template for rendered projects."""


def test_template_contains_release_issue_template(rendered) -> None:
    project_dir, _ = rendered
    expected = project_dir / ".github" / "ISSUE_TEMPLATE" / "release_tagged_version.md"
    assert expected.is_file(), f"{expected} not found"

    content = expected.read_text(encoding="utf-8")
    assert "Review commits since the last tagged release" in content
    assert "CHANGELOG.md" in content
    assert "setuptools_scm" in content
