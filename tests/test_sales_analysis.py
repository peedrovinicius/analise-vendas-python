import pandas as pd
import pytest

from src.analytics.sales_analysis import (
    category_revenue,
    customer_purchase_frequency,
    customer_segment_summary,
    monthly_sales,
    repeat_customer_rate,
    sales_by_seller,
    sales_by_state,
    top_n_revenue_share,
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
            "product_category_name_english": ["beauty", "beauty", "sports"],
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


def test_sales_by_state_calculates_share_aov_and_freight_ratio() -> None:
    result = sales_by_state(_sales())
    row = result.loc[result["customer_state"] == "SP"].iloc[0]
    assert row["revenue"] == pytest.approx(200.0)
    assert row["freight"] == pytest.approx(20.0)
    assert row["average_order_value"] == pytest.approx(200.0)
    assert row["freight_to_revenue"] == pytest.approx(0.1)
    assert result["revenue_share"].sum() == pytest.approx(1.0)


def test_sales_by_seller_calculates_revenue_and_share() -> None:
    result = sales_by_seller(_sales())
    row = result.loc[result["seller_id"] == "s1"].iloc[0]
    assert row["revenue"] == pytest.approx(150.0)
    assert row["items"] == 2
    assert row["orders"] == 2
    assert result["revenue_share"].sum() == pytest.approx(1.0)


def test_repeat_customer_rate_uses_unique_customer_id() -> None:
    assert repeat_customer_rate(_sales()) == pytest.approx(0.5)


def test_customer_purchase_frequency_counts_distinct_orders() -> None:
    result = customer_purchase_frequency(_sales())
    row = result.loc[result["customer_unique_id"] == "c1"].iloc[0]
    assert row["orders"] == 2
    assert row["revenue"] == pytest.approx(150.0)


def test_customer_segment_summary_separates_repeat_and_one_time_customers() -> None:
    result = customer_segment_summary(_sales())

    one_time = result.loc[result["customer_segment"] == "one_time"].iloc[0]
    repeat = result.loc[result["customer_segment"] == "repeat"].iloc[0]

    assert one_time["customers"] == 1
    assert one_time["orders"] == 1
    assert one_time["items"] == 1
    assert one_time["revenue"] == pytest.approx(200.0)
    assert one_time["revenue_share"] == pytest.approx(200 / 350)
    assert one_time["average_orders_per_customer"] == pytest.approx(1.0)
    assert one_time["average_revenue_per_customer"] == pytest.approx(200.0)

    assert repeat["customers"] == 1
    assert repeat["orders"] == 2
    assert repeat["items"] == 2
    assert repeat["revenue"] == pytest.approx(150.0)
    assert repeat["revenue_share"] == pytest.approx(150 / 350)
    assert repeat["average_orders_per_customer"] == pytest.approx(2.0)
    assert repeat["average_revenue_per_customer"] == pytest.approx(150.0)


def test_customer_segment_summary_returns_empty_result_without_realized_sales() -> None:
    result = customer_segment_summary(_sales().assign(is_realized_sale=False))

    assert result.empty
    assert list(result.columns) == [
        "customer_segment",
        "customers",
        "orders",
        "items",
        "revenue",
        "revenue_share",
        "average_orders_per_customer",
        "average_revenue_per_customer",
    ]


def test_category_revenue_calculates_share_aov_and_freight_ratio() -> None:
    result = category_revenue(_sales())
    row = result.loc[result["product_category_name_english"] == "sports"].iloc[0]
    assert row["revenue"] == pytest.approx(200.0)
    assert row["freight"] == pytest.approx(20.0)
    assert row["average_order_value"] == pytest.approx(200.0)
    assert row["freight_to_revenue"] == pytest.approx(0.1)
    assert result["revenue_share"].sum() == pytest.approx(1.0)


def test_top_n_revenue_share_is_bounded() -> None:
    result = sales_by_state(_sales())
    assert top_n_revenue_share(result, 1) == pytest.approx(200 / 350)
    assert top_n_revenue_share(result, 10) == pytest.approx(1.0)


def test_top_n_revenue_share_returns_zero_for_invalid_n_or_empty_data() -> None:
    result = sales_by_state(_sales())
    assert top_n_revenue_share(result, 0) == 0.0
    assert top_n_revenue_share(result, -1) == 0.0
    assert top_n_revenue_share(result.iloc[0:0], 1) == 0.0


def test_analytics_return_empty_results_without_realized_sales() -> None:
    sales = _sales().assign(is_realized_sale=False)

    assert monthly_sales(sales).empty
    assert sales_by_state(sales).empty
    assert sales_by_seller(sales).empty
    assert customer_purchase_frequency(sales).empty
    assert customer_segment_summary(sales).empty
    assert category_revenue(sales).empty
    assert repeat_customer_rate(sales) == 0.0


def test_sales_by_state_handles_zero_total_revenue() -> None:
    sales = _sales().assign(price=0.0)
    result = sales_by_state(sales)
    assert result["revenue_share"].eq(0.0).all()
    assert result["freight_to_revenue"].eq(0.0).all()


def test_category_revenue_handles_zero_total_revenue() -> None:
    sales = _sales().assign(price=0.0)
    result = category_revenue(sales)
    assert result["revenue_share"].eq(0.0).all()
    assert result["freight_to_revenue"].eq(0.0).all()
