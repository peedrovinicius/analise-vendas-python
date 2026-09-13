"""Transformações analíticas para o dataset Brazilian E-Commerce Public Dataset by Olist."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REALIZED_ORDER_STATUSES = {"delivered"}


def load_olist_tables(raw_dir: str | Path) -> dict[str, pd.DataFrame]:
    """Carrega os nove arquivos CSV esperados da base Olist.

    Parameters
    ----------
    raw_dir:
        Diretório que contém os CSVs originais da fonte.

    Returns
    -------
    dict[str, pandas.DataFrame]
        Tabelas indexadas por nome lógico.

    Raises
    ------
    FileNotFoundError
        Se algum arquivo obrigatório não estiver presente.
    """
    raw_path = Path(raw_dir)
    files = {
        "customers": "olist_customers_dataset.csv",
        "geolocation": "olist_geolocation_dataset.csv",
        "order_items": "olist_order_items_dataset.csv",
        "order_payments": "olist_order_payments_dataset.csv",
        "order_reviews": "olist_order_reviews_dataset.csv",
        "orders": "olist_orders_dataset.csv",
        "products": "olist_products_dataset.csv",
        "sellers": "olist_sellers_dataset.csv",
        "category_translation": "product_category_name_translation.csv",
    }

    missing = [name for name in files.values() if not (raw_path / name).exists()]
    if missing:
        raise FileNotFoundError(
            "Arquivos Olist ausentes em "
            f"{raw_path}: {', '.join(missing)}"
        )

    return {
        key: pd.read_csv(raw_path / filename)
        for key, filename in files.items()
    }


def build_item_sales_fact(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Constrói uma visão analítica no nível de item de pedido.

    A tabela resultante usa ``order_items`` como granularidade e incorpora
    apenas dimensões que preservam essa granularidade. Pagamentos e avaliações
    ficam fora desta transformação porque possuem cardinalidades 1:N em
    relação a pedidos e poderiam duplicar métricas quando agregados diretamente.
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
        customers[["customer_id", "customer_unique_id", "customer_city", "customer_state"]],
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

    sales["gross_item_value"] = sales["price"] * sales["order_item_id"].where(
        sales["order_item_id"].notna(), 1
    )
    sales["gross_item_value"] = sales["price"]
    sales["total_item_value"] = sales["price"] + sales["freight_value"]
    sales["is_realized_sale"] = sales["order_status"].isin(REALIZED_ORDER_STATUSES)
    sales["purchase_date"] = sales["order_purchase_timestamp"].dt.date
    sales["purchase_year"] = sales["order_purchase_timestamp"].dt.year.astype("Int64")
    sales["purchase_month"] = sales["order_purchase_timestamp"].dt.month.astype("Int64")

    return sales
