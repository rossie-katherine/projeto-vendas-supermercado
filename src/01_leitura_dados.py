# Leitura e inspeção inicial do CSV exportado do PostgreSQL (camada Raw)
# Este script NÃO altera os dados, só mostra como eles estão


from pathlib import Path  # trabalhar com caminhos de pastas

import pandas as pd  # biblioteca principal para tabelas de dados


CAMINHO_CSV = Path("data/raw/raw_vendas_exportada.csv")


# LER O ARQUIVO 
def carregar_dados(caminho):
    # read_csv lê o arquivo e devolve um DataFrame (a tabela do pandas)
    df = pd.read_csv(caminho)
    return df


#  INSPECIONAR 
def inspecionar(df):
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)

   
    print("=== TAMANHO (linhas, colunas) ===")
    print(df.shape)

    
    print("\n=== PRIMEIRAS LINHAS ===")
    print(df.head())

    
    print("\n=== TIPOS DAS COLUNAS ===")
    df.info()

    
    print("\n=== ESTATÍSTICAS DESCRITIVAS ===")
    print(df.describe())

   
    print("\n=== VALORES NULOS POR COLUNA ===")
    print(df.isna().sum())

    
    print("\n=== LINHAS DUPLICADAS ===")
    print(df.duplicated().sum())

   
    print("\n=== IDs DE VENDA REPETIDOS ===")
    print(df["invoice_id"].duplicated().sum())


# EXECUÇÃO 
if __name__ == "__main__":
    dados = carregar_dados(CAMINHO_CSV)
    inspecionar(dados)

    
# OBSERVAÇÕES DA INSPEÇÃO 
# - Base com 1000 linhas e 17 colunas, sem valores nulos ou duplicados
# - sale_date está como texto, no formato americano (mês/dia/ano)
# - sale_time está como texto, no formato de 12 horas (AM/PM)
# - Valores monetários possuem 4 casas decimais, enquanto o banco trabalha com 2
# - gross_margin_percentage apresenta o mesmo valor em todas as linhas (4,76)
# - Nomes das colunas estão em inglês, enquanto o dicionário do projeto usa português
# - Não há quantidade menor ou igual a 0 nem avaliação fora da faixa de 0 a 10