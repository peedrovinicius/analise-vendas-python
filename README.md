# Sistema de Gestão e Análise de Vendas

> Projeto em reconstrução e evolução a partir de uma análise inicial em Python.

## Sobre o projeto

O projeto está sendo reconstruído com base no **Brazilian E-Commerce Public Dataset by Olist**, uma base pública de dados comerciais anonimizados de comércio eletrônico brasileiro.

A proposta é evoluir de uma análise exploratória inicial para um projeto completo de dados e aplicação, passando por ingestão, validação, tratamento, análise, visualização e, posteriormente, integração com backend e frontend.

## Fonte dos dados

**Brazilian E-Commerce Public Dataset by Olist**

Fonte: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Detalhes da fonte, arquivos, características e licença estão documentados em [docs/fonte-dados.md](./docs/fonte-dados.md).

## Status atual

A versão anterior do projeto utilizava uma pequena base criada diretamente no notebook para fins de estudo. Essa abordagem será substituída por dados públicos reais e anonimizados.

A análise e os resultados da versão anterior não são considerados resultados do projeto atual.

## Direção técnica

A evolução planejada do projeto contempla:

- ingestão de dados públicos;
- validação e qualidade dos dados;
- transformação e preparação;
- definição de métricas e regras de negócio;
- análise exploratória e analítica;
- visualizações orientadas a negócio;
- testes automatizados;
- organização do código em módulos reutilizáveis;
- documentação técnica;
- posteriormente, backend, frontend e publicação da aplicação.

As tecnologias serão adicionadas conforme a necessidade real de cada etapa.

## Estrutura inicial

```text
.
├── dados/
├── docs/
│   └── fonte-dados.md
├── analise_vendas.ipynb
├── README.md
└── requirements.txt
```

A estrutura será ampliada conforme a reconstrução do projeto avançar.

## Projeto anterior

O notebook [analise_vendas.ipynb](./analise_vendas.ipynb) permanece no repositório como registro da versão inicial do projeto. Ele será revisado e posteriormente substituído ou reorganizado conforme a nova arquitetura seja implementada.
