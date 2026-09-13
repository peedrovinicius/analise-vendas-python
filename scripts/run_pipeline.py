"""Executa o pipeline oficial e imprime os KPIs calculados."""

# isort: skip_file

from __future__ import annotations

import json
from pathlib import Path

from src.pipeline import run_pipeline


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    raw_dir = project_root / "dados" / "raw"
    kpis = run_pipeline(raw_dir)

    print(json.dumps(kpis, indent=2, ensure_ascii=False))
