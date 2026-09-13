"""Executa o pipeline e imprime os KPIs oficiais da base carregada."""

from __future__ import annotations

import json
from pathlib import Path

from src.analytics.sales_kpis import calculate_sales_kpis
from src.transformation.olist import build_item_sales_fact, load_olist_tables


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    raw_dir = project_root / "dados" / "raw"

    tables = load_olist_tables(raw_dir)
    sales = build_item_sales_fact(tables)
    kpis = calculate_sales_kpis(sales)

    print(json.dumps(kpis, indent=2, ensure_ascii=False))
