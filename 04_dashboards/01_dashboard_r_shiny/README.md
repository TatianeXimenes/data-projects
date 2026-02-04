# 📊 Employee Attrition Dashboard — R Shiny

Dashboard interativo desenvolvido em **R Shiny** para análise de **Employee Attrition (rotatividade de colaboradores)**, com foco em visualização exploratória, indicadores-chave (KPIs) e filtros dinâmicos.

Este projeto faz parte da **Cayegoria – Dashboard Interativo**, com o objetivo de demonstrar habilidades em **R, Shiny, análise de dados e storytelling visual**.

---

## Objetivo do Projeto

Criar um dashboard interativo que permita:
- Explorar taxas de attrition por diferentes dimensões
- Analisar o impacto de cargo, idade e trabalho remoto
- Disponibilizar KPIs claros para tomada de decisão
- Demonstrar boas práticas de organização de projeto em R

---

## Principais Funcionalidades

### 🔹 KPIs Dinâmicos
- **Attrition Rate (%)**
- **Total de Colaboradores**
- **% de Colaboradores Remotos**

Todos os KPIs são **reativos aos filtros** aplicados.

### 🔹 Filtros Interativos
- Cargo (`Job Role`)
- Faixa etária
- Regime de trabalho remoto

### 🔹 Visualizações
- Attrition por Cargo (proporção)
- Attrition por Trabalho Remoto
- Tabela interativa com os dados filtrados

---

## Tecnologias Utilizadas

- **R**
- **Shiny**
- **dplyr**
- **ggplot2**
- **data.table**
- **DT**
- **scales**

---

## Estrutura do Projeto

```text
04_dashboards/
└── 01_dashboard_r_shiny/
    ├── app/
    │   ├── app.R
    │   ├── ui.R
    │   └── server.R
    ├── raw/data/
    │   └── employee_attrition.csv
    ├── screenshots/
    │   └── dashboard_overview.pdf
    └── README.md
```

---

### Como Executar o Projeto

1. Clone o repositório:
git clone https://github.com/seu-usuario/nome-do-repositorio.git

2. Abra o R ou RStudio
3. Instale os pacotes necessários (se ainda não tiver):
install.packages(c(
  "shiny", "dplyr", "ggplot2", "data.table",
  "DT", "scales"
))

4. Execute o app:
setwd("04_dashboards/01_dashboard_r_shiny/app")
shiny::runApp()

### Exemplo de Uso
O dashboard permite responder perguntas como:

- Quais cargos apresentam maior taxa de attrition?
- O trabalho remoto influencia a rotatividade?
- Existe diferença de attrition por faixa etária?

### Limitações e Próximos Passos
1. Limitações Atuais
- Execução local (sem deploy em nuvem)
- Base de dados estática

2. Melhorias Futuras
- Deploy em ShinyApps.io ou Docker
- Integração com banco de dados
- Inclusão de mais métricas (tempo de empresa, renda, satisfação)
- Versionamento de dados
