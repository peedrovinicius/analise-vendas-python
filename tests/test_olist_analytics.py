import pandas as pd
import pytest

from src.analytics.olist import calculate_sales_kpis


def sample_sales() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "is_realized_sale": [True, True, False],
            "order_id": ["o1", "o1", "o2"],
            "customer_unique_id": ["c1", "c1", "c2"],
            "product_id": ["p1", "p2", "p3"],
            "price": [100.0, 50.0, 999.0],
            "freight_value": [10.0, 5.0, 99.0],
        }
    )


def test_calculate_sales_kpis_ignores_non_realized_sales() -> None:
    result = calculate_sales_kpis(sample_sales())

    assert result["gross_revenue"] == 150.0
    assert result["freight_value"] == 15.0
    assert result["total_orders"] == 1
    assert result["total_customers"] == 1
    assert result["total_items"] == 2
    assert result["average_order_value"] == 150.0
    assert result["average_item_price"] == 75.0


def test_calculate_sales_kpis_returns_zero_for_empty_realized_set() -> None:
    sales = sample_sales().assign(is_realized_sale=False)

    result = calculate_sales_kpis(sales)

    assert result["gross_revenue"] == 0.0
    assert result["total_orders"] == 0
    assert result["average_order_value"] == 0.0
    assert result["average_item_price"] == 0.0


def test_calculate_sales_kpis_requires_columns() -> None:
    with pytest.raises(ValueError, match="Colunas obrigatórias ausentes"):
        calculate_sales_kpis(pd.DataFrame({"price": [10.0]}))
