# Execução local

## 1. Obter os dados

Baixe o **Brazilian E-Commerce Public Dataset by Olist** diretamente da fonte indicada em `docs/fonte-dados.md`.

Não coloque os arquivos brutos no GitHub. O `.gitignore` do projeto já bloqueia os diretórios de dados brutos e processados.

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

No ambiente virtual do projeto:

```bash
pip install -r requirements.txt
```

## 4. Executar a auditoria

Na raiz do repositório:

```bash
python scripts/auditar_olist.py
```

O script não altera os dados. Ele informa, para cada arquivo, quantidade de linhas, quantidade de colunas, linhas duplicadas, células nulas, colunas com nulos, chaves configuradas e possíveis duplicidades nessas chaves.

## 5. Próxima etapa

Os resultados da execução serão usados para preencher `docs/qualidade-dados.md` com números reais e definir as regras de tratamento antes da criação de métricas.
