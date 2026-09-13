from pathlib import Path

import pandas as pd

from src.ingestion.olist import DATASET_FILES, EXPECTED_FILES, load_olist_tables, validate_source_directory


def _write_all_expected_files(tmp_path: Path) -> None:
    for table_name, file_name in DATASET_FILES.items():
        pd.DataFrame({"value": [table_name]}).to_csv(tmp_path / file_name, index=False)


def test_validate_source_directory_accepts_complete_source(tmp_path: Path) -> None:
    _write_all_expected_files(tmp_path)
    validate_source_directory(tmp_path)


def test_expected_files_match_dataset_mapping() -> None:
    assert EXPECTED_FILES == tuple(DATASET_FILES.values())


def test_load_olist_tables_uses_canonical_table_names(tmp_path: Path) -> None:
    _write_all_expected_files(tmp_path)
    tables = load_olist_tables(tmp_path)

    assert set(tables) == set(DATASET_FILES)
    assert all(isinstance(frame, pd.DataFrame) for frame in tables.values())
