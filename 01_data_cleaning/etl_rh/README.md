# 📊 ETL RH — Pipeline de Dados para Recursos Humanos

Projeto de Engenharia de Dados com foco em **extração, transformação, carga e análise exploratória** de dados de Recursos Humanos.  
O objetivo é construir uma pipeline reprodutível, gerar métricas relevantes de RH e visualizar indicadores para suporte à tomada de decisão.

# Arquitetura do Projeto

![Diagrama](./reports/diagrama_etl_rh.png)

# Fluxo do Projeto

1. **Raw Data** – Importação de arquivos CSV/SQL
2. **ETL Scripts (Python/Pandas)** – Coleta e preparação dos dados
3. **Transformações** – Tratamento, limpeza e enriquecimento
4. **PostgreSQL** – Armazenamento dos dados refinados
5. **Geração de Gráficos** – Visualizações exploratórias
6. **Reports/Imagens** – Exportação dos gráficos finais
7. **README** – Documentação do projeto e resultados

# Tecnologias utilizadas
| Categoria      | Ferramenta                     |
| -------------- | ------------------------------ |
| Linguagem      | Python                         |
| Banco de Dados | PostgreSQL                     |
| Bibliotecas    | Pandas, SQLAlchemy             |
| Visualização   | Python + Matplotlib            |
| Versionamento  | Git + GitHub                   |


# Gráficos e metricas

| Nome do Gráfico                         | Descrição                                                            |
| --------------------------------------- | -------------------------------------------------------------------- |
| Média salarial por cargo                | Analisa como o salário varia conforme a função                       |
| Performance média por nível             | Mostra a avaliação média de performance por nível hierárquico        |
| Média de promoções por nível            | Indica quais níveis recebem mais promoções                           |
| Satisfação média por cargo              | Avalia o nível médio de satisfação por função                        |
| Tempo médio na empresa por nível        | Mostra quanto tempo, em média, cada nível permanece na empresa       |
| Distribuição de colaboradores por cargo | Quantidade de funcionários por função/cargo                          |
| Distribuição por nível educacional      | Percentual de funcionários por escolaridade                          |
| Oportunidades de liderança              | Quantidade de funcionários em cargos de liderança por área           |
| Horas extras vs trabalho remoto         | Proporção de horas extras entre quem trabalha remoto e no escritório |
| Turnover por estado civil               | Avalia impacto do estado civil no desligamento                       |
| Turnover por cargo                      | Identifica funções com maior taxa de saída                           |
| Turnover por nível de satisfação        | Correlação entre satisfação e desligamento                           |


## Visualizações e Insights

### Média salarial por cargo
![Média salarial por cargo](./reports/avg_income_by_role.png)

### Performance média por nível
![Performance média por nível](./reports/avg_performance_by_level.png)

### Média de promoções por nível
![Promoções por nível](./reports/avg_promotions_by_level.png)

### Satisfação média por cargo
![Satisfação média por cargo](./reports/avg_satisfaction_by_role.png)

### Tempo médio na empresa por nível
![Tempo médio por nível](./reports/avg_years_by_level.png)

### Distribuição de colaboradores por cargo
![Distribuição por cargo](./reports/distribution_by_role.png)

### Distribuição por nível educacional
![Distribuição educacional](./reports/education_distribution.png)

### Oportunidades de liderança
![Oportunidades de liderança](./reports/leadership_opportunities.png)

### Horas extras vs trabalho remoto
![Horas extras vs remoto](./reports/overtime_vs_remote.png)

### Turnover por estado civil
![Turnover por estado civil](./reports/turnover_by_marital.png)

### Turnover por cargo
![Turnover por cargo](./reports/turnover_by_role.png)

### Turnover por nível de satisfação
![Turnover por satisfação](./reports/turnover_by_satisfaction.png)


