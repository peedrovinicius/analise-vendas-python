"""Métricas de negócio para a análise de vendas da Olist."""

from __future__ import annotations

import pandas as pd


def calculate_sales_kpis(sales: pd.DataFrame) -> dict[str, float | int]:
    """Calcula KPIs sobre itens associados a pedidos realizados."""
    realized = sales.loc[sales["is_realized_sale"]].copy()

    if realized.empty:
        return {
            "orders": 0,
            "items": 0,
            "customers": 0,
            "revenue": 0.0,
            "freight": 0.0,
            "revenue_with_freight": 0.0,
            "average_order_value": 0.0,
        }

    revenue = float(realized["price"].sum())
    freight = float(realized["freight_value"].sum())
    orders = int(realized["order_id"].nunique())

    return {
        "orders": orders,
        "items": int(len(realized)),
        "customers": int(realized["customer_unique_id"].nunique()),
        "revenue": revenue,
        "freight": freight,
        "revenue_with_freight": revenue + freight,
        "average_order_value": revenue / orders if orders else 0.0,
    }


def revenue_by_category(sales: pd.DataFrame) -> pd.DataFrame:
    """Agrega receita e itens por categoria para pedidos realizados."""
    realized = sales.loc[sales["is_realized_sale"]].copy()
    return (
        realized.groupby(
            "product_category_name_english", dropna=False, as_index=False
        )
        .agg(revenue=("price", "sum"), items=("order_item_id", "size"))
        .sort_values("revenue", ascending=False)
    )
