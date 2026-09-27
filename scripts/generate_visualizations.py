"""Regenera as visualizações SVG publicadas no README a partir dos dados brutos."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from src.analytics.sales_analysis import monthly_sales, sales_by_state
from src.analytics.sales_kpis import revenue_by_category
from src.ingestion.olist import load_olist_tables
from src.transformation.olist import build_item_sales_fact
from src.validation.olist_schema import validate_core_tables

CATEGORY_LABELS = {
    "auto": "Automotivo",
    "bed_bath_table": "Cama, mesa e banho",
    "computers_accessories": "Computadores e acessórios",
    "cool_stuff": "Artigos diversos",
    "furniture_decor": "Móveis e decoração",
    "health_beauty": "Saúde e beleza",
    "housewares": "Utilidades domésticas",
    "sports_leisure": "Esporte e lazer",
    "toys": "Brinquedos",
    "watches_gifts": "Relógios e presentes",
}


def _figure(figsize: tuple[float, float]) -> Figure:
    figure = Figure(figsize=figsize)
    FigureCanvasAgg(figure)
    return figure


def _category_label(value: object) -> str:
    if pd.isna(value):
        return "Sem categoria"
    category = str(value)
    return CATEGORY_LABELS.get(category, category.replace("_", " ").title())


def generate_visualizations(sales: pd.DataFrame, output_dir: str | Path) -> list[Path]:
    """Gera os três SVGs documentados no README usando a fato analítica."""
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    generated: list[Path] = []

    monthly = monthly_sales(sales)
    figure = _figure((12, 5))
    axis = figure.subplots()
    axis.plot(monthly["purchase_month_start"], monthly["revenue"], marker="o")
    axis.set_title("Evolução mensal da receita: pedidos entregues")
    axis.set_xlabel("Mês de compra")
    axis.set_ylabel("Receita dos itens (R$)")
    axis.tick_params(axis="x", labelrotation=45)
    figure.tight_layout()
    path = destination / "evolucao-mensal.svg"
    figure.savefig(path, format="svg", metadata={"Date": None})
    generated.append(path)

    states = sales_by_state(sales).head(10).sort_values("revenue")
    figure = _figure((9, 6))
    axis = figure.subplots()
    axis.barh(states["customer_state"], states["revenue"])
    axis.set_title("Receita por UF: pedidos entregues")
    axis.set_xlabel("Receita dos itens (R$)")
    axis.set_ylabel("UF do cliente")
    figure.tight_layout()
    path = destination / "receita-por-uf.svg"
    figure.savefig(path, format="svg", metadata={"Date": None})
    generated.append(path)

    categories = revenue_by_category(sales).head(10).sort_values("revenue")
    labels = categories["product_category_name_english"].map(_category_label)
    figure = _figure((10, 6))
    axis = figure.subplots()
    axis.barh(labels, categories["revenue"])
    axis.set_title("Receita por categoria: pedidos entregues")
    axis.set_xlabel("Receita dos itens (R$)")
    axis.set_ylabel("Categoria")
    figure.tight_layout()
    path = destination / "receita-por-categoria.svg"
    figure.savefig(path, format="svg", metadata={"Date": None})
    generated.append(path)

    return generated


def main() -> None:
    """Carrega a fonte, valida a estrutura e regenera os SVGs do projeto."""
    project_root = Path(__file__).resolve().parents[1]
    raw_dir = project_root / "dados" / "raw"
    output_dir = project_root / "assets"

    tables = load_olist_tables(raw_dir)
    validate_core_tables(tables)
    sales = build_item_sales_fact(tables)

    for path in generate_visualizations(sales, output_dir):
        print(path.relative_to(project_root))


if __name__ == "__main__":
    main()
