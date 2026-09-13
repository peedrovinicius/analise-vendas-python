# Storytelling analítico

## Contexto

O projeto analisa dados públicos e anonimizados de comércio eletrônico brasileiro da Olist. A visão principal utiliza itens associados a pedidos com status `delivered` para representar vendas realizadas.

## Perguntas de negócio

1. Como a receita evolui ao longo do período observado?
2. Onde a receita está concentrada no Brasil?
3. Quais categorias concentram maior parcela da receita?
4. Qual é o nível de recorrência dos clientes?
5. Existe concentração relevante entre vendedores?

## Achados atuais

### Receita e operação

A visão de pedidos entregues reúne **96.478 pedidos** e **110.197 itens**, com **R$ 13.221.498,11** em valor de produtos e **R$ 2.198.275,64** em frete.

### Concentração geográfica

São Paulo, Rio de Janeiro e Minas Gerais concentram **63,38% da receita** dos itens de pedidos entregues. Esse resultado descreve concentração observada na base e não permite, isoladamente, concluir que a localização seja causa do desempenho.

### Categorias

As cinco maiores categorias respondem por **39,83% da receita**. O ranking deve ser interpretado junto com volume de itens e número de pedidos, evitando confundir preço médio com demanda.

### Recorrência

**3,00%** dos clientes únicos da visão de pedidos entregues tiveram mais de um pedido. A métrica é calculada usando `customer_unique_id`, preservando a identidade do cliente entre pedidos.

### Vendedores

Os dez maiores vendedores respondem por **13,27% da receita** dos itens de pedidos entregues. O resultado sugere que a receita não está concentrada em um único vendedor, mas deve ser analisado junto com cobertura e volume de vendedores.

## Limitações de interpretação

- O dataset representa uma operação específica da Olist e não deve ser tratado como retrato de todo o comércio eletrônico brasileiro.
- Receita é definida neste projeto como soma de `price` em itens de pedidos entregues.
- Frete é analisado separadamente.
- O período inicial e final possuem cobertura temporal assimétrica. Dezembro de 2016, por exemplo, possui pouca observação na visão de pedidos entregues e não deve ser usado isoladamente para inferir sazonalidade.
- Ausência de custo do produto impede inferir lucro ou margem sem fonte adicional.
