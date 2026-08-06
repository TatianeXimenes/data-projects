#📄 Desafio Técnico

Você acaba de entrar na equipe de Engenharia de Dados do Banco Digital.

O time de Prevenção à Fraude precisa de uma base analítica consolidada para analisar o comportamento financeiro dos clientes.

Você recebeu cinco bases de dados e deverá construir um pipeline em PySpark para disponibilizar um dataset analítico para o time.

O restante das regras será discutido etapa à etapa.

## Exploração dos dados 

Antes de escrever qualquer transformação, faça exatamente o que um Engenheiro de Dados faria:

- Leia todas as bases com PySpark.
- Entenda o schema de cada uma.
- Identifique as chaves de relacionamento.
- Verifique o volume de registros.
- Faça uma exploração inicial dos dados.

## Construção da camada Silver

Depois da sua exploração inicial, fizemos uma reunião com o time de Prevenção à Fraude.

Eles aprovaram sua análise inicial e agora pediram a construção da primeira camada tratada.

Essa camada será utilizada por outros times posteriormente. 

Você NÃO deve criar ainda a tabela analítica final. Primeiro precisamos garantir que os dados possuem qualidade.

Você deverá gerar quatro DataFrames tratados: clientes_tratado, contas_tratado, pix_tratado, cartao_tratado.

1. Regras de negócio

- Base Clientes

Durante a exploração você encontrou IDs duplicados e renda nula. Agora decida como tratar.

- Base Contas

Precisamos responder: Existe alguma conta sem cliente? Existe cliente sem conta?
Se existir. Como o pipeline deve tratar?

- Base PIX

A equipe informou que:
Para análises financeiras PIX cancelado e PIX falhado não representam movimentação financeira.
Você precisa decidir. Eles permanecem na base?

- Base Cartão

Precisamos descobrir: 
Existe compra com valor <= 0?
Existe categoria inválida?
Existe conta inexistente?

2. Padronização

Todas as datas deverão possuir o mesmo tipo.
Todas as colunas monetárias deverão possuir o mesmo tipo.
Todos os nomes das colunas deverão seguir um padrão consistente.
Você decide qual.

3. Escrita

Ao final grave as quatro bases em silver/
clientes, contas. pix, cartao. Utilizando Parquet.

## Construção da camada Gold
O time de Prevenção à Fraude quer uma única tabela analítica.
O objetivo é criar o arquivo gold/clientes_movimentacao.parquet

- Regras
Cada linha representa um cliente.

- A tabela deverá conter
Dados cadastrais: id_cliente, nome, sexo, idade, UF, cidade, gerente_regional, região, renda.

Conta: tipo_conta, status_conta, data_abertura.

PIX: quantidade_pix, valor_total_pix, ticket_medio_pix, maior_pix, menor_pix.

Cartão: quantidade_compras, valor_total_cartao, ticket_medio_cartao, maior_compra, menor_compra.

- Novas regras
Crie as seguintes colunas derivadas.

1. Faixa de renda: Até 3 mil -> Baixa; 3 mil a 10 mil -> Média; Acima de 10 mil -> Alta.
2. Perfil financeiro: Baseado na soma do pix + cartão, classifique a movimentação entre baixa, média e alta.
3. Faixa etária.
4. Cliente ativo.

- Liste os clientes que: nunca fizeram PIX, nunca fizeram compra, possuem renda nula, movimentaram mais de 100 mil.
