"""Pipeline principal de ingestão, transformação e KPIs."""

from __future__ import annotations

from pathlib import Path

from src.analytics.sales_kpis import calculate_sales_kpis
from src.transformation.olist import build_item_sales_fact, load_olist_tables


def run_pipeline(raw_dir: str | Path) -> dict[str, float | int]:
    """Executa o fluxo principal de vendas sobre os CSVs da Olist."""
    tables = load_olist_tables(raw_dir)
    sales = build_item_sales_fact(tables)
    return calculate_sales_kpis(sales)
