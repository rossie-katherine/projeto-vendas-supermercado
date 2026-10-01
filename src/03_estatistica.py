# Estatística descritiva, respostas às perguntas de negócio e gráficos
# Entrada: data/processed/vendas_tratadas.csv
# Saída: gráficos em resultados/

# ---------- BIBLIOTECAS ----------
from pathlib import Path  # trabalhar com caminhos de pastas

import matplotlib.pyplot as plt  # biblioteca para fazer gráficos
import pandas as pd  # biblioteca principal para tabelas de dados

# ---------- CONFIGURAÇÕES ----------
CAMINHO_ENTRADA = Path("data/processed/vendas_tratadas.csv")
PASTA_RESULTADOS = Path("resultados")


# ---------- FUNÇÃO: LER O ARQUIVO ----------
def carregar_dados(caminho):
    # parse_dates faz o pandas entender data_venda como data
    return pd.read_csv(caminho, parse_dates=["data_venda"])


# ---------- FUNÇÃO: CONFERIR CATEGORIAS ----------
def conferir_categorias(df):
    # Mostra todos os valores que existem em cada coluna de categoria
    # (serve para conferir o dicionário de dados e os CHECKs do SQL)
    for coluna in ["Filial", "Cidade", "tipo_cliente", "Gênero",
                   "forma_pagamento", "linha_produto"]:
        print(f"\n=== {coluna} ===")
        print(df[coluna].value_counts())


# ---------- FUNÇÃO: GRÁFICO DE BARRAS ----------
def grafico_barras(serie, titulo, rotulo_x, rotulo_y, nome_arquivo):
    # Cria a figura e desenha as barras a partir da série (índice = eixo x)
    fig, ax = plt.subplots(figsize=(9, 5))
    serie.plot(kind="bar", ax=ax, color="steelblue")

    # Título e nomes dos eixos
    ax.set_title(titulo)
    ax.set_xlabel(rotulo_x)
    ax.set_ylabel(rotulo_y)

    # Inclina os nomes do eixo x para não ficarem amontoados
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    # Salva em resultados/ e fecha a figura
    fig.savefig(PASTA_RESULTADOS / nome_arquivo, dpi=150)
    plt.close(fig)


# ---------- PERGUNTA 1: FILIAL COM MAIOR FATURAMENTO ----------
def pergunta_1(df):
    print("\n=== PERGUNTA 1: Qual filial apresentou o maior faturamento? ===")
    # HIPÓTESE (troque por uma frase sua): a filial com mais vendas
    # deve ser também a de maior faturamento.
    # Faturamento = soma de valor_total (receita_bruta aqui é o lucro)
    faturamento = (df.groupby("Filial")["valor_total"].sum()
                   .sort_values(ascending=False))
    print(faturamento.round(2))

    grafico_barras(faturamento, "Faturamento por filial",
                   "Filial", "Faturamento", "p1_faturamento_filial.png")
    return faturamento


# ---------- PERGUNTA 2: FILIAL COM MAIS VENDAS ----------
def pergunta_2(df):
    print("\n=== PERGUNTA 2: Qual filial realizou mais vendas? ===")
    # HIPÓTESE (troque por uma frase sua): as filiais têm quantidades
    # de vendas parecidas.
    # Cada linha da tabela é uma venda, então contamos as linhas por filial
    quantidade = df["Filial"].value_counts()
    print(quantidade)

    grafico_barras(quantidade, "Quantidade de vendas por filial",
                   "Filial", "Número de vendas", "p2_vendas_filial.png")
    return quantidade


# ---------- PERGUNTA 3: LINHA DE PRODUTO COM MAIOR FATURAMENTO ----------
def pergunta_3(df):
    print("\n=== PERGUNTA 3: Qual linha de produto faturou mais? ===")
    # HIPÓTESE (troque por uma frase sua): a linha com mais vendas
    # é a de maior faturamento.
    faturamento = (df.groupby("linha_produto")["valor_total"].sum()
                   .sort_values(ascending=False))
    print(faturamento.round(2))

    grafico_barras(faturamento, "Faturamento por linha de produto",
                   "Linha de produto", "Faturamento",
                   "p3_faturamento_linha_produto.png")
    return faturamento


# ---------- PERGUNTA 4: LINHA DE PRODUTO COM MELHOR AVALIAÇÃO ----------
def pergunta_4(df):
    print("\n=== PERGUNTA 4: Qual linha tem a melhor avaliação média? ===")
    # HIPÓTESE (troque por uma frase sua): as avaliações médias são
    # parecidas entre as linhas.
    media = (df.groupby("linha_produto")["Avaliação"].mean()
             .sort_values(ascending=False))
    print(media.round(2))

    grafico_barras(media, "Avaliação média por linha de produto",
                   "Linha de produto", "Avaliação média (0 a 10)",
                   "p4_avaliacao_linha_produto.png")
    return media


# ---------- EXECUÇÃO ----------
if __name__ == "__main__":
    # Garante que a pasta resultados/ existe
    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)

    dados = carregar_dados(CAMINHO_ENTRADA)
    conferir_categorias(dados)
    pergunta_1(dados)
    pergunta_2(dados)
    pergunta_3(dados)
    pergunta_4(dados)