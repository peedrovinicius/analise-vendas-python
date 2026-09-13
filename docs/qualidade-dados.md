# Qualidade dos dados

## Escopo da auditoria

A primeira auditoria foi executada sobre os 9 arquivos CSV da base pública Brazilian E-Commerce Public Dataset by Olist disponibilizados no arquivo recebido para este projeto.

A auditoria mede a estrutura dos arquivos, valores ausentes, duplicidades de linhas, unicidade de chaves, intervalos de datas, valores numéricos inválidos e integridade referencial entre as tabelas.

## Resultado estrutural

| Arquivo | Linhas | Colunas | Valores nulos | Linhas duplicadas |
|---|---:|---:|---:|---:|
| `olist_customers_dataset.csv` | 99.441 | 5 | 0 | 0 |
| `olist_geolocation_dataset.csv` | 1.000.163 | 5 | 0 | 261.831 |
| `olist_order_items_dataset.csv` | 112.650 | 7 | 0 | 0 |
| `olist_order_payments_dataset.csv` | 103.886 | 5 | 0 | 0 |
| `olist_order_reviews_dataset.csv` | 99.224 | 7 | 145.903 | 0 |
| `olist_orders_dataset.csv` | 99.441 | 8 | 4.908 | 0 |
| `olist_products_dataset.csv` | 32.951 | 9 | 2.448 | 0 |
| `olist_sellers_dataset.csv` | 3.095 | 4 | 0 | 0 |
| `product_category_name_translation.csv` | 71 | 2 | 0 | 0 |

## Chaves e unicidade

As seguintes chaves apresentaram unicidade na auditoria:

- `orders.order_id`: 0 duplicidades;
- `customers.customer_id`: 0 duplicidades;
- `products.product_id`: 0 duplicidades;
- `sellers.seller_id`: 0 duplicidades;
- `product_category_name_translation.product_category_name`: 0 duplicidades;
- `order_items.(order_id, order_item_id)`: 0 duplicidades;
- `order_payments.(order_id, payment_sequential)`: 0 duplicidades.

`order_reviews.review_id` não deve ser tratado isoladamente como chave primária: foram encontrados 814 linhas adicionais com `review_id` repetido, envolvendo 789 identificadores repetidos. A combinação `review_id + order_id` não apresentou duplicidades.

## Valores ausentes

### Reviews

`order_reviews` possui 145.903 células nulas. Os nulos estão concentrados nos campos textuais e não devem ser preenchidos automaticamente com valores artificiais. A presença de comentário não será tratada como requisito para a existência de uma avaliação.

### Orders

`order_approved_at`: 160 nulos.

`order_delivered_carrier_date`: 1.783 nulos.

`order_delivered_customer_date`: 2.965 nulos.

Esses campos representam etapas diferentes do ciclo do pedido. Nulos podem ser legítimos para pedidos que ainda não avançaram determinada etapa ou para determinados status; a regra de tratamento será definida considerando `order_status`.

### Products

A tabela de produtos possui 2.448 células nulas distribuídas entre atributos descritivos e dimensionais. Nenhuma imputação será feita antes de avaliar o impacto de cada coluna na análise.

## Datas

Na tabela `orders`, `order_purchase_timestamp` não possui nulos e cobre o intervalo de **2016-09-04 21:15:19 a 2018-10-17 17:30:18**.

As demais datas de ciclo de vida possuem nulos conforme registrado acima. A conversão para tipos temporais ocorrerá na etapa de transformação.

## Status dos pedidos

Foram encontrados os seguintes status:

- `delivered`: 96.478
- `shipped`: 1.107
- `canceled`: 625
- `unavailable`: 609
- `invoiced`: 314
- `processing`: 301
- `created`: 5
- `approved`: 2

A definição de quais status representam vendas válidas para cada KPI será feita explicitamente. Não será aplicada uma regra genérica de “somar todos os pedidos”.

## Valores numéricos

`order_items.price` e `order_items.freight_value` não possuem valores negativos.

`order_payments.payment_value` não possui valores negativos.

Foram encontrados **2 registros** com `payment_installments <= 0`. Esses registros serão investigados antes de qualquer tratamento.

Os atributos numéricos de produto não apresentaram valores negativos na auditoria inicial.

## Duplicidades da geolocalização

`olist_geolocation_dataset.csv` contém 261.831 linhas exatamente duplicadas. Isso não será tratado como erro automaticamente: a granularidade dessa tabela é diferente das demais e precisa ser definida antes de qualquer agregação ou relacionamento com CEP.

## Integridade referencial

Na auditoria inicial não foram encontrados registros órfãos para os seguintes relacionamentos:

- `order_items.order_id` → `orders.order_id`;
- `order_items.product_id` → `products.product_id`;
- `order_items.seller_id` → `sellers.seller_id`;
- `orders.customer_id` → `customers.customer_id`.

Também não foram encontradas categorias na tabela de tradução que não existam na coluna `product_category_name` dos produtos não nulos.

## Decisões até o momento

1. Não remover nulos automaticamente.
2. Não remover duplicidades da geolocalização sem avaliar sua granularidade.
3. Não usar `review_id` isoladamente como chave primária.
4. Não agregar pagamentos diretamente aos itens sem controlar a cardinalidade.
5. Definir os KPIs a partir de regras explícitas de negócio e status dos pedidos.
6. Investigar os dois registros com `payment_installments <= 0`.

## Próxima etapa

A próxima etapa será a criação da camada de transformação, começando pela padronização de tipos, datas e colunas e pela definição formal das regras de tratamento identificadas nesta auditoria.
