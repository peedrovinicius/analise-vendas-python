# Engenharia do projeto

## Objetivo

A camada de engenharia existe para tornar o fluxo de análise reproduzível, testável e verificável.

## Ferramentas

- Python 3.11+;
- Pandas para manipulação analítica;
- Matplotlib para visualizações;
- Pytest para testes automatizados;
- Ruff para lint e verificação de qualidade;
- GitHub Actions para execução automática das verificações.

## Execução das verificações

Instale as dependências de desenvolvimento:

```bash
pip install -e ".[dev]"
```

Execute o lint:

```bash
ruff check src tests scripts
```

Execute os testes:

```bash
pytest -q
```

## CI

O workflow `.github/workflows/ci.yml` executa lint e testes automaticamente em pushes e pull requests.

## Princípios

1. Regras de negócio devem ficar em funções reutilizáveis e testáveis.
2. O notebook deve orquestrar e comunicar a análise, não concentrar toda a lógica do projeto.
3. Métricas devem preservar a granularidade definida no modelo.
4. Falhas de estrutura devem ser explícitas; não devemos mascarar problemas de dados com tratamento silencioso.
5. Novas dependências e ferramentas entram somente quando houver necessidade técnica comprovável.
