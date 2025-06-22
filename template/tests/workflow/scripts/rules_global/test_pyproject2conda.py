"""Unit tests for the pyproject2conda wrapper script."""

import importlib.util
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).parents[4]
SCRIPT = ROOT / "workflow/scripts/rules_global/pyproject2conda.py"
if not SCRIPT.exists():
    pytest.skip(f"Cannot find {SCRIPT}", allow_module_level=True)

spec = importlib.util.spec_from_file_location("pyproject2conda", str(SCRIPT))
P2C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P2C)  # type: ignore[no-untyped-call]


def _fake_snakemake(tmp_path: Path, env_file: str) -> SimpleNamespace:
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    return SimpleNamespace(
        input=SimpleNamespace(
            toml=str(tmp_path / "dummy_pyproject.toml"),
        ),
        params=SimpleNamespace(
            env_name=env_file.split("-", 1)[1].replace(".yaml", ""),
        ),
        output=SimpleNamespace(yaml=str(tmp_path / env_file)),
        log=SimpleNamespace(
            loguru=str(log_dir / "pyproject2conda.loguru.log"),
            stdout=str(log_dir / "pyproject2conda.stdout.log"),
        ),
    )


def _patch_subprocess(monkeypatch, out_dir: Path, files_to_create: list[str]):
    calls: list[list[str]] = []

    def _stub(cmd, check, stdout, stderr):
        calls.append(cmd)
        for name in files_to_create:
            (out_dir / name).touch()
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(P2C.subprocess, "run", _stub)
    return calls


def test_main_invokes_pyproject2conda(tmp_path, monkeypatch):
    env_file = "py312-core.yaml"
    smk = _fake_snakemake(tmp_path, env_file)
    calls = _patch_subprocess(monkeypatch, Path(smk.output.yaml).parent, [env_file])

    P2C.main(smk)

    assert calls == [
        [
            "pyproject2conda",
            "project",
            "-f",
            smk.input.toml,
            "--envs",
            smk.params.env_name,
        ]
    ]
    assert Path(smk.output.yaml).exists()
    assert "Generated env" in Path(smk.log.loguru).read_text(encoding="utf-8")
