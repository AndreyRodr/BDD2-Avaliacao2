from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import mysql.connector
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os
import sqlite3

# ==============================================================================
# CONFIGURAÇÕES GERAIS E BANCO DE DADOS
# ==============================================================================

# Configurações do MySQL
MYSQL_CONFIG = {
    "host": "127.0.0.1",
    "database": "fraud_detection",
    "user": "root",
    "password": "root"
}
MYSQL_TABLE = 'transactions_mysql'

# Configurações do MongoDB Atlas (Nuven)
MONGO_URI = "SUA-URI-NO-MONGO-ATLAS" 
MONGO_DB_NAME = "fraude_nosql"
MONGO_COLLECTION = 'transactions_mongo'

# Função auxiliar para garantir o caminho base correto do projeto na VM
def get_base_path():
    """Retorna o caminho absoluto para a pasta raiz do projeto."""
    home_dir = os.environ.get('HOME', '/home/aluno')
    return os.path.join(home_dir, 'projeto_fraude__bdd2')


# ==============================================================================
# LÓGICA ETL: CAMADA BRONZE (E -> L)
# ==============================================================================

def extract_and_load_bronze(**kwargs):
    """Extrai dados de MySQL e MongoDB, unifica e salva na Camada Bronze (TXT)."""
    
    base_dir = get_base_path()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_path = os.path.join(base_dir, f"data_lakehouse/bronze/raw_data_{timestamp}.txt")
    
    print("Iniciando extração e consolidação...")
    
    # Extração do MySQL
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        df_mysql = pd.read_sql(f"SELECT * FROM {MYSQL_TABLE};", conn)
        conn.close()
        print(f"-> Extraídas {len(df_mysql)} linhas do MySQL.")
    except Exception as e:
        print(f"Erro MySQL: {e}")
        raise

    # Extração do MongoDB
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        collection = db[MONGO_COLLECTION]
        mongo_data = list(collection.find({}, {'_id': 0})) 
        df_mongo = pd.DataFrame(mongo_data)
        client.close()
        print(f"-> Extraídas {len(df_mongo)} linhas do MongoDB.")
    except PyMongoError as e:
        print(f"Erro MongoDB (DNS/Conexão). Detalhe: {e}")
        raise

    # Consolidação e Carga (TXT)
    if not df_mongo.empty and not df_mysql.empty:
        df_mongo.columns = df_mysql.columns 
    
    df_consolidado = pd.concat([df_mysql, df_mongo], ignore_index=True)
    
    df_consolidado.to_csv(final_path, index=False, sep=',', encoding='utf-8')
    print(f"🚀 Dados brutos salvos na Camada BRONZE: {final_path}")
    
    # Retorna o caminho para a próxima tarefa (Silver) via XCom
    return final_path


# ==============================================================================
# LÓGICA ETL: CAMADA SILVER (T)
# ==============================================================================

def transform_to_silver(ti):
    """Lê o TXT bruto (Bronze), faz a limpeza e a Feature Engineering, salva na Camada Silver (CSV)."""
    
    # Recupera o caminho do arquivo Bronze (XCom)
    bronze_path = ti.xcom_pull(
        task_ids='load_to_bronze_txt',
        key='return_value'
    )
    
    if not bronze_path or not os.path.exists(bronze_path):
        raise FileNotFoundError("Não foi possível encontrar o arquivo da Camada Bronze via XCom.")

    df = pd.read_csv(bronze_path, sep=',')
    
    # LIMPEZA E TRATAMENTO
    print(f"Iniciando transformação em {len(df)} linhas...")
    
    # Tratamento Básico de Nulos (Imputação por Média)
    df['Amount'].fillna(df['Amount'].median(), inplace=True)
    
    # FEATURE ENGINEERING
    # Cria uma feature de densidade (Amount / Tempo)
    df['Density'] = df['Amount'] / (df['Time'] + 1)
    
    # Carga na Camada Silver
    base_dir = get_base_path()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    silver_path = os.path.join(base_dir, f"data_lakehouse/silver/clean_data_{timestamp}.csv")
    
    df.to_csv(silver_path, index=False)
    
    print(f"🚀 Dados limpos e transformados salvos na Camada SILVER: {silver_path}")
    
    # Retorna o caminho para a próxima tarefa (Gold) via XCom
    return silver_path


# ==============================================================================
# LÓGICA ETL: CAMADA GOLD (L - Carga Final)
# ==============================================================================

def load_to_gold(ti):
    """Lê o CSV limpo (Silver) e carrega no SQLite (Camada Gold) para consumo final."""
    
    # Recupera o caminho do arquivo Silver (XCom)
    silver_path = ti.xcom_pull(
        task_ids='transform_to_silver_csv',
        key='return_value'
    )
    
    if not silver_path or not os.path.exists(silver_path):
        raise FileNotFoundError("Não foi possível encontrar o arquivo da Camada Silver.")

    # Leitura dos Dados Limpos
    df = pd.read_csv(silver_path)
    
    # Conexão ao SQLite (Gold)
    base_dir = get_base_path()
    sqlite_db_path = os.path.join(base_dir, "data_lakehouse/gold/fraud_analysis.sqlite")
    
    conn = sqlite3.connect(sqlite_db_path)
    
    # CARGA NA TABELA FINAL
    TABLE_NAME = 'final_transactions'
    
    # Substitui a tabela existente com os novos dados
    df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
    
    conn.close()
    
    print(f"🚀 Carga ETL concluída. {len(df)} registos inseridos no SQLite (Camada GOLD).")


# ==============================================================================
# DEFINIÇÃO DO DAG (ORQUESTRAÇÃO)
# ==============================================================================

# Argumentos padrão
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1), 
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'fraud_detection_etl_pipeline',
    default_args=default_args,
    description='Pipeline ETL de Fraude em Cartão de Crédito - Arquitetura Medalhão',
    schedule=timedelta(days=1),  # CORREÇÃO: Usamos 'schedule'
    catchup=False,
    tags=['jcrbdd2', 'medallion', 'etl'],
) as dag:
    
    # TAREFA 1: BRONZE (E -> L) - Extração e Consolidação de Fontes
    bronze_load_task = PythonOperator(
        task_id='load_to_bronze_txt',
        python_callable=extract_and_load_bronze,
    )
    
    # TAREFA 2: SILVER (T) - Transformação, Limpeza e Feature Engineering
    silver_transform_task = PythonOperator(
        task_id='transform_to_silver_csv',
        python_callable=transform_to_silver,
    )
    
    # TAREFA 3: GOLD (L) - Carga Final para o Banco de Dados de Consumo (SQLite)
    gold_load_task = PythonOperator(
        task_id='load_to_gold_sqlite',
        python_callable=load_to_gold,
    )
    
    # Define a Ordem de Execução: Bronze >> Silver >> Gold
    bronze_load_task >> silver_transform_task >> gold_load_task