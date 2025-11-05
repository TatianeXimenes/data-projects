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

| Métrica                         | Descrição                               |
| ------------------------------- | --------------------------------------- |
| Turnover por Satisfação         | Como a satisfação impacta desligamentos |
| Turnover por Cargo              | Risco de saída por função               |
| Média salarial por cargo        | Distribuição salarial                   |
| Promoções por nível             | Meritocracia e carreira                 |
| Anos na empresa por nível       | Tempo médio na organização              |
| Trabalho remoto vs horas extras | Dinâmica moderna de trabalho            |
| Satisfação Média por Cargo      | Cultura e clima organizacional          |

