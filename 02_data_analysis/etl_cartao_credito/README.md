# 📊 Análise de Churn em Cartão de Crédito - Projeto de Data Science
## Descrição
Projeto de análise preditiva de churn (cancelamento) em uma empresa de cartão de crédito. O objetivo é identificar padrões comportamentais e características dos clientes que tendem a cancelar seus cartões, permitindo ações preventivas para retenção.

## Problema de Negócio
A empresa observou um aumento significativo no cancelamento de cartões, causando prejuízos financeiros. O desafio é:

Identificar os principais fatores que levam ao cancelamento
Segmentar clientes com maior risco de churn
Propor ações estratégicas de retenção

## Metodologia
Fase 1: Exploração e Limpeza de Dados
Importação e codificação correta dos dados (latin1)
Remoção de colunas irrelevantes (CLIENTNUM)
Tratamento de valores nulos (dropna())
Análise descritiva inicial

Fase 2: Análise Exploratória (EDA)
Distribuição das categorias (Clientes Ativos vs. Cancelados)
Análise de todas as variáveis via histogramas interativos
Identificação de padrões visuais nos gráficos

Fase 3: Análise de Insights
Foco na categoria de cartão "Blue" (onde ocorre 92% dos cancelamentos)
Investigação da relação entre contatos, transações e churn
Segmentação de clientes críticos
Análise 80/20 (Princípio de Pareto)

## Principais Descobertas
1. Categoria do Cartão 📋
92% dos cancelamentos ocorrem na categoria "Blue"
Insight: Cartões da categoria Blue podem não oferecer benefícios competitivos

2. Frequência de Contatos 📞
100% dos clientes que ligaram 6 vezes cancelaram
Quanto mais contatos, maior a probabilidade de churn
Insight: Problemas não resolvidos levam à insatisfação

3. Uso do Cartão 💳
Clientes com menos de 60 transações/ano têm alto risco
Baixo uso do limite disponível correlaciona com cancelamento
Insight: Clientes que não usam ativamente tendem a cancelar

4. Segmento Crítico 🚨
Cliente crítico: Menos de 60 transações + Mais de 2 contatos
Este grupo representa 13% dos cancelamentos
Insight: Foco eficiente para ações de retenção

## Visualizações Interativas
- Tecnologia Utilizada
Plotly Express: Gráficos interativos e dinâmicos
Histogramas por categoria: Comparação visual entre Ativos e Cancelados
Análise multivariada: 18 variáveis analisadas individualmente

## Exemplos de Gráficos:
Distribuição por categoria de cartão
Contatos vs. Cancelamentos
Transações vs. Categoria
Limite vs. Uso do cartão

## Plano de Ação Proposto
Ação 1: Revisão da Categoria Blue 🎯
Análise competitiva: Comparar benefícios com concorrentes
Reposicionamento: Melhorar vantagens da categoria
Segmentação: Oferecer upgrade para categorias superiores

Ação 2: Melhoria no Atendimento 📞
Protocolo especial: Para clientes com múltiplos contatos
Resolução proativa: Antecipar problemas recorrentes
Métricas: Reduzir necessidade de contatos repetidos

Ação 3: Incentivo ao Uso do Cartão 💳
Programa de pontos: Para transações acima de 60/ano
Benefícios progressivos: Mais vantagens com mais uso
Campanhas segmentadas: Para clientes com baixa utilização

Ação 4: Sistema de Alertas 🚨
Monitoramento: Clientes com <60 transações + >2 contatos
Intervenção proativa: Oferta de benefícios para retenção
Foco 80/20: 13% dos casos causam impacto significativo

## Insights de Data Science
- Técnicas Aplicadas:
Análise Exploratória (EDA): Entendimento dos dados
Visualização de Dados: Comunicação eficaz
Segmentação: Identificação de padrões
Princípio 80/20: Foco nos fatores mais impactantes

- Próximos Passos Técnicos:
Modelo preditivo: Machine Learning para prever churn
Análise de sobrevivência: Tempo até cancelamento
Testes A/B: Validação das ações propostas
Dashboard em tempo real: Monitoramento contínuo

## Resumo Executivo
Problema: Alta taxa de cancelamento de cartões causa prejuízos
Solução: Identificação de 4 fatores-chave e 4 ações estratégicas
Impacto: Redução estimada de 20% no churn com foco em 13% dos casos
Tecnologia: Python, Pandas, Plotly para análise e visualização
Resultado: Plano de ação data-driven para retenção de clientes


