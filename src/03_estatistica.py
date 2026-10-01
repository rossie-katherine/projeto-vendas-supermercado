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


# ---------- PERGUNTA 5: FORMA DE PAGAMENTO MAIS USADA ----------
def pergunta_5(df):
    print("\n=== PERGUNTA 5: Qual a forma de pagamento mais usada? ===")
    # HIPÓTESE (troque por uma frase sua): o cartão de crédito
    # é a forma de pagamento mais usada.
    pagamentos = df["forma_pagamento"].value_counts()
    print(pagamentos)

    grafico_barras(pagamentos, "Vendas por forma de pagamento",
                   "Forma de pagamento", "Número de vendas",
                   "p5_forma_pagamento.png")
    return pagamentos


# ---------- PERGUNTA 6: VALOR MÉDIO DAS VENDAS ----------
def pergunta_6(df):
    print("\n=== PERGUNTA 6: Qual o valor médio das vendas? ===")
    # HIPÓTESE (troque por uma frase sua): a média fica acima da mediana,
    # porque poucas vendas muito grandes puxam a média para cima.
    media = df["valor_total"].mean()
    mediana = df["valor_total"].median()
    print(f"Valor médio: {media:.2f}")
    print(f"Mediana: {mediana:.2f}")
    print(df["valor_total"].describe().round(2))

    # Histograma: mostra como os valores das vendas se distribuem
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(df["valor_total"], bins=20, color="steelblue", edgecolor="white")
    ax.axvline(media, color="red", linestyle="--",
               label=f"Média: {media:.2f}")
    ax.axvline(mediana, color="orange", linestyle="--",
               label=f"Mediana: {mediana:.2f}")
    ax.set_title("Distribuição do valor das vendas")
    ax.set_xlabel("Valor total da venda")
    ax.set_ylabel("Número de vendas")
    ax.legend()
    plt.tight_layout()
    fig.savefig(PASTA_RESULTADOS / "p6_valor_medio_vendas.png", dpi=150)
    plt.close(fig)
    return media


# ---------- PERGUNTA 7: MAIOR VENDA REGISTRADA ----------
def pergunta_7(df):
    print("\n=== PERGUNTA 7: Qual foi a maior venda registrada? ===")
    # HIPÓTESE (troque por uma frase sua): a maior venda tem a quantidade
    # máxima (10 unidades) e um preço unitário alto.
    # idxmax devolve a posição da linha com o maior valor_total
    maior = df.loc[df["valor_total"].idxmax()]
    print(maior[["id_venda", "Filial", "linha_produto", "Quantidade",
                 "preco_unitario", "valor_total", "data_venda"]])

    # Confere se há empate no valor máximo
    empates = (df["valor_total"] == df["valor_total"].max()).sum()
    print(f"Vendas com esse valor máximo: {empates}")

    # Gráfico das 10 maiores vendas
    top10 = (df.nlargest(10, "valor_total")
             .set_index("id_venda")["valor_total"])
    grafico_barras(top10, "As 10 maiores vendas", "ID da venda",
                   "Valor total", "p7_maiores_vendas.png")
    return maior


# ---------- PERGUNTA 8: DIA DA SEMANA COM MAIS VENDAS ----------
ORDEM_DIAS = ["segunda-feira", "terça-feira", "quarta-feira",
              "quinta-feira", "sexta-feira", "sábado", "domingo"]


def pergunta_8(df):
    print("\n=== PERGUNTA 8: Em qual dia da semana há mais vendas? ===")
    # HIPÓTESE (troque por uma frase sua): o fim de semana
    # concentra mais vendas.
    # reindex coloca os dias na ordem da semana, de segunda a domingo
    por_dia = df["dia_semana"].value_counts().reindex(ORDEM_DIAS)
    print(por_dia)
    print(f"Dia com mais vendas: {por_dia.idxmax()} ({por_dia.max()} vendas)")

    grafico_barras(por_dia, "Vendas por dia da semana", "Dia da semana",
                   "Número de vendas", "p8_vendas_dia_semana.png")
    return por_dia


# ---------- SALVAR AS RESPOSTAS EM TEXTO ----------
def salvar_respostas(fat_filial, qtd_filial, fat_linha, aval_linha,
                     pagamentos, media, maior, por_dia):
    linhas = [
        "RESPOSTAS ÀS PERGUNTAS DE NEGÓCIO",
        "",
        f"1. Maior faturamento: {fat_filial.idxmax()} "
        f"({fat_filial.max():.2f})",
        f"2. Mais vendas: {qtd_filial.idxmax()} ({qtd_filial.max()} vendas)",
        f"3. Linha com maior faturamento: {fat_linha.idxmax()} "
        f"({fat_linha.max():.2f})",
        f"4. Melhor avaliação média: {aval_linha.idxmax()} "
        f"({aval_linha.max():.2f})",
        f"5. Forma de pagamento mais usada: {pagamentos.idxmax()} "
        f"({pagamentos.max()} vendas)",
        f"6. Valor médio das vendas: {media:.2f}",
        f"7. Maior venda: {maior['id_venda']} "
        f"({maior['valor_total']:.2f}, filial {maior['Filial']})",
        f"8. Dia com mais vendas: {por_dia.idxmax()} "
        f"({por_dia.max()} vendas)",
    ]
    caminho = PASTA_RESULTADOS / "respostas_negocio.txt"
    caminho.write_text("\n".join(linhas), encoding="utf-8")
    print(f"\nRespostas salvas em: {caminho}")


# ---------- EXECUÇÃO ----------
if __name__ == "__main__":
    # Garante que a pasta resultados/ existe
    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)

    dados = carregar_dados(CAMINHO_ENTRADA)
    conferir_categorias(dados)

    fat_filial = pergunta_1(dados)
    qtd_filial = pergunta_2(dados)
    fat_linha = pergunta_3(dados)
    aval_linha = pergunta_4(dados)
    pagamentos = pergunta_5(dados)
    media = pergunta_6(dados)
    maior = pergunta_7(dados)
    por_dia = pergunta_8(dados)

    salvar_respostas(fat_filial, qtd_filial, fat_linha, aval_linha,
                     pagamentos, media, maior, por_dia)