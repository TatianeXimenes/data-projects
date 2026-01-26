# 🏦 Análise de Churn Bancário com PySpark
## Descrição
Projeto de análise preditiva de churn de clientes bancários utilizando PySpark no Databricks. O objetivo é identificar padrões e prever quais clientes têm maior probabilidade de deixar o banco, permitindo ações preventivas de retenção.

## Objetivo
Desenvolver um modelo preditivo para classificar clientes em risco de churn (cancelamento de conta) baseado em características demográficas, comportamentais e financeiras.

## Dataset
Nome: Bank Churners Dataset
Origem: Dataset público de clientes bancários
Registros: 10.127 clientes
Variável alvo: Attrition_Flag (Existing Customer vs Attrited Customer)

## Tecnologias Utilizadas
PySpark: Processamento distribuído
Databricks: Ambiente de execução
scikit-learn: Pré-processamento e encoding
Python 3: Linguagem principal
Pandas: Manipulação auxiliar de dados

## Análise de Qualidade dos Dados
Função personalizada completudeVar() para analisar:
Quantidade de duplicados por coluna
Quantidade de valores nulos
Quantidade de valores únicos
Total de registros


## Métricas de Avaliação
Acurácia
Precision e Recall
F1-Score
Matriz de Confusão
ROC-AUC

## Resultados Esperados
- Insights de Negócio
Perfil de clientes com alto churn: Identificação de características comuns
Fatores de risco: Variáveis mais correlacionadas com churn
Segmentação: Grupos de clientes para diferentes estratégias

- Métricas do Modelo
Acurácia alvo: > 85%
Recall para churn: > 80% (capturar a maioria dos cancelamentos)
Precision: Minimizar falsos positivos

## Pipeline de Machine Learning
- Fluxo Completo
1. Extração → 2. Limpeza → 3. Análise Exploratória → 
4. Pré-processamento → 5. Feature Engineering → 
6. Modelagem → 7. Avaliação → 8. Deploy

- Feature Engineering Implementado
Encoding categórico: One-Hot Encoding
Normalização: Variáveis numéricas (planejado)
Seleção de features: Baseada em importância (planejado)

## Desafios e Limitações
- Desafios Técnicos
Desequilíbrio de classes: Mais clientes ativos que inativos
Multicolinearidade: Correlação entre features
Overfitting: Modelo muito complexo para dados limitados

- Soluções Implementadas/Planejadas
# Para desequilíbrio
from imblearn.over_sampling import SMOTE

# Para multicolinearidade
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Para overfitting
from sklearn.model_selection import cross_val_score

- Melhorias do Modelo
Testar diferentes algoritmos: Random Forest, XGBoost, Gradient Boosting
Tuning de hiperparâmetros: Grid Search/Random Search
Ensemble methods: Combinação de modelos
Deep Learning: Redes neurais para dados tabulares

- Expansão do Projeto
Pipeline automatizado: Airflow/MLflow
API de predição: FastAPI/Flask
Dashboard interativo: Streamlit/Dash
Monitoramento contínuo: Drift detection

## Status do Projeto
- Concluído
Carregamento e limpeza inicial dos dados
Análise de completude e qualidade
Pré-processamento básico (encoding)
Planejamento do pipeline de ML

- Em Andamento
Desenvolvimento do modelo de regressão logística
Feature engineering adicional
Avaliação de métricas de negócio

- Próximas Etapas
Implementação completa do modelo
Validação com dados de teste
Dashboard de visualização
Documentação técnica detalhada


