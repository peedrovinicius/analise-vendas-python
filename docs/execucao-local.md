# Execução local

## 1. Obter os dados

Baixe o **Brazilian E-Commerce Public Dataset by Olist** diretamente da fonte indicada em `docs/fonte-dados.md`.

Os arquivos brutos não devem ser versionados no GitHub. O `.gitignore` bloqueia os diretórios de dados brutos e processados.

## 2. Estrutura esperada

Coloque os 9 arquivos CSV diretamente em:

```text
dados/raw/
```

Arquivos esperados:

```text
olist_orders_dataset.csv
olist_order_items_dataset.csv
olist_customers_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_geolocation_dataset.csv
product_category_name_translation.csv
```

## 3. Instalar dependências

Na raiz do repositório, de preferência em um ambiente virtual:

```bash
pip install -r requirements.txt
pip install -e . --no-deps
```

## 4. Executar o pipeline oficial

```bash
python scripts/run_pipeline.py
```

O script chama `src.pipeline.run_pipeline`, que executa ingestão, validação de schema, transformação e cálculo dos KPIs consolidados.

## 5. Executar a auditoria dos arquivos

```bash
python scripts/auditar_olist.py
```

A auditoria informa características estruturais dos arquivos, incluindo volume, colunas, nulos, duplicidades e verificações de chaves. Ela não altera os dados.

## 6. Executar os testes e gates de qualidade

```bash
ruff format --check src tests scripts
ruff check src tests scripts
mypy src
pytest -q --cov=src --cov-branch --cov-report=term-missing --cov-fail-under=80
pip-audit -r requirements.txt
pre-commit run --all-files
```

Esses mesmos gates são executados automaticamente pelo workflow de CI em `.github/workflows/ci.yml`.

## Resultado esperado

Com a versão atual da base utilizada no projeto, a execução do pipeline reproduz os KPIs consolidados documentados em `docs/insights-iniciais.md` e `docs/insights-negocio.md`.
