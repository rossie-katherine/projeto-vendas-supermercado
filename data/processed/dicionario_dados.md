# Dicionário de dados: vendas_tratadas.csv

Arquivo: `data/processed/vendas_tratadas.csv` (1000 linhas, 20 colunas).
Gerado por `src/02_etl_vendas.py` a partir de `data/raw/raw_vendas_exportada.csv`.

# Colunas originais (17)

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| id_venda | VARCHAR(50) | PRIMARY KEY, NOT NULL | Identificador único da venda (coluna original: Invoice ID) |
| Filial | VARCHAR(10) | NOT NULL | Nome da filial: Alex, Giza ou Cairo (Branch) |
| Cidade | VARCHAR(100) | NOT NULL | Cidade da filial (City) |
| tipo_cliente | VARCHAR(50) | | Tipo de cliente: Member ou Normal (Customer type) |
| Gênero | VARCHAR(20) | | Gênero do cliente (Gender) |
| linha_produto | VARCHAR(150) | NOT NULL | Categoria do produto vendido (Product line) |
| preco_unitario | NUMERIC(10,2) | NOT NULL, CHECK >= 0 | Preço de uma unidade (Unit price) |
| Quantidade | INTEGER | NOT NULL, CHECK > 0 | Unidades vendidas (Quantity) |
| Imposto | NUMERIC(10,2) | CHECK >= 0 | Imposto de 5% sobre a venda (Tax 5%) |
| valor_total | NUMERIC(12,2) | NOT NULL, CHECK >= 0 | Valor total da venda com imposto, conferido: preço x quantidade + imposto (Sales) |
| data_venda | DATE | NOT NULL | Data da venda, convertida do formato mês/dia/ano (Date) |
| hora_venda | TIME | | Horário da venda, convertido do formato 12 horas (Time) |
| forma_pagamento | VARCHAR(50) | NOT NULL | Forma de pagamento: Cash, Credit card ou Ewallet (Payment) |
| custo_mercadoria | NUMERIC(12,2) | CHECK >= 0 | Custo da mercadoria vendida (cogs) |
| margem_percentual | NUMERIC(10,2) | | Margem bruta em %, igual a 4,76 em todas as linhas (gross margin percentage) |
| receita_bruta | NUMERIC(12,2) | CHECK >= 0 | Renda bruta da venda, que neste dataset coincide com o imposto (gross income) |
| Avaliação | NUMERIC(4,2) | CHECK entre 0 e 10 | Nota dada pelo cliente (Rating) |

# Colunas derivadas (3)

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| dia_semana | TEXT | | Dia da semana da venda em português, calculado a partir de data_venda |
| mes | INTEGER | | Mês da venda, de 1 a 12, calculado a partir de data_venda |
| hora_do_dia | INTEGER | | Hora cheia da venda, de 0 a 23, calculada a partir de hora_venda |

# Decisões de tratamento

- **Base sem nulos e duplicados:** o ETL verificou esses casos e nenhuma linha precisou ser removida.
- **Regras de negócio:** não foram encontradas linhas com valores negativos, quantidade menor ou igual a zero ou avaliações fora da escala de 0 a 10.
- **Valores monetários:** arredondados para 2 casas decimais durante o tratamento.
- **Formato dos dados:** arquivo CSV separado por vírgula e codificado em UTF-8.