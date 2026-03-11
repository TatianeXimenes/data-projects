# Dashboard de Segmentação e Valor do Cliente
## Contexto de Negócio

Instituições financeiras lidam com grandes carteiras de clientes que apresentam diferentes níveis de engajamento, comportamento financeiro e rentabilidade. Compreender esses padrões é essencial para desenvolver estratégias mais eficazes de retenção, relacionamento e priorização de clientes.

Este projeto tem como objetivo construir um dashboard analítico de segmentação de clientes, permitindo analisar padrões de comportamento financeiro, níveis de engajamento e características do perfil do cliente para apoiar decisões orientadas por dados.

O dashboard utiliza informações relacionadas a atividade transacional, uso de crédito e métricas de engajamento para analisar diferentes grupos de clientes.

### Perguntas de Negócio

O dashboard foi desenvolvido para responder às seguintes perguntas:

1. Como os clientes estão distribuídos entre os diferentes segmentos de valor?
2. Quais padrões comportamentais caracterizam os clientes de maior valor?
3. Como o volume e a frequência de transações variam entre os segmentos?
4. Quais segmentos apresentam maior nível de inatividade?
5. Quais características financeiras e de perfil estão associadas aos clientes de maior valor?

### Público-Alvo

Este dashboard foi desenvolvido para apoiar a tomada de decisão de áreas como:

- Marketing
- Gestão de Relacionamento com Clientes (CRM)
- Estratégia de Negócios
- Times de Analytics

### Fonte dos Dados

O dataset utilizado contém informações anonimizadas de clientes, incluindo:

- comportamento transacional
- uso de crédito
- métricas de engajamento
- características do perfil do cliente

A partir dessas variáveis, foi criada uma nova variável chamada customer_value_class, desenvolvida em um projeto anterior de Machine Learning, que classifica os clientes em três segmentos de valor:

- Low Value (Baixo Valor)
- Medium Value (Valor Médio)
- High Value (Alto Valor)

Este dashboard utiliza essa segmentação para analisar padrões financeiros e comportamentais entre os diferentes grupos de clientes.


### Objetivo do Dashboard

O objetivo do dashboard é transformar os dados em insights acionáveis, permitindo identificar:

1. clientes de alto valor para priorização estratégica
2. padrões de comportamento financeiro entre diferentes segmentos
3. sinais de risco relacionados à inatividade
4. oportunidades de melhoria em estratégias de relacionamento com clientes
