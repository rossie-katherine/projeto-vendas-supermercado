# ETL da camada Tratada: renomeia, converte tipos e cria colunas derivadas
# Entrada: data/raw/raw_vendas_exportada.csv
# Saída: data/processed/vendas_tratadas.csv

# ---------- BIBLIOTECAS ----------
from pathlib import Path  # trabalhar com caminhos de pastas

import pandas as pd  # biblioteca principal para tabelas de dados

# ---------- CONFIGURAÇÕES ----------
CAMINHO_ENTRADA = Path("data/raw/raw_vendas_exportada.csv")
CAMINHO_SAIDA = Path("data/processed/vendas_tratadas.csv")

# Tradução dos nomes do CSV (inglês) para os nomes do dicionário de dados
COLUNAS = {
    "invoice_id": "id_venda",
    "branch": "Filial",
    "city": "Cidade",
    "customer_type": "tipo_cliente",
    "gender": "Gênero",
    "product_line": "linha_produto",
    "unit_price": "preco_unitario",
    "quantity": "Quantidade",
    "tax_5pct": "Imposto",
    "sales": "valor_total",
    "sale_date": "data_venda",
    "sale_time": "hora_venda",
    "payment": "forma_pagamento",
    "cogs": "custo_mercadoria",
    "gross_margin_percentage": "margem_percentual",
    "gross_income": "receita_bruta",
    "rating": "Avaliação",
}


# ---------- FUNÇÃO 1: LER O ARQUIVO ----------
def carregar_dados(caminho):
    # Lê o CSV exportado do banco e devolve um DataFrame
    return pd.read_csv(caminho)


# ---------- FUNÇÃO 2: RENOMEAR COLUNAS ----------
def renomear_colunas(df):
    # rename troca os nomes usando o dicionário COLUNAS
    return df.rename(columns=COLUNAS)


# ---------- FUNÇÃO 3: CONVERTER TIPOS (CASTING) ----------
def converter_tipos(df):
    # Trabalha numa cópia para não mexer no DataFrame original
    df = df.copy()

    # Colunas de texto: tira espaços sobrando no começo e no fim
    colunas_texto = ["id_venda", "Filial", "Cidade", "tipo_cliente",
                     "Gênero", "linha_produto", "forma_pagamento"]
    for coluna in colunas_texto:
        df[coluna] = df[coluna].str.strip()

    # Data: formato americano, mês/dia/ano (ex.: 1/5/2019 = 5 de janeiro)
    df["data_venda"] = pd.to_datetime(df["data_venda"], format="%m/%d/%Y")

    # Hora: formato de 12 horas com AM/PM (ex.: 1:08:00 PM)
    df["hora_venda"] = pd.to_datetime(
        df["hora_venda"], format="%I:%M:%S %p"
    ).dt.time

    # Números inteiros e decimais
    df["Quantidade"] = df["Quantidade"].astype(int)
    colunas_decimais = ["preco_unitario", "Imposto", "valor_total",
                        "custo_mercadoria", "margem_percentual",
                        "receita_bruta", "Avaliação"]
    for coluna in colunas_decimais:
        df[coluna] = df[coluna].astype(float)

    return df


# ---------- FUNÇÃO 4: NULOS E DUPLICADOS ----------
def tratar_nulos_e_duplicados(df):
    # Mostra quantos nulos existem em cada coluna
    print("=== NULOS POR COLUNA ===")
    print(df.isna().sum())

    linhas_antes = len(df)

    # Campos críticos: sem eles a venda não serve para análise.
    # Decisão: se algum estiver vazio, a linha é removida.
    colunas_criticas = ["id_venda", "Filial", "Cidade", "linha_produto",
                        "preco_unitario", "Quantidade", "valor_total",
                        "data_venda", "forma_pagamento"]
    df = df.dropna(subset=colunas_criticas)

    # Cada venda tem um id único: se o id se repetir, fica só a primeira
    df = df.drop_duplicates(subset="id_venda")

    print(f"Linhas removidas (nulos ou duplicadas): {linhas_antes - len(df)}")
    return df


# ---------- FUNÇÃO 5: CONFERIR O VALOR TOTAL ----------
def conferir_valor_total(df):
    # Regra do dataset: valor_total = preço x quantidade + imposto
    esperado = df["preco_unitario"] * df["Quantidade"] + df["Imposto"]

    # Diferença em valor absoluto (aceita até 1 centavo de arredondamento)
    diferenca = (df["valor_total"] - esperado).abs()
    divergentes = (diferenca > 0.01).sum()

    print(f"Vendas com valor_total diferente do calculado: {divergentes}")
    return df


# ---------- FUNÇÃO 6: CASOS LIMÍTROFES ----------
def tratar_casos_limitrofes(df):
    # Regras de negócio do dicionário de dados
    valido = (
        (df["preco_unitario"] >= 0)
        & (df["Quantidade"] > 0)
        & (df["Imposto"] >= 0)
        & (df["valor_total"] >= 0)
        & (df["custo_mercadoria"] >= 0)
        & (df["receita_bruta"] >= 0)
        & (df["Avaliação"].between(0, 10))
    )

    # ~valido significa "o contrário de valido"
    print(f"Linhas fora das regras de negócio: {(~valido).sum()}")

    # Mantém só as linhas que respeitam as regras
    return df[valido]


# ---------- FUNÇÃO 7: COLUNAS DERIVADAS ----------
def criar_colunas_derivadas(df):
    df = df.copy()

    # Dia da semana em português (0 = segunda-feira ... 6 = domingo)
    dias = {0: "segunda-feira", 1: "terça-feira", 2: "quarta-feira",
            3: "quinta-feira", 4: "sexta-feira", 5: "sábado", 6: "domingo"}
    df["dia_semana"] = df["data_venda"].dt.dayofweek.map(dias)

    # Mês da venda (número de 1 a 12)
    df["mes"] = df["data_venda"].dt.month

    # Hora cheia da venda (número de 0 a 23), tirada da coluna hora_venda
    df["hora_do_dia"] = df["hora_venda"].apply(lambda h: h.hour)

    return df


# ---------- FUNÇÃO 8: ARREDONDAR ----------
def arredondar_valores(df):
    # O banco e o dicionário usam 2 casas decimais
    colunas = ["preco_unitario", "Imposto", "valor_total",
               "custo_mercadoria", "margem_percentual",
               "receita_bruta", "Avaliação"]
    df[colunas] = df[colunas].round(2)
    return df


# ---------- FUNÇÃO 9: SALVAR ----------
def salvar_dados(df, caminho):
    # Garante que data/processed existe
    caminho.parent.mkdir(parents=True, exist_ok=True)

    # index=False evita gravar a coluna de números da esquerda
    df.to_csv(caminho, index=False, encoding="utf-8")
    print(f"Arquivo salvo em: {caminho} ({len(df)} linhas)")


# ---------- EXECUÇÃO ----------
if __name__ == "__main__":
    dados = carregar_dados(CAMINHO_ENTRADA)
    dados = renomear_colunas(dados)
    dados = converter_tipos(dados)
    dados = tratar_nulos_e_duplicados(dados)
    dados = conferir_valor_total(dados)
    dados = tratar_casos_limitrofes(dados)
    dados = criar_colunas_derivadas(dados)
    dados = arredondar_valores(dados)
    salvar_dados(dados, CAMINHO_SAIDA)

    # Mostra os tipos e as primeiras linhas para conferir
    dados.info()
    print(dados.head())