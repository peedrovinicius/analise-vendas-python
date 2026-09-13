"""Validação de schema para as tabelas críticas da base Olist."""

from __future__ import annotations

import pandas as pd
import pandera.pandas as pa


ORDERS_SCHEMA = pa.DataFrameSchema(
    {
        "order_id": pa.Column(str, nullable=False, unique=True),
        "customer_id": pa.Column(str, nullable=False),
        "order_status": pa.Column(str, nullable=False),
        "order_purchase_timestamp": pa.Column(str, nullable=False),
    },
    strict=False,
    coerce=False,
)

ORDER_ITEMS_SCHEMA = pa.DataFrameSchema(
    {
        "order_id": pa.Column(str, nullable=False),
        "order_item_id": pa.Column(int, nullable=False),
        "product_id": pa.Column(str, nullable=False),
        "seller_id": pa.Column(str, nullable=False),
        "price": pa.Column(float, nullable=False, checks=pa.Check.ge(0)),
        "freight_value": pa.Column(float, nullable=False, checks=pa.Check.ge(0)),
    },
    strict=False,
    coerce=False,
)


def validate_core_tables(tables: dict[str, pd.DataFrame]) -> None:
    """Valida as tabelas críticas antes da transformação."""
    ORDERS_SCHEMA.validate(tables["orders"], lazy=True)
    ORDER_ITEMS_SCHEMA.validate(tables["order_items"], lazy=True)
