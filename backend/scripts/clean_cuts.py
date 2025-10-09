import os
import time


CUTS_FOLDER = r"C:\Users\Administrator\Projetos\pdfGeneratorProj\backend\src\cuts"


MAX_AGE_SECONDS = 60 * 60  

def limpar_recortes():
    agora = time.time()

    for nome_arquivo in os.listdir(CUTS_FOLDER):
        if nome_arquivo.startswith("recorte_") and nome_arquivo.endswith(".png"):
            caminho_completo = os.path.join(CUTS_FOLDER, nome_arquivo)
            idade = agora - os.path.getmtime(caminho_completo)
            if idade > MAX_AGE_SECONDS:
                try:
                    os.remove(caminho_completo)
                    print(f"[INFO] Arquivo removido: {nome_arquivo}")
                except Exception as e:
                    print(f"[ERRO] Não foi possível remover {nome_arquivo}: {e}")

if __name__ == "__main__":
    limpar_recortes()
