# Análise de vendas e faturamento com Python

[![CI](https://github.com/peedrovinicius/analise-vendas-python/actions/workflows/ci.yml/badge.svg)](https://github.com/peedrovinicius/analise-vendas-python/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-3.x-150458?logo=pandas&logoColor=white)

Projeto de engenharia e análise de dados construído a partir do **Brazilian E-Commerce Public Dataset by Olist**, uma base pública e anonimizada de comércio eletrônico brasileiro.

## O case

O objetivo é transformar dados transacionais de e-commerce em indicadores confiáveis para entender **receita, comportamento de clientes e concentração das vendas**.

A análise foi estruturada como um fluxo reprodutível de dados em Python, com ingestão, validação de schema, transformação, cálculo de indicadores, testes automatizados, controle de qualidade e documentação dos resultados.

### Perguntas de negócio

- Qual foi a receita dos pedidos entregues?
- Como a receita evoluiu ao longo do tempo?
- Quais estados concentram maior parcela da receita?
- Quais categorias apresentam maior participação?
- Qual é o nível de recorrência dos clientes?
- Quanto da receita está concentrada nos principais vendedores?

## Principais resultados

A execução atual foi recalculada sobre os nove arquivos públicos da Olist e reproduziu os indicadores registrados na análise inicial:

| Indicador | Resultado |
|---|---:|
| Pedidos entregues | **96.478** |
| Itens vendidos em pedidos entregues | **110.197** |
| Receita dos itens | **R$ 13.221.498,11** |
| Frete | **R$ 2.198.275,64** |
| Clientes únicos | **93.358** |
| Ticket médio por pedido | **R$ 137,04** |

Os indicadores adicionais de segmentação de clientes, concentração geográfica, categorias, vendedores e evolução mensal estão documentados em [docs/insights-negocio.md](./docs/insights-negocio.md).

## Principais insights

A análise complementar mostra que:

- **3,00%** dos clientes são recorrentes, responsáveis por **5,51% da receita** observada;
- **SP, RJ e MG** concentram **63,38% da receita**;
- as cinco principais categorias representam **39,83% da receita**;
- a concentração entre vendedores e a evolução mensal são analisadas separadamente para evitar misturar granularidades e interpretações.

Os números acima são descritivos e não implicam causalidade. As definições e limitações estão documentadas em [docs/insights-negocio.md](./docs/insights-negocio.md) e [docs/metodologia.md](./docs/metodologia.md).

## Visualizações

### Evolução mensal

![Evolução mensal](./assets/evolucao-mensal.svg)

### Receita por estado

![Receita por UF](./assets/receita-por-uf.svg)

### Receita por categoria

![Receita por categoria](./assets/receita-por-categoria.svg)

As regras de leitura dessas visualizações estão documentadas em [docs/visualizacoes.md](./docs/visualizacoes.md).

## Engenharia do projeto

O fluxo foi separado por responsabilidade:

```text
Dados públicos
    ↓
Ingestão
    ↓
Validação de schema
    ↓
Transformação
    ↓
Indicadores e análises
    ↓
Testes + qualidade
    ↓
Resultados documentados
```

A execução oficial é centralizada em `src/pipeline.py`, que coordena ingestão, validação, transformação e cálculo dos KPIs.

A análise exploratória fica no notebook, enquanto as regras reutilizáveis permanecem na camada `src/`.

### Qualidade de software

O projeto possui CI automatizado com:

- Ruff — formatação e lint;
- mypy — verificação estática de tipos;
- pytest + coverage — testes automatizados;
- pip-audit — auditoria de dependências;
- pre-commit — validações antes do commit.

## Modelo e qualidade dos dados

A análise utiliza `order_items` como referência transacional no nível de item de pedido. Os relacionamentos com pedidos, clientes, produtos, categorias e vendedores são controlados para preservar a granularidade.

Para os KPIs de receita realizada, são considerados itens pertencentes a pedidos com status `delivered`.

`price` representa a receita dos itens. `freight_value` é apresentado separadamente e não é tratado automaticamente como receita de produto.

Pagamentos e avaliações não são unidos diretamente à tabela de itens sem tratamento específico de cardinalidade.

A auditoria e as regras de qualidade estão documentadas em [docs/qualidade-dados.md](./docs/qualidade-dados.md).

## Fonte dos dados

**Brazilian E-Commerce Public Dataset by Olist**  
Fonte: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Detalhes da fonte, arquivos, características e licença estão documentados em [docs/fonte-dados.md](./docs/fonte-dados.md).

## Estrutura

```text
.
├── dados/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── auditoria-inicial.md
│   ├── engenharia.md
│   ├── execucao-local.md
│   ├── fonte-dados.md
│   ├── insights-iniciais.md
│   ├── insights-negocio.md
│   ├── metodologia.md
│   ├── modelo-dados.md
│   ├── qualidade-dados.md
│   ├── storytelling.md
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
│   ├── validation/
│   └── pipeline.py
├── tests/
│   ├── test_olist_transformation.py
│   └── test_sales_analysis.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Execução local

Para reproduzir a análise:

```bash
git clone https://github.com/peedrovinicius/analise-vendas-python.git
cd analise-vendas-python
python -m venv .venv
```

Ative o ambiente virtual conforme o seu sistema e instale as dependências:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

Coloque os nove arquivos CSV da Olist em `dados/raw/` e execute:

```bash
python scripts/run_pipeline.py
```

A análise exploratória está em [notebooks/analise_olist.ipynb](./notebooks/analise_olist.ipynb). O fluxo completo e os detalhes de reprodução estão descritos em [docs/execucao-local.md](./docs/execucao-local.md).

## Documentação

- [Metodologia](./docs/metodologia.md)
- [Engenharia do projeto](./docs/engenharia.md)
- [Execução local](./docs/execucao-local.md)
- [Fonte dos dados](./docs/fonte-dados.md)
- [Modelo de dados](./docs/modelo-dados.md)
- [Qualidade dos dados](./docs/qualidade-dados.md)
- [Insights de negócio](./docs/insights-negocio.md)
- [Auditoria inicial](./docs/auditoria-inicial.md)
- [Visualizações](./docs/visualizacoes.md)
- [Storytelling](./docs/storytelling.md)

## Limitações

- Receita não representa lucro ou margem.
- Os KPIs de receita realizada consideram pedidos com `order_status = delivered`.
- A série temporal utiliza a data de compra.
- A cobertura de 2016 e 2018 é parcial.
- A recorrência é calculada apenas sobre o histórico disponível no dataset e não representa, isoladamente, retenção ou churn.
- Não são feitas inferências causais a partir das diferenças descritivas observadas.

## Status

**Análise e pipeline validados.**

A camada atual está focada em engenharia e análise de dados. A evolução para backend e aplicação web será desenvolvida separadamente no projeto de gerenciamento de pacientes odontológicos.