# Carregamento dos pacotes
library(data.table)
library(dplyr)
library(tidyverse)
library(GGally)
library(corrplot)
library(caret)
library(pROC)


# Caminho da base
setwd("/home/tatiane/data-projects/02_data_analysis/etl_marketing_digital/raw/data/")

# Leitura
df <- fread("digital_marketing_campaign_dataset.csv", header = TRUE, dec = ".")

# Estrutura da base
glimpse(df)
summary(df)

# Distribuição
cols <- colnames(df)

for (col in cols) {
  cat("\n---", col, "---\n")
  df %>%
    group_by(across(all_of(col))) %>%
    summarise(count = n()) %>%
    print()
}

# Mudança no valor da coluna 'conversion'
#df <- df %>%
#  mutate(across(c(Conversion), ~ifelse(. == 1, "sim", "não")))
# Validação da transformação
#df %>% group_by(Conversion) %>% summarise(n())
