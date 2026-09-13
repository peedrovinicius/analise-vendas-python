"""Análises de negócio derivadas da fato de itens da Olist."""

from __future__ import annotations

import pandas as pd


def _realized_sales(sales: pd.DataFrame) -> pd.DataFrame:
    """Retorna apenas os itens classificados como vendas realizadas."""
    return sales.loc[sales["is_realized_sale"]].copy()


def _add_revenue_share(result: pd.DataFrame) -> pd.DataFrame:
    """Adiciona a participação da receita no total do resultado."""
    total = result["revenue"].sum()
    result["revenue_share"] = result["revenue"].div(total) if total else 0.0
    return result


def _add_freight_ratio(result: pd.DataFrame) -> pd.DataFrame:
    """Adiciona a relação entre frete e receita, protegendo divisão por zero."""
    result["freight_to_revenue"] = (
        result["freight"].div(result["revenue"]).where(result["revenue"] != 0, 0.0)
    )
    return result


def monthly_sales(sales: pd.DataFrame) -> pd.DataFrame:
    """Agrega vendas realizadas por mês de compra."""
    realized = _realized_sales(sales)
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
    total = result["revenue"].sum()
    result["cumulative_revenue_share"] = result["revenue"].cumsum().div(total) if total else 0.0
    return _add_freight_ratio(result)


def sales_by_state(sales: pd.DataFrame) -> pd.DataFrame:
    """Agrega receita, frete, volume e ticket médio pelo estado do cliente."""
    realized = _realized_sales(sales)
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
    result = _add_revenue_share(result)
    return _add_freight_ratio(result)


def sales_by_seller(sales: pd.DataFrame) -> pd.DataFrame:
    """Agrega receita e volume por vendedor."""
    realized = _realized_sales(sales)
    result = (
        realized.groupby("seller_id", as_index=False)
        .agg(
            revenue=("price", "sum"),
            items=("order_item_id", "size"),
            orders=("order_id", "nunique"),
        )
        .sort_values("revenue", ascending=False)
    )
    return _add_revenue_share(result)


def customer_metrics(sales: pd.DataFrame) -> pd.DataFrame:
    """Calcula métricas por cliente para segmentação e análise de valor."""
    realized = _realized_sales(sales)
    result = (
        realized.groupby("customer_unique_id", as_index=False)
        .agg(
            revenue=("price", "sum"),
            orders=("order_id", "nunique"),
            items=("order_item_id", "size"),
        )
        .sort_values("revenue", ascending=False)
    )
    result["average_order_value"] = result["revenue"].div(result["orders"])
    result["items_per_order"] = result["items"].div(result["orders"])
    result["customer_segment"] = result["orders"].gt(1).map(
        {True: "repeat", False: "one_time"}
    )
    return result


def customer_purchase_frequency(sales: pd.DataFrame) -> pd.DataFrame:
    """Resume receita, pedidos e itens por cliente único."""
    return customer_metrics(sales)[["customer_unique_id", "revenue", "orders", "items"]]


def customer_segment_summary(sales: pd.DataFrame) -> pd.DataFrame:
    """Resume clientes em segmentos de compra única e recorrente."""
    customers = customer_metrics(sales)
    if customers.empty:
        return pd.DataFrame(
            columns=[
                "customer_segment",
                "customers",
                "orders",
                "items",
                "revenue",
                "revenue_share",
                "average_orders_per_customer",
                "average_revenue_per_customer",
            ]
        )

    result = (
        customers.groupby("customer_segment", as_index=False)
        .agg(
            customers=("customer_unique_id", "nunique"),
            orders=("orders", "sum"),
            items=("items", "sum"),
            revenue=("revenue", "sum"),
        )
        .sort_values("revenue", ascending=False)
    )
    result = _add_revenue_share(result)
    result["average_orders_per_customer"] = result["orders"].div(result["customers"])
    result["average_revenue_per_customer"] = result["revenue"].div(result["customers"])
    return result


def repeat_customer_rate(sales: pd.DataFrame) -> float:
    """Calcula a proporção de clientes únicos com mais de um pedido."""
    customers = customer_metrics(sales)
    if customers.empty:
        return 0.0
    return float(customers["customer_segment"].eq("repeat").mean())


def category_revenue(sales: pd.DataFrame) -> pd.DataFrame:
    """Agrega receita, frete, itens, pedidos e ticket médio por categoria traduzida."""
    realized = _realized_sales(sales)
    result = realized.groupby("product_category_name_english", dropna=False, as_index=False).agg(
        revenue=("price", "sum"),
        freight=("freight_value", "sum"),
        items=("order_item_id", "size"),
        orders=("order_id", "nunique"),
    )
    result = result.sort_values("revenue", ascending=False)
    result["average_order_value"] = result["revenue"].div(result["orders"])
    result = _add_revenue_share(result)
    return _add_freight_ratio(result)


def top_n_revenue_share(grouped: pd.DataFrame, n: int, revenue_column: str = "revenue") -> float:
    """Retorna a participação da receita concentrada nos n primeiros grupos."""
    if n <= 0 or grouped.empty:
        return 0.0
    total = grouped[revenue_column].sum()
    if total == 0:
        return 0.0
    return float(grouped.nlargest(n, revenue_column)[revenue_column].sum() / total)
