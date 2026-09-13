"""Ingestão dos arquivos CSV do Brazilian E-Commerce Public Dataset by Olist."""

from pathlib import Path

import pandas as pd

DATASET_FILES = {
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

EXPECTED_FILES = tuple(DATASET_FILES.values())


def validate_source_directory(data_dir: str | Path) -> None:
    """Valida a presença de todos os arquivos CSV esperados."""
    path = Path(data_dir)
    missing = [name for name in EXPECTED_FILES if not (path / name).is_file()]
    if missing:
        missing_text = "\n".join(f"- {name}" for name in missing)
        raise FileNotFoundError(f"Arquivos Olist ausentes em {path.resolve()}:\n{missing_text}")


def load_olist_tables(data_dir: str | Path) -> dict[str, pd.DataFrame]:
    """Carrega os nove arquivos Olist usando nomes canônicos de tabela."""
    validate_source_directory(data_dir)
    path = Path(data_dir)
    return {table_name: pd.read_csv(path / file_name) for table_name, file_name in DATASET_FILES.items()}
