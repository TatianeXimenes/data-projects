# Correção de Base de Dados Problemática
Projeto focado na limpeza intensiva de uma base fake com múltiplos problemas de qualidade.

## Contexto:
Base fake: 100 registros simulando dados reais problemáticos
Problemas comuns: Erros de digitação, formatos inconsistentes, dados inválidos
Foco: Padronização de nomes e datas

1. Principais Problemas Endereçados:
- Nomes:
Inconsistências de capitalização (joão, João, JOÃO)
Caracteres especiais mal formatados
Abreviações inconsistentes
Nomes duplicados com variações

- Datas:
Múltiplos formatos (DD/MM/YYYY, MM-DD-YY, YYYY/MM/DD)
Datas inválidas (31/02/2023)
Separadores inconsistentes
Fusos horários misturados

## Técnicas Aplicadas:
Expressões Regulares para padronização
Validação de domínios para campos categóricos
Conversão inteligente de formatos de data
Deduplicação com matching fuzzy
Imputação cuidadosa de valores faltantes

## Saída:
Base limpa com 100% de consistência
Metadados de qualidade gerados
Relatório de transformações aplicadas
Scripts reutilizáveis para outros datasets
