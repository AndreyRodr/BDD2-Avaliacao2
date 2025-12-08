import kagglehub
import shutil
import os

# 1. Baixar o dataset (Isso vai para a pasta de cache do sistema)
print("Iniciando download do Kaggle (mlg-ulb/creditcardfraud)...")
path_cache = kagglehub.dataset_download("mlg-ulb/creditcardfraud")

print(f"Download concluído no cache: {path_cache}")

# 2. Mover para a pasta atual
# Define a pasta onde este script está rodando como destino
pasta_destino = os.path.dirname(os.path.abspath(__file__))

# Procura o arquivo .csv dentro da pasta baixada e move para cá
arquivo_encontrado = False
for nome_arquivo in os.listdir(path_cache):
    if nome_arquivo.endswith('.csv'):
        origem = os.path.join(path_cache, nome_arquivo)
        destino = os.path.join(pasta_destino, nome_arquivo)
        
        print(f"Movendo '{nome_arquivo}' para: {pasta_destino}")
        shutil.move(origem, destino)
        arquivo_encontrado = True

if arquivo_encontrado:
    print("\n--- SUCESSO! ---")
    print(f"O arquivo csv está pronto na sua pasta: {pasta_destino}")
else:
    print("\nERRO: Nenhum arquivo .csv foi encontrado no download.")

    