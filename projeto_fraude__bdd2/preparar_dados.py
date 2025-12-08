import pandas as pd
import json

# Este script lê o arquivo credit-card.csv, divide-o em dois,
# salva a primeira metade como CSV e a segunda metade como JSON.

def preparar_dados():
    print("A ler o arquivo original...")
    
    # Tenta ler o arquivo de dados de crédito.
    try:
        # Assumindo que o arquivo credit-card.csv está na mesma pasta do script
        df = pd.read_csv('creditcard.csv')
    except FileNotFoundError:
        print("🚨 Erro: Arquivo 'credit-card.csv' não encontrado. Por favor, coloque-o na pasta do projeto.")
        return

    total_linhas = len(df)
    # floor division para garantir que o corte é um inteiro
    metade = total_linhas // 2
    
    print(f"Total de linhas: {total_linhas}. Cortando na linha: {metade}")

    # Divide o dataframe usando iloc (seleção por índice)
    df_parte1 = df.iloc[:metade] # Do início até a metade (para MySQL)
    df_parte2 = df.iloc[metade:] # Da metade até o fim (para MongoDB)

    # Salva a Parte 1 como CSV (Requisito para o MySQL)
    print("A salvar credit-card1.csv...")
    df_parte1.to_csv('credit-card1.csv', index=False)

    # Salva a Parte 2 como JSON (Requisito para o MongoDB)
    # O 'orient=records' cria a lista de objetos, ideal para o MongoDB
    print("A salvar credit-card2.json...")
    df_parte2.to_json('credit-card2.json', orient='records', indent=4)

    print("✅ Concluído! Arquivos de origem prontos para ingestão.")

if __name__ == "__main__":
    preparar_dados()