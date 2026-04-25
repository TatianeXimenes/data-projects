# 📊 Customer Value Classification — Machine Learning Project
## Visão Geral

Este projeto tem como objetivo classificar clientes em diferentes níveis de valor para o negócio (Low, Medium e High Value), utilizando técnicas de Machine Learning, com foco em qualidade analítica, interpretabilidade e impacto de negócio.

A solução foi desenvolvida de forma estruturada, seguindo boas práticas de ciência de dados, desde a análise exploratória até a avaliação final do modelo.

## Objetivo de Negócio

Criar uma segmentação de clientes baseada em comportamento financeiro e relacionamento, capaz de apoiar decisões como:

- priorização de clientes
- definição de estratégias de relacionamento
- direcionamento de campanhas
- otimização do uso de recursos comerciais

## Estrutura do Projeto
03_machine_learning/
└── etl_customer_value_classification/
    ├── notebooks/
    │   ├── 01_eda.ipynb
    │   ├── 02_target_engineering.ipynb
    │   ├── 03_feature_engineering.ipynb
    │   ├── 04_modeling.ipynb
    │   └── 05_evaluation.ipynb
    ├── raw/
    │   ├── data/
    │   ├── processed/
    │   └── model_input/
    └── README.md

## Metodologia
#### 1. Análise Exploratória (EDA)

Avaliação da distribuição das variáveis;
Identificação de padrões comportamentais;
Análise inicial de correlação e variáveis relevantes.

#### 2. Target Engineering

Criação de um score contínuo de valor do cliente;
Normalização das variáveis financeiras.

Conversão do score em classes: Low_Value, Medium_Value e High_Value.

Validação da distribuição e sanity checks.

#### 3. Feature Engineering

Separação clara entre features e target;
Construção de pipeline de pré-processamento;
Persistência dos conjuntos de treino e teste para reprodutibilidade.

#### 4. Modelagem

Modelos avaliados:
Regressão Logística (baseline);
Random Forest;
Métrica principal: F1-score macro;
Validação cruzada para avaliação de generalização.

#### 5. Avaliação

Classification report;
Matriz de confusão;
Análise qualitativa dos erros;
Interpretação de impacto de negócio;
Análise de importância das variáveis (Random Forest).

## Principais Resultados

Regressão Logística apresentou o melhor desempenho global;
F1-score macro elevado e consistente;
Validação cruzada confirmou boa capacidade de generalização;
Erros concentrados entre classes adjacentes (Medium ↔ High);
Baixo risco de impacto negativo para decisões estratégicas.

##  Principais Insights

O valor do cliente é fortemente influenciado por:
volume de transações;
frequência de uso;
limite de crédito;
Variáveis demográficas tiveram menor relevância;
Modelos simples e interpretáveis foram mais adequados ao problema.

## Modelo Final Escolhido

🏆 Regressão Logística

- Motivos:

Melhor desempenho em F1-score macro;
Maior interpretabilidade;
Menor complexidade computacional;
Melhor alinhamento com aplicações de negócio.

## Tecnologias Utilizadas

Python,
Pandas, NumPy,
Scikit-learn,
Jupyter Notebook,
Git & GitHub.
