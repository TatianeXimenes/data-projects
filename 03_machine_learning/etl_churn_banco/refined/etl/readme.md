## Contexto Técnico

Este projeto foi inicialmente desenvolvido para execução completa no Databricks Community Edition.
Durante a implementação, foram encontradas limitações do ambiente relacionadas ao uso de Spark ML
(StringIndexer, VectorAssembler), comuns em ambientes restritos.

Como alternativa técnica, foi adotada uma abordagem híbrida:
- Spark utilizado para ingestão e preparação inicial dos dados
- Conversão para pandas para aplicação de pipeline de Machine Learning com scikit-learn

Essa decisão permitiu manter boas práticas de ML (pipeline, encoding, balanceamento de classes),
além de garantir reprodutibilidade local.

O projeto está estruturado de forma que pode ser facilmente migrado para:
- Databricks Full Edition
- Azure Databricks
- AWS EMR / Glue

