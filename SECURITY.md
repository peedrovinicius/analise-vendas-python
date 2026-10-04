# Política de segurança

## Escopo

Este repositório contém um projeto de engenharia e análise de dados baseado no conjunto público e anonimizado da Olist.

Relatos de segurança são relevantes quando envolvem, por exemplo:

- dependências vulneráveis;
- execução insegura de scripts;
- exposição acidental de segredos;
- arquivos de ambiente ou credenciais versionados;
- manipulação inesperada de caminhos ou entradas;
- riscos no pipeline de CI;
- publicação acidental de dados que não deveriam estar no repositório.

## Como relatar

Não publique credenciais, tokens ou detalhes sensíveis em uma issue pública.

Prefira um canal privado disponível no GitHub para o repositório. Se não houver um canal privado habilitado, entre em contato com o mantenedor pelo perfil do GitHub e compartilhe apenas o necessário para estabelecer uma comunicação segura.

Ao relatar, inclua quando possível:

- descrição objetiva do problema;
- passos mínimos para reprodução;
- commit ou versão afetada;
- impacto esperado;
- evidências sem segredos ou dados pessoais;
- sugestão de correção, se houver.

## Dados e privacidade

O projeto deve utilizar somente os dados públicos previstos em sua documentação.

Não adicione ao repositório:

- dados pessoais reais;
- credenciais de serviços;
- tokens de API;
- chaves privadas;
- arquivos locais com segredos;
- datasets obtidos de fontes sem permissão de redistribuição.

Arquivos locais de dados devem respeitar as regras definidas no `.gitignore` e na documentação de origem dos dados.

## Dependências e CI

Mudanças em dependências devem preservar o uso do lockfile com hashes e passar pelas verificações automatizadas disponíveis, incluindo auditoria de dependências.

Alterações no pipeline devem manter o princípio do menor privilégio para permissões do GitHub Actions.

## Correções

Falhas confirmadas devem ser corrigidas antes de qualquer divulgação pública detalhada quando houver risco de exploração ou exposição de dados.
