"""Transformações analíticas para o Brazilian E-Commerce Public Dataset by Olist."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.ingestion.olist import load_olist_tables

REALIZED_ORDER_STATUSES = {"delivered"}


def load_olist_tables_for_transformation(raw_dir: str | Path) -> dict[str, pd.DataFrame]:
    """Mantém uma interface compatível para chamadas antigas do módulo."""
    return load_olist_tables(raw_dir)


def build_item_sales_fact(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Constrói uma visão analítica no nível de item de pedido.

    ``order_items`` define a granularidade. Dimensões 1:N por pedido, como
    pagamentos e avaliações, não são agregadas diretamente para evitar
    duplicação de métricas.
    """
    orders = tables["orders"].copy()
    items = tables["order_items"].copy()
    products = tables["products"].copy()
    sellers = tables["sellers"].copy()
    customers = tables["customers"].copy()
    translation = tables["category_translation"].copy()

    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"], errors="coerce"
    )

    sales = items.merge(
        orders[
            [
                "order_id",
                "customer_id",
                "order_status",
                "order_purchase_timestamp",
            ]
        ],
        on="order_id",
        how="left",
        validate="many_to_one",
    )

    sales = sales.merge(
        customers[
            ["customer_id", "customer_unique_id", "customer_city", "customer_state"]
        ],
        on="customer_id",
        how="left",
        validate="many_to_one",
    )

    sales = sales.merge(
        products[["product_id", "product_category_name"]],
        on="product_id",
        how="left",
        validate="many_to_one",
    )

    sales = sales.merge(
        translation,
        on="product_category_name",
        how="left",
        validate="many_to_one",
    )

    sales = sales.merge(
        sellers[["seller_id", "seller_city", "seller_state"]],
        on="seller_id",
        how="left",
        validate="many_to_one",
    )

    sales["gross_item_value"] = sales["price"]
    sales["total_item_value"] = sales["price"] + sales["freight_value"]
    sales["is_realized_sale"] = sales["order_status"].isin(REALIZED_ORDER_STATUSES)
    sales["purchase_date"] = sales["order_purchase_timestamp"].dt.normalize()
    sales["purchase_year"] = sales["order_purchase_timestamp"].dt.year.astype("Int64")
    sales["purchase_month"] = sales["order_purchase_timestamp"].dt.month.astype("Int64")

    return sales
