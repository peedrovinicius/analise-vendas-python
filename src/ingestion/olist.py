"""Ingestão dos arquivos CSV do Brazilian E-Commerce Public Dataset by Olist."""

from pathlib import Path
from typing import Dict

import pandas as pd

EXPECTED_FILES = (
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_geolocation_dataset.csv",
    "product_category_name_translation.csv",
)


def validate_source_directory(data_dir: str | Path) -> None:
    """Validate that all expected Olist CSV files are available.

    Args:
        data_dir: Directory containing the downloaded Olist CSV files.

    Raises:
        FileNotFoundError: If one or more expected files are missing.
    """
    path = Path(data_dir)
    missing = [name for name in EXPECTED_FILES if not (path / name).is_file()]
    if missing:
        missing_text = "\n".join(f"- {name}" for name in missing)
        raise FileNotFoundError(
            "Arquivos Olist ausentes em "
            f"{path.resolve()}:\n{missing_text}"
        )


def load_olist_data(data_dir: str | Path) -> Dict[str, pd.DataFrame]:
    """Load all Olist CSV files into a dictionary keyed by dataset name."""
    validate_source_directory(data_dir)
    path = Path(data_dir)

    return {
        file_name.removesuffix(".csv"): pd.read_csv(path / file_name)
        for file_name in EXPECTED_FILES
    }
