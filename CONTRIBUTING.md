# Contribuindo

Contribuições são bem-vindas quando preservam a reprodutibilidade da análise, a granularidade dos dados e a interpretação correta dos indicadores.

## Antes de começar

1. Procure uma issue aberta relacionada ao tema.
2. Se a mudança não estiver registrada, abra uma issue com problema, motivação e escopo.
3. Informe se a proposta altera definição de KPI, granularidade, filtro de pedidos, fonte ou regra de validação.

## Fluxo recomendado

1. Crie uma branch curta e específica a partir de `main`.
2. Faça uma alteração por tema.
3. Inclua ou atualize testes quando houver mudança de comportamento.
4. Execute as validações locais.
5. Abra um Pull Request com contexto suficiente para revisão.

Validação principal:

```bash
ruff format --check src tests scripts
ruff check src tests scripts
mypy src
pytest -q --cov=src --cov-branch --cov-report=term-missing --cov-fail-under=80
```

## Regras de qualidade

- não alterar resultados publicados sem evidência e reprodução;
- preservar a granularidade item de pedido nas análises que dependem dela;
- não misturar frete com receita de produto;
- manter os KPIs de receita realizada restritos a pedidos `delivered`;
- não versionar os CSVs brutos da Olist;
- documentar mudanças em metodologia, fonte, KPIs ou visualizações;
- manter commits e Pull Requests com escopo claro.

## Pull Requests

Inclua no PR:

- problema resolvido;
- arquivos ou componentes afetados;
- testes e validações executados;
- impacto em KPIs ou resultados publicados, quando houver;
- evidência visual apenas quando a mudança afetar gráficos.

Mudanças pequenas e bem delimitadas são preferíveis a PRs muito amplos.
