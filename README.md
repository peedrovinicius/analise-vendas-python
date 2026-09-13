# Sistema de Gestão e Análise de Vendas

Projeto de engenharia e análise de dados construído a partir do **Brazilian E-Commerce Public Dataset by Olist**, uma base pública e anonimizada de comércio eletrônico brasileiro.

## Sobre o projeto

O projeto foi reconstruído para demonstrar um fluxo completo de dados em Python, incluindo ingestão, validação de schema, transformação, cálculo de indicadores, testes automatizados, análise de qualidade e documentação dos resultados.

A versão atual utiliza exclusivamente os dados públicos da Olist. A base fictícia utilizada na versão inicial foi descontinuada.

## Objetivos analíticos

A análise responde a questões sobre:

- receita e volume de pedidos entregues;
- evolução mensal da receita;
- concentração geográfica das vendas;
- categorias com maior participação na receita;
- recorrência de clientes;
- concentração de receita entre vendedores.

## Fonte dos dados

**Brazilian E-Commerce Public Dataset by Olist**  
Fonte: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Detalhes da fonte, arquivos, características e licença estão documentados em [docs/fonte-dados.md](./docs/fonte-dados.md).

## Modelo e qualidade dos dados

A análise utiliza `order_items` como referência transacional no nível de item de pedido. Os relacionamentos com pedidos, clientes, produtos, categorias e vendedores são controlados para preservar a granularidade.

Pagamentos e avaliações não são unidos diretamente à tabela de itens sem tratamento específico de cardinalidade.

A auditoria e as regras de qualidade estão documentadas em [docs/qualidade-dados.md](./docs/qualidade-dados.md).

## Principais decisões de negócio

Para os KPIs de receita realizada, são considerados itens pertencentes a pedidos com status `delivered`.

`price` representa a receita dos itens. `freight_value` é apresentado separadamente e não é tratado automaticamente como receita de produto.

Pedidos com outros status permanecem disponíveis para análises operacionais, mas não entram no KPI de receita realizada definido nesta versão.

## Resultados validados

A execução atual foi recalculada sobre os nove arquivos públicos da Olist e reproduziu os indicadores registrados na análise inicial:

- **96.478** pedidos entregues;
- **110.197** itens;
- **R$ 13.221.498,11** de receita dos itens;
- **R$ 2.198.275,64** de frete;
- **93.358** clientes únicos;
- **R$ 137,04** de ticket médio por pedido.

Os indicadores adicionais de segmentação, concentração geográfica, categorias, vendedores e evolução mensal estão documentados em [docs/insights-negocio.md](./docs/insights-negocio.md).

## Estrutura

```text
.
├── dados/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── auditoria-inicial.md
│   ├── execucao-local.md
│   ├── fonte-dados.md
│   ├── insights-iniciais.md
│   ├── insights-negocio.md
│   ├── modelo-dados.md
│   ├── qualidade-dados.md
│   └── visualizacoes.md
├── notebooks/
│   └── analise_olist.ipynb
├── assets/
│   ├── evolucao-mensal.svg
│   ├── receita-por-uf.svg
│   └── receita-por-categoria.svg
├── scripts/
│   ├── auditar_olist.py
│   └── run_pipeline.py
├── src/
│   ├── analytics/
│   ├── ingestion/
│   ├── transformation/
│   └── pipeline.py
├── tests/
│   ├── test_olist_transformation.py
│   └── test_sales_analysis.py
├── analise_vendas.ipynb
├── requirements.txt
└── README.md
```

## Pipeline e qualidade de software

A execução oficial é centralizada em `src/pipeline.py`, responsável por coordenar ingestão, validação, transformação e cálculo dos KPIs.

O projeto possui CI automatizado com:

- Ruff para formatação e lint;
- mypy para verificação de tipos;
- pytest com cobertura mínima configurada;
- pip-audit para auditoria de dependências;
- pre-commit para validações adicionais.

## Notebook

A análise atual está em [notebooks/analise_olist.ipynb](./notebooks/analise_olist.ipynb). O notebook antigo permanece temporariamente em `analise_vendas.ipynb` como registro da versão inicial.

## Status

**Análise e pipeline validados.**

A próxima evolução do projeto pode concentrar-se na camada de visualização e, posteriormente, na construção de uma aplicação web integrada ao pipeline de dados.

## Limitações

- Receita não representa lucro ou margem.
- Os KPIs de receita realizada consideram pedidos com `order_status = delivered`.
- A série temporal utiliza a data de compra.
- A cobertura de 2016 e 2018 é parcial.
- A recorrência é calculada apenas sobre o histórico disponível no dataset e não representa, isoladamente, retenção ou churn.
- Não são feitas inferências causais a partir das diferenças descritivas observadas.
