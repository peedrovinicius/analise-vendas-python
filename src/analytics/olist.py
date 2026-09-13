"""Métricas de negócio para a base Brazilian E-Commerce Public Dataset by Olist."""

from __future__ import annotations

import pandas as pd


def calculate_sales_kpis(sales: pd.DataFrame) -> dict[str, float | int]:
    """Calcula KPIs sobre uma visão no nível de item de pedido.

    A função utiliza somente linhas marcadas como vendas realizadas por
    ``is_realized_sale``. O valor de venda considera apenas ``price``; frete é
    mantido como métrica separada para evitar misturar conceitos.
    """
    required = {
        "is_realized_sale",
        "order_id",
        "customer_unique_id",
        "product_id",
        "price",
        "freight_value",
    }
    missing = required.difference(sales.columns)
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {sorted(missing)}")

    realized = sales.loc[sales["is_realized_sale"]].copy()

    gross_revenue = float(realized["price"].sum())
    freight_revenue = float(realized["freight_value"].sum())
    total_items = int(len(realized))
    total_orders = int(realized["order_id"].nunique())
    total_customers = int(realized["customer_unique_id"].nunique())
    total_products = int(realized["product_id"].nunique())

    return {
        "gross_revenue": gross_revenue,
        "freight_value": freight_revenue,
        "order_value_including_freight": gross_revenue + freight_revenue,
        "total_items": total_items,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "total_products": total_products,
        "average_order_value": gross_revenue / total_orders
        if total_orders
        else 0.0,
        "average_item_price": gross_revenue / total_items if total_items else 0.0,
    }
