# 📊 Sistema de Análise Multicritério para Seleção de Localização de Centro de Distribuição

## Descrição
Este projeto implementa um sistema de análise multicritério para seleção da melhor localização para um centro de distribuição (CD) entre capitais brasileiras. Combina TOPSIS e Soma Ponderada (WSM) para ranquear cidades com base em custos, tempo de entrega e potencial de consumo.

## Objetivo
Auxiliar na tomada de decisão estratégica para implantação de centros de distribuição através de:

Análise quantitativa de múltiplos critérios
Ranking objetivo de cidades candidatas
Diagnóstico detalhado de pontos fortes e fracos
Visualização clara dos resultados

## Critérios de Avaliação
1. Custo Imobiliário Composto (40%)
Aluguel por m² (R$)
Preço de terreno (índice)
Custo de mão de obra (índice)
Carga tributária (índice)

2. Tempo de Entrega Médio (35%)
Tempo de viagem rodoviário ponderado pela demanda
Considera distâncias para todos os estados
Ponderação pelo potencial de consumo dos destinos

3. Potencial de Consumo (25%)
Captação de demanda (modelo gravitacional)
Decaimento exponencial por tempo de viagem
População × Renda × Índice de consumo

## Tecnologias Utilizadas
Python 3
Pandas: Manipulação de dados
NumPy: Cálculos numéricos
Matplotlib: Visualização
JSON: Configuração de pesos

## Métodos de Análise
1. Soma Ponderada (WSM)
Método aditivo simples
Normalização Min-Max
Todos os critérios convertidos para "benefício"

2. TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)
Considera distância para solução ideal e anti-ideal
Preserva natureza dos critérios (custo vs. benefício)
Normalização vetorial

3. Método Combinado
Ranking final: Média dos scores de WSM e TOPSIS
Robustez: Reduz viés de método único
Consistência: Validação cruzada implícita

## Saídas Geradas
1. ranking.csv
Posição final de cada cidade
Scores individuais (WSM e TOPSIS)
Score final combinado

2. diagnostico.csv
Valores normalizados de cada critério
Dados brutos de referência
Análise detalhada por dimensão

3. ranking.png
Gráfico de barras do ranking
Visualização rápida dos resultados
Pronto para apresentações


