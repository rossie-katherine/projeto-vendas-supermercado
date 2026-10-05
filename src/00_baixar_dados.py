# Script que baixa o dataset Supermarket Sales do Kaggle e salva em data/raw/

# ---------- BIBLIOTECAS ----------
import shutil  # serve para copiar arquivos
from pathlib import Path  # serve para trabalhar com caminhos de pastas

import kagglehub  # biblioteca que baixa dados do Kaggle

# ---------- CONFIGURAÇÕES ----------
# Nome do dataset no Kaggle (é a parte final do link)
DATASET = "faresashraf1001/supermarket-sales"

# Pasta onde o CSV vai ficar guardado no projeto
PASTA_DESTINO = Path("data/raw")


# ---------- FUNÇÃO PRINCIPAL ----------
def baixar_dados():
    # Baixa o dataset para uma pasta temporária (cache)
    # e devolve o caminho dessa pasta
    caminho_cache = Path(kagglehub.dataset_download(DATASET))

    # Garante que data/raw existe (se já existir, não dá erro)
    PASTA_DESTINO.mkdir(parents=True, exist_ok=True)

    # Procura todos os arquivos .csv na pasta temporária
    for arquivo in caminho_cache.glob("*.csv"):
        # Monta o caminho final: data/raw/nome_do_arquivo.csv
        destino = PASTA_DESTINO / arquivo.name

        # Copia o arquivo para dentro do projeto, sem alterar o conteúdo
        shutil.copy(arquivo, destino)

        # Mostra na tela onde o arquivo foi salvo
        print(f"Arquivo salvo em: {destino}")


# Esta linha faz o script rodar só quando você executa o arquivo diretamente
if __name__ == "__main__":
    baixar_dados()