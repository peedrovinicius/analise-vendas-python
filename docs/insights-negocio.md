# Insights de negócio

## Escopo

Os indicadores desta etapa consideram itens associados a pedidos com status `delivered`. A receita utilizada é a soma de `price` dos itens; o frete é analisado separadamente.

A execução foi recalculada sobre os nove arquivos públicos da Olist usados pelo pipeline atual. Os KPIs consolidados coincidem com os valores registrados em `docs/insights-iniciais.md`, validando a consistência da execução antes do aprofundamento analítico.

## 1. Segmentação de clientes

Considerando `customer_unique_id`, foram identificados **93.358 clientes** com itens em pedidos entregues. Desses, **90.557 (97,00%)** fizeram apenas um pedido e **2.801 (3,00%)** fizeram mais de um pedido.

Os clientes recorrentes responderam por **R$ 728.408,75**, equivalente a **5,51% da receita**. Apesar de representarem apenas 3,00% da base de clientes, apresentaram receita média de **R$ 260,05 por cliente**, contra **R$ 137,96** entre os clientes de compra única.

A média de pedidos por cliente recorrente foi de **2,11 pedidos**, enquanto o segmento de compra única tem, por definição, **1,00 pedido por cliente**.

### Interpretação

A visão analisada é predominantemente composta por clientes de compra única. Os clientes recorrentes são uma parcela pequena da base, mas apresentam maior valor médio por cliente e respondem por uma participação de receita superior à sua participação no número de clientes.

### Limitação

A taxa de 3,00% descreve a recorrência dentro do histórico disponível no dataset. Ela não deve ser interpretada automaticamente como retenção ou churn, pois não há informação sobre clientes antes ou depois da janela observada.

## 2. Concentração geográfica

São Paulo representa **38,33% da receita**, Rio de Janeiro **13,31%** e Minas Gerais **11,74%**. Juntos, os três estados concentram **63,38% da receita**.

São Paulo também lidera em pedidos entregues, com **40.501 pedidos**, e em clientes, com **39.156 clientes**.

### Interpretação

A receita observada está fortemente concentrada no Sudeste, especialmente em São Paulo. A concentração deve ser analisada em conjunto com volume de pedidos, clientes e ticket médio, e não como evidência isolada de causalidade.

## 3. Categorias de maior receita

As cinco maiores categorias por receita são:

1. `health_beauty` — **R$ 1.233.131,72** (**9,33%** da receita).
2. `watches_gifts` — **R$ 1.166.176,98** (**8,82%**).
3. `bed_bath_table` — **R$ 1.023.434,76** (**7,74%**).
4. `sports_leisure` — **R$ 954.852,55** (**7,22%**).
5. `computers_accessories` — **R$ 888.724,61** (**6,72%**).

Juntas, essas cinco categorias representam **39,83% da receita**.

A liderança em receita não significa liderança em margem ou lucro, pois o dataset utilizado não fornece custo dos produtos.

### Interpretação

A receita está distribuída entre várias categorias. `health_beauty` é a maior categoria em receita, mas responde por menos de 10% da receita total, enquanto as cinco primeiras concentram pouco menos de 40%.

## 4. Evolução temporal

A série calculada possui **23 meses**, de setembro de 2016 a agosto de 2018. A receita dos itens foi de **R$ 40.470,98 em 2016**, **R$ 5.962.902,01 em 2017** e **R$ 7.218.125,12 em 2018**, valores que coincidem com o registro inicial.

O maior mês em receita foi **novembro de 2017**, com **R$ 987.765,37** em itens. Nesse mês foram registrados **7.289 pedidos entregues** e **8.475 itens**.

### Interpretação

Existe crescimento relevante na série mensal, mas a comparação entre anos exige cautela porque 2016 e 2018 possuem cobertura parcial. O maior valor mensal observado não deve, sozinho, ser interpretado como evidência de sazonalidade.

## 5. Vendedores

Os 10 maiores vendedores por receita concentram **13,27% da receita** dos pedidos entregues. O maior vendedor individual representa **1,72%** da receita.

### Interpretação

A concentração entre vendedores é menor que a concentração geográfica observada nos três principais estados. A receita não depende de um único vendedor ou de um grupo muito pequeno de vendedores.

## 6. Validação contra os insights iniciais

A nova execução reproduziu os principais números já documentados em `docs/insights-iniciais.md`:

- **96.478** pedidos entregues;
- **110.197** itens;
- **R$ 13.221.498,11** de receita dos itens;
- **R$ 2.198.275,64** de frete;
- **R$ 15.419.773,75** em itens + frete;
- **93.358** clientes únicos;
- **R$ 137,04** de ticket médio de pedido.

Também foram confirmados os valores anuais de receita, os cinco primeiros rankings de categorias, os principais estados, a concentração dos 10 maiores vendedores e a quantidade de clientes recorrentes registrada anteriormente. fileciteturn33file0

## Limitações

- Receita não deve ser interpretada como lucro ou margem.
- Os KPIs realizados consideram pedidos com `order_status = delivered`.
- A série temporal usa a data de compra.
- A cobertura anual é parcial em 2016 e 2018.
- A recorrência é calculada sobre o histórico disponível na base e não representa, isoladamente, retenção ou churn.
- Relações com pagamentos, avaliações e geolocalização devem ser analisadas separadamente para evitar duplicação de métricas.
- Nenhum insight causal é inferido apenas a partir das diferenças descritivas observadas.
