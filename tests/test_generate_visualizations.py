from pathlib import Path

import pandas as pd
from scripts.generate_visualizations import generate_visualizations


def _sales() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "order_item_id": [1, 1, 1],
            "customer_unique_id": ["c1", "c2", "c3"],
            "customer_state": ["CE", "SP", "RJ"],
            "price": [100.0, 200.0, 150.0],
            "freight_value": [10.0, 20.0, 15.0],
            "product_category_name_english": [
                "health_beauty",
                "sports_leisure",
                "toys",
            ],
            "order_purchase_timestamp": [
                "2018-01-15 10:00:00",
                "2018-02-15 10:00:00",
                "2018-03-15 10:00:00",
            ],
            "is_realized_sale": [True, True, True],
        }
    )


def test_generate_visualizations_creates_documented_svgs(tmp_path: Path) -> None:
    generated = generate_visualizations(_sales(), tmp_path)

    assert {path.name for path in generated} == {
        "evolucao-mensal.svg",
        "receita-por-uf.svg",
        "receita-por-categoria.svg",
    }
    assert all(path.is_file() for path in generated)
    assert all("<svg" in path.read_text(encoding="utf-8") for path in generated)
