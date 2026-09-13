# Engenharia do projeto

## Objetivo

A camada de engenharia existe para tornar o fluxo de dados reproduzível, testável e verificável.

## Ambiente oficial

- Python 3.11;
- dependências diretas e de desenvolvimento fixadas em `pyproject.toml` e `requirements.txt`;
- Pandas para manipulação analítica;
- Matplotlib e JupyterLab para exploração e apresentação;
- Pandera para validação de schema nas tabelas críticas;
- Pytest + pytest-cov para testes e cobertura;
- Ruff para lint e formatação;
- Mypy para verificação estática;
- pip-audit para auditoria de vulnerabilidades conhecidas;
- pre-commit para qualidade local;
- GitHub Actions para automação dos gates.

As versões utilizadas estão fixadas no projeto e refletem o ambiente validado pela CI.

## Gates de qualidade

Antes de considerar uma alteração pronta, o projeto deve passar por:

```bash
ruff format --check src tests scripts
ruff check src tests scripts
mypy src
pytest -q --cov=src --cov-report=term-missing --cov-fail-under=80
pip-audit -r requirements.txt
pre-commit run --all-files
```

A ordem acima também representa a sequência usada pelo workflow de CI. Um gate com erro interrompe os seguintes, permitindo identificar o primeiro bloqueio da alteração.

## CI

O workflow `.github/workflows/ci.yml` executa os gates automaticamente em pushes e pull requests. O pipeline falha no primeiro gate com erro para impedir que problemas de estilo, tipos, testes ou dependências avancem silenciosamente.

## Dados

A entrada é validada antes da transformação. As tabelas críticas possuem schema explícito para campos essenciais, unicidade de chaves e não negatividade dos valores monetários aplicáveis.

## Arquitetura

A ingestão é centralizada em `src/ingestion/olist.py`. As transformações ficam em `src/transformation/`, métricas e análises em `src/analytics/` e validações de dados em `src/validation/`.

O notebook atua como camada de exploração e comunicação e não deve duplicar regras de negócio implementadas em `src/`.

## Testes

Os testes cobrem ingestão, schema, transformação, KPIs e análises de negócio. A CI exige cobertura mínima de 80% sobre `src/` e cobertura de branches.

O percentual é um gate de regressão; o objetivo principal é proteger comportamentos e regras de negócio relevantes.

## Pré-commit

O `.pre-commit-config.yaml` executa Ruff e formatação localmente antes dos commits. A CI também executa `pre-commit run --all-files` para manter a mesma regra de qualidade local e remota.

## Reprodutibilidade

As dependências diretas estão fixadas. O projeto ainda não publica um lockfile transitivo gerado por um resolvedor como `uv` ou Poetry; essa limitação fica declarada em vez de ser ocultada.

## Princípios

1. Regras de negócio ficam em funções reutilizáveis e testáveis.
2. Métricas preservam a granularidade definida no modelo.
3. Falhas de estrutura e qualidade são explícitas.
4. Nenhum resultado é publicado sem rastreabilidade para dados e regras.
5. Ferramentas entram por necessidade técnica, não por quantidade.
