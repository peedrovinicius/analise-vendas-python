# Qualidade dos dados

## Escopo da auditoria

A primeira auditoria foi executada sobre os 9 arquivos CSV da base pública Brazilian E-Commerce Public Dataset by Olist disponibilizados para este projeto.

## Volume das tabelas

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

`order_reviews.review_id` não deve ser tratado isoladamente como chave primária: foram encontrados 1.603 linhas participando de repetição de `review_id`. A combinação `review_id + order_id` não apresentou duplicidades.

## Valores ausentes

### Reviews

`order_reviews` possui 145.903 células nulas, concentradas principalmente nos campos textuais. Esses nulos não serão preenchidos automaticamente com valores artificiais.

### Orders

`order_approved_at`: 160 nulos.

`order_delivered_carrier_date`: 1.783 nulos.

`order_delivered_customer_date`: 2.965 nulos.

Esses campos representam etapas diferentes do ciclo do pedido. O tratamento será definido considerando `order_status` e a finalidade de cada métrica.

### Products

A tabela de produtos possui 2.448 células nulas distribuídas entre atributos descritivos. Nenhuma imputação será feita antes de avaliar o impacto de cada coluna.

## Datas

`order_purchase_timestamp` não possui nulos e cobre o intervalo de **2016-09-04 21:15:19 a 2018-10-17 17:30:18**.

## Status dos pedidos

- `delivered`: 96.478
- `shipped`: 1.107
- `canceled`: 625
- `unavailable`: 609
- `invoiced`: 314
- `processing`: 301
- `created`: 5
- `approved`: 2

A regra inicial para **venda realizada** é `order_status = delivered`.

Os demais status serão preservados para análises operacionais e não serão excluídos silenciosamente.

Na tabela `order_items`, isso corresponde a 110.197 itens de pedidos entregues, com R$ 13.221.498,11 em `price`.

## Valores numéricos

`order_items.price` e `order_items.freight_value` não possuem valores negativos.

`order_payments.payment_value` não possui valores negativos.

Foram encontrados **2 registros** com `payment_installments <= 0`. Eles serão investigados antes de qualquer indicador baseado em parcelamento.

Também foram encontrados 9 pagamentos com `payment_value = 0`; eles serão preservados até a definição da regra financeira correspondente.

## Duplicidades da geolocalização

`olist_geolocation_dataset.csv` contém 261.831 linhas exatamente duplicadas. Isso não será removido automaticamente, pois essa tabela possui granularidade própria por prefixo de CEP e poderá exigir uma regra de deduplicação específica.

## Integridade referencial

Não foram encontrados registros órfãos nos principais relacionamentos:

- `order_items.order_id` → `orders.order_id`: 0;
- `order_items.product_id` → `products.product_id`: 0;
- `order_items.seller_id` → `sellers.seller_id`: 0;
- `orders.customer_id` → `customers.customer_id`: 0.

## Regras de modelagem

`order_items` permanece como referência da granularidade transacional de itens.

`order_payments` e `order_reviews` não serão unidos diretamente à tabela de itens para métricas agregadas sem prévia adequação de granularidade, pois ambos podem possuir múltiplos registros por pedido.

Os joins dimensionais implementados no código usam validação de cardinalidade para evitar multiplicação silenciosa de linhas.

## Decisões até o momento

1. Preservar os dados brutos e não alterá-los durante a auditoria.
2. Não preencher nulos automaticamente.
3. Não remover duplicidades da geolocalização sem regra documentada.
4. Não usar `review_id` isoladamente como chave primária.
5. Considerar `delivered` como venda realizada para os KPIs de receita realizada.
6. Preservar os demais status para análises operacionais.
7. Investigar os 2 registros com `payment_installments <= 0`.
8. Evitar joins que alterem a granularidade da tabela de fatos.

## Próxima etapa

A próxima etapa será formalizar a camada `processed` e as regras de transformação, mantendo rastreabilidade entre dados brutos, dados tratados e métricas produzidas.
