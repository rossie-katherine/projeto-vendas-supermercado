# ETL da camada Tratada: renomeia, converte tipos e cria colunas derivadas
# Entrada: data/raw/raw_vendas_exportada.csv
# Saída: data/processed/vendas_tratadas.csv


from pathlib import Path  # trabalhar com caminhos de pastas

import pandas as pd  # biblioteca principal para tabelas de dados


CAMINHO_ENTRADA = Path("data/raw/raw_vendas_exportada.csv")
CAMINHO_SAIDA = Path("data/processed/vendas_tratadas.csv")

# Tradução dos nomes do CSV para os nomes do dicionário de dados
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


# LER O ARQUIVO 
def carregar_dados(caminho):
    # Lê o CSV exportado do banco e devolve um DataFrame
    return pd.read_csv(caminho)


# RENOMEAR COLUNAS
def renomear_colunas(df):
    # rename troca os nomes usando o dicionário COLUNAS
    return df.rename(columns=COLUNAS)


# CONVERTER TIPOS (CASTING) 
def converter_tipos(df):
    df = df.copy()

    # Tira espaços sobrando no começo e no fim das colunas de texto
    colunas_texto = ["id_venda", "Filial", "Cidade", "tipo_cliente",
                     "Gênero", "linha_produto", "forma_pagamento"]
    for coluna in colunas_texto:
        df[coluna] = df[coluna].str.strip()

    # Data: formato americano
    df["data_venda"] = pd.to_datetime(df["data_venda"], format="%m/%d/%Y")

    # Hora: formato de 12 horas com AM/PM 
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


# NULOS E DUPLICADOS 
def tratar_nulos_e_duplicados(df):
    # Mostra quantos nulos existem em cada coluna
    print("=== NULOS POR COLUNA ===")
    print(df.isna().sum())

    linhas_antes = len(df)

    # Campos críticos: se algum estiver vazio, a linha é removida
    colunas_criticas = ["id_venda", "Filial", "Cidade", "linha_produto",
                        "preco_unitario", "Quantidade", "valor_total",
                        "data_venda", "forma_pagamento"]
    df = df.dropna(subset=colunas_criticas)

    # Cada venda tem um id único: se o id se repetir, fica só a primeira
    df = df.drop_duplicates(subset="id_venda")

    print(f"Linhas removidas (nulos ou duplicadas): {linhas_antes - len(df)}")
    return df


# CONFERIR O VALOR TOTAL 
def conferir_valor_total(df):
    # valor_total = preço x quantidade + imposto
    esperado = df["preco_unitario"] * df["Quantidade"] + df["Imposto"]

    
    diferenca = (df["valor_total"] - esperado).abs()
    divergentes = (diferenca > 0.01).sum()

    print(f"Vendas com valor_total diferente do calculado: {divergentes}")
    return df


# CASOS LIMÍTROFES 
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

    # ~valido significa "o contrário de válido"
    print(f"Linhas fora das regras de negócio: {(~valido).sum()}")

    
    return df[valido]


# COLUNAS DERIVADAS 
def criar_colunas_derivadas(df):
    df = df.copy()

    # Dia da semana em português 
    dias = {0: "segunda-feira", 1: "terça-feira", 2: "quarta-feira",
            3: "quinta-feira", 4: "sexta-feira", 5: "sábado", 6: "domingo"}
    df["dia_semana"] = df["data_venda"].dt.dayofweek.map(dias)

    # Mês da venda 
    df["mes"] = df["data_venda"].dt.month

    # Hora cheia da venda 
    df["hora_do_dia"] = df["hora_venda"].apply(lambda h: h.hour)

    return df


# ARREDONDAR 
def arredondar_valores(df):
    # O banco e o dicionário usam 2 casas decimais
    colunas = ["preco_unitario", "Imposto", "valor_total",
               "custo_mercadoria", "margem_percentual",
               "receita_bruta", "Avaliação"]
    df[colunas] = df[colunas].round(2)
    return df


# SALVAR 
def salvar_dados(df, caminho):
    caminho.parent.mkdir(parents=True, exist_ok=True)

    # index=False evita gravar a coluna de números da esquerda
    df.to_csv(caminho, index=False, encoding="utf-8")
    print(f"Arquivo salvo em: {caminho} ({len(df)} linhas)")


# EXECUÇÃO 
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

    # Tipos e as primeiras linhas para conferir
    dados.info()
    print(dados.head())