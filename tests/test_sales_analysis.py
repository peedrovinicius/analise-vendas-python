import pandas as pd
import pytest

from src.analytics.sales_analysis import (
    customer_purchase_frequency,
    monthly_sales,
    repeat_customer_rate,
    sales_by_state,
)


def _sales() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "order_item_id": [1, 1, 1],
            "customer_unique_id": ["c1", "c1", "c2"],
            "customer_state": ["CE", "CE", "SP"],
            "seller_id": ["s1", "s1", "s2"],
            "price": [100.0, 50.0, 200.0],
            "freight_value": [10.0, 5.0, 20.0],
            "order_purchase_timestamp": [
                "2018-01-15 10:00:00",
                "2018-02-15 10:00:00",
                "2018-02-20 10:00:00",
            ],
            "is_realized_sale": [True, True, True],
        }
    )


def test_monthly_sales_calculates_aov_and_growth() -> None:
    result = monthly_sales(_sales())
    assert len(result) == 2
    assert result.loc[0, "revenue"] == pytest.approx(100.0)
    assert result.loc[0, "average_order_value"] == pytest.approx(100.0)
    assert result.loc[1, "revenue_mom_growth"] == pytest.approx(1.5)


def test_sales_by_state_calculates_share() -> None:
    result = sales_by_state(_sales())
    assert result.loc[result["customer_state"] == "SP", "revenue"].iloc[0] == pytest.approx(200.0)
    assert result["revenue_share"].sum() == pytest.approx(1.0)


def test_repeat_customer_rate_uses_unique_customer_id() -> None:
    assert repeat_customer_rate(_sales()) == pytest.approx(0.5)


def test_customer_purchase_frequency_counts_distinct_orders() -> None:
    result = customer_purchase_frequency(_sales())
    row = result.loc[result["customer_unique_id"] == "c1"].iloc[0]
    assert row["orders"] == 2
    assert row["revenue"] == pytest.approx(150.0)
