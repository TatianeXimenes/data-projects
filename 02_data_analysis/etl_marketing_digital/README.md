# 📊 Marketing Analysis em R
Análise exploratória, estatística e modelagem aplicada a dados de campanhas de Marketing Digital utilizando R.
O objetivo deste projeto é compreender o comportamento dos usuários, avaliar a performance das campanhas e identificar oportunidades de otimização com base em dados.

# Descrição do Projeto

Este repositório contém uma análise completa de dados de marketing, incluindo:
* Exploração estatística das variáveis de campanha;
* Relações entre métricas de engajamento e conversão;
* Visualizações com foco em insights;
* Modelagem preditiva com regressão logística;
* Avaliação de desempenho via curva ROC e AUC;
* Relatórios reprodutíveis gerados com RMarkdown;
* A análise tem como foco entender quais fatores influenciam a conversão, como investimento, engajamento, comportamento no site, fidelidade e outros.

# Objetivos
* Investigar padrões e variáveis associadas à taxa de conversão;
* Explorar a relação entre métricas de marketing (CTR, e-mail, visitas, tempo no site);
* Criar gráficos e diagnósticos para apoiar insights estratégicos;
* Desenvolver um modelo estatístico para previsão de conversão;
* Construir relatórios reproduzíveis em HTML ou PDF.

# Estrutura do Projeto
marketing_analysis_R/
├── data/                 # Bases utilizadas (.csv)
├── scripts/              # Scripts R e análises (.R, .Rmd)
├── reports/              # Resultados finais: gráficos, HTML, PDF
├── docs/                 # Documentação (ex.: dicionário de dados)
└── README.md             # Este arquivo

# Tecnologias e Pacotes Utilizados

Linguagem: R

Principais pacotes:
* tidyverse – manipulação e visualização
* dplyr – transformação de dados
* ggplot2 – gráficos e visualizações
* data.table – importação eficiente
* corrplot – matriz de correlação
* pROC – curva ROC e AUC
* knitr / rmarkdown – relatórios HTML/PDF

# Principais Etapas da Análise
1. **Carregamento e limpeza da base**
Importação da base de campanhas de marketing e preparação para análise.

2. **Análise exploratória**
Estatísticas descritivas
Distribuições
Correlações
Comparações entre segmentos (tipo de campanha, canal etc.)

3. **Testes estatísticos**
Qui-quadrado para verificar associação entre campanhas e conversão
Correlações com a variável alvo

4. **Modelagem**
Regressão logística para prever probabilidade de conversão
Interpretação dos coeficientes e significância
Avaliação com curva ROC e AUC

5. **Gerando relatórios**
Todos os resultados são organizados em arquivos .Rmd, com possibilidade de exportar para HTML.