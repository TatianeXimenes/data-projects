# 📊 Data Analysis - Portfólio de Projetos ETL e Análise de Dados
## Sobre este Diretório
Diretório dedicado a projetos avançados de ETL (Extract, Transform, Load) e análise de dados, com foco em problemas do mundo real envolvendo múltiplas fontes de dados, critérios complexos e limpeza de dados em grande escala.

## Projetos Incluídos até o momento
### 1. etl_multicriterio_recife_salvador
Sistema de Análise Multicritério para Dados Urbanos das Capitais
Objetivo: Comparação socioeconômica entre Recife e Salvador
Fontes: Dados públicos, IBGE, prefeituras, APIs governamentais
Transformações: Normalização, padronização, criação de indicadores compostos
Saídas: Dashboards comparativos, relatórios de indicadores urbanos
Tecnologias: Python, Pandas, APIs REST, PostgreSQL
Conceitos: Análise multicritério, dados urbanos, indicadores sociais

### 2. etl_cartao_credito
Pipeline de Processamento de Transações de Cartão de Crédito
Objetivo: Detecção de padrões e anomalias em transações financeiras
Desafios: Dados sensíveis, conformidade (LGPD), volumes altos
Processos: Anonimização, agregação temporal, feature engineering
Análises: Segmentação de clientes, sazonalidade, risco de fraude
Tecnologias: Python, Pandas, Scikit-learn, criptografia
Conceitos: Fintech, segurança de dados, análise temporal

### 3. etl_marketing_digital
Integração de Dados de Marketing Multi-canal
Objetivo: Unificar dados de Google Analytics, mídias sociais e CRM
Canais: Facebook Ads, Google Ads, Instagram, Email Marketing
ETL: Transformação de formatos diferentes, criação de UTM tracking
Métricas: ROI, CAC, LTV, conversão, engajamento
Tecnologias: Python, APIs (Google, Meta), Pandas, SQL
Conceitos: Marketing analytics, attribution modeling, funil de vendas

### 4. etl_pnad_continua
Processamento da Pesquisa Nacional por Amostra de Domicílios Contínua
Objetivo: Análise trimestral do mercado de trabalho brasileiro
Complexidade: Dados hierárquicos, pesos amostrais, inflação
Indicadores: Taxa de desocupação, renda média, informalidade
Segmentações: Por região, gênero, raça, faixa etária
Tecnologias: Python, Pandas, estatística inferencial
Conceitos: Econometria, dados oficiais, análise laboral

## Stack Tecnológica Comum
- Ferramentas Principais
Python 3.8+: Linguagem core para todos os projetos
Pandas/NumPy: Manipulação eficiente de dados
SQL: Bancos relacionais (PostgreSQL/MySQL)
APIs REST: Integração com serviços externos
Docker: Containerização para reprodutibilidade

- KPIs de Processamento
Tempo médio de ETL: < 30 minutos
Taxa de sucesso: > 99.5%
Coverage de testes: > 80%
Documentação: 100% dos pipelines


