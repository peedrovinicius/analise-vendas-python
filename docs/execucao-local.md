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

## 4. Registrar a identidade dos arquivos de origem

Depois de obter os nove CSVs e antes de executar a análise, gere o manifesto criptográfico:

```bash
python scripts/source_manifest.py generate
```

O arquivo `dados/source-manifest.json` registra SHA-256, tamanho em bytes e quantidade de registros de cada CSV. Para confirmar posteriormente que os arquivos locais são exatamente os mesmos:

```bash
python scripts/source_manifest.py validate
```

O manifesto deve ser gerado a partir do mesmo conjunto de arquivos usado para validar e publicar os resultados. O projeto não inventa hashes quando os arquivos brutos não estão disponíveis.

## 5. Executar o pipeline oficial

```bash
python scripts/run_pipeline.py
```

O script chama `src.pipeline.run_pipeline`, que executa ingestão, validação de schema, transformação e cálculo dos KPIs consolidados.

## 6. Regenerar as visualizações publicadas

```bash
python scripts/generate_visualizations.py
```

O comando recria em `assets/` os SVGs de evolução mensal, receita por UF e receita por categoria usando a mesma fato analítica e as mesmas regras de venda realizada do projeto.

## 7. Validar os resultados publicados

```bash
python scripts/validate_published_results.py
```

A validação recalcula KPIs consolidados, receita anual, principais estados, principais categorias, recorrência de clientes e concentração de vendedores. Qualquer divergência em relação aos resultados publicados encerra o comando com erro.

Essa verificação depende dos nove CSVs originais em `dados/raw/` e funciona como teste de integração sobre a base completa, separado dos testes sintéticos executados pela CI.

## 8. Executar a auditoria dos arquivos

```bash
python scripts/auditar_olist.py
```

A auditoria informa características estruturais dos arquivos, incluindo volume, colunas, nulos, duplicidades e verificações de chaves. Ela não altera os dados.

## 9. Executar os testes e gates de qualidade

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
