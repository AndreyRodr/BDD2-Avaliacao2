import json
from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConfigurationError
# Este script conecta ao MongoDB Atlas (nuvem) e carrega
# o arquivo credit-card2.json (metade 2) para a coleção NoSQL.

# 🚨 MUITO IMPORTANTE: SUBSTITUI COM A TUA URI REAL (inclui usuário e senha!) 🚨
MONGO_URI = "SUA-URI-NO-MONGO-ATLAS"
DB_NAME = "fraude_nosql"
COLLECTION_NAME = "transactions_mongo"
JSON_FILE = 'credit-card2.json' 

def carregar_json():
    """Lê o arquivo JSON e retorna a lista de documentos para inserção."""
    try:
        with open(JSON_FILE, 'r') as f:
            dados = json.load(f)
            print(f"Lidos {len(dados)} documentos do {JSON_FILE}.")
            return dados
    except FileNotFoundError:
        print(f"Erro: Arquivo {JSON_FILE} não encontrado.")
        return None
    except json.JSONDecodeError:
        print("Erro: O arquivo JSON não está formatado corretamente.")
        return None

def ingestao_mongo():
    """Conecta ao MongoDB e insere os dados."""
    dados = carregar_json()
    if not dados:
        return

    try:
        # Conexão ao Cliente
        client = MongoClient(MONGO_URI)
        client.admin.command('ping') # Testa a conexão
        print("✅ Conexão ao MongoDB Atlas bem-sucedida!")
        
        # Acesso ao Banco de Dados e Coleção
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        print("A iniciar a inserção dos dados...")
        
        # A inserção no MongoDB é geralmente mais tolerante a grandes pacotes
        resultado = collection.insert_many(dados)
        
        print(f"🚀 Inserção concluída! {len(resultado.inserted_ids)} registos inseridos na coleção '{COLLECTION_NAME}'.")
        
        client.close()

    except (PyMongoError, ConfigurationError) as e:
    # PyMongoError abrange erros de conexão, timeout, etc.
        print(f"🚨 Erro de Conexão ou Configuração. Verifica URI e IP de acesso! Detalhe: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    ingestao_mongo()