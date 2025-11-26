# Verificar, instalar e carregar pacotes
verificar_instalar_carregar <- function(pacote) {
  if (!require(pacote, character.only = TRUE)) {
    install.packages(pacote)
    library(pacote, character.only = TRUE)
  }
}
# Pacotes necessários
pacotes <- c("arrow","ggplot2","scales","dplyr","stringi")
lapply(pacotes, verificar_instalar_carregar)

## Filtros aplicados: 
## 1. considerar apenas quem tem remuneração 'rmh_todos_trabalhos', excluir os nulos;
## 2. exclusão de raça tida como 'ignorada';
## 3. junção da cor 'preta' e 'parda'.

# Carregamento da base
dados_PNAD_cont <- read_parquet("/home/tatiane/Downloads/NINSOC/base_final/pnadc_2023_2025_3_filtrada/dados_PNAD_cont.parquet")
attach(dados_PNAD_cont)
dim(dados_PNAD_cont)

summary(dados_PNAD_cont$rmh_todos_trabalhos)
table(dados_PNAD_cont$tp_remuneracao_habitual)

# Tabelas de frequência e proporções
# Tabela de frequência simples
table(dados_PNAD_cont$sexo, dados_PNAD_cont$ind_pobreza)
# Proporções
round(prop.table(table(dados_PNAD_cont$sexo, dados_PNAD_cont$ind_pobreza), margin = 1),3)

# Frequência simples por ano
table(dados_PNAD_cont$ano, dados_PNAD_cont$sexo, dados_PNAD_cont$ind_pobreza)
# Proporções dentro de cada sexo por ano
round(prop.table(table(dados_PNAD_cont$ano, dados_PNAD_cont$sexo, dados_PNAD_cont$ind_pobreza), margin = c(1,2)), 3)

# Tabela de frequência simples
table(dados_PNAD_cont$raca_cor, dados_PNAD_cont$ind_pobreza)
# Proporções
round(prop.table(table(dados_PNAD_cont$raca_cor, dados_PNAD_cont$ind_pobreza), margin = 1),3)

# Frequência simples por ano
table(dados_PNAD_cont$ano, dados_PNAD_cont$raca_cor, dados_PNAD_cont$ind_pobreza)
# Proporções dentro de cada raça/cor por ano
round(prop.table(table(dados_PNAD_cont$ano, dados_PNAD_cont$raca_cor, dados_PNAD_cont$ind_pobreza), margin = c(1,2)), 3)

# Criar dataframe com os dados
dados <- data.frame(
  ano = rep(c(2023, 2024, 2025), times = 8),
  raca_cor = rep(c("Amarela", "Branca", "Indigena", "PardaPreta"), each = 3, times = 2),
  indicador = rep(c("Fora da pobreza", "Na pobreza"), each = 12),
  proporcao = c(
    # Fora da pobreza (0)
    0.496, 0.621, 0.664,   # Amarela
    0.547, 0.616, 0.658,   # Branca
    0.295, 0.357, 0.412,   # Indígena
    0.350, 0.429, 0.469,   # Parda/Preta
    # Na pobreza (1)
    0.504, 0.379, 0.336,   # Amarela
    0.453, 0.384, 0.342,   # Branca
    0.705, 0.643, 0.588,   # Indígena
    0.650, 0.571, 0.531    # Parda/Preta
  )
)

# Gráfico de linhas
ggplot(dados, aes(x = ano, y = proporcao, color = raca_cor, linetype = indicador)) +
  geom_line(size = 1.2) +
  geom_point(size = 2) +
  scale_y_continuous(labels = scales::percent_format(accuracy = 1)) +
  labs(
    title = "Evolucao da pobreza por raca/cor (2023-2025)",
    x = "Ano",
    y = "Proporcao",
    color = "Raca/Cor",
    linetype = "Indicador"
  ) +
  theme_minimal(base_size = 14) +
  theme(legend.position = "bottom")

# Tabela cruzada
xtabs(~ sexo + raca_cor + ind_pobreza, data = dados_PNAD_cont)
# Proporções por sexo e raça/cor
round(prop.table(xtabs(~ sexo + raca_cor + ind_pobreza, data = dados_PNAD_cont), margin = c(1,2)),3)

# Tabela cruzada completa
xtabs(~ ano + sexo + raca_cor + ind_pobreza, data = dados_PNAD_cont)
# Proporções por sexo e raça/cor dentro de cada ano
round(prop.table(xtabs(~ ano + sexo + raca_cor + ind_pobreza, data = dados_PNAD_cont), margin = c(2,3)), 3)


hist(rmh_todos_trabalhos[rmh_todos_trabalhos<50000])
length(rmh_todos_trabalhos[rmh_todos_trabalhos<50000])
dim(dados_PNAD_cont)

dados_PNAD_cont %>%
  group_by(ind_pobreza) %>%
  summarise(
    media_rendimento   = mean(rmh_todos_trabalhos, na.rm = TRUE),
    mediana_rendimento = median(rmh_todos_trabalhos, na.rm = TRUE),
    .groups = "drop"
  )

