# Auditoria inicial da base Olist

## Status

**Etapa:** perfil estrutural da fonte concluído; validação computacional local pendente.

Esta etapa registra somente características confirmadas na documentação pública da fonte e em referências técnicas que reproduzem os arquivos originais. Contagens de nulos, duplicidades, chaves e consistência entre tabelas serão calculadas pelo próprio projeto após a ingestão dos arquivos.

## Fonte

**Brazilian E-Commerce Public Dataset by Olist**

Fonte original: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

A Olist descreve o conjunto como dados comerciais reais de comércio eletrônico brasileiro, anonimizados, cobrindo aproximadamente 100 mil pedidos entre 2016 e 2018. O conjunto possui 9 arquivos relacionais.

## Inventário estrutural conhecido

| Arquivo | Registros conhecidos | Função analítica inicial |
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

As contagens acima são referências públicas do conjunto e serão reconfirmadas automaticamente durante a ingestão.

## Chaves e granularidade

### Orders

`order_id` identifica o pedido. A tabela possui `customer_id`, status e timestamps do ciclo do pedido.

### Customers

`customer_id` é a chave usada para relacionar o pedido ao cadastro do cliente. `customer_unique_id` é a identificação adequada para analisar recompra do mesmo cliente em pedidos diferentes.

### Order Items

A granularidade é **um item de pedido**. `order_id` pode aparecer várias vezes quando um pedido contém múltiplos itens. O registro também informa `order_item_id`, `product_id`, `seller_id`, `shipping_limit_date`, `price` e `freight_value`.

### Payments

A granularidade é de registros de pagamento por pedido, identificados pelo conjunto de pedido e sequência do pagamento. Um pedido pode possuir múltiplos registros de pagamento.

### Reviews

A tabela contém a avaliação associada ao pedido e pode possuir mais de um registro relacionado ao mesmo `order_id`. Não será unida diretamente à tabela de itens sem controle da granularidade.

### Products

`product_id` identifica o produto. A tabela contém informações de categoria e atributos físicos.

### Sellers

`seller_id` identifica o vendedor.

### Geolocation

A geolocalização trabalha em nível de prefixo de CEP e será tratada como fonte auxiliar. Não deve ser assumida como uma dimensão 1:1 sem validação da cardinalidade.

## Riscos de qualidade já conhecidos

A documentação da fonte informa que um pedido pode possuir vários itens e que diferentes itens do mesmo pedido podem ser atendidos por vendedores distintos. Isso torna a granularidade um risco central para qualquer cálculo de faturamento, frete ou quantidade de pedidos.

As datas do ciclo de pedido possuem campos que podem ficar ausentes dependendo do status do pedido. Esses valores não serão preenchidos artificialmente: serão medidos e tratados segundo regras documentadas.

Pagamentos e avaliações podem possuir múltiplos registros por pedido. Somar esses valores depois de um `merge` direto com itens pode produzir duplicação e resultados incorretos.

## Regras de auditoria que serão executadas

1. Contagem de linhas e colunas por arquivo.
2. Tipagem efetiva de cada coluna.
3. Taxa e contagem de valores ausentes.
4. Duplicidade de chaves.
5. Integridade referencial entre chaves relacionadas.
6. Cardinalidade dos relacionamentos.
7. Intervalos e consistência temporal.
8. Valores negativos ou incompatíveis com o significado das colunas.
9. Consistência categórica.
10. Outliers quantitativos relevantes.
11. Comparação das métricas antes e depois do tratamento.

## Regra de ouro

Nenhuma métrica do projeto será publicada antes de a sua definição, granularidade e regra de cálculo estarem documentadas e validadas sobre os dados ingeridos.

## Referências

- Olist. *Brazilian E-Commerce Public Dataset by Olist*. Kaggle. https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- https://github.com/fortunewalla/olist
- https://db.in.tum.de/teaching/ws2526/DBSandere/notebook.html?lang=en
