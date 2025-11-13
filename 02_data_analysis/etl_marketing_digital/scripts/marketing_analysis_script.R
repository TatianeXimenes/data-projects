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

# 1. Análise exploratória
# Taxa geral de conversão
mean(df$Conversion)

# Distribuição das variáveis principais
df %>%
  select(Age, Income, AdSpend, ClickThroughRate, ConversionRate, TimeOnSite) %>%
  gather(variable, value) %>%
  ggplot(aes(value)) +
  geom_histogram(fill = "#69b3a2", color = "white") +
  facet_wrap(~variable, scales = "free") +
  theme_minimal()

# Matriz de correlação
num_vars <- df %>%
  select(Age, Income, AdSpend, ClickThroughRate, ConversionRate,
         WebsiteVisits, PagesPerVisit, TimeOnSite,
         EmailOpens, EmailClicks, PreviousPurchases, LoyaltyPoints)

corr_matrix <- cor(num_vars, use = "complete.obs")
corrplot(corr_matrix, method = "color", tl.cex = 0.7)

# Foco em relação com vendas
correlations_to_target <- sapply(num_vars, function(x)
  cor(x, df$Conversion, method = "pearson", use = "complete.obs")
)

sort(correlations_to_target, decreasing = TRUE)

# Taxa de conversão por canal
df %>%
  group_by(CampaignChannel) %>%
  summarise(ConversionRate = mean(Conversion),
            Count = n()) %>%
  arrange(desc(ConversionRate))

ggplot(df, aes(x = CampaignChannel, fill = factor(Conversion))) +
  geom_bar(position = "fill") +
  labs(y = "Proporção de Conversão", fill = "Convertido") +
  theme_minimal()

# Teste qui-quadrado
chisq.test(table(df$CampaignType, df$Conversion))

# AdSpend vs ConversionRate (relação investimento x resultado)
ggplot(df, aes(x = AdSpend, y = ConversionRate)) +
  geom_point(alpha = 0.6) +
  geom_smooth(method = "lm", color = "red") +
  theme_minimal()

# CTR vs ConversionRate (relação investimento x resultado)
ggplot(df, aes(x = ClickThroughRate, y = ConversionRate)) +
  geom_point(alpha = 0.6, color = "#0073C2FF") +
  geom_smooth(method = "lm", se = FALSE) +
  theme_minimal()

# Medição do impacto de cada variável na probabilidade de conversão (regressão logística)
model <- glm(Conversion ~ Age + Income + AdSpend + ClickThroughRate +
               TimeOnSite + EmailClicks + PreviousPurchases + LoyaltyPoints,
             data = df, family = binomial)

summary(model)

## Avaliação do modelo
# Predições
df$pred <- predict(model, type = "response")

# Curva ROC
roc_obj <- roc(df$Conversion, df$pred)
plot(roc_obj, col = "blue")
auc(roc_obj)
