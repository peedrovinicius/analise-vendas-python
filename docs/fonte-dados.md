# Fonte dos dados

## Dataset

**Brazilian E-Commerce Public Dataset by Olist**

Fonte pública disponibilizada pela Olist no Kaggle:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

## Descrição

O dataset contém dados de pedidos de comércio eletrônico realizados entre **2016 e 2018**, com aproximadamente **100 mil pedidos**. Os dados são comerciais e foram **anonimizados** antes da publicação.

A versão publicada é organizada em múltiplos arquivos relacionais, incluindo dados de clientes, pedidos, itens dos pedidos, pagamentos, avaliações, produtos, vendedores, geolocalização e tradução das categorias de produtos.

## Arquivos de origem

- `olist_customers_dataset.csv`
- `olist_geolocation_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_order_reviews_dataset.csv`
- `olist_orders_dataset.csv`
- `olist_products_dataset.csv`
- `olist_sellers_dataset.csv`
- `product_category_name_translation.csv`

## Característica importante dos dados

O dataset representa uma estrutura relacional. Um pedido pode possuir vários itens, e os itens podem estar associados a diferentes vendedores. Por isso, a definição da granularidade de cada tabela e o tratamento dos relacionamentos serão etapas obrigatórias da análise.

A identificação de recompra deve considerar `customer_unique_id`, pois `customer_id` é associado individualmente aos pedidos na estrutura disponibilizada pela Olist.

## Licença

O dataset é disponibilizado sob a licença **CC BY-NC-SA 4.0**.

Este projeto não redistribui os arquivos brutos do dataset. A fonte original deve ser acessada diretamente no endereço indicado acima, respeitando os termos da licença.

## Uso no projeto

A base será utilizada para construir um fluxo de análise de dados com foco em:

- ingestão de dados públicos;
- validação e qualidade dos dados;
- transformação e preparação;
- análise de vendas;
- indicadores de negócio;
- visualização;
- posteriormente, uma aplicação web integrada ao processamento analítico.

## Referência

Olist. *Brazilian E-Commerce Public Dataset by Olist*. Kaggle. https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
