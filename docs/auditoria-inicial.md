# Auditoria inicial da base Olist

## Status

**Etapa:** perfil estrutural e validação computacional concluídos.

Esta documentação registra as características da fonte e os principais pontos de atenção identificados antes e durante a construção da camada analítica. As contagens, chaves, duplicidades, nulos, integridade referencial e regras de qualidade foram reconfirmadas pela auditoria do projeto.

## Fonte

**Brazilian E-Commerce Public Dataset by Olist**

Fonte original: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

A Olist descreve o conjunto como dados comerciais reais de comércio eletrônico brasileiro, anonimizados, cobrindo aproximadamente 100 mil pedidos entre 2016 e 2018. O conjunto possui 9 arquivos relacionais.

## Inventário estrutural

| Arquivo | Registros | Função analítica |
|---|---:|---|
| `olist_orders_dataset.csv` | 99.441 | Pedidos e ciclo de entrega |
| `olist_order_items_dataset.csv` | 112.650 | Itens vendidos; principal granularidade transacional |
| `olist_order_payments_dataset.csv` | 103.886 | Transações de pagamento |
| `olist_order_reviews_dataset.csv` | 99.224 | Avaliações dos pedidos |
| `olist_customers_dataset.csv` | 99.441 | Cliente e localização do pedido |
| `olist_products_dataset.csv` | 32.951 | Cadastro de produtos |
| `olist_sellers_dataset.csv` | 3.095 | Cadastro de vendedores |
| `olist_geolocation_dataset.csv` | 1.000.163 | Geolocalização por prefixo de CEP |
| `product_category_name_translation.csv` | 71 | Tradução de categorias |

## Chaves e granularidade

### Orders

`order_id` identifica o pedido. A tabela possui `customer_id`, status e timestamps do ciclo do pedido.

### Customers

`customer_id` é a chave usada para relacionar o pedido ao cadastro do cliente. `customer_unique_id` é utilizado para analisar recompra do mesmo cliente em pedidos diferentes.

### Order Items

A granularidade é **um item de pedido**. `order_id` pode aparecer várias vezes quando um pedido contém múltiplos itens. O registro também informa `order_item_id`, `product_id`, `seller_id`, `shipping_limit_date`, `price` e `freight_value`.

### Payments

A granularidade é de registros de pagamento por pedido, identificados pelo conjunto de pedido e sequência do pagamento. Um pedido pode possuir múltiplos registros de pagamento.

### Reviews

A tabela contém avaliações associadas aos pedidos e pode possuir mais de um registro relacionado ao mesmo `order_id`. Não é unida diretamente à fato de itens sem controle da granularidade.

### Products

`product_id` identifica o produto. A tabela contém informações de categoria e atributos físicos.

### Sellers

`seller_id` identifica o vendedor.

### Geolocation

A geolocalização trabalha em nível de prefixo de CEP e é tratada como fonte auxiliar. Não é assumida como dimensão 1:1 sem validação de cardinalidade.

## Principais achados de qualidade

- As chaves principais de pedidos, clientes, produtos e vendedores não apresentaram duplicidades.
- `order_items.(order_id, order_item_id)` e `order_payments.(order_id, payment_sequential)` também apresentaram unicidade.
- `order_reviews.review_id` não deve ser tratado isoladamente como chave primária; a combinação `review_id + order_id` apresentou unicidade.
- Existem campos nulos em etapas do ciclo de pedidos, atributos de produtos e conteúdo textual de avaliações.
- A geolocalização possui 261.831 linhas exatamente duplicadas.
- Não foram encontrados registros órfãos nos principais relacionamentos utilizados pela transformação.
- `order_items.price`, `freight_value` e `order_payments.payment_value` não possuem valores negativos.
- Foram identificados 2 registros com `payment_installments <= 0` e 9 pagamentos com `payment_value = 0`; ambos permanecem fora dos KPIs centrais atuais.

## Riscos de modelagem

Um pedido pode possuir vários itens e diferentes itens do mesmo pedido podem ser atendidos por vendedores distintos. Essa característica torna a definição da granularidade essencial para qualquer cálculo de receita, frete ou quantidade de pedidos.

Pagamentos e avaliações podem possuir múltiplos registros por pedido. Unir essas tabelas diretamente à fato de itens sem tratamento pode multiplicar linhas e inflar métricas.

## Regra adotada

Para os KPIs de receita realizada, são considerados itens associados a pedidos com `order_status = delivered`. `price` representa a receita dos itens e `freight_value` é analisado separadamente.

## Regra de ouro

Nenhuma métrica do projeto deve ser publicada antes de sua definição, granularidade e regra de cálculo estarem documentadas e validadas sobre os dados ingeridos.

## Referência

Olist. *Brazilian E-Commerce Public Dataset by Olist*. Kaggle. https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
