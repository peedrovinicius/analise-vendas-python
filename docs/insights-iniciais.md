# Insights iniciais

Esta página registra apenas resultados calculados a partir dos arquivos públicos da Olist disponibilizados para o projeto e processados pela camada analítica.

## Escopo

Os KPIs desta etapa consideram itens associados a pedidos com `order_status = delivered`. Pedidos com outros status permanecem disponíveis para análises operacionais e não são removidos da fonte.

## Resultados consolidados

- Pedidos entregues: **96.478**.
- Itens associados a pedidos entregues: **110.197**.
- Receita dos itens (`price`): **R$ 13.221.498,11**.
- Frete associado aos itens: **R$ 2.198.275,64**.
- Valor de itens + frete: **R$ 15.419.773,75**.
- Clientes únicos com itens em pedidos entregues: **93.358**.
- Ticket médio de pedido, considerando apenas `price`: **R$ 137,04**.

## Evolução temporal

A receita dos itens em pedidos entregues foi de **R$ 40.470,98 em 2016**, **R$ 5.962.902,01 em 2017** e **R$ 7.218.125,12 em 2018** dentro do período disponível na base.

O crescimento temporal será analisado com cuidado porque a cobertura de 2016 e 2018 é parcial. Portanto, os valores anuais não devem ser comparados sem considerar o número de meses efetivamente cobertos em cada ano.

## Categorias

As categorias com maior receita dos itens foram:

1. `health_beauty` — R$ 1.233.131,72.
2. `watches_gifts` — R$ 1.166.176,98.
3. `bed_bath_table` — R$ 1.023.434,76.
4. `sports_leisure` — R$ 954.852,55.
5. `computers_accessories` — R$ 888.724,61.

Esses rankings representam receita dos itens e não margem ou lucro, pois o dataset utilizado não fornece custo dos produtos.

## Estados

São Paulo concentrou **R$ 5.067.633,16** de receita dos itens e **40.501 pedidos entregues**, sendo o principal estado cliente nas duas métricas nesta etapa.

Rio de Janeiro e Minas Gerais aparecem na sequência em receita dos itens, com **R$ 1.759.651,13** e **R$ 1.552.481,83**, respectivamente.

## Concentração de vendedores

Os 10 maiores vendedores por receita dos itens representam aproximadamente **13,27%** da receita dos pedidos entregues analisados.

O maior vendedor individual representa aproximadamente **1,72%** da receita. A concentração não é, portanto, dominada por um único vendedor na métrica utilizada.

## Recorrência de clientes

Considerando `customer_unique_id`, **2.801 de 93.358 clientes** tiveram mais de um pedido entregue, correspondendo a aproximadamente **3,00%** dos clientes desta visão.

Este indicador será aprofundado posteriormente porque a base permite separar cliente recorrente, frequência e valor monetário sem depender de `customer_id` isolado.

## Limitações

- Receita não deve ser interpretada como lucro ou margem.
- O cálculo atual usa a data de compra para o eixo temporal e pedidos entregues para os KPIs realizados.
- A cobertura anual é parcial em 2016 e 2018.
- Relações com pagamentos, avaliações e geolocalização serão modeladas separadamente para evitar duplicação de métricas.
- Nenhum insight causal é inferido apenas a partir de diferenças descritivas.
