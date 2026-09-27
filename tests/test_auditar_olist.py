import pandas as pd
from scripts.auditar_olist import KEY_COLUMNS, audit_dataframe

from src.ingestion.olist import DATASET_FILES


def test_audit_key_mapping_matches_canonical_table_names() -> None:
    assert set(KEY_COLUMNS) == set(DATASET_FILES)


def test_audit_dataframe_checks_composite_key_duplicates() -> None:
    frame = pd.DataFrame(
        {
            "order_id": ["o1", "o1", "o2"],
            "order_item_id": [1, 1, 1],
        }
    )

    report = audit_dataframe("order_items", frame)

    assert report["key_columns"] == ["order_id", "order_item_id"]
    assert report["duplicate_key_rows"] == 1


def test_audit_dataframe_checks_payment_sequence_key() -> None:
    frame = pd.DataFrame(
        {
            "order_id": ["o1", "o1", "o1"],
            "payment_sequential": [1, 2, 2],
        }
    )

    report = audit_dataframe("order_payments", frame)

    assert report["key_columns"] == ["order_id", "payment_sequential"]
    assert report["duplicate_key_rows"] == 1
