"""Valida os resultados publicados contra uma execução integral da base Olist."""

from __future__ import annotations

import math
from pathlib import Path

from src.analytics.sales_analysis import (
    customer_purchase_frequency,
    monthly_sales,
    sales_by_seller,
    sales_by_state,
)
from src.analytics.sales_kpis import calculate_sales_kpis, revenue_by_category
from src.ingestion.olist import load_olist_tables
from src.transformation.olist import build_item_sales_fact
from src.validation.olist_schema import validate_core_tables

EXPECTED_KPIS: dict[str, int | float] = {
    "orders": 96_478,
    "items": 110_197,
    "customers": 93_358,
    "revenue": 13_221_498.11,
    "freight": 2_198_275.64,
    "revenue_with_freight": 15_419_773.75,
    "average_order_value": 137.04,
}

EXPECTED_YEAR_REVENUE = {
    2016: 40_470.98,
    2017: 5_962_902.01,
    2018: 7_218_125.12,
}

EXPECTED_STATE_REVENUE = {
    "SP": 5_067_633.16,
    "RJ": 1_759_651.13,
    "MG": 1_552_481.83,
}

EXPECTED_CATEGORY_REVENUE = {
    "health_beauty": 1_233_131.72,
    "watches_gifts": 1_166_176.98,
    "bed_bath_table": 1_023_434.76,
    "sports_leisure": 954_852.55,
    "computers_accessories": 888_724.61,
}

EXPECTED_REPEAT_CUSTOMERS = 2_801
EXPECTED_TOP10_SELLER_SHARE = 0.1327
EXPECTED_TOP_SELLER_SHARE = 0.0172


def _assert_close(name: str, actual: float, expected: float, tolerance: float) -> None:
    if not math.isclose(actual, expected, abs_tol=tolerance, rel_tol=0.0):
        raise AssertionError(f"{name}: esperado {expected}, obtido {actual}")


def validate_published_results(raw_dir: str | Path) -> None:
    """Recalcula e confronta os números publicados no README e na documentação."""
    tables = load_olist_tables(raw_dir)
    validate_core_tables(tables)
    sales = build_item_sales_fact(tables)

    kpis = calculate_sales_kpis(sales)
    for name in ("orders", "items", "customers"):
        if kpis[name] != EXPECTED_KPIS[name]:
            raise AssertionError(
                f"{name}: esperado {EXPECTED_KPIS[name]}, obtido {kpis[name]}"
            )
    for name in ("revenue", "freight", "revenue_with_freight"):
        _assert_close(name, float(kpis[name]), float(EXPECTED_KPIS[name]), 0.01)
    _assert_close(
        "average_order_value",
        float(kpis["average_order_value"]),
        float(EXPECTED_KPIS["average_order_value"]),
        0.005,
    )

    monthly = monthly_sales(sales)
    annual = monthly.assign(year=monthly["purchase_month_start"].dt.year).groupby("year")[
        "revenue"
    ].sum()
    for year, expected in EXPECTED_YEAR_REVENUE.items():
        _assert_close(f"revenue_{year}", float(annual.loc[year]), expected, 0.01)

    states = sales_by_state(sales).set_index("customer_state")
    for state, expected in EXPECTED_STATE_REVENUE.items():
        _assert_close(f"state_{state}", float(states.loc[state, "revenue"]), expected, 0.01)

    categories = revenue_by_category(sales).set_index("product_category_name_english")
    for category, expected in EXPECTED_CATEGORY_REVENUE.items():
        _assert_close(
            f"category_{category}",
            float(categories.loc[category, "revenue"]),
            expected,
            0.01,
        )

    customers = customer_purchase_frequency(sales)
    repeat_customers = int(customers["orders"].gt(1).sum())
    if repeat_customers != EXPECTED_REPEAT_CUSTOMERS:
        raise AssertionError(
            "repeat_customers: "
            f"esperado {EXPECTED_REPEAT_CUSTOMERS}, obtido {repeat_customers}"
        )

    sellers = sales_by_seller(sales)
    total_seller_revenue = float(sellers["revenue"].sum())
    top10_share = float(sellers.head(10)["revenue"].sum() / total_seller_revenue)
    top_share = float(sellers.iloc[0]["revenue"] / total_seller_revenue)
    _assert_close("top10_seller_share", top10_share, EXPECTED_TOP10_SELLER_SHARE, 0.00005)
    _assert_close("top_seller_share", top_share, EXPECTED_TOP_SELLER_SHARE, 0.00005)


def main() -> None:
    """Executa a validação integral e encerra com erro em qualquer divergência."""
    project_root = Path(__file__).resolve().parents[1]
    validate_published_results(project_root / "dados" / "raw")
    print("Resultados publicados validados com sucesso.")


if __name__ == "__main__":
    main()
