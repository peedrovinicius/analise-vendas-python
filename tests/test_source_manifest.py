from pathlib import Path

import pytest
from scripts.source_manifest import build_manifest, validate_manifest, write_manifest

from src.ingestion.olist import EXPECTED_FILES


def _write_source_files(directory: Path) -> None:
    for index, file_name in enumerate(EXPECTED_FILES):
        (directory / file_name).write_text(
            f"column\nvalue-{index}\n",
            encoding="utf-8",
        )


def test_build_manifest_fingerprints_all_expected_files(tmp_path: Path) -> None:
    _write_source_files(tmp_path)

    manifest = build_manifest(tmp_path)
    files = manifest["files"]

    assert isinstance(files, dict)
    assert set(files) == set(EXPECTED_FILES)
    assert all(len(entry["sha256"]) == 64 for entry in files.values())
    assert all(entry["data_rows"] == 1 for entry in files.values())


def test_validate_manifest_accepts_unchanged_source(tmp_path: Path) -> None:
    _write_source_files(tmp_path)
    manifest_path = tmp_path / "manifest.json"
    write_manifest(tmp_path, manifest_path)

    validate_manifest(tmp_path, manifest_path)


def test_validate_manifest_detects_modified_source(tmp_path: Path) -> None:
    _write_source_files(tmp_path)
    manifest_path = tmp_path / "manifest.json"
    write_manifest(tmp_path, manifest_path)

    changed = tmp_path / EXPECTED_FILES[0]
    changed.write_text("column\nmodified\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Falha de integridade"):
        validate_manifest(tmp_path, manifest_path)
