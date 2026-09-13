# Modelo de dados

## Fonte

O projeto utiliza o **Brazilian E-Commerce Public Dataset by Olist**, conjunto público e anonimizado de dados de comércio eletrônico brasileiro.

## Arquivos da fonte

A base é composta por 9 arquivos CSV:

- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_customers_dataset.csv`
- `olist_products_dataset.csv`
- `olist_sellers_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_order_reviews_dataset.csv`
- `olist_geolocation_dataset.csv`
- `product_category_name_translation.csv`

## Granularidade

A tabela de referência para análise transacional será `order_items`.

Sua granularidade é **um item de pedido**. Um mesmo `order_id` pode aparecer em várias linhas quando um pedido contém múltiplos itens.

## Relacionamentos principais

```text
customers
    │ 1:N
    ▼
 orders
    │ 1:N
    ▼
order_items ───── N:1 ───── products
    │
    └────────── N:1 ───── sellers

orders ───── 1:N ───── order_payments
orders ───── 1:N ───── order_reviews

products ──── N:1 ───── product_category_name_translation
```

## Chaves e cuidados

- `orders.order_id` identifica um pedido.
- `customers.customer_id` identifica o vínculo do cliente com um pedido; `customer_unique_id` permite identificar o mesmo cliente em compras diferentes.
- `order_items` deve ser analisada no nível de item, considerando o identificador do pedido e a sequência do item.
- `products.product_id` identifica o produto.
- `sellers.seller_id` identifica o vendedor.
- `order_payments` e `order_reviews` podem possuir múltiplos registros relacionados ao mesmo pedido e não devem ser unidos diretamente à tabela de itens sem controle da granularidade.
- `geolocation` possui dados por prefixo de CEP e deve ser tratada como fonte auxiliar de localização.

## Regra de modelagem inicial

A modelagem analítica será definida após a auditoria dos arquivos reais. Não será feito um `merge` indiscriminado de todas as tabelas.

A principal preocupação será preservar a granularidade e evitar duplicação de valores em métricas como faturamento, frete, pagamentos e quantidade de pedidos.
