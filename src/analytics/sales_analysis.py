"""Análises de negócio derivadas da fato de itens da Olist."""

from __future__ import annotations

import pandas as pd


def monthly_sales(sales: pd.DataFrame) -> pd.DataFrame:
    """Agrega vendas realizadas por mês de compra."""
    realized = sales.loc[sales["is_realized_sale"]].copy()
    realized["purchase_month_start"] = (
        pd.to_datetime(realized["order_purchase_timestamp"], errors="coerce")
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    result = (
        realized.groupby("purchase_month_start", as_index=False)
        .agg(
            revenue=("price", "sum"),
            freight=("freight_value", "sum"),
            items=("order_item_id", "size"),
            orders=("order_id", "nunique"),
            customers=("customer_unique_id", "nunique"),
        )
        .sort_values("purchase_month_start")
    )
    result["average_order_value"] = result["revenue"].div(result["orders"])
    result["revenue_mom_growth"] = result["revenue"].pct_change()
    return result


def sales_by_state(sales: pd.DataFrame) -> pd.DataFrame:
    """Agrega receita, frete, volume e ticket médio pelo estado do cliente."""
    realized = sales.loc[sales["is_realized_sale"]].copy()
    result = (
        realized.groupby("customer_state", as_index=False)
        .agg(
            revenue=("price", "sum"),
            freight=("freight_value", "sum"),
            items=("order_item_id", "size"),
            orders=("order_id", "nunique"),
            customers=("customer_unique_id", "nunique"),
        )
        .sort_values("revenue", ascending=False)
    )
    result["average_order_value"] = result["revenue"].div(result["orders"])
    total = result["revenue"].sum()
    result["revenue_share"] = result["revenue"].div(total) if total else 0.0
    result["freight_to_revenue"] = result["freight"].div(result["revenue"]).where(result["revenue"] != 0, 0.0)
    return result


def sales_by_seller(sales: pd.DataFrame) -> pd.DataFrame:
    """Agrega receita e volume por vendedor."""
    realized = sales.loc[sales["is_realized_sale"]].copy()
    result = (
        realized.groupby("seller_id", as_index=False)
        .agg(
            revenue=("price", "sum"),
            items=("order_item_id", "size"),
            orders=("order_id", "nunique"),
        )
        .sort_values("revenue", ascending=False)
    )
    total = result["revenue"].sum()
    result["revenue_share"] = result["revenue"].div(total) if total else 0.0
    return result


def customer_purchase_frequency(sales: pd.DataFrame) -> pd.DataFrame:
    """Resume receita, pedidos e itens por cliente único."""
    realized = sales.loc[sales["is_realized_sale"]].copy()
    return (
        realized.groupby("customer_unique_id", as_index=False)
        .agg(
            revenue=("price", "sum"),
            orders=("order_id", "nunique"),
            items=("order_item_id", "size"),
        )
        .sort_values("revenue", ascending=False)
    )


def repeat_customer_rate(sales: pd.DataFrame) -> float:
    """Calcula a proporção de clientes únicos com mais de um pedido."""
    customers = customer_purchase_frequency(sales)
    if customers.empty:
        return 0.0
    return float((customers["orders"] > 1).mean())


def category_revenue(sales: pd.DataFrame) -> pd.DataFrame:
    """Agrega receita, frete, itens, pedidos e ticket médio por categoria traduzida."""
    realized = sales.loc[sales["is_realized_sale"]].copy()
    result = realized.groupby("product_category_name_english", dropna=False, as_index=False).agg(
        revenue=("price", "sum"),
        freight=("freight_value", "sum"),
        items=("order_item_id", "size"),
        orders=("order_id", "nunique"),
    )
    result = result.sort_values("revenue", ascending=False)
    result["average_order_value"] = result["revenue"].div(result["orders"])
    total = result["revenue"].sum()
    result["revenue_share"] = result["revenue"].div(total) if total else 0.0
    result["freight_to_revenue"] = result["freight"].div(result["revenue"]).where(result["revenue"] != 0, 0.0)
    return result


def top_n_revenue_share(grouped: pd.DataFrame, n: int, revenue_column: str = "revenue") -> float:
    """Retorna a participação da receita concentrada nos n primeiros grupos."""
    if n <= 0 or grouped.empty:
        return 0.0
    total = grouped[revenue_column].sum()
    if total == 0:
        return 0.0
    return float(grouped.nlargest(n, revenue_column)[revenue_column].sum() / total)
