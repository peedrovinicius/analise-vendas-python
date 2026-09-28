## Resumo

Descreva o problema e a alteração realizada.

## Validação

- [ ] `ruff format --check src tests scripts`
- [ ] `ruff check src tests scripts`
- [ ] `mypy src`
- [ ] `pytest -q --cov=src --cov-branch --cov-report=term-missing --cov-fail-under=80`

## Impacto

Informe se a mudança altera KPI, granularidade, filtro de pedidos, fonte ou regra de validação.

## Checklist

- [ ] a granularidade dos dados foi preservada;
- [ ] receita de produto e frete continuam separados;
- [ ] KPIs de receita realizada continuam restritos a pedidos `delivered`;
- [ ] CSVs brutos da Olist não foram versionados;
- [ ] mudanças metodológicas foram documentadas.
