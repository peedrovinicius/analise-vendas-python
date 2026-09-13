import pandas as pd
import pytest
import pandera.pandas as pa

from src.validation.olist_schema import validate_core_tables


def _tables() -> dict[str, pd.DataFrame]:
    return {
        "orders": pd.DataFrame(
            {
                "order_id": ["o1"],
                "customer_id": ["c1"],
                "order_status": ["delivered"],
                "order_purchase_timestamp": ["2018-01-01 10:00:00"],
            }
        ),
        "order_items": pd.DataFrame(
            {
                "order_id": ["o1"],
                "order_item_id": [1],
                "product_id": ["p1"],
                "seller_id": ["s1"],
                "price": [100.0],
                "freight_value": [10.0],
            }
        ),
    }


def test_validate_core_tables_accepts_valid_schema() -> None:
    validate_core_tables(_tables())


def test_validate_core_tables_rejects_negative_price() -> None:
    tables = _tables()
    tables["order_items"].loc[0, "price"] = -1.0

    with pytest.raises(pa.errors.SchemaErrors):
        validate_core_tables(tables)


def test_validate_core_tables_rejects_duplicate_order_id() -> None:
    tables = _tables()
    tables["orders"] = pd.concat([tables["orders"], tables["orders"]], ignore_index=True)

    with pytest.raises(pa.errors.SchemaErrors):
        validate_core_tables(tables)
