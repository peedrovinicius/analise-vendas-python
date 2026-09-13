import pandas as pd

from src import pipeline


def test_run_pipeline_orchestrates_loading_validation_transformation_and_kpis(monkeypatch) -> None:
    tables = {"orders": pd.DataFrame(), "order_items": pd.DataFrame()}
    sales = pd.DataFrame(
        {
            "order_id": ["o1"],
            "order_item_id": [1],
            "customer_unique_id": ["u1"],
            "price": [100.0],
            "freight_value": [10.0],
            "is_realized_sale": [True],
        }
    )
    expected = {
        "orders": 1,
        "items": 1,
        "customers": 1,
        "revenue": 100.0,
        "freight": 10.0,
        "revenue_with_freight": 110.0,
        "average_order_value": 100.0,
    }

    monkeypatch.setattr(pipeline, "load_olist_tables", lambda _: tables)
    monkeypatch.setattr(pipeline, "validate_core_tables", lambda _: None)
    monkeypatch.setattr(pipeline, "build_item_sales_fact", lambda _: sales)
    monkeypatch.setattr(pipeline, "calculate_sales_kpis", lambda _: expected)

    assert pipeline.run_pipeline("dados/raw") == expected
