# Visualizações analíticas

As visualizações desta etapa foram geradas a partir da fato analítica de itens associados a pedidos com status `delivered`.

## 1. Evolução mensal

![Evolução mensal](../assets/evolucao-mensal.svg)

Mostra a receita de itens por mês de compra. Meses sem registros não são preenchidos artificialmente.

## 2. Concentração por estado

![Receita por UF](../assets/receita-por-uf.svg)

Apresenta os 10 estados com maior receita, considerando o estado do cliente.

## 3. Concentração por categoria

![Receita por categoria](../assets/receita-por-categoria.svg)

Apresenta as 10 categorias com maior receita dos itens entregues.

## Regras de leitura

- Receita considera `price` dos itens de pedidos entregues.
- Frete é tratado separadamente.
- O ranking por UF utiliza `customer_state`, não `seller_state`.
- As visualizações não devem ser interpretadas como causalidade: mostram associação e concentração observadas na base.
