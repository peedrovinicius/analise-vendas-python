# Metodologia

O projeto utiliza dados públicos do **Brazilian E-Commerce Public Dataset by Olist** para construir uma análise reproduzível de vendas e faturamento.

## Fluxo analítico

1. Identificação e documentação da fonte pública.
2. Ingestão dos nove arquivos CSV.
3. Auditoria de qualidade e estrutura.
4. Validação das tabelas críticas.
5. Transformação para a granularidade analítica de item de pedido.
6. Aplicação das regras de negócio para definir vendas realizadas.
7. Construção dos indicadores de vendas, clientes, categorias, estados e vendedores.
8. Análise exploratória e visualização dos resultados.
9. Testes automatizados, verificação de tipos e auditoria de dependências.
10. Documentação dos resultados e limitações.

## Granularidade e regras de negócio

`order_items` é a referência transacional para os indicadores de receita dos itens.

Para os KPIs de receita realizada, são considerados itens associados a pedidos com `order_status = delivered`.

`price` é tratado como receita dos itens. `freight_value` permanece separado e não é incorporado automaticamente à receita de produto.

Relacionamentos com tabelas que podem possuir múltiplos registros por pedido, como pagamentos e avaliações, exigem tratamento específico de cardinalidade antes de qualquer agregação conjunta.

## Princípios

- utilizar dados públicos e resultados reproduzíveis;
- não inventar dados ou resultados;
- manter rastreabilidade entre dados, transformação e métricas;
- preservar a granularidade definida para cada indicador;
- documentar limitações e decisões de tratamento;
- adicionar complexidade somente quando houver justificativa técnica.

## Estado atual

A ingestão, validação, transformação, cálculo dos KPIs, análises de negócio e testes automatizados estão implementados.

Os resultados publicados em `docs/insights-negocio.md` foram recalculados e conferidos contra `docs/insights-iniciais.md`.

A camada de visualização já possui artefatos documentados em `docs/visualizacoes.md`. Evoluções futuras podem adicionar uma aplicação web sem alterar as regras analíticas consolidadas na camada `src/`.
