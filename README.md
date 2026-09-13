# Sistema de Gestão e Análise de Vendas

Projeto de dados e aplicação em evolução, construído a partir do **Brazilian E-Commerce Public Dataset by Olist**, uma base pública e anonimizada de comércio eletrônico brasileiro.

## Sobre o projeto

O projeto começou como uma análise exploratória simples em Python e está sendo reconstruído para demonstrar um fluxo mais completo de dados: ingestão, auditoria, transformação, análise, visualização, testes e, posteriormente, integração com backend, frontend e publicação.

A base fictícia utilizada na versão inicial foi descontinuada. Os resultados atuais são calculados a partir dos dados públicos da Olist.

## Objetivos analíticos

A análise atual busca responder:

- quanto foi vendido em pedidos entregues;
- como a receita evoluiu ao longo do tempo;
- onde a demanda está concentrada no Brasil;
- quais categorias de produtos concentram receita;
- qual é o nível de recorrência dos clientes.

## Fonte dos dados

**Brazilian E-Commerce Public Dataset by Olist**  
Fonte: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Detalhes da fonte, arquivos, características e licença estão documentados em [docs/fonte-dados.md](./docs/fonte-dados.md).

## Modelo e qualidade dos dados

A análise utiliza `order_items` como referência transacional no nível de item de pedido. Os relacionamentos com pedidos, clientes, produtos, categorias e vendedores são controlados para preservar a granularidade.

Pagamentos e avaliações não são unidos diretamente à tabela de itens sem tratamento específico de cardinalidade.

A auditoria de dados está documentada em [docs/qualidade-dados.md](./docs/qualidade-dados.md).

## Principais decisões de negócio

Para os KPIs de receita realizada, são considerados itens pertencentes a pedidos com status `delivered`.

`price` representa a receita dos itens. `freight_value` é apresentado separadamente e não é tratado automaticamente como receita de produto.

Pedidos com outros status permanecem disponíveis para análises operacionais, mas não entram no KPI de receita realizada definido nesta versão.

## Estrutura atual

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
│   ├── modelo-dados.md
│   └── qualidade-dados.md
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

## Notebook

O arquivo [analise_vendas.ipynb](./analise_vendas.ipynb) apresenta a análise exploratória atual com base nos dados da Olist, incluindo KPIs, evolução mensal, receita por estado, categorias de produtos e recorrência de clientes.

## Resultados atuais

Os primeiros resultados oficiais da nova versão estão documentados em [docs/insights-iniciais.md](./docs/insights-iniciais.md).

## Status

**Em desenvolvimento.**

As próximas etapas incluem aprofundamento da análise, melhoria das visualizações, expansão dos testes, organização do ambiente de execução e, posteriormente, construção da aplicação web.
