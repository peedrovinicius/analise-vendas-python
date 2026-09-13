# Engenharia do projeto

## Objetivo

A camada de engenharia existe para tornar o fluxo de dados reproduzível, testável e verificável.

## Ambiente

- Python 3.11–3.13;
- dependências diretas fixadas em `pyproject.toml` e `requirements.txt`;
- Pandas para manipulação analítica;
- Matplotlib/JupyterLab para exploração e apresentação;
- Pandera para validação de schema nas tabelas críticas;
- Pytest + pytest-cov para testes e cobertura;
- Ruff para lint e formatação;
- Mypy para verificação estática;
- pip-audit para auditoria de dependências;
- GitHub Actions para automação da qualidade.

As versões utilizadas foram fixadas com base nas releases atuais verificadas no PyPI em setembro de 2026. citeturn842111search0turn127243search1turn127243search4turn842111search2turn842111search7turn842111search1turn842111search3turn127243search0

## Gates de qualidade

Antes de considerar uma alteração pronta, o projeto deve passar por:

```bash
ruff format --check src tests scripts
ruff check src tests scripts
mypy src
pytest -q --cov=src --cov-report=term-missing --cov-fail-under=80
pip-audit -r requirements.txt
```

## CI

O workflow `.github/workflows/ci.yml` executa os cinco gates automaticamente em pushes e pull requests.

## Dados

A entrada é validada antes da transformação. As tabelas `orders` e `order_items` possuem schema explícito para campos essenciais, unicidade de `order_id` e não negatividade dos valores monetários críticos.

## Arquitetura

A ingestão é centralizada em `src/ingestion/olist.py`. Transformações ficam em `src/transformation/`, métricas em `src/analytics/` e validações de dados em `src/validation/`.

O notebook atua como camada de exploração e comunicação; não deve duplicar regras de negócio já implementadas em `src/`.

## Testes

Os testes cobrem ingestão, validação de schema, transformação, KPIs, análises de negócio e orquestração do pipeline. A CI exige cobertura mínima de 80% sobre `src/`.

O percentual é um gate de regressão, não um objetivo isolado: cobertura adicional deve acompanhar comportamento relevante do sistema.

## Pré-commit

O arquivo `.pre-commit-config.yaml` aplica Ruff e formatação localmente antes dos commits.

## Limitação de reprodutibilidade

O projeto fixa as dependências diretas, mas o ambiente ainda não versiona um lockfile completo de dependências transitivas. Essa etapa poderá ser adicionada quando o fluxo de resolução com `uv` puder ser executado no ambiente de desenvolvimento.

## Princípios

1. Regras de negócio devem ficar em funções reutilizáveis e testáveis.
2. O notebook deve orquestrar e comunicar a análise, não concentrar a lógica do projeto.
3. Métricas devem preservar a granularidade definida no modelo.
4. Falhas de estrutura e de qualidade devem ser explícitas.
5. Nenhum resultado deve ser publicado sem rastreabilidade para os dados e regras que o produziram.
6. Ferramentas entram por necessidade técnica, não por quantidade.
