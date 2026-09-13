from pathlib import Path

import pandas as pd
import pytest

from src.transformation.olist import build_item_sales_fact, load_olist_tables


def _minimal_tables() -> dict[str, pd.DataFrame]:
    return {
        "customers": pd.DataFrame(
            {
                "customer_id": ["c1"],
                "customer_unique_id": ["u1"],
                "customer_city": ["Fortaleza"],
                "customer_state": ["CE"],
            }
        ),
        "geolocation": pd.DataFrame(),
        "order_items": pd.DataFrame(
            {
                "order_id": ["o1", "o1"],
                "order_item_id": [1, 2],
                "product_id": ["p1", "p2"],
                "seller_id": ["s1", "s1"],
                "shipping_limit_date": ["2018-01-01", "2018-01-01"],
                "price": [100.0, 50.0],
                "freight_value": [10.0, 5.0],
            }
        ),
        "order_payments": pd.DataFrame(),
        "order_reviews": pd.DataFrame(),
        "orders": pd.DataFrame(
            {
                "order_id": ["o1"],
                "customer_id": ["c1"],
                "order_status": ["delivered"],
                "order_purchase_timestamp": ["2018-01-02 10:00:00"],
            }
        ),
        "products": pd.DataFrame(
            {
                "product_id": ["p1", "p2"],
                "product_category_name": ["beleza", "informatica"],
            }
        ),
        "sellers": pd.DataFrame(
            {
                "seller_id": ["s1"],
                "seller_city": ["Fortaleza"],
                "seller_state": ["CE"],
            }
        ),
        "category_translation": pd.DataFrame(
            {
                "product_category_name": ["beleza", "informatica"],
                "product_category_name_english": ["beauty", "computers"],
            }
        ),
    }


def test_build_item_sales_fact_preserves_item_granularity() -> None:
    result = build_item_sales_fact(_minimal_tables())
    assert len(result) == 2
    assert result["order_id"].nunique() == 1
    assert result["gross_item_value"].sum() == pytest.approx(150.0)
    assert result["total_item_value"].sum() == pytest.approx(165.0)


def test_realized_sale_is_true_only_for_delivered_orders() -> None:
    tables = _minimal_tables()
    tables["orders"] = tables["orders"].assign(order_status=["canceled"])
    result = build_item_sales_fact(tables)
    assert not result["is_realized_sale"].any()


def test_loader_raises_when_expected_file_is_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_olist_tables(tmp_path)