dados_PNAD_cont %>%
  mutate(faixa_rendimento = cut(rmh_todos_trabalhos,
                                breaks = c(0, 10000, 50000, Inf),
                                labels = c("Até 10.000", "10.000 a 50.000", "Mais de 50.000"),
                                right = TRUE)) %>%
  count(faixa_rendimento) %>%
  mutate(proporcao = n / sum(n))

# Criar faixas de rendimento
dados_faixas <- dados_PNAD_cont %>%
  mutate(faixa_rendimento = cut(rmh_todos_trabalhos,
                                breaks = c(0, 10000, 50000, Inf),
                                labels = c("Até 10.000", "10.000 a 50.000", "Mais de 50.000"),
                                right = TRUE)) %>%
  count(faixa_rendimento) %>%
  mutate(proporcao = round(n / sum(n), 3))

# Gráfico de barras com % dentro das barras
ggplot(dados_faixas, aes(x = faixa_rendimento, y = proporcao, fill = faixa_rendimento)) +
  geom_col(show.legend = FALSE) +
  geom_text(aes(label = scales::percent(proporcao, accuracy = 0.1)),
            position = position_stack(vjust = 0.5),
            color = "black", size = 3) +
  scale_y_continuous(labels = percent_format(accuracy = 0.1)) +
  labs(x = "Faixa de rendimento", y = "Proporção",
       title = "Distribuição das faixas de rendimento (rmh_todos_trabalhos)")

# Gráficos
# Distribuição da pobreza por sexo
ggplot(dados_PNAD_cont, aes(x = sexo, fill = factor(ind_pobreza))) +
  geom_bar(position = "fill") +
  geom_text(stat = "count",
            aes(label = scales::percent(..count../tapply(..count.., ..x.., sum)[..x..], accuracy = 0.1)),
            position = position_fill(vjust = 0.5), color = "black",
            size = 3) +
  labs(y = "Proporcao", fill = "Pobreza", title = "Indice de pobreza por sexo")

# Calcular proporções por ano e sexo
dados_sexo_ano <- dados_PNAD_cont %>%
  group_by(ano, sexo, ind_pobreza) %>%
  summarise(n = n(), .groups = "drop") %>%
  group_by(ano, sexo) %>%
  mutate(prop = n / sum(n))

# Gráfico - Índice de pobreza por sexo ao longo dos anos
ggplot(dados_sexo_ano, aes(x = ano, y = prop, fill = factor(ind_pobreza))) +
  geom_col(position = "stack") +
  geom_text(aes(label = scales::percent(prop, accuracy = 0.1)),
            position = position_stack(vjust = 0.5), color = "black", size = 3) +
  facet_wrap(~sexo) +
  labs(y = "Proporcao", fill = "Pobreza",
       title = "Indice de pobreza por sexo ao longo dos anos")

# Distribuição da pobreza por raça/cor
ggplot(dados_PNAD_cont, aes(x = raca_cor, fill = factor(ind_pobreza))) +
  geom_bar(position = "fill") +
  geom_text(stat = "count",
            aes(label = scales::percent(..count../tapply(..count.., ..x.., sum)[..x..], accuracy = 0.1)),
            position = position_fill(vjust = 0.5), color = "black",
            size = 3) +
  labs(y = "Proporcao", fill = "Pobreza", title = "Indice de pobreza por raca/cor")

# Calcular proporções por ano e raça/cor
dados_raca_ano <- dados_PNAD_cont %>%
  group_by(ano, raca_cor, ind_pobreza) %>%
  summarise(n = n(), .groups = "drop") %>%
  group_by(ano, raca_cor) %>%
  mutate(prop = n / sum(n))

# Gráfico -Índice de pobreza por raça/cor ao longo dos anos
ggplot(dados_raca_ano, aes(x = ano, y = prop, fill = factor(ind_pobreza))) +
  geom_col(position = "stack") +
  geom_text(aes(label = scales::percent(prop, accuracy = 0.1)),
            position = position_stack(vjust = 0.5), color = "black", size = 3) +
  facet_wrap(~raca_cor) +
  labs(y = "Proporcao", fill = "Pobreza",
       title = "Indice de pobreza por raca/cor ao longo dos anos")

# Cruzando sexo e raça/cor
# Calcular proporções por sexo e raça/cor
dados_plot <- dados_PNAD_cont %>%
  group_by(sexo, raca_cor, ind_pobreza) %>%
  summarise(n = n(), .groups = "drop") %>%
  group_by(sexo, raca_cor) %>%
  mutate(prop = n / sum(n))

# Gráfico com % dentro das barras
ggplot(dados_plot, aes(x = raca_cor, y = prop, fill = factor(ind_pobreza))) +
  geom_col(position = "stack") +
  geom_text(aes(label = scales::percent(prop, accuracy = 0.1)),
            position = position_stack(vjust = 0.5), color = "black",
            size = 3) +
  facet_wrap(~sexo) +
  labs(y = "Proporcao", fill = "Pobreza", 
       title = "Indice de pobreza por sexo e raca/cor")
