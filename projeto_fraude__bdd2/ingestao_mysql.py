import pandas as pd
import mysql.connector
from mysql.connector import Error

# Este script conecta ao MySQL, cria a tabela e carrega
# os dados de transações da primeira metade do dataset (credit-card1.csv).

# Configurações do Banco de Dados MySQL
DB_CONFIG = {
    "host": "127.0.0.1",
    "database": "fraud_detection",
    "user": "root",
    "password": "root"
}
CSV_FILE = 'credit-card1.csv'
TABLE_NAME = 'transactions_mysql'

def criar_conexao():
    """Cria uma conexão com o servidor MySQL."""
    try:
        # Tenta conectar ao MySQL. O container pode demorar alguns segundos a inicializar.
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("✅ Conexão com o MySQL estabelecida com sucesso!")
            return conn
    except Error as e:
        print(f"🚨 Erro ao conectar ao MySQL. O container está a correr? Detalhe: {e}")
        return None

def criar_tabela(conn, df):
    """Cria a tabela no banco de dados MySQL com a estrutura correta."""
    cursor = conn.cursor()
    
    # Define os tipos de dados para as 31 colunas
    colunas_sql = []
    for col in df.columns:
        if col in ['Time', 'Class']:
            colunas_sql.append(f"`{col}` INT")
        elif col in ['Amount']:
            colunas_sql.append(f"`{col}` DECIMAL(10, 2)") 
        else:
            colunas_sql.append(f"`{col}` DECIMAL(10, 5)") 

    colunas_sql_str = ', '.join(colunas_sql)
    
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        {colunas_sql_str}
    );
    """
    try:
        cursor.execute(create_table_query)
        print(f"Tabela '{TABLE_NAME}' verificada/criada com sucesso.")
    except Error as e:
        print(f"Erro ao criar a tabela: {e}")
    finally:
        cursor.close()

def carregar_dados(conn):
    """Lê o CSV, insere os dados em lotes (chunks) na tabela."""
    CHUNK_SIZE = 1000 

    try:
        # ver o CSV
        df = pd.read_csv(CSV_FILE)
        print(f"Lidas {len(df)} linhas do {CSV_FILE}.")
        
        cursor = conn.cursor()
        
        # Garante que a tabela existe
        criar_tabela(conn, df)
        
        # Prepara o comando SQL de INSERT (fora do loop)
        colunas = ', '.join([f'`{col}`' for col in df.columns])
        placeholders = ', '.join(['%s'] * len(df.columns))
        insert_query = f"INSERT INTO {TABLE_NAME} ({colunas}) VALUES ({placeholders})"
        
        print(f"A iniciar a inserção dos dados em lotes de {CHUNK_SIZE}...")
        
        # Iterar sobre o DataFrame em lotes (chunking)
        for i in range(0, len(df), CHUNK_SIZE):
            df_chunk = df.iloc[i:i + CHUNK_SIZE]
            lista_de_tuples = [tuple(row) for row in df_chunk.values]
            
            # Executa a inserção apenas para o lote atual
            cursor.executemany(insert_query, lista_de_tuples)
            
            print(f"Lote inserido: {i} a {min(i + CHUNK_SIZE, len(df))}")

        conn.commit()
        print(f"🚀 Inserção concluída! {len(df)} registos inseridos no total.")
        
    except FileNotFoundError:
        print(f"Erro: Arquivo {CSV_FILE} não encontrado.")
    except Error as e:
        print(f"Erro de inserção de dados: {e}")
    finally:
        if cursor:
            cursor.close()

if __name__ == "__main__":
    conexao = criar_conexao()
    if conexao:
        carregar_dados(conexao)
        conexao.close()