# Qualidade dos dados

Esta documentação registra as verificações de qualidade que serão executadas sobre a base pública antes da produção de métricas e insights.

## Princípio

Nenhuma métrica de negócio será considerada válida antes da verificação da integridade dos dados necessários para calculá-la.

## Verificações

### Estrutura

- presença dos 9 arquivos esperados;
- nomes e quantidade de colunas;
- quantidade de registros;
- tipos de dados;
- compatibilidade entre chaves relacionadas.

### Completude

- valores nulos por coluna;
- campos essenciais ausentes;
- proporção de registros incompletos.

### Unicidade

- duplicidade de identificadores;
- duplicidade de combinações que deveriam ser únicas;
- efeitos de duplicação após relacionamentos.

### Validade

- datas válidas e coerentes;
- valores monetários válidos;
- quantidades compatíveis com o significado das colunas;
- categorias e códigos consistentes.

### Relacionamentos

- pedidos sem cliente correspondente;
- itens sem pedido correspondente;
- itens sem produto correspondente;
- itens sem vendedor correspondente;
- demais chaves estrangeiras relevantes.

### Granularidade e métricas

A tabela usada para cada métrica deverá ter granularidade compatível com a fórmula. Relacionamentos 1:N entre pedidos, itens, pagamentos e avaliações serão tratados com cuidado para evitar duplicação de receita, frete, pagamentos ou quantidade.

## Registro dos resultados

Cada problema encontrado será documentado com:

1. regra de validação;
2. resultado quantitativo;
3. impacto identificado;
4. decisão de tratamento;
5. justificativa.

Nenhum registro será removido ou alterado sem documentação da decisão.

## Status

A auditoria quantitativa ainda não foi executada porque a base pública ainda não foi ingerida no ambiente de processamento. Os números serão registrados somente após a leitura efetiva dos arquivos.