import pandas as pd
import pytest

from src.analytics.sales_kpis import calculate_sales_kpis, revenue_by_category


def test_calculate_sales_kpis_uses_unique_orders_and_customers() -> None:
    sales = pd.DataFrame(
        {
            "order_id": ["o1", "o1", "o2"],
            "order_item_id": [1, 2, 1],
            "customer_unique_id": ["u1", "u1", "u2"],
            "price": [100.0, 50.0, 200.0],
            "freight_value": [10.0, 5.0, 20.0],
            "is_realized_sale": [True, True, False],
        }
    )
    result = calculate_sales_kpis(sales)
    assert result["orders"] == 1
    assert result["items"] == 2
    assert result["customers"] == 1
    assert result["revenue"] == pytest.approx(150.0)
    assert result["freight"] == pytest.approx(15.0)
    assert result["revenue_with_freight"] == pytest.approx(165.0)
    assert result["average_order_value"] == pytest.approx(150.0)


def test_calculate_sales_kpis_returns_zero_for_empty_realized_sales() -> None:
    sales = pd.DataFrame(
        {
            "order_id": pd.Series(dtype="string"),
            "order_item_id": pd.Series(dtype="int64"),
            "customer_unique_id": pd.Series(dtype="string"),
            "price": pd.Series(dtype="float64"),
            "freight_value": pd.Series(dtype="float64"),
            "is_realized_sale": pd.Series(dtype="bool"),
        }
    )
    result = calculate_sales_kpis(sales)
    assert result["orders"] == 0
    assert result["revenue"] == 0.0
    assert result["average_order_value"] == 0.0


def test_revenue_by_category_sorts_descending() -> None:
    sales = pd.DataFrame(
        {
            "product_category_name_english": ["A", "B", "A"],
            "price": [100.0, 250.0, 50.0],
            "order_item_id": [1, 1, 2],
            "is_realized_sale": [True, True, True],
        }
    )
    result = revenue_by_category(sales)
    assert result.iloc[0]["product_category_name_english"] == "B"
    assert result.iloc[0]["revenue"] == pytest.approx(250.0)
