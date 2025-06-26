"""Test runner extras functionality."""

import importlib
import importlib.util

import pytest


def test_snakemake_package_is_installed():
    """Test that the snakemake package is installed and importable."""
    try:
        import snakemake

        # Verify the module has expected attributes
        assert hasattr(
            snakemake, "__version__"
        ), "snakemake package should have a __version__ attribute"
    except ImportError:
        pytest.fail("snakemake package is not installed or not importable")


def test_snakemake_importlib_check():
    """Alternative test using importlib to check snakemake installation."""
    try:
        spec = importlib.util.find_spec("snakemake")
        assert spec is not None, "snakemake package spec not found"
        assert spec.origin is not None, "snakemake package origin not found"
    except Exception as e:
        pytest.fail(f"Failed to find snakemake package using importlib: {e}")
