"""Auditoria estrutural inicial dos arquivos Olist.

Uso:
    python scripts/auditar_olist.py

Os arquivos CSV devem estar em dados/raw/.
O script não modifica os dados.
"""

from pathlib import Path

import pandas as pd

from src.ingestion.olist import EXPECTED_FILES, load_olist_data


DATA_DIR = Path("dados/raw")

KEY_COLUMNS = {
    "olist_orders_dataset": ["order_id"],
    "olist_order_items_dataset": ["order_id", "order_item_id"],
    "olist_customers_dataset": ["customer_id"],
    "olist_products_dataset": ["product_id"],
    "olist_sellers_dataset": ["seller_id"],
    "olist_order_payments_dataset": [],
    "olist_order_reviews_dataset": [],
    "olist_geolocation_dataset": [],
    "product_category_name_translation": ["product_category_name"],
}


def audit_dataframe(name: str, df: pd.DataFrame) -> dict[str, object]:
    """Return structural and quality indicators for one DataFrame."""
    result: dict[str, object] = {
        "dataset": name,
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_cells": int(df.isna().sum().sum()),
        "missing_columns": int((df.isna().sum() > 0).sum()),
        "columns_list": list(df.columns),
    }

    keys = KEY_COLUMNS.get(name, [])
    if keys:
        result["key_columns"] = keys
        result["duplicate_key_rows"] = int(df.duplicated(subset=keys).sum())
    else:
        result["key_columns"] = []
        result["duplicate_key_rows"] = None

    return result


def main() -> None:
    """Load the source files and print a reproducible audit summary."""
    datasets = load_olist_data(DATA_DIR)

    print("=== AUDITORIA INICIAL — OLIST ===")
    print(f"Diretório: {DATA_DIR.resolve()}")
    print(f"Arquivos esperados: {len(EXPECTED_FILES)}")
    print()

    reports = [audit_dataframe(name, df) for name, df in datasets.items()]

    for report in reports:
        print(f"[{report['dataset']}]")
        print(f"  Linhas: {report['rows']:,}")
        print(f"  Colunas: {report['columns']}")
        print(f"  Linhas duplicadas: {report['duplicate_rows']:,}")
        print(f"  Células nulas: {report['missing_cells']:,}")
        print(f"  Colunas com nulos: {report['missing_columns']}")
        print(f"  Chave(s): {report['key_columns'] or 'não definida nesta etapa'}")
        if report["duplicate_key_rows"] is not None:
            print(f"  Linhas duplicadas na chave: {report['duplicate_key_rows']:,}")
        print("  Colunas:")
        for column in report["columns_list"]:
            print(f"    - {column}")
        print()


if __name__ == "__main__":
    main()
