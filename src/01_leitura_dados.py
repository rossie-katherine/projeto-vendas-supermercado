# Leitura e inspeção inicial do CSV exportado do PostgreSQL (camada Raw)
# Este script NÃO altera os dados, só mostra como eles estão

# ---------- BIBLIOTECAS ----------
from pathlib import Path  # trabalhar com caminhos de pastas

import pandas as pd  # biblioteca principal para tabelas de dados

# ---------- CONFIGURAÇÕES ----------
# Arquivo que exportamos do banco na Fase 2
CAMINHO_CSV = Path("data/raw/raw_vendas_exportada.csv")


# ---------- FUNÇÃO 1: LER O ARQUIVO ----------
def carregar_dados(caminho):
    # read_csv lê o arquivo e devolve um DataFrame (a tabela do pandas)
    df = pd.read_csv(caminho)
    return df


# ---------- FUNÇÃO 2: INSPECIONAR ----------
def inspecionar(df):
    # Mostra todas as colunas na tela, sem cortar com "..."
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)

    # 1. Tamanho da tabela: (linhas, colunas)
    print("=== TAMANHO (linhas, colunas) ===")
    print(df.shape)

    # 2. As 5 primeiras linhas
    print("\n=== PRIMEIRAS LINHAS ===")
    print(df.head())

    # 3. Tipo de cada coluna e quantidade de valores preenchidos
    print("\n=== TIPOS DAS COLUNAS ===")
    df.info()

    # 4. Estatística básica das colunas numéricas
    print("\n=== ESTATÍSTICAS DESCRITIVAS ===")
    print(df.describe())

    # 5. Quantidade de valores ausentes (nulos) em cada coluna
    print("\n=== VALORES NULOS POR COLUNA ===")
    print(df.isna().sum())

    # 6. Quantidade de linhas totalmente duplicadas
    print("\n=== LINHAS DUPLICADAS ===")
    print(df.duplicated().sum())

    # 7. Quantidade de ids de venda repetidos
    print("\n=== IDs DE VENDA REPETIDOS ===")
    print(df["invoice_id"].duplicated().sum())


# ---------- EXECUÇÃO ----------
# Esta linha faz o script rodar só quando você executa o arquivo diretamente
if __name__ == "__main__":
    dados = carregar_dados(CAMINHO_CSV)
    inspecionar(dados)

    
# ---------- OBSERVAÇÕES DA INSPEÇÃO ----------
# - Base com 1000 linhas e 17 colunas, sem valores nulos e sem duplicados
# - sale_date está como texto, no formato americano (mês/dia/ano)
# - sale_time está como texto, no formato de 12 horas (AM/PM)
# - Valores monetários têm 4 casas decimais, mas o banco usa 2
# - gross_margin_percentage é igual em todas as linhas (4,76)
# - Nomes das colunas em inglês, o dicionário do projeto usa português
# - Não há quantidade <= 0 nem avaliação fora da faixa 0 a 10