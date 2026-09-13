# Insights de negócio

## Escopo

Os indicadores desta etapa consideram itens associados a pedidos com status `delivered`. A métrica de receita utilizada é a soma de `price` dos itens; o frete é analisado separadamente.

## 1. Concentração geográfica

São Paulo representa **38,33% da receita** da visão de pedidos entregues. Rio de Janeiro representa **13,31%** e Minas Gerais **11,74%**. Juntos, os três estados concentram **63,38% da receita**.

### Interpretação

A demanda observada está fortemente concentrada no Sudeste, especialmente em São Paulo.

### Implicação analítica

Análises de expansão, atendimento e cobertura regional devem considerar essa concentração como ponto de partida. O resultado, porém, não permite concluir isoladamente que concentração de receita seja causada por maior demanda, maior ticket, maior presença de clientes ou composição de categorias.

## 2. Categorias de maior receita

As cinco maiores categorias por receita são `health_beauty`, `watches_gifts`, `bed_bath_table`, `sports_leisure` e `computers_accessories`. Juntas, representam aproximadamente **39,83% da receita**.

A categoria líder é `health_beauty`, com **R$ 1,23 milhão**, equivalente a aproximadamente **9,33% da receita** da visão analisada.

### Interpretação

A receita é distribuída entre diversas categorias, sem uma única categoria dominante. Ainda assim, existe concentração moderada nas cinco maiores categorias.

### Implicação analítica

O próximo aprofundamento deve comparar participação de receita com quantidade de itens e pedidos, evitando confundir volume de vendas com geração de receita.

## 3. Recorrência de clientes

Na visão de pedidos entregues, **3,00% dos clientes únicos possuem mais de um pedido**.

### Interpretação

A base observada é predominantemente composta por clientes que aparecem uma única vez na visão de pedidos entregues.

### Limitação

Essa taxa é calculada sobre o histórico disponível no dataset e não deve ser interpretada automaticamente como taxa de retenção ou churn. O período observado e a ausência de histórico fora da base limitam esse tipo de inferência.

## 4. Evolução temporal

A série mensal apresenta forte crescimento entre os primeiros meses e o restante da janela. Novembro de 2017 foi o mês com maior receita entre os meses calculados, com aproximadamente **R$ 987,8 mil**.

Dezembro de 2016 apresenta apenas um pedido entregue na visão filtrada e, portanto, não deve ser utilizado isoladamente para afirmar sazonalidade.

### Interpretação

Há evidência de evolução temporal relevante, mas o primeiro mês da série possui baixa cobertura de pedidos entregues e exige cautela em comparações.

## 5. Vendedores

Os 10 maiores vendedores concentram aproximadamente **13,27% da receita** da visão de pedidos entregues.

### Interpretação

A receita não está concentrada em um pequeno grupo de vendedores na mesma intensidade observada na concentração geográfica.

## Próximas análises

- comparar receita por categoria com volume de itens e pedidos;
- analisar ticket médio por estado e categoria;
- aprofundar o comportamento de clientes recorrentes;
- investigar a relação entre frete, valor dos itens e localização;
- avaliar concentração por vendedor com métricas complementares;
- construir visualizações orientadas aos principais achados.
